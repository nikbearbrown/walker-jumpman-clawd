"""4K contact pages, source-preserving audio checks and word-aligned SRT."""
import argparse,hashlib,json,math,subprocess,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SHEET=json.loads((ROOT/'beat_sheet.json').read_text())
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def frame(source,t,out,last=False):
    # A rounded seek at the final frame can land beyond EOF. Decode the final
    # second and reverse it to select the actual last decoded frame instead.
    seek=['-sseof','-1'] if last else ['-ss',f'{t:.6f}']
    filt=['-vf','reverse'] if last else []
    subprocess.run(['ffmpeg','-v','error','-y',*seek,'-i',str(source),*filt,'-frames:v','1',str(out)],check=True)
    if not out.is_file():raise RuntimeError(f'No decoded frame at {t}: {out}')
def pages(records,folder,name,each=12):
    font=ImageFont.truetype(str(ROOT/'remotion/public/Inter-Regular.ttf'),24)
    for start in range(0,len(records),each):
        page=Image.new('RGB',(1800,1480),'#FAF9F5');draw=ImageDraw.Draw(page)
        for i,r in enumerate(records[start:start+each]):
            im=Image.open(folder/r['path']).convert('RGB');im.thumbnail((580,326));x=i%3*600+10;y=i//3*370+36
            page.paste(im,(x,y));draw.text((x,y-29),r['label'],font=font,fill='#3D3929')
        page.save(folder/f'{name}-{start//each+1:03}.jpg',quality=95)
def contacts(only=None):
    folder=ROOT/'_qc/beats';folder.mkdir(exist_ok=True);rows=[]
    for b in SHEET['beats']:
        if only and b['beat_id'] not in only:continue
        src=ROOT/'media'/f"{b['beat_id']}.mp4"
        if not src.exists():continue
        info=probe(src);v=next(s for s in info['streams'] if s['codec_type']=='video');assert (v['width'],v['height'])==(3840,2160)
        for fraction in [.15,.5,.85]:
            p=folder/f"{b['beat_id']}-{round(fraction*100)}.png"
            if not p.exists() or p.stat().st_mtime<src.stat().st_mtime:frame(src,float(info['format']['duration'])*fraction,p)
            rows.append({'path':p.name,'label':f"{b['beat_id']} · {fraction:.0%}"})
    pages(rows,folder,'contact');print('CONTACTS',len(rows),'frames',math.ceil(len(rows)/12),'pages',flush=True)
def audio():
    state=json.loads((ROOT/'build-state.json').read_text());assert state['status']=='ready';master=Path(state['output'])
    def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32).astype(float)
    actual_all=decode(master);offset=0.;rows=[]
    for b in SHEET['beats']:
        d=b.get('render_duration_s',b['actual_duration_s']);expected=decode(ROOT/b['audio_file']);actual=actual_all[round(offset*16000):round((offset+d)*16000)]
        n=min(len(actual),len(expected));best=-1.;best_lag=0
        for lag in range(-32,33):
            lo,hi=max(0,-lag)+160,min(n,n-lag)-160;x=expected[lo:hi];y=actual[lo+lag:hi+lag];den=np.linalg.norm(x)*np.linalg.norm(y)
            score=float(np.dot(x,y)/den) if den else 0.
            if score>best:best,best_lag=score,lag
        peak=float(np.abs(actual).max());row={'beat':b['beat_id'],'start_s':offset,'similarity':best,'alignment_samples_16khz':best_lag,'peak':peak,'passed':best>=.95 and peak>.0001};rows.append(row);print(row,flush=True);offset+=d
    outro=SHEET['beats'][-1];assert outro['kind']=='outro_jingle' and not outro['narration_text'];assert sha(Path(outro['jingle_source']))==outro['jingle_sha256']==sha(ROOT/outro['audio_file'])
    result={'passed':all(r['passed'] for r in rows),'beats':rows,'scope':'Source-to-final audio preservation, not a human pronunciation approval.','max_alignment_ms':2,'outro_sha256':outro['jingle_sha256']};save(ROOT/'_qc/master-audio-qc.json',result);assert result['passed']
