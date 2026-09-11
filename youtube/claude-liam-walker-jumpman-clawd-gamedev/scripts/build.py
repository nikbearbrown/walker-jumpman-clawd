"""Measured audio, source-result edit decisions, canonical scene rendering."""
import argparse,hashlib,importlib.util,json,math,os,shutil,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
ART=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art')
SHEET=ROOT/'beat_sheet.json'
FPS=30
def run(args,**kw):return subprocess.run(list(map(str,args)),check=True,**kw)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True))
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def load():return json.loads(SHEET.read_text())
def lock():
    sheet=load()
    if sheet['metadata'].get('audio_locked'):raise SystemExit('Already locked; do not pad twice.')
    for b in sheet['beats']:
        if b['narration_text']:
            source=ROOT/'mp3'/f"beat-{b['beat_id']}.mp3";lead=b.get('lead_silence_s',0)
            d=math.ceil((probe(source)+lead+.3)*FPS)/FPS
            dest=ROOT/'audio'/f"{b['beat_id']}.wav"
            run(['ffmpeg','-v','error','-y','-i',source,'-af',f'adelay={round(lead*1000)}:all=1,apad','-t',str(d),'-ar','48000','-ac','2','-c:a','pcm_s16le',dest])
            b.update(audio_file=dest.relative_to(ROOT).as_posix(),actual_duration_s=d)
        else:
            choices=sorted((ART/'svg/claude/mp3').glob('*.mp3'));source=choices[sum(map(ord,sheet['metadata']['slug']))%len(choices)]
            dest=ROOT/'audio/outro-jingle.mp3';shutil.copy2(source,dest)
            b.update(audio_file='audio/outro-jingle.mp3',actual_duration_s=math.ceil(probe(dest)*FPS)/FPS,kind='outro_jingle',jingle_source=str(source),jingle_sha256=sha(dest))
            b.pop('silent',None);b.pop('audio_policy',None)
        if b['shot'].get('remotion'):b['shot']['remotion']['props']['durationSeconds']=b['actual_duration_s']
    sheet['metadata'].update(audio_locked=True,duration_s=sum(b['actual_duration_s'] for b in sheet['beats']))
    save(SHEET,sheet)
    (ROOT/'SHOPPING.md').write_text('# Audio-locked asset plan\n\nNo paid generation needed. Actual Godot captures and code-native scenes supply the visuals. All %d beats have renderable sources, including the regular outro.\n\nMeasured runtime: %.3f seconds.\n'%(len(sheet['beats']),sheet['metadata']['duration_s']))
    print('AUDIO LOCKED',sheet['metadata']['duration_s'],flush=True)
def cues():
    sheet=load();words=json.loads((ROOT/'mp3/words.json').read_text());rows=[]
    import re
    norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
    for b in sheet['beats']:
        if not b.get('cue_phrases'):continue
        tokens=words['beats'][b['beat_id']];bound=[]
        for cue in b['cue_phrases']:
            target=list(map(norm,cue['phrase'].split()))
            hits=[i for i in range(len(tokens)) if [norm(x['text']) for x in tokens[i:i+len(target)]]==target]
            if not hits:raise ValueError(f"Unmatched {b['beat_id']}: {cue['phrase']}")
            bound.append({'at':tokens[hits[0]]['startFrame']/words['fps']+b.get('lead_silence_s',0),'line':cue['line'],'label':cue['label']})
        b['shot']['remotion']['props']['cues']=sorted(bound,key=lambda x:x['at']);rows.append({'beat':b['beat_id'],'cues':bound})
    save(SHEET,sheet);save(ROOT/'evidence/cue-timing.json',{'method':'Known-script words aligned to local TTS; unmatched words interpolate between recognition anchors.','rows':rows})
def overlay(path,title,sub):
    im=Image.new('RGBA',(3840,2160));d=ImageDraw.Draw(im)
    font=lambda n:ImageFont.truetype(str(ROOT/'remotion/public/Inter-Regular.ttf'),n)
    # The empty region above the level, below the fixed HUD. No action occlusion.
    d.rounded_rectangle((140,451,3200,601),radius=14,fill='#fffdf7')
    d.text((176,467),title,font=font(44),fill='#25354a')
    d.text((176,534),sub,font=font(34),fill='#25354a')
    im.save(path)
