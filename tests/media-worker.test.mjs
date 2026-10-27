import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash,generateKeyPairSync,sign} from 'node:crypto';
const keys=generateKeyPairSync('ec',{namedCurve:'prime256v1'}),publicKey=keys.publicKey.export({type:'spki',format:'der'}).toString('base64');
import {createAssetWorker} from '../desktop/media-worker.mjs';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
function fixture(html='APP'){
 const contents={'index.html':html,'assets/reviewed/test.jpg':'PHOTO'};
 const files=Object.fromEntries(Object.entries(contents).map(([path,body])=>[path,{hash:hash(body),bytes:Buffer.byteLength(body),mime:path.endsWith('jpg')?'image/jpeg':'text/html'}]));
 const manifest={digest:hash(JSON.stringify(files)),files};activeDigest=manifest.digest;return {contents,manifest};
}
function bucket(){const objects=new Map();return {objects,async head(key){const item=objects.get(key);return item?{customMetadata:item.metadata.customMetadata||{}}:null;},async get(key){const item=objects.get(key);if(!item)return null;return {body:new Blob([item.body]).stream(),text:async()=>Buffer.from(item.body).toString()};},async put(key,body,metadata={}){objects.set(key,{body:typeof body==='string'?Buffer.from(body):Buffer.from(body),metadata});},async list({prefix,cursor,limit}){const keys=[...objects.keys()].filter(key=>key.startsWith(prefix)).sort(),start=Number(cursor||0),selected=keys.slice(start,start+limit);return {objects:selected.map(key=>({key})),truncated:start+limit<keys.length,cursor:String(start+limit)};}};}
const request=(path,{method='GET',body,headers={}}={},manifest=null)=>{const stamp=String(Date.now()),message=[stamp,method,path,manifest?.digest||activeDigest].join('\n');const signature=sign('sha256',Buffer.from(message),{key:keys.privateKey,dsaEncoding:'ieee-p1363'}).toString('base64');return new Request('https://visu.test'+path,{method,body,headers:{'x-visu-media':'1','x-visu-upload-time':stamp,'x-visu-upload-signature':signature,...headers}});};
let activeDigest='';
async function upload(worker,env,f){for(const [path,body] of Object.entries(f.contents)){const r=await worker.fetch(request('/api/media/'+f.manifest.files[path].hash,{method:'PUT',body},f.manifest),env);assert.equal(r.status,200);}}

test('signed media API rejects cross-site submissions and files outside the committed manifest',async()=>{
 const f=fixture(),worker=createAssetWorker(f.manifest),env={BUCKET:bucket(),VISU_MEDIA_PUBLIC_KEY:publicKey};
 assert.equal((await worker.fetch(new Request('https://visu.test/api/media/missing'),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/missing',{headers:{origin:'https://attacker.test'}}),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/'+hash('unknown'),{method:'PUT',body:'unknown'}),env)).status,404);
 assert.equal((await worker.fetch(request('/api/media/'+f.manifest.files['index.html'].hash,{method:'PUT',body:'BAD'}),env)).status,400);
 assert.equal(env.BUCKET.objects.size,0);
});
test('publication activates only a complete bank and serves the original bytes with correct headers',async()=>{
 const f=fixture(),worker=createAssetWorker(f.manifest),env={BUCKET:bucket(),VISU_MEDIA_PUBLIC_KEY:publicKey};
 assert.equal((await worker.fetch(request('/api/media/activate',{method:'POST'}),env)).status,409);
 await upload(worker,env,f);assert.equal((await worker.fetch(request('/api/media/activate',{method:'POST'}),env)).status,200);
 assert.equal(await (await worker.fetch(request('/'),env)).text(),'APP');
 const photo=await worker.fetch(request('/assets/reviewed/test.jpg'),env);assert.equal(photo.headers.get('content-type'),'image/jpeg');assert.equal(await photo.text(),'PHOTO');
 assert.equal((await worker.fetch(request('/supabase/schema.sql'),env)).status,404);
 assert.equal((await worker.fetch(request('/assets/reviewed/test.jpg',{headers:{'if-none-match':'"'+hash('PHOTO')+'"'}}),env)).status,304);
});
test('a newer publication keeps the previous app available until its new resources are uploaded',async()=>{
 const old=fixture('OLD'),next=fixture('NEW'),env={BUCKET:bucket(),VISU_MEDIA_PUBLIC_KEY:publicKey},first=createAssetWorker(old.manifest),second=createAssetWorker(next.manifest);
 await upload(first,env,old);await first.fetch(request('/api/media/activate',{method:'POST'},old.manifest),env);
 assert.equal(await (await second.fetch(request('/'),env)).text(),'OLD');
 const missing=await (await second.fetch(request('/api/media/missing'),env)).json();assert.deepEqual(missing.missing,[hash('NEW')]);
 await upload(second,env,next);await second.fetch(request('/api/media/activate',{method:'POST'}),env);
 assert.equal(await (await second.fetch(request('/'),env)).text(),'NEW');
});

test('a public audience cannot update media with a forged, expired or cross-version signature',async()=>{
 const f=fixture(),env={BUCKET:bucket(),VISU_MEDIA_PUBLIC_KEY:publicKey},worker=createAssetWorker(f.manifest);
 assert.equal((await worker.fetch(new Request('https://visu.test/api/media/activate',{method:'POST',headers:{'x-visu-media':'1'}}),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/missing',{headers:{'x-visu-upload-signature':'AA=='}}),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/missing',{headers:{'x-visu-upload-time':'1000000000000'}}),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/missing',{}, {digest:'another-version'}),env)).status,403);
 assert.equal((await worker.fetch(request('/api/media/missing'),{BUCKET:bucket()})).status,403);
});
