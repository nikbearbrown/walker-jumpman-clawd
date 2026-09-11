import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Img,staticFile,delayRender,continueRender,interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {ClaudeComposerAsk} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/ClaudeComposerAsk';
import {BrutalistHesitantWriter} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/BrutalistHesitantWriter';
import {ClaudeVerdictArtifact} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/ClaudeVerdictArtifact';
import {ClaudeTitleOutro} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/ClaudeTitleOutro';
import {GodotDevWorkbench,godotDevWorkbenchSchema} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/GodotDevWorkbench';
import {WalkerGodotSetup,walkerGodotSetupSchema} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/WalkerGodotSetup';
const fontGate=delayRender('Local fonts');
Promise.all([['EB Garamond','EBGaramond-Regular.ttf'],['Inter','Inter-Regular.ttf'],['PT Mono','PTMono-Regular.ttf']].map(async([family,file])=>{const f=new FontFace(family,`url(${staticFile(file)})`);await f.load();document.fonts.add(f);})).then(()=>continueRender(fontGate));
const INK='#3D3929',BG='#FAF9F5',ACC='#BE593A',EDGE='#C9C4B9';
const titleStyle:any={position:'absolute',left:110,right:110,top:65,fontFamily:'"EB Garamond",Georgia,serif',fontSize:68,lineHeight:1.08,color:INK};
type Props={title:string;rows?:string[][];note?:string;mode?:string;image?:string;collider?:boolean;durationSeconds?:number;cueSeconds?:number[]};
const AssignmentBoard:React.FC<Props>=(p)=>{
 const f=useCurrentFrame(),{fps}=useVideoConfig(),t=f/fps;
 const rowTimes=p.cueSeconds||[.5,3,6];
 const active=Math.max(0,rowTimes.reduce((n,c,i)=>t>=c?i:n,0));
 return <AbsoluteFill style={{background:BG,color:INK,fontFamily:'Inter,sans-serif'}}>
  <div style={titleStyle}>{p.title}</div>
  <div style={{position:'absolute',left:110,top:178,right:110,height:2,background:EDGE}}/>
  {(p.rows||[]).map(([label,value],i)=><div key={i} style={{position:'absolute',left:120,right:120,top:240+i*210,height:174,borderLeft:`6px solid ${i===active?ACC:EDGE}`,borderBottom:`1px solid ${EDGE}`,padding:'18px 30px',boxSizing:'border-box',opacity:interpolate(t,[rowTimes[i]||0,(rowTimes[i]||0)+.3],[.55,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
   <div style={{fontSize:30,lineHeight:1.2,color:'#66614F',marginBottom:20}}>{label}</div>
   <div style={{fontFamily:p.mode==='repos'&&i<2?'"PT Mono",monospace':'Inter,sans-serif',fontSize:p.mode==='repos'?35:39,lineHeight:1.25,overflowWrap:'anywhere'}}>{value}</div>
  </div>)}
  <div style={{position:'absolute',left:120,right:150,bottom:80,fontSize:27,lineHeight:1.3,color:INK}}>{p.note}</div>
 </AbsoluteFill>;
};
const EnginePreview:React.FC<Props>=(p)=><AbsoluteFill style={{background:BG,color:INK,fontFamily:'Inter,sans-serif'}}>
 <Img src={staticFile(p.image!)} style={{position:'absolute',width:1920,height:1080}}/>
 <div style={titleStyle}>{p.title}</div>
 <div style={{position:'absolute',left:125,top:190,fontSize:27}}>{p.note}</div>
 <div style={{position:'absolute',left:350,top:255,fontSize:32}}>Facing right</div>
 <div style={{position:'absolute',left:1190,top:255,fontSize:32}}>Facing left</div>
 <div style={{position:'absolute',left:125,bottom:70,fontSize:32}}>{p.collider?'Orange = actual physics rectangle · 18 × 28 units':'Procedural art · no imported sprite sheet'}</div>
 <div style={{position:'absolute',right:125,bottom:70,fontSize:30,fontFamily:'"EB Garamond",Georgia,serif'}}>@NikBearBrown</div>
</AbsoluteFill>;
const Thesis:React.FC<any>=(p)=><BrutalistHesitantWriter {...p} contextTitle="Iteration 1 · one change at a time" contextItems={[{label:'Now',detail:'Clawd in the existing First Steps level.'},{label:'Later',detail:'Task mini-goals and the level extension.'}]} yOffset={-80} brandLabel="@NikBearBrown"/>;
const Verdict:React.FC<any>=(p)=><ClaudeVerdictArtifact {...p} brandLabel="@NikBearBrown"/>;
const entries:any[]=[['AssignmentBoard',AssignmentBoard],['EnginePreview',EnginePreview],['ClaudeComposerAsk',ClaudeComposerAsk],['BrutalistHesitantWriter',Thesis],['ClaudeVerdictArtifact',Verdict],['ClaudeTitleOutro',ClaudeTitleOutro],['GodotDevWorkbench',(p:any)=><GodotDevWorkbench {...godotDevWorkbenchSchema.parse(p)}/>],['WalkerGodotSetup',(p:any)=><WalkerGodotSetup {...walkerGodotSetupSchema.parse(p)}/>]];
const Root=()=> <>{entries.map(([id,component])=><Composition key={id} id={id} component={component} width={1920} height={1080} fps={30} durationInFrames={300} defaultProps={{durationSeconds:10}} calculateMetadata={({props})=>({durationInFrames:Math.ceil((props.durationSeconds||10)*30)})}/>)}</>;
registerRoot(Root);