def subtitles():
    words=json.loads((ROOT/'mp3/words.json').read_text());cues=[];offset=0.
    def stamp(t):
        h,v=divmod(round(t*1000),3600000);m,v=divmod(v,60000);s,ms=divmod(v,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
    for b in SHEET['beats']:
        seq=words['beats'].get(b['beat_id'],[]);groups=[];group=[]
        for w in seq:
            group.append(w)
            if len(' '.join(x['text'] for x in group))>58 or (len(group)>=5 and w['text'].endswith(('.', '?','!'))):groups.append(group);group=[]
        if group:groups.append(group)
        for i,g in enumerate(groups):
            start=g[0]['startFrame']/30;end=max(start+.25,g[-1]['endFrame']/30)
            if i+1<len(groups):end=min(end,groups[i+1][0]['startFrame']/30)
            end=min(end,b['actual_duration_s'])
            if end<=start:raise ValueError('Zero-length subtitle; fix alignment rather than dropping words.')
            cues.append(f'{len(cues)+1}\n{stamp(offset+start)} --> {stamp(offset+end)}\n'+'\n'.join(textwrap.wrap(' '.join(x['text'] for x in g),42,break_on_hyphens=False,break_long_words=False)))
        offset+=b['actual_duration_s']
    target=ROOT/'exports/landscape'/f"{SHEET['metadata']['slug']}.srt";target.write_text('\n\n'.join(cues)+'\n');print(target,len(cues),'cues')
def sweep():
    state=json.loads((ROOT/'build-state.json').read_text());assert state['status']=='ready';src=Path(state['output']);folder=ROOT/'_qc/master-sweep';folder.mkdir(exist_ok=True)
    cached=list(folder.glob('sample-*.png'))
    expected=round(float(probe(src)['format']['duration'])*2)
    if len(cached)!=expected or any(p.stat().st_mtime<src.stat().st_mtime for p in cached):
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf','fps=2','-compression_level','1',str(folder/'sample-%05d.png')],check=True)
    records=[{'path':p.name,'seconds':(int(p.stem.split('-')[1])-1)/2,'label':f'{(int(p.stem.split("-")[1])-1)/2:.2f}s','kind':'2fps'} for p in sorted(folder.glob('sample-*.png'))]
    offset=0
    for b in SHEET['beats']:
        d=b.get('render_duration_s',b['actual_duration_s'])
        for label,t in [('start',0),('15',d*.15),('50',d*.5),('85',d*.85),('end',d-1/30)]:
            out=folder/f"{b['beat_id']}-{label}.png"
            if not out.exists() or out.stat().st_mtime<src.stat().st_mtime:
                frame(src,offset+t,out,last=b==SHEET['beats'][-1] and label=='end')
            records.append({'path':out.name,'seconds':offset+t,'label':f"{b['beat_id']} {label} · {offset+t:.2f}s",'kind':'beat boundary/steady-state'})
        offset+=d
    seen={};unique=[]
    for r in sorted(records,key=lambda r:r['seconds']):
        im=Image.open(folder/r['path']).convert('RGB');assert im.size==(3840,2160);digest=hashlib.sha256(im.tobytes()).hexdigest();r['pixel_sha256']=digest
        if digest not in seen:seen[digest]=r['path'];unique.append(r)
        r['representative']=seen[digest]
    pages(unique,folder,'page')
    save(folder/'manifest.json',{'source':str(src),'source_sha256':sha(src),'samples':len(records),'unique_frames':len(unique),'pages':math.ceil(len(unique)/12),'records':records})
    print('SWEEP',len(records),'samples',len(unique),'unique frames',math.ceil(len(unique)/12),'pages',flush=True)
def report():
    state=json.loads((ROOT/'build-state.json').read_text());assert state['status']=='ready';out=Path(state['output']);info=probe(out);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(3840,2160,'30/1');assert abs(float(info['format']['duration'])-SHEET['metadata']['duration_s'])<.15
    receipt={'output':str(out),'sha256':sha(out),'duration_s':float(info['format']['duration']),'video':v,'audio':a,'human_review':'pending','publication':'not published','existing_films':'preserved'};save(ROOT/'_qc/master-receipt.json',receipt);print(json.dumps({k:receipt[k] for k in ['output','sha256','duration_s','human_review','publication']},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('task',choices=['contacts','audio','subtitles','sweep','report']);ap.add_argument('--only',nargs='*');args=ap.parse_args()
    {'contacts':lambda:contacts(args.only),'audio':audio,'subtitles':subtitles,'sweep':sweep,'report':report}[args.task]()
