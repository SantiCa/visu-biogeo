const dbPromise=new Promise((resolve,reject)=>{
  const req=indexedDB.open('visu-biogeo-v3',1);
  req.onupgradeneeded=()=>req.result.createObjectStore('kv');
  req.onsuccess=()=>resolve(req.result); req.onerror=()=>reject(req.error);
});
export async function read(key,fallback) {
  const db=await dbPromise;
  return new Promise((resolve,reject)=>{const r=db.transaction('kv').objectStore('kv').get(key);r.onsuccess=()=>resolve(r.result??fallback);r.onerror=()=>reject(r.error);});
}
export async function write(key,value) {
  const db=await dbPromise;
  return new Promise((resolve,reject)=>{const tx=db.transaction('kv','readwrite');tx.objectStore('kv').put(value,key);tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);});
}
