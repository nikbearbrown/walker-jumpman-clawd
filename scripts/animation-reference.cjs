// Regenerate independent numeric reference values from Brutalist's TypeScript.
// Usage: node scripts/animation-reference.cjs /absolute/path/to/brutalist.art
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const art=path.resolve(process.argv[2]||'../brutalist.art');
const file=path.join(art,'runtime/remotion/src/scenes/ClaudeMascotScene.tsx');
const source=fs.readFileSync(file,'utf8');
const ts=require(path.join(art,'runtime/remotion/node_modules/typescript'));
const code=source.slice(source.indexOf('interface AnimState'),source.indexOf('// SVG mascot renderer'));
const interpolate=(v,x,y)=>{if(v<=x[0])return y[0];for(let i=1;i<x.length;i++)if(v<=x[i])return y[i-1]+(v-x[i-1])/(x[i]-x[i-1])*(y[i]-y[i-1]);return y.at(-1)};
const context={exports:{},interpolate,Math};vm.createContext(context);
vm.runInContext(ts.transpileModule(code,{compilerOptions:{module:ts.ModuleKind.CommonJS}}).outputText,context);
const names=['idle','bounce','wave','look','walk','run','think','type','sleep','error','nod','shake','dance','stretch','crouch','jump','spin','celebrate'];
const rows=[];
for(const name of names)for(const seconds of [0,1/30,2/30,.1,.231,.73,1.03,2.69,4.21]){
 const s=context.exports.computeAnimation(name,seconds*30,30);
 rows.push({name,seconds,expected:{x:s.mascotTx,y:s.mascotTy,sx:s.mascotScaleX,sy:s.mascotScaleY,left_arm:s.leftArmTy,right_arm:s.rightArmTy,eye_x:s.eyeTx,eye_h:s.leftEyeH,legs:[s.leg1Ty,s.leg2Ty,s.leg3Ty,s.leg4Ty]}});
}
const out={source:'brutalist.art/runtime/remotion/src/scenes/ClaudeMascotScene.tsx',source_sha256:crypto.createHash('sha256').update(source).digest('hex'),rows};
fs.writeFileSync(path.join(__dirname,'../godot/tests/clawd-reference.json'),JSON.stringify(out,null,2)+'\n');
console.log(rows.length+' independent animation samples written.');
