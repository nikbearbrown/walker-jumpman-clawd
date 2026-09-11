// Historical command now forwards to the Clawd manifest writer. Original source
// remains in Git history; never overwrite the starter's historical receipt.
require('./clawd-build.cjs');
process.exit(0);
// Legacy implementation retained below as reference only, never executed.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '..');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const files = {};
function walk(dir) {
  for (const item of fs.readdirSync(dir, {withFileTypes:true})) {
    if (item.name === '.godot') continue;
    const full = path.join(dir, item.name);
    if (item.isDirectory()) walk(full);
    else if (item.isFile()) files[path.relative(root,full)] = hash(fs.readFileSync(full));
  }
}
walk(path.join(root,'godot'));
files['walker-jumpman.command'] = hash(fs.readFileSync(path.join(root,'walker-jumpman.command')));
const sorted = Object.fromEntries(Object.entries(files).sort(([a],[b])=>a.localeCompare(b)));
const evidence = path.join(root,'evidence');
const reports = fs.readdirSync(evidence).filter(n=>/^(mechanics|keyboard)-.*\.json$/.test(n));
const latest = prefix => reports.filter(n=>n.startsWith(prefix)).sort((a,b)=>fs.statSync(path.join(evidence,b)).mtimeMs-fs.statSync(path.join(evidence,a)).mtimeMs)[0];
const selected = [latest('mechanics'),latest('keyboard')];
const results = selected.map(name=>({file:'evidence/'+name,...JSON.parse(fs.readFileSync(path.join(evidence,name),'utf8'))}));
if(results.some(r=>r.failures!==0)) throw Error('Latest report failed; cannot mark build ready');
const record = {
  project:'walker-jumpman', build_id:hash(JSON.stringify(sorted)),
  created_at:new Date().toISOString(),
  engine:'4.7.2.stable.official.ed1daf0bf', renderer:'Compatibility',
  scope:'First Steps local control/retry slice', source_sha256:sorted,
  tests:results.map(r=>({file:r.file,checks:r.results.length,failures:r.failures})),
  machine_checks_passed:results.reduce((n,r)=>n+r.results.length,0),
  human_playtest_sessions:0, exported:false, game_published:false,
  screenshots:['01-menu','02-failure','03-jump','04-complete'].map(n=>({file:'evidence/screens/'+n+'.png',sha256:hash(fs.readFileSync(path.join(evidence,'screens',n+'.png')))}))
};
fs.writeFileSync(path.join(evidence,'build-manifest.json'), JSON.stringify(record,null,2)+'\n');
console.log(JSON.stringify({build_id:record.build_id,source_files:Object.keys(sorted).length,checks:record.machine_checks_passed,tests:record.tests},null,2));
