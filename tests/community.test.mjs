import test from 'node:test';
import assert from 'node:assert/strict';
import {memberPermissions,fetchCommunity,Community} from '../community.mjs';
import {examMatches,examYears,studyLists} from '../catalogue.mjs';
import {studyNoteHTML} from '../notes.mjs';

test('disabled, absent and partial memberships fail closed; capabilities stay independent',()=>{
 for(const member of [null,{}, {enabled:false,is_admin:true,can_add_images:true}])assert.deepEqual(memberPermissions(member),{member:false,admin:false,add:false,edit:false,review:false,comment:false});
 const uploader=memberPermissions({enabled:true,can_add_images:true});assert.equal(uploader.add,true);assert.equal(uploader.review,false);assert.equal(uploader.edit,false);
 assert.equal(memberPermissions({enabled:true,can_edit_images:true}).review,false);
 assert.equal(memberPermissions({enabled:true,is_admin:true}).review,true);
});
test('revocation clears a cached shared bank before reading any shared table',async()=>{
 const calls=[];const client={from(table){calls.push(table);return {select(){return this;},eq(){return this;},async maybeSingle(){return {data:{enabled:false,is_admin:true},error:null};}};}};
 const result=await fetchCommunity(client,{userId:'a',isCurrent:()=>true,previous:{images:[{id:'private'}]}});
 assert.deepEqual(result,{member:null,images:[],edits:[]});assert.deepEqual(calls,['visu_members']);
});
test('a delayed membership response cannot attach another account’s shared data',async()=>{
 let resolve;let current=true;const pending=new Promise(r=>resolve=r);const client={from(){return {select(){return this;},eq(){return this;},maybeSingle(){return pending;}};}};
 const task=fetchCommunity(client,{userId:'a',isCurrent:()=>current});current=false;resolve({data:{enabled:true}});assert.equal(await task,null);
});
test('shared mutations bind the expected actor and use the guarded dispatcher',async()=>{
 const descriptor=Object.getOwnPropertyDescriptor(navigator,'onLine');Object.defineProperty(navigator,'onLine',{value:true,configurable:true});
 try{let sent;const community=new Community({getIdentity:()=>({account:'a',revision:1}),getClient:()=>({rpc:async(name,args)=>{sent={name,args};return {data:null};}})});community.state.member={enabled:true,can_review_images:true};
  await community.rpc('visu_set_image_status',{p_item:'x',p_key:'k',p_status:'approved'},'review');assert.deepEqual(sent,{name:'visu_dispatch',args:{p_actor:'a',p_action:'visu_set_image_status',p_payload:{p_item:'x',p_key:'k',p_status:'approved'}}});
 }finally{if(descriptor)Object.defineProperty(navigator,'onLine',descriptor);else delete navigator.onLine;}
});
test('exam region, year and evidence must match the same occurrence',()=>{
 const item={sources:['Listado visu de rocas.pdf'],examEvents:[{region:'Andalucía',year:2023,evidenceType:'recognition'},{region:'Madrid',year:2025,evidenceType:'context'}]};
 assert.ok(studyLists(item).includes('Exámenes anteriores'));assert.equal(examMatches(item,{region:'Madrid',year:'2023'}),false);assert.equal(examMatches(item,{region:'Madrid',year:'2025',evidenceType:'recognition'}),false);assert.equal(examMatches(item,{region:'Madrid',year:'2025',evidenceType:'context'}),true);
 assert.deepEqual(examYears([{region:'Madrid',year:2025},{region:'Madrid',year:2025},{region:'Andalucía',year:2023}],'Madrid'),[2025]);
});
test('resolved notes show etymology and missing family explicitly without mnemonics',()=>{
 const helpers={esc:s=>String(s),link:(url,title)=>title};const html=studyNoteHTML({scientificName:'Example',kind:'organismo'},{etymology:'Documented root',mnemonic:'Do not show this'},{},helpers);
 assert.ok(html.includes('Documented root'));assert.ok(html.includes('Familia y etimología pendientes'));assert.ok(!html.includes('<details'));assert.ok(!html.includes('Do not show this'));
});
