// Secrets are supplied only on stdin and are never written into the package.
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {generateKeyPairSync,sign} from 'node:crypto';
// Only the verification key leaves this process. The signing key stays in memory.
const signingKeys=generateKeyPairSync('ec',{namedCurve:'prime256v1'});
console.log(JSON.stringify({uploadPublicKey:signingKeys.publicKey.export({type:'spki',format:'der'}).toString('base64')}));
function privateSettings(){return new Promise((resolve,reject)=>{
 let input='';const tty=process.stdin.isTTY;
 const clean=()=>{process.stdin.removeListener('data',data);process.stdin.removeListener('end',end);if(tty)process.stdin.setRawMode(false);process.stdin.pause();};
 const end=()=>{clean();reject(Error('Upload settings were not supplied'));};
 const data=chunk=>{input+=chunk;if(input.includes('\u0003')){clean();reject(Error('Upload cancelled'));return;}const at=input.search(/[\r\n]/);if(at>=0){clean();try{resolve(JSON.parse(input.slice(0,at)));}catch{reject(Error('Invalid upload settings'));}}};
 if(tty)process.stdin.setRawMode(true);process.stdin.setEncoding('utf8');process.stdin.on('data',data);process.stdin.once('end',end);process.stdin.resume();
 console.log('Ready for private media upload settings on stdin (input is hidden).');
});}
const config=await privateSettings();
const root=resolve(config.root),manifest=JSON.parse(await readFile(config.manifest,'utf8'));
const headers={'OAI-Sites-Authorization':'Bearer '+config.serviceToken,'X-Visu-Media':'1'};
async function call(path,options={}){
 for(let attempt=0;attempt<4;attempt++){
  const stamp=String(Date.now()),message=[stamp,options.method||'GET',new URL(path,config.origin).pathname,manifest.digest].join('\n');
  const signature=sign('sha256',Buffer.from(message),{key:signingKeys.privateKey,dsaEncoding:'ieee-p1363'}).toString('base64');
  const response=await fetch(new URL(path,config.origin),{...options,headers:{...headers,...options.headers,'X-Visu-Upload-Time':stamp,'X-Visu-Upload-Signature':signature},redirect:'manual'});
  if(response.status===429||response.status>=500){if(attempt===3)throw Error('Media service HTTP '+response.status);const retry=Number(response.headers.get('retry-after'))||2*(attempt+1);await new Promise(r=>setTimeout(r,Math.min(30,retry)*1000));continue;}
  if(!response.ok)throw Error('Media service HTTP '+response.status);
  return response;
 }
}
const plan=await (await call('/api/media/missing')).json();
if(plan.digest!==manifest.digest)throw Error('Published manifest does not match the upload source');
const missing=new Set(plan.missing),entries=Object.entries(manifest.files).filter(([,file])=>missing.delete(file.hash));
let cursor=0,completed=0,bytes=0;
console.log(JSON.stringify({phase:'upload',missing:entries.length,total:plan.total}));
await Promise.all(Array.from({length:6},async()=>{
 while(cursor<entries.length){const [path,file]=entries[cursor++],base=path.startsWith('assets/reviewed/')?root:resolve(config.coreRoot||root);const source=resolve(join(base,path));if(!source.startsWith(base+'\\')&&!source.startsWith(base+'/'))throw Error('Invalid local asset path');
  const body=await readFile(source);await call('/api/media/'+file.hash,{method:'PUT',body,headers:{'content-type':file.mime}});completed++;bytes+=body.length;
  if(completed%50===0||completed===entries.length)console.log(JSON.stringify({uploaded:completed,total:entries.length,bytes}));
 }
}));
const result=await (await call('/api/media/activate',{method:'POST'})).json();
if(config.report)await writeFile(config.report,JSON.stringify({...result,uploaded:completed,bytes},null,2));
console.log(JSON.stringify({phase:'active',...result,uploaded:completed,bytes}));
