"""Reuse only byte-identical scene recipes at exactly the same measured duration."""
import hashlib,json,shutil
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]
walk=GAME/'youtube/claude-liam-walker-jumpman-clawd-walkthrough'
dev=GAME/'youtube/claude-liam-walker-jumpman-clawd-gamedev'
a=json.loads((walk/'beat_sheet.json').read_text());b=json.loads((dev/'beat_sheet.json').read_text())
by_a={x['beat_id']:x for x in a['beats']};by_b={x['beat_id']:x for x in b['beats']};records=[]
for x,y in [('B01','B01'),('B02','B02'),('B13','B17'),('B14','B18'),('B18','B23'),('B19','B24')]:
    src=by_a[x];dst=by_b[y]
    for key in ['pattern','props']:
        assert src['shot']['remotion'][key]==dst['shot']['remotion'][key],(x,y,'different recipe')
    assert (walk/'remotion/src/index.tsx').read_bytes()==(dev/'remotion/src/index.tsx').read_bytes(), 'Different scene implementation'
    assert src['actual_duration_s']==dst['actual_duration_s'],(x,y,'different clock')
    clip=walk/'media'/f'{x}.mp4';assert clip.is_file()
    shutil.copy2(clip,dev/'media'/f'{y}.mp4')
    records.append({'source_reel':walk.name,'source_beat':x,'destination_beat':y,'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'reason':'Identical scene recipe and measured duration; reuse already inspected 4K output.'})
(dev/'evidence/reused-scenes.json').write_text(json.dumps(records,indent=2)+'\n')
print('Reused',len(records),'identical scene renders.')
