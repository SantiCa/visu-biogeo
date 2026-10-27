import test from 'node:test';import assert from 'node:assert/strict';
import {quizFields,evaluateIdentification} from '../classification-learning.mjs';
import {selectExamPhotos,eligibleExamPhotos} from '../exam-photos.mjs';
import {taxonReference,RANK_ETYMOLOGIES} from '../taxon-reference.mjs';
test('common name is graded independently without disclosing it in the name field, and missing names never penalize',()=>{
 const item={scientificName:'Quercus ilex',kind:'organismo'},tax={rank:'species',commonNames:['Encina','Carrasca'],ranks:{genus:'Quercus'}};
 assert(quizFields(item,tax,{},false).some(f=>f.key==='common'&&f.required));
 assert.equal(evaluateIdentification(item,tax,{}, {name:'Quercus ilex',common:'la encina'},false).results.common,true);
 const wrong=evaluateIdentification(item,tax,{}, {name:'Quercus ilex',common:'alcornoque'},false);assert.equal(wrong.results.name,true);assert.equal(wrong.results.common,false);assert(wrong.repeat);
 assert.equal(evaluateIdentification(item,{}, {},{name:'Quercus ilex'},false).results.common,null);
 assert.equal(evaluateIdentification(item,{}, {},{name:'Quercus ilex',common:'carrasca'},false,{profile:{commonName:'Encina, carrasca'}}).results.common,true);
});
test('Andalusia never silently falls back to details, context or unevaluated views',()=>{
 const diag={key:'d1',url:'a',examUse:'diagnostic'},detail={key:'p',url:'b',examUse:'detail'},unknown={key:'u',url:'c'};
 assert.deepEqual(selectExamPhotos([diag,detail,unknown],{mode:'andalucia'}),[]);
 const second={...diag,key:'d2',url:'d'};assert.deepEqual(new Set(selectExamPhotos([diag,detail,unknown,second],{mode:'andalucia'}).map(p=>p.key)),new Set(['d1','d2']));
});
test('Madrid detail questions never contain a complete image as an answer hint; personal assessments do not mutate shared media',()=>{
 const images=[{key:'whole',url:'a',examUse:'diagnostic'},{key:'detail',url:'b',examUse:'detail'},{key:'unknown',url:'c',reviewKey:'id'}],copy=structuredClone(images);
 assert.deepEqual(selectExamPhotos(images,{mode:'madrid',detailsOnly:true}).map(p=>p.key),['detail']);
 assert(selectExamPhotos(images,{mode:'madrid',rng:()=>0}).every(p=>p.examUse==='detail'));
 assert.equal(eligibleExamPhotos(images,'andalucia',{id:{value:{use:'diagnostic'}}}).length,2);assert.deepEqual(images,copy);
});
test('taxon references distinguish the etymology of a rank from the name and keep unknown roots explicit',()=>{
 for(const rank of Object.keys(RANK_ETYMOLOGIES)){const r=taxonReference(rank,'Unknown');assert(r.rankSource.startsWith('https://dle.rae.es/'));assert(r.taxonEtymology.includes('pendiente'));}
 assert(taxonReference('phylum','Arthropoda').taxonSource.includes('openstax'));
 assert.equal(taxonReference('family','Testidae',{familyNotes:{Testidae:{etymology:'Documented construction'}}}).taxonEtymology,'Documented construction');
});
