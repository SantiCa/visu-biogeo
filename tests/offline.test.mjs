import test from 'node:test';
import assert from 'node:assert/strict';
import {PHOTO_CACHE,photoUrls,downloadPhotos,imageAvailable} from '../offline.mjs';
function storage(){const values=new Map();const cache={match:async u=>values.get(u),put:async(u,r)=>values.set(u,r),keys:async()=>[...values.keys()].map(url=>({url}))};return {values,cache,open:async name=>{assert.equal(name,PHOTO_CACHE);return cache;},match:async()=>null};}

test('bundled desktop photos work without Internet and still respect the saved-only filter',()=>{
 const options={online:false,savedOnly:false,savedUrls:new Set(),base:'http://127.0.0.1:8081/'};
 const photo={url:'./assets/reviewed/specimen.jpg'};
 assert.equal(imageAvailable(photo,options),false);
 assert.equal(imageAvailable(photo,{...options,bundledDesktop:true}),true);
 assert.equal(imageAvailable(photo,{...options,bundledDesktop:true,savedOnly:true}),false);
 assert.equal(imageAvailable({url:'https://other.test/specimen.jpg'},{...options,bundledDesktop:true}),false);
 assert.equal(imageAvailable({url:'data:image/jpeg;base64,photo'},options),true);
});

test('an authentication page is never counted as a downloaded photo',async()=>{
 const cacheStorage=storage();
 const result=await downloadPhotos(['https://example.test/photo.jpg'],{cacheStorage,fetcher:async()=>new Response('<html>Sign in</html>',{headers:{'content-type':'text/html'}})});
 assert.equal(result.failed,1);assert.equal(result.downloaded,0);assert.equal(cacheStorage.values.size,0);
});
test('offline selection applies the per-entry limit and excludes private data URLs',()=>{const items=[{id:'a'},{id:'b'}],images={a:[{url:'./a.jpg'},{url:'./b.jpg'},{url:'./c.jpg'}],b:[{url:'./a.jpg'},{url:'data:image/jpeg;base64,x'}]};assert.deepEqual(photoUrls(items,i=>images[i.id],2,'https://example.test/'),['https://example.test/a.jpg','https://example.test/b.jpg']);});
test('download resumes without fetching existing files and preserves successes on a failure',async()=>{const cacheStorage=storage();const urls=['https://example.test/a','https://example.test/b'];let fetched=0;const fetcher=async u=>{fetched++;return new Response('photo',{status:u.endsWith('b')?404:200});};const r=await downloadPhotos(urls,{cacheStorage,fetcher});assert.equal(r.downloaded,1);assert.equal(r.failed,1);assert.equal(cacheStorage.values.size,1);const resumed=await downloadPhotos(urls,{cacheStorage,fetcher:async()=>new Response('photo')});assert.equal(resumed.alreadyCached,1);assert.equal(resumed.downloaded,1);assert.equal(cacheStorage.values.size,2);assert.equal(fetched,2);});
test('stopping a download preserves files already saved',async()=>{const cacheStorage=storage();let stop=false;const r=await downloadPhotos(['https://example.test/a','https://example.test/b'],{cacheStorage,fetcher:async()=>new Response('photo'),onProgress:()=>{stop=true;},shouldStop:()=>stop});assert.equal(r.downloaded,1);assert.equal(r.cancelled,true);assert.equal(cacheStorage.values.size,1);});

test('storage exhaustion stops downloads and retains previously saved photographs',async()=>{const cacheStorage=storage();const originalPut=cacheStorage.cache.put;cacheStorage.cache.put=async(u,r)=>{if(cacheStorage.values.size)throw new DOMException('Full','QuotaExceededError');await originalPut(u,r);};let fetched=0;const r=await downloadPhotos(['https://example.test/a','https://example.test/b','https://example.test/c'],{cacheStorage,fetcher:async()=>{fetched++;return new Response('photo');}});assert.equal(fetched,2);assert.equal(r.downloaded,1);assert.equal(r.failed,1);assert.match(r.error,/espacio/);assert.equal(cacheStorage.values.size,1);});