def footage(only=None,force=False):
    sheet=load();edits=[]
    for b in sheet['beats']:
        if not b.get('gameplay_take') or (only and b['beat_id'] not in only):continue
        bid=b['beat_id'];source=ROOT/b['shot']['evidence_media'];target=ROOT/'media'/f'{bid}.mp4'
        raw=probe(source);start=0
        # Preserve the complete captured interval, including its observed replay.
        # Extra repeats for narration are explicitly labelled; never retime a
        # gameplay recording or manufacture an additional successful attempt.
        end=raw
        played=end-start;total=b['actual_duration_s']
        gallery=b['gameplay_take'].startswith('gallery-') or b['gameplay_take']=='inspector'
        if not gallery: assert total>=played,'Narration shorter than played action; never silently trim gameplay.'
        label=ROOT/'media'/f'{bid}-label.png';hold=ROOT/'media'/f'{bid}-hold.png'
        if not gallery:
            overlay(label,b['heading'],'Actual Godot output · scripted normal input · walker-jumpman-clawd')
            overlay(hold,b['heading'],'REPLAY for inspection · same captured take, not an additional test')
        if not target.exists() or force:
            print('FOOTAGE',bid,flush=True)
            if gallery:
                assert total <= raw, 'Capture a longer gallery; do not silently loop the diagnostic.'
                run(['ffmpeg','-v','error','-y','-i',source,'-t',str(total),'-an','-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p',target])
            else:
                run(['ffmpeg','-v','error','-y','-stream_loop','-1','-i',source,'-i',label,'-i',hold,'-filter_complex_threads','2','-filter_complex',f"[0:v]fps=30[base];[base][1:v]overlay=0:0:enable='lt(t,{played})'[v1];[v1][2:v]overlay=0:0:enable='gte(t,{played})'[out]",'-map','[out]','-t',str(total),'-an','-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p',target])
        b['qc']={'full_bleed':True,'full_bleed_reason':'Actual native 4K Godot gameplay fills the frame; not a slide with title-safe margins. Inspect all original HUD text and action.',
            'contrast_reason':'The world includes a dimming scrim on state cards. Region checks measure actual stable text, while manual full-frame review checks game/action/card readability. Other gates remain enabled.',
            'contrast_regions':[{'label':'Title','box':[.025,.025,.40,.082]},{'label':'Controls','box':[.025,.10,.70,.15]},{'label':'Evidence disclosure','box':[.045,.215,.81,.275]},{'label':'Game footer','box':[.025,.94,.45,.995]}]}
        if gallery:
            b['qc']={'contrast_reason':'Native Godot diagnostic: measure its actual text bands; inspect the drawings separately. All other gates remain enabled.', 'contrast_regions':[
                {'label':'Diagnostic title','box':[.05,.04,.91,.105]},
                {'label':'Diagnostic disclosure','box':[.05,.108,.95,.178]},
                {'label':'Diagnostic footer','box':[.05,.88,.95,.94]}]}
        edits.append({'beat':bid,'source':str(source.relative_to(ROOT)),'source_sha256':sha(source),'source_start_s':start,'source_end_s':min(end,total),'normal_speed_interval_s':min(played,total),'repeat_after_s':played if not gallery and total>played else None,'replay_labelled':not gallery,'output_duration_s':total,'retimed':False,'output_sha256':sha(target)})
    save(SHEET,sheet)
    old=ROOT/'evidence/edit-map.json';prior=json.loads(old.read_text()) if old.exists() else []
    by={r['beat']:r for r in prior};by.update({r['beat']:r for r in edits});save(old,list(by.values()))
def render(only=None,force=False):
    sys.path.insert(0,str(ART/'runtime/scripts'))
    spec=importlib.util.spec_from_file_location('canonical',ART/'runtime/scripts/remotion_scenes.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    mod.PROJECT=ROOT/'remotion';mod.ENTRY='src/index.tsx';mod.CONSUMERS=ROOT/'remotion/consumers.json'
    os.environ['ART_CHROME']='/Users/bear/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';os.environ['ART_CHROME_MODE']='chrome-for-testing'
    sheet=load()
    for b in sheet['beats']:
        if not b['shot'].get('remotion') or (only and b['beat_id'] not in only):continue
        print('RENDER',b['beat_id'],flush=True);result=mod.render_beat(ROOT,b,force);print(result,flush=True)
        if result.startswith('FAIL'):raise RuntimeError(result)
        from datetime import datetime,timezone
        mod.stamp(b,ROOT,datetime.now(timezone.utc).isoformat());save(SHEET,sheet)
    mod.update_consumers(sheet,ROOT)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('task',choices=['lock','cues','footage','render']);ap.add_argument('--only',nargs='*');ap.add_argument('--force',action='store_true');args=ap.parse_args()
    {'lock':lock,'cues':cues,'footage':lambda:footage(args.only,args.force),'render':lambda:render(args.only,args.force)}[args.task]()
