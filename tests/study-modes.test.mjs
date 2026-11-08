import test from 'node:test';import assert from 'node:assert/strict';
import {quizFields,evaluateIdentification} from '../classification-learning.mjs';
import {selectExamPhotos,eligibleExamPhotos} from '../exam-photos.mjs';
import {taxonReference,RANK_ETYMOLOGIES} from '../taxon-reference.mjs';
test('common name is graded independently without disclosing it in the name field, and missing names never penalize',()=>{
 const item={scientificName:'Quercus ilex',kind:'organismo'},tax={rank:'species',commonNames:['Encina','Carrasca'],ranks:{genus:'Quercus'}};
 assert(quizFields(item,tax,{},false).some(f=>f.key==='common'&&f.expected==='Encina'));
 assert.equal(evaluateIdentification(item,tax,{}, {name:'Quercus ilex',common:'la encina'},false).results.common,true);
 const wrong=evaluateIdentification(item,tax,{}, {name:'Quercus ilex',common:'alcornoque'},false);assert.equal(wrong.results.name,true);assert.equal(wrong.results.common,false);assert(wrong.repeat);
 assert.equal(evaluateIdentification(item,{}, {},{name:'Quercus ilex'},false).results.common,null);
 assert.equal(evaluateIdentification(item,{}, {},{name:'Quercus ilex',common:'carrasca'},false,{profile:{commonName:'Encina, carrasca'}}).results.common,true);
});
test('regional forms follow the documented identification tasks and preserve general practice',()=>{
 const item={scientificName:'Quercus ilex',kind:'organismo',aliases:['Quercus smilax']};
 const tax={commonName:'Encina',ranks:{kingdom:'Plantae',phylum:'Tracheophyta',class:'Magnoliopsida',family:'Fagaceae',genus:'Quercus'}};
 const fields=region=>quizFields(item,tax,{},true,{},region);
 assert.deepEqual(fields('andalucia').map(f=>f.key),['name','phylum']);
 assert.equal(fields('andalucia')[1].label,'División');
 assert.equal(quizFields({...item,scientificName:'Apis mellifera'},{ranks:{kingdom:'Animalia',phylum:'Arthropoda'}},{},true,{},'andalucia')[1].label,'Filo');
 for(const region of ['madrid','castilla-la-mancha']){
  assert.deepEqual(fields(region).map(f=>f.key),['name']);
  const check=name=>evaluateIdentification(item,tax,{}, {name,genus:'Quercus'},true,{region});
  assert.equal(check('ilex').correct,false);
  assert.equal(check('Quercus smilax').correct,true);
 }
 assert.equal(evaluateIdentification(item,tax,{}, {name:'QUERCUS ILEX'},true,{region:'madrid'}).correct,false);
 assert.deepEqual(fields('ambas').map(f=>f.key),['name','common','phylum','family','genus']);
});
test('Andalusia includes documented geology fields without asking for the 2025 formula cue as an answer',()=>{
 const mineral={scientificName:'Olivino',kind:'mineral'};
 const geo={domain:'mineral',classification:'Silicatos',path:['Silicatos','Nesosilicatos'],formulaQuiz:true,formula:'(Mg,Fe)₂SiO₄'};
 const fields=region=>quizFields(mineral,{},geo,true,{},region).map(f=>f.key);
 assert.deepEqual(fields('andalucia'),['name','classification','silicateType']);
 assert.deepEqual(fields('ambas'),['name','classification','formula']);
 assert.deepEqual(fields('castilla-la-mancha'),['name']);
});
test('partial submissions score only attempted, documented fields and explicit reveal still schedules review',()=>{
 const item={scientificName:'Quercus ilex',kind:'organismo'};
 const tax={ranks:{kingdom:'Plantae',phylum:'Tracheophyta'}};
 const check=(values,options={})=>evaluateIdentification(item,tax,{},values,true,{region:'andalucia',...options});
 assert.deepEqual(check({name:'Quercus ilex',phylum:'  '}).results,{name:true,phylum:null});
 const partial=check({phylum:'Tracheophyta'});
 assert.deepEqual(partial.results,{name:null,phylum:true});
 assert.equal(partial.correct,null);
 assert.equal(partial.repeat,false);
 assert.equal(check({phylum:'Bryophyta'}).repeat,true);
 assert.equal(check({}, {reveal:true}).repeat,true);
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
