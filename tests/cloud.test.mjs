import test from 'node:test';
import assert from 'node:assert/strict';
import {publicCloudConfig,synchronizeAccount} from '../cloud.mjs';

const initial=()=>({records:{local:{total:2,correct:1,lastReviewed:10}},overrides:{},decisions:{},preferences:{},media:{local:[{url:'data:image/jpeg;base64,private'}]}});
function fakeClient({member=true,rows=[],afterRead=()=>{},afterMember=()=>{}}={}){
 const uploads=[];
 return {uploads,from(table){return {select(){return this;},eq(){return this;},order(){return this;},async maybeSingle(){afterMember();return {data:member?{user_id:'A'}:null,error:null};},async range(from,to){afterRead();return {data:rows.slice(from,to+1),error:null};}};},async rpc(name,args){assert.equal(name,'merge_study_states');uploads.push(...args.incoming);return {error:null};}};
}

test('only public project keys can be shipped in the client',()=>{
 assert.equal(publicCloudConfig({}),null);
 assert.deepEqual(publicCloudConfig({url:'https://demo.supabase.co/',publishableKey:'sb_publishable_example'}),{url:'https://demo.supabase.co',key:'sb_publishable_example'});
 const jwt=role=>'eyJ.'+btoa(JSON.stringify({role}))+'.example';
 assert.equal(publicCloudConfig({url:'https://demo.supabase.co',anonKey:jwt('anon')}).key,jwt('anon'));
 assert.throws(()=>publicCloudConfig({url:'https://demo.supabase.co',publishableKey:'sb_secret_example'}));
 assert.throws(()=>publicCloudConfig({url:'https://demo.supabase.co',anonKey:jwt('service_role')}));
 assert.throws(()=>publicCloudConfig({url:'http://demo.supabase.co',publishableKey:'sb_publishable_example'}));
});

test('a signed-in account without membership cannot synchronize',async()=>{
 const client=fakeClient({member:false});let saved=false;
 await assert.rejects(synchronizeAccount(client,{userId:'A',state:initial(),isCurrent:()=>true,persist:async()=>{saved=true;}}),/no está autorizada/);
 assert.equal(saved,false);assert.equal(client.uploads.length,0);
});

test('switching accounts while downloading cancels without mixing or uploading state',async()=>{
 let current=true;const state=initial(),original=structuredClone(state);
 const client=fakeClient({rows:[{item_id:'remote',state:{total:8,lastReviewed:20}}],afterRead:()=>{current=false;}});let saved=false;
 assert.deepEqual(await synchronizeAccount(client,{userId:'A',state,isCurrent:()=>current,persist:async()=>{saved=true;}}),{cancelled:true});
 assert.deepEqual(state,original);assert.equal(saved,false);assert.equal(client.uploads.length,0);
});

test('switching after local persistence never uploads the previous account as the new account',async()=>{
 let current=true;const client=fakeClient();
 assert.deepEqual(await synchronizeAccount(client,{userId:'A',state:initial(),isCurrent:()=>current,persist:async()=>{current=false;}}),{cancelled:true});
 assert.equal(client.uploads.length,0);
});

test('two devices merge progress and preferences but never upload local photo data',async()=>{
 const client=fakeClient({rows:[{item_id:'local',state:{total:4,correct:3,lastReviewed:20}},{item_id:'__preferences_v3',state:{preferences:{practiceFamily:{value:true,updatedAt:100}},overrides:{local:{count:2,updatedAt:100}}}}]});
 const state=initial();let saved;
 const result=await synchronizeAccount(client,{userId:'A',state,isCurrent:()=>true,persist:async value=>{saved=structuredClone(value);}});
 assert.equal(result.cancelled,false);assert.equal(saved.records.local.total,4);assert.equal(saved.preferences.practiceFamily.value,true);
 assert.ok(client.uploads.every(row=>row.user_id==='A'));
 assert.ok(!JSON.stringify(client.uploads).includes('data:image'));
 assert.equal(client.uploads.find(x=>x.item_id==='__preferences_v3').state.overrides.local.count,2);
});

test('more than one page is read and writes respect the database batch limit',async()=>{
 const rows=Array.from({length:703},(_,i)=>({item_id:'item-'+i,state:{total:1,lastReviewed:1}}));
 const client=fakeClient({rows}),sizes=[];const rpc=client.rpc;client.rpc=async(name,args)=>{sizes.push(args.incoming.length);return rpc(name,args);};
 const state=initial();await synchronizeAccount(client,{userId:'A',state,isCurrent:()=>true,persist:async()=>{}});
 assert.equal(Object.keys(state.records).length,704);assert.ok(sizes.every(x=>x<=100));assert.equal(client.uploads.length,705);
});
