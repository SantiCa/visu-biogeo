import {readFile,writeFile} from 'node:fs/promises';import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url),manifest=JSON.parse(await readFile(new URL('hosting/visu-biogeo-media/media-manifest.json',root),'utf8')),origin='https://visu-biogeo-santica.nimblequail260.chatgpt.site/';
const paths=['index.html','app.js','styles.css','engine.mjs','classification-learning.mjs','taxonomy-guide.mjs','taxon-reference.mjs','exam-photos.mjs','data/learning-taxonomy.json','data/learning-geology.json','data/study-notes.json','data/curated-images.json','sw.js'];
const checks=await Promise.all(paths.map(async path=>{const response=await fetch(new URL(path,origin),{cache:'no-store'}),bytes=new Uint8Array(await response.arrayBuffer());let checked=bytes,providerScriptAdded=false;
 // The hosting provider appends its security challenge to HTML responses. Verify
 // the exact original markup separately; do not alter the response or protection.
 if(path==='index.html'){
  const text=new TextDecoder().decode(bytes),providerScripts=[...text.matchAll(/<script>[^<]*window\.__CF\$cv\$params[^<]*<\/script>/g)].map(m=>m[0]).filter(s=>s.includes('/cdn-cgi/challenge-platform/scripts/jsd/main.js'));
  if(providerScripts.length===1){checked=new TextEncoder().encode(text.replace(providerScripts[0],''));providerScriptAdded=true;}
 }
 return {path,status:response.status,hashMatches:createHash('sha256').update(checked).digest('hex')===manifest.files[path].hash,...(providerScriptAdded?{providerScriptAdded}: {})};}));
const response=await fetch(new URL('api/media/activate',origin),{method:'POST'});const report={publicFiles:checks,unsignedActivationStatus:response.status,site:origin,manifestDigest:manifest.digest};
await writeFile(new URL('output/validation-zero-photos-v8.11.json',root),JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(checks.some(r=>r.status!==200||!r.hashMatches)||response.status!==403)process.exitCode=1;
