export const PHOTO_CACHE='visu-photo-library-v1';
export function imageAvailable(image,{online,savedOnly,savedUrls,bundledDesktop=false,base}) {
  if(image.url.startsWith('data:'))return true;
  try{const url=new URL(image.url,base),origin=new URL(base).origin,localFolder=new URL('./assets/reviewed/',base).pathname;
    const bundled=bundledDesktop&&url.origin===origin&&url.pathname.startsWith(localFolder);
    return savedUrls.has(url.href)||(!savedOnly&&(online||bundled));
  }catch{return false;}
}
export function photoUrls(items,imagesFor,limit=0,base=globalThis.location?.href) {
  return [...new Set(items.flatMap(item=>{
    const images=imagesFor(item);return (limit?images.slice(0,limit):images).map(im=>im.url);
  }).filter(url=>!url.startsWith('data:')).map(url=>new URL(url,base).href))];
}
export async function savedPhotoUrls(cacheStorage=globalThis.caches) {
  if(!cacheStorage)return new Set();const result=new Set();
  for(const name of await cacheStorage.keys()){
    if(name!==PHOTO_CACHE && !/^visu-biogeo-|^visu-bio-geo-/.test(name))continue;
    const cache=await cacheStorage.open(name);for(const req of await cache.keys())result.add(req.url);
  }
  return result;
}
export async function downloadPhotos(urls,{cacheStorage=globalThis.caches,fetcher=globalThis.fetch,onProgress=()=>{},shouldStop=()=>false}={}) {
  if(!cacheStorage)throw Error('Este navegador necesita HTTPS o localhost para guardar el modo sin conexión.');
  const cache=await cacheStorage.open(PHOTO_CACHE);const progress={total:urls.length,completed:0,downloaded:0,alreadyCached:0,failed:0,cancelled:false};
  for(const url of urls){
    if(shouldStop()){progress.cancelled=true;break;}
    try{
      if(await cache.match(url)){progress.alreadyCached++;}
      else{
        const existing=await cacheStorage.match(url);
        const response=existing||await fetcher(url,{mode:new URL(url).origin===globalThis.location?.origin?'same-origin':'no-cors'});
        if(!response.ok && response.type!=='opaque')throw Error('HTTP '+response.status);
        if(response.redirected||/text\/html/i.test(response.headers?.get('content-type')||''))throw Error('La fuente requiere acceder de nuevo antes de guardar la foto.');
        await cache.put(url,response.clone());progress.downloaded++;
      }
    }catch(error){progress.failed++;if(error.name==='QuotaExceededError'){progress.error='No queda espacio disponible. Se conservan las fotos ya guardadas.';break;}}
    progress.completed++;onProgress({...progress});
  }
  onProgress({...progress});return progress;
}
