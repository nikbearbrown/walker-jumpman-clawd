"""Bind measured new captures to both recipes; source unchanged or fail closed."""
import hashlib,json,shutil,subprocess
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]
WALK=GAME/'youtube/claude-liam-walker-jumpman-clawd-walkthrough'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
manifest=json.loads((GAME/'evidence/clawd/build-manifest.json').read_text())
for path,digest in manifest['source_sha256'].items():assert sha(GAME/path)==digest,path
for kind in ['walkthrough','gamedev']:
    root=GAME/'youtube'/f'claude-liam-walker-jumpman-clawd-{kind}'
    sheet=json.loads((root/'beat_sheet.json').read_text())
    save(root/'evidence/source-build.json',manifest)
    for file in ['CHANGE-BRIEF.md','FRICTIONAL.md','SOURCES.md']:shutil.copy2(GAME/file,root/'evidence'/file)
    captures={};docs=[]
    takes=sorted({b['gameplay_take'] for b in sheet['beats'] if b.get('gameplay_take')})
    for take in takes:
        capture_take='inspector-v3' if take=='inspector' else take+'-v2' if take.startswith('gallery-') else take
        src=WALK/'capture'/f'{capture_take}.mp4'
        receipt=json.loads((WALK/'capture'/f'{capture_take}-receipt.json').read_text())
        assert receipt['status']=='PASS' and receipt['build_id']==manifest['build_id'] and receipt['video_sha256']==sha(src),take
        dst=root/'media'/f'source-{take}.mp4';shutil.copy2(src,dst)
        for suffix in ['-receipt.json','-inputs.jsonl','-states.jsonl']:shutil.copy2(WALK/'capture'/f'{capture_take}{suffix}',root/'evidence'/f'{take}{suffix}')
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(src)],text=True))
        docs.append({'take':take,'duration_s':duration,'sha256':sha(src),'method':receipt.get('method',receipt.get('input_method'))})
        if take!='inspector':captures[take]={'path':dst.relative_to(root).as_posix(),'sha256':sha(dst),'build_id':manifest['build_id'],'method':'scripted-input','input_log':f'evidence/{take}-inputs.jsonl','duration_s':duration}
    if kind=='walkthrough':
        rows=[]
        for feature,take,bid in json.loads((root/'evidence/feature-beats.json').read_text()):
            if take=='inspector':continue # Diagnostic art is not a claimed input-driven game feature.
            b=next(b for b in sheet['beats'] if b['beat_id']==bid)
            inputs=[json.loads(l) for l in (root/'evidence'/f'{take}-inputs.jsonl').read_text().splitlines()]
            action=next((x['time_s'] for x in inputs if x.get('kind')=='key_down'),.1)
            rows.append({'id':feature,'status':'implemented','evidence':[{'capture':take,'beat_id':bid,'start_s':0,'action_s':action,'end_s':min(captures[take]['duration_s']-.05,b.get('actual_duration_s',999)),'observation':b['heading'],'riff':b['narration_text']}]})
        for feature,reason in [('task-mini-goals','Future design only'),('level-extension','Later Assignment 1 work'),('new-hazards','Later design decision'),('cherries-settings-export','Historical full GDD, not this playable slice')]:rows.append({'id':feature,'status':'planned','reason':reason,'evidence':[]})
        save(root/'coverage.json',{'schema_version':1,'game':{'name':'walker-jumpman-clawd','build_id':manifest['build_id']},'captures':captures,'features':rows})
    else:
        ledger=json.loads((root/'gamedev-evidence.json').read_text())
        for pair in ledger['code_result_pairs']:pair['media']['sha256']=sha(root/pair['media']['path'])
        save(root/'gamedev-evidence.json',ledger)
    save(root/'evidence/capture-sources.json',docs)
    (root/'CAPTURE.md').write_text('# Native engine evidence\n\n'+
        'Build ID: '+manifest['build_id']+'. SHA-256 of sorted source-hash JSON; see evidence/source-build.json.\n\n'+
        'Godot 4.7.2.stable.official.ed1daf0bf, Compatibility. Native 3840×2160 SubViewport from a 640×360 logical game canvas, 60-Hz fixed simulation and 30-fps PNG capture. Offline rendering is not a real-time performance benchmark.\n\n'+
        'Gameplay driver: scripted physical key events via Godot Input and SubViewport delivery; no teleports, internal test_control, or state injection. Focus loss is an explicitly simulated Window event. Gallery pages are selected with gallery key events, then their diagnostic display clock is advanced per rendered frame (600 frames for 20 seconds). Inspector is a staged draw using the actual art helper and original collider dimensions, not gameplay. These diagnostic clocks do not alter normal gameplay simulation. These are not human playtests.\n\n'+
        'Bounded capture drivers and per-take inputs, states, hashes and receipts are retained. All sources copied inside each reel. Audio: the game has no sound; local Liam narration only until the regular stock outro. No invented game effects. Full actual action intervals play at normal simulation speed; additional review replays are visibly labelled as the same take, not independent tests. Gallery excerpts are native continuously animated previews, never gameplay claims.\n')
    print('Prepared',kind,len(takes),'captures')
