import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

test('a catalogue update bypasses stale HTTP responses, remains available offline and preserves saved photos',async()=>{
 const origin='https://visu.test/',handlers={},stores=new Map();let online=true,loginRedirect=false;
 const key=input=>new URL(typeof input==='string'?input:input.url,origin).href;
 const fetcher=async(input,options={})=>{
  if(!online)throw Error('offline');
  if(loginRedirect){const response=new Response('<html>Sign in</html>',{headers:{'content-type':'text/html'}});Object.defineProperty(response,'redirected',{value:true});return response;}
  const bypass=['reload','no-store'].includes(options.cache||input.cache);
  return new Response(bypass?'updated catalogue':'stale HTTP catalogue');
 };
 const caches={
  async open(name){if(!stores.has(name))stores.set(name,new Map());const values=stores.get(name);return {
   async addAll(requests){for(const req of requests)values.set(key(req),(await fetcher(req)).clone());},
   async put(req,response){values.set(key(req),response.clone());},
   async match(req){return values.get(key(req))?.clone();}
  };},
  async keys(){return [...stores.keys()];},async delete(name){return stores.delete(name);},
  async match(req){for(const values of stores.values())if(values.has(key(req)))return values.get(key(req)).clone();}
 };
 const photos=await caches.open('visu-photo-library-v1');await photos.put('./sample.jpg',new Response('saved photo'));
 await caches.open('visu-biogeo-old');
 class WorkerRequest extends Request{constructor(input,options){super(key(input),options);}}
 const self={location:{origin:new URL(origin).origin},clients:{claim:async()=>{}},skipWaiting:async()=>{},addEventListener:(type,handler)=>{handlers[type]=handler;}};
 vm.runInNewContext(readFileSync(new URL('../sw.js',import.meta.url),'utf8'),{self,caches,fetch:fetcher,Request:WorkerRequest,Response,URL});
 async function lifecycle(type){let work;handlers[type]({waitUntil:p=>{work=p;}});await work;}
 await lifecycle('install');await lifecycle('activate');
 assert.ok(!stores.has('visu-biogeo-old'));assert.equal(await (await photos.match('./sample.jpg')).text(),'saved photo');
 const current=await caches.open([...stores.keys()].find(name=>name.startsWith('visu-biogeo-')));
 assert.equal(await (await current.match('./data/species.json')).text(),'updated catalogue');
 async function catalogue(){let response;const tasks=[];handlers.fetch({request:{method:'GET',url:origin+'data/species.json',destination:'',mode:'cors'},respondWith:p=>{response=p;},waitUntil:p=>tasks.push(p)});const result=await response;await Promise.all(tasks);return result.text();}
 assert.equal(await catalogue(),'updated catalogue');
 loginRedirect=true;assert.equal(await catalogue(),'updated catalogue','login page must not replace the cached catalogue');
 let authIntercepted=false;handlers.fetch({request:{method:'GET',url:origin+'signin-with-chatgpt?state=private',destination:'',mode:'navigate'},respondWith:()=>{authIntercepted=true;}});
 assert.equal(authIntercepted,false,'authentication routes must not be cached');
 online=false;assert.equal(await catalogue(),'updated catalogue');
});
