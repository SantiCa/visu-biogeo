const CACHE='visu-biogeo-v8.13',PHOTOS='visu-photo-library-v1';
const CORE=['./','./index.html','./styles.css','./theme.js','./app.js','./engine.mjs','./offline.mjs','./storage.mjs','./config.js','./manifest.webmanifest','./icons/icon.svg','./data/species.json','./data/images.json','./data/curated-images.json','./data/andalucia-priority.json','./data/inaturalist-images.json','./data/geological-images.json','./data/geodil-images.json','./data/commons-extra-images.json','./data/priority-additions.json','./data/cloud-images.json','./data/asturnatura-images.json','./data/taxonomy.json','./data/teaching-images.json','./data/petrography-images.json','./data/study-notes.json','./data/family-notes.json'];
CORE.push('./catalogue.mjs','./data/classification.json');
CORE.push('./notes.mjs','./tooltips.mjs','./community.mjs','./data/exams.json');
CORE.push('./cloud.mjs','./install.mjs','./icons/icon-180.png','./icons/icon-192.png','./icons/icon-512.png','./vendor/16296a5ca2509267.mjs','./vendor/8286d33a1ce5055b.mjs','./vendor/a20988a4e1db6b4f.mjs','./vendor/b9737199fdd59f88.mjs','./vendor/c253187f3a945751.mjs','./vendor/f504778958a3bac0.mjs','./vendor/supabase.mjs');
CORE.push('./classification-learning.mjs','./data/learning-taxonomy.json','./data/learning-geology.json');
CORE.push('./taxonomy-guide.mjs');
CORE.push('./taxon-reference.mjs','./exam-photos.mjs');
const BASE=self.location.href||self.location.origin+'/',CORE_PATHS=new Set(CORE.map(path=>new URL(path,BASE).pathname));
function usable(req,response){const path=new URL(req.url,BASE).pathname,type=response.headers.get('content-type')||'';return response.ok&&!response.redirected&&(!/text\/html/i.test(type)||path.endsWith('/')||path.endsWith('/index.html'));}
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>Promise.all(CORE.map(async path=>{const req=new Request(path,{cache:'reload'}),response=await fetch(req);if(!usable(req,response))throw Error('App resources require a valid signed-in response');await cache.put(req,response);}))).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>/^visu-biogeo-|^visu-bio-geo-/.test(k)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 const req=event.request,url=new URL(req.url);if(req.method!=='GET'||(url.origin!==self.location.origin&&req.destination!=='image'))return;
 if(req.destination==='image'){
  event.respondWith((async()=>{const library=await caches.open(PHOTOS);const saved=await library.match(req);if(saved)return saved;try{const response=await fetch(req);if(response.type!=='opaque'&&!usable(req,response))return await caches.match(req)||Response.error();if(response.ok&&url.origin===self.location.origin){const clone=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(req,clone)));}return response;}catch{return await caches.match(req)||Response.error();}})());return;
 }
 if(!CORE_PATHS.has(url.pathname))return;
 // Network first: never leave corrected catalog/image manifests trapped in an old cache.
 const cacheKey=url.origin+url.pathname;
 event.respondWith(fetch(req,{cache:'no-store'}).then(async response=>{if(!usable(req,response))return await caches.match(cacheKey)||Response.error();const clone=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(cacheKey,clone)));return response;}).catch(async()=>{const cache=await caches.open(CACHE);return await cache.match(cacheKey)||(req.mode==='navigate'?await cache.match('./index.html'):null)||Response.error();}));
});

