import {mergeRecords} from './engine.mjs';

export function publicCloudConfig(config={}) {
 const key=String(config.publishableKey||config.anonKey||'').trim(),url=String(config.url||'').replace(/\/$/,'');
 if(!url&&!key)return null;
 if(!/^https:\/\/[^/?#]+$/.test(url))throw Error('La dirección de sincronización debe ser HTTPS.');
 if(key.startsWith('sb_secret_'))throw Error('La app solo admite la clave pública del proyecto.');
 if(!key.startsWith('sb_publishable_')){
  try{const role=JSON.parse(atob(key.split('.')[1].replace(/-/g,'+').replace(/_/g,'/'))).role;if(role!=='anon')throw Error();}
  catch{throw Error('Introduce una clave publishable o anon, nunca una clave secreta.');}
 }
 return {url,key};
}

export function mergeTimed(local={},remote={}) {
 const result={...local};
 for(const [id,value] of Object.entries(remote||{}))if(!result[id]||(value.updatedAt||0)>(result[id].updatedAt||0))result[id]=value;
 return result;
}

// A captured state and generation check keep an old request out of a new account.
// RLS and the database membership check remain authoritative, even with modified clients.
export async function synchronizeAccount(client,{userId,state,isCurrent,persist}) {
 const cancelled=()=>!isCurrent();
 if(cancelled())return {cancelled:true};
 const membership=await client.from('visu_members').select('user_id').eq('user_id',userId).eq('enabled',true).maybeSingle();
 if(cancelled())return {cancelled:true};
 if(membership.error)throw membership.error;
 if(!membership.data)throw Error('Esta cuenta no está autorizada para sincronizar con este proyecto.');
 const rows=[];
 for(let from=0;;from+=500){
  const {data:batch,error}=await client.from('study_states').select('item_id,state').eq('user_id',userId).order('item_id').range(from,from+499);
  if(cancelled())return {cancelled:true};
  if(error)throw error;
  rows.push(...batch);if(batch.length<500)break;
 }
 const remote={};
 for(const row of rows){
  if(row.item_id==='__preferences_v3'){
   state.overrides=mergeTimed(state.overrides,row.state.overrides);
   state.decisions=mergeTimed(state.decisions,row.state.decisions);
   state.preferences=mergeTimed(state.preferences,row.state.preferences);
  }else remote[row.item_id]=row.state;
 }
 state.records=mergeRecords(state.records,remote);
 await persist(state);
 if(cancelled())return {cancelled:true};
 const upload=Object.entries(state.records).map(([item_id,itemState])=>({user_id:userId,item_id,state:itemState}));
 upload.push({user_id:userId,item_id:'__preferences_v3',state:{overrides:state.overrides,decisions:state.decisions,preferences:state.preferences}});
 for(let i=0;i<upload.length;i+=100){
  if(cancelled())return {cancelled:true};
  const {error}=await client.rpc('merge_study_states',{incoming:upload.slice(i,i+100)});
  if(cancelled())return {cancelled:true};
  if(error)throw error;
 }
 return {cancelled:false,uploaded:upload.length};
}
