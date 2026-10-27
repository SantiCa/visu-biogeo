// Read access follows the Site audience. Every bank update also needs a signed
// request from the uploader whose public key the Site owner configured.
const MANIFEST=/*__MANIFEST__*/null;
const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'content-type':'application/json','cache-control':'no-store','x-content-type-options':'nosniff'}});
const waiting=()=>new Response('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Visu BioGeo</title><body style="font:18px system-ui;max-width:650px;margin:12vh auto;padding:24px;color:#123c32"><h1>Visu BioGeo</h1><p>Estamos guardando el banco de imágenes de esta instalación privada.</p><p>La aplicación estará disponible cuando termine la copia.</p></body></html>',{headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-store'}});

export function createAssetWorker(current){
 const byHash=new Map(Object.values(current.files).map(file=>[file.hash,file]));
 let previousManifest=null;
 let importedPublicKey=null,publicKeyValue=null;
 async function authorizedUpload(request,env,path){
  const stamp=request.headers.get('x-visu-upload-time'),signature=request.headers.get('x-visu-upload-signature');
  if(!env.VISU_MEDIA_PUBLIC_KEY||!stamp||!/^\d{13}$/.test(stamp)||Math.abs(Date.now()-Number(stamp))>300000||!signature)return false;
  try{
   const decode=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
   if(publicKeyValue!==env.VISU_MEDIA_PUBLIC_KEY){importedPublicKey=await crypto.subtle.importKey('spki',decode(env.VISU_MEDIA_PUBLIC_KEY),{name:'ECDSA',namedCurve:'P-256'},false,['verify']);publicKeyValue=env.VISU_MEDIA_PUBLIC_KEY;}
   const message=[stamp,request.method,path,current.digest].join('\n');
   return await crypto.subtle.verify({name:'ECDSA',hash:'SHA-256'},importedPublicKey,decode(signature),new TextEncoder().encode(message));
  }catch{return false;}
 }
 async function storedHashes(bucket){
  const hashes=new Set();let cursor;
  do{const page=await bucket.list({prefix:'blobs/',limit:1000,...(cursor?{cursor}:{})});for(const item of page.objects)hashes.add(item.key.slice(6));cursor=page.truncated?page.cursor:undefined;}while(cursor);
  return hashes;
 }
 async function activeManifest(bucket){
  const head=await bucket.head('active-manifest.json');if(!head)return null;
  const digest=head.customMetadata?.digest;
  if(digest===current.digest)return current;
  if(previousManifest?.digest===digest)return previousManifest;
  const object=await bucket.get('active-manifest.json');if(!object)return null;
  previousManifest=JSON.parse(await object.text());return previousManifest;
 }
 return {async fetch(request,env){
  if(!env.BUCKET)return json({error:'Media storage is not connected'},503);
  const url=new URL(request.url),path=url.pathname;
  if(path.startsWith('/api/media/')){
   // Never rely on a custom header or the public/private audience as permission.
   if(request.headers.get('x-visu-media')!=='1')return json({error:'Forbidden'},403);
   const origin=request.headers.get('origin');if(origin&&origin!==url.origin)return json({error:'Forbidden origin'},403);
   if(!await authorizedUpload(request,env,path))return json({error:'Uploader signature required'},403);
   if(path==='/api/media/missing'&&request.method==='GET'){
    const stored=await storedHashes(env.BUCKET);const missing=[...byHash.keys()].filter(hash=>!stored.has(hash));
    return json({digest:current.digest,total:byHash.size,missing});
   }
   if(path==='/api/media/activate'&&request.method==='POST'){
    const stored=await storedHashes(env.BUCKET);const missing=[...byHash.keys()].filter(hash=>!stored.has(hash));
    if(missing.length)return json({error:'Incomplete bank',missing:missing.length},409);
    await env.BUCKET.put('active-manifest.json',JSON.stringify(current),{httpMetadata:{contentType:'application/json'},customMetadata:{digest:current.digest}});
    return json({active:true,digest:current.digest,files:Object.keys(current.files).length});
   }
   const match=/^\/api\/media\/([a-f0-9]{64})$/.exec(path);
   if(match&&request.method==='PUT'){
    const file=byHash.get(match[1]);if(!file)return json({error:'Unknown asset'},404);
    const declared=Number(request.headers.get('content-length'));
    if(declared&&declared!==file.bytes)return json({error:'Incorrect length'},400);
    if(file.bytes>20*1024*1024)return json({error:'Asset too large'},413);
    const bytes=await request.arrayBuffer();if(bytes.byteLength!==file.bytes)return json({error:'Incorrect length'},400);
    const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');
    if(hash!==match[1])return json({error:'Incorrect asset hash'},400);
    await env.BUCKET.put('blobs/'+hash,bytes,{httpMetadata:{contentType:file.mime}});
    return json({stored:true,hash});
   }
   return json({error:'Method or route not supported'},405);
  }
  if(request.method!=='GET'&&request.method!=='HEAD')return new Response('Method not allowed',{status:405});
  const active=await activeManifest(env.BUCKET);if(!active)return path==='/'||path==='/index.html'?waiting():new Response('Preparing app',{status:503});
  let decoded;try{decoded=decodeURIComponent(path);}catch{return new Response('Invalid path',{status:400});}
  const relative=decoded==='/'?'index.html':decoded.slice(1),file=active.files[relative];
  if(!file)return new Response('Not found',{status:404});
  const headers={'content-type':file.mime,'content-length':String(file.bytes),'x-content-type-options':'nosniff','referrer-policy':'no-referrer','etag':'"'+file.hash+'"','cache-control':relative.startsWith('assets/reviewed/')?'private, max-age=31536000, immutable':'no-cache'};
  if(request.headers.get('if-none-match')===headers.etag)return new Response(null,{status:304,headers});
  if(request.method==='HEAD')return new Response(null,{headers});
  const object=await env.BUCKET.get('blobs/'+file.hash);if(!object)return new Response('Asset not available',{status:503});
  return new Response(object.body,{headers});
 }};
}
export default createAssetWorker(MANIFEST||{digest:'unbuilt',files:{}});
