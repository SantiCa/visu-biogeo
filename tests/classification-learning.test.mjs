import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';
import {buildClassificationForest,quizFields,evaluateIdentification,formulaMatches,phylumLabel} from '../classification-learning.mjs';
import {review,DAY} from '../engine.mjs';
const item={id:'encina',kind:'organismo',scientificName:'Quercus ilex',family:'Fagaceae',aliases:[]};
const tax={rank:'species',ranks:{kingdom:'Plantae',phylum:'Tracheophyta',class:'Magnoliopsida',order:'Fagales',family:'Fagaceae',genus:'Quercus',species:'Quercus ilex'}};
test('ranked quiz accepts an epithet with its correct genus and keeps fields independent',()=>{
 const result=evaluateIdentification(item,tax,{}, {name:'ilex',genus:'Quercus',family:'fagaceae',phylum:'Tracheophyta'});assert.equal(result.repeat,false);assert.equal(phylumLabel(tax),'División');
 const wrong=evaluateIdentification(item,tax,{}, {name:'Quercus ilex',genus:'Pinus',family:'Fagaceae',phylum:'Tracheophyta'});assert.equal(wrong.correct,true);assert.equal(wrong.results.genus,false);assert.equal(wrong.repeat,true);
 assert.equal(evaluateIdentification(item,tax,{}, {name:'ilex',genus:'Pinus'}).correct,false);
});
test('genus-only fossils and unresolved ranks never invent a species or penalize unavailable taxonomy',()=>{
 const genus={...item,kind:'fosil',scientificName:'Conus sp.',aliases:[]};const fields=quizFields(genus,{rank:'genus',ranks:{genus:'Conus'}},{});assert(!fields.some(f=>f.key==='genus'));assert.equal(fields.find(f=>f.key==='phylum').expected,null);
 assert.equal(evaluateIdentification(genus,{rank:'genus',ranks:{genus:'Conus'}},{},{name:'Conus',family:'Fagaceae'}).results.phylum,null);
});
test('chemical grading respects elements, parentheses, hydration and documented variable formulas',()=>{
 const geo={formula:'CaSO4·2H2O',formulaQuiz:true};assert(formulaMatches('Ca S O₄ · 2H₂O',geo));assert(formulaMatches('CaH4SO6',geo));assert(!formulaMatches('CaSO4',geo));assert(!formulaMatches('CaSO4·3H2O',geo));
 assert(!formulaMatches('CO',{formula:'Co',formulaQuiz:true}));assert(formulaMatches('Ca2Al2Si3O10(OH)2',{formula:'Ca2Al(AlSi3O10)(OH)2',formulaQuiz:true}));assert(formulaMatches('(Fe,Mg)2SiO4',{formula:'(Mg,Fe)2SiO4',formulaQuiz:true}));
 assert(!formulaMatches('CaCO3',{formula:null,formulaQuiz:false}));
});
test('any classification error schedules ten minutes and persists separate counters without mutating previous records',()=>{
 const old={total:5,correct:4,fields:{genus:{total:2,correct:2}}},snapshot=structuredClone(old),r=review(old,{correct:true,fieldResults:{name:true,genus:false,phylum:null},difficulty:'easy',now:1000});
 assert.equal(r.correct,5);assert.equal(r.dueAt,1000+10/1440*DAY);assert.deepEqual(r.fields.genus,{total:3,correct:2});assert(!r.fields.phylum);assert.deepEqual(old,snapshot);
});
test('all catalogue entries appear once in the classification tree, and every mineral and rock has a documented path',async()=>{
 const load=async n=>JSON.parse(await readFile(new URL('../data/'+n,import.meta.url),'utf8'));const [catalog,t,g]=await Promise.all(['species.json','learning-taxonomy.json','learning-geology.json'].map(load));
 const tree=buildClassificationForest(catalog,t,g),leaves=[];function walk(n){if(n.itemId)leaves.push(n.itemId);n.children?.forEach(walk);}walk(tree);assert.equal(leaves.length,catalog.length);assert.equal(new Set(leaves).size,catalog.length);
 for(const item of catalog.filter(i=>['mineral','roca'].includes(i.kind))){assert(g[item.id]?.path.length>=2,item.id);assert(g[item.id].sources.length,item.id);if(item.kind==='roca'){assert.equal(g[item.id].formula,null);assert.equal(g[item.id].formulaQuiz,false);}}
});
