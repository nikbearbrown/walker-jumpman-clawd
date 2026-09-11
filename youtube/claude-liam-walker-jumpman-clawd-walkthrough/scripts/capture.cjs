const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const reel=path.resolve(__dirname,'..'),game=path.resolve(reel,'../..');
const engine='/Applications/Godot.app/Contents/MacOS/Godot';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const manifest=JSON.parse(fs.readFileSync(path.join(game,'evidence/clawd/build-manifest.json')));
function checkSource(){for(const [p,h] of Object.entries(manifest.source_sha256))if(hash(path.join(game,p))!==h)throw Error('Game changed: '+p)}
checkSource();
const copy=path.join(reel,'_capture-project'),capture=path.join(reel,'capture');
fs.mkdirSync(copy,{recursive:true});fs.mkdirSync(capture,{recursive:true});
cp.execFileSync('rsync',['-a','--exclude=.godot',path.join(game,'godot/') ,copy+'/']);
fs.copyFileSync(path.join(__dirname,'capture_driver.gd'),path.join(copy,'capture_driver.gd'));
fs.copyFileSync(path.join(__dirname,'gallery_capture.gd'),path.join(copy,'gallery_capture.gd'));
const takes=process.argv.slice(2).length?process.argv.slice(2):['controls','jump','spike','fall','pause','coyote','buffer','finish'];
for(const take of takes){
 if(!/^[a-z0-9-]+$/.test(take))throw Error('Invalid take');
 const receipt=path.join(capture,take+'-receipt.json');
 if(fs.existsSync(receipt))throw Error('Take exists; preserve it before recapturing: '+take);
 console.log('Capturing '+take+' from the unmodified game');
 const driver=take.startsWith('gallery-')||take.startsWith('inspector')?'gallery_capture.gd':'capture_driver.gd';
 const args=['--path',copy,'--script','res://'+driver,'--fixed-fps','60','--quit-after',driver==='gallery_capture.gd'?'9600':'2400','--',capture,take];
 const result=cp.spawnSync(engine,args,{encoding:'utf8',timeout:300000,maxBuffer:2000000});
 fs.writeFileSync(path.join(capture,take+'-process.json'),JSON.stringify({command:[engine,...args],exit_code:result.status,stdout:result.stdout,stderr:result.stderr,error:result.error?.message},null,2)+'\n');
 console.log(result.stdout);
 if(result.status!==0||!fs.existsSync(receipt))throw Error('Capture failed: '+take+' '+result.stderr);
 const r=JSON.parse(fs.readFileSync(receipt));
 if(r.status!=='PASS'||r.frames<2||r.test_mode||r.test_control)throw Error('Bad capture receipt');
 const rows=fs.readFileSync(path.join(capture,take+'-states.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
 for(let i=1;i<rows.length;i++){const a=rows[i-1],b=rows[i];if(a.state===1&&b.state===1&&b.player_tick>a.player_tick+1)throw Error('Capture skipped physics ticks: '+take)}
 const movie=path.join(capture,take+'.mp4');
 cp.execFileSync('ffmpeg',['-y','-v','error','-framerate','30','-i',path.join(capture,'frames',take,'%06d.png'),'-frames:v',String(r.frames),'-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',movie],{timeout:180000});
 Object.assign(r,{build_id:manifest.build_id,source_commit:cp.execFileSync('git',['rev-parse','HEAD'],{cwd:game,encoding:'utf8'}).trim(),source_worktree:'Clawd modifications, exact build_id is authoritative',driver_sha256:hash(path.join(__dirname,driver)),video_sha256:hash(movie),no_skipped_physics_ticks:driver==='capture_driver.gd'});
 fs.writeFileSync(receipt,JSON.stringify(r,null,2)+'\n');
 checkSource();console.log('Verified real 4K take: '+take);
}
