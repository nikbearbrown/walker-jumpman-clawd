// A new manifest, never overwrite the starter's historical receipts.
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),hash=v=>crypto.createHash('sha256').update(v).digest('hex');
const baseline='9387542ca473b0a252c43bfe6d4fd39b61f8d439';
const previous=p=>cp.execFileSync('git',['show',baseline+':'+p],{cwd:root,encoding:'utf8'});
const now=p=>fs.readFileSync(path.join(root,p),'utf8');
const controller=s=>s.slice(s.indexOf('func _physics_process('),s.indexOf('\nfunc ',s.indexOf('func _physics_process(')+5));
if(controller(previous('godot/features/player/player.gd'))!==controller(now('godot/features/player/player.gd')))throw Error('Physics function changed');
const preserved=['godot/features/player/tuning.gd','godot/levels/first_steps.json','godot/ui/hud.gd'];
for(const p of preserved)if(previous(p)!==now(p))throw Error('Invariant changed: '+p);
const files={};function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name==='.godot')continue;const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile())files[path.relative(root,p)]=hash(fs.readFileSync(p));}}
walk(path.join(root,'godot'));
const sorted=Object.fromEntries(Object.entries(files).sort(([a],[b])=>a.localeCompare(b)));
const record={project:'walker-jumpman-clawd',baseline_commit:baseline,created_at:new Date().toISOString(),build_id:hash(JSON.stringify(sorted)),source_sha256:sorted,invariants:{physics_function:'byte-identical',preserved_files:preserved,level_extension:'not implemented',mini_goals:'not implemented'},human_playtest_sessions:0};
fs.writeFileSync(path.join(root,'evidence/clawd/build-manifest.json'),JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record.invariants));console.log(record.build_id);
