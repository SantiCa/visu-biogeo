import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {answerMatches,priorityInfo} from '../engine.mjs';
import {studyLists} from '../catalogue.mjs';
const load=name=>JSON.parse(readFileSync(new URL('../data/'+name,import.meta.url)));
const catalog=load('species.json'),history=load('andalucia-priority.json'),evidence=load('solved-exam-evidence.json');
const entry=id=>catalog.find(x=>x.id===id);

test('every imported answer retains a real key page and a numbered question',()=>{
 const docs=new Map(evidence.documents.map(d=>[d.filename,d]));
 assert.equal(new Set(evidence.occurrences.map(r=>r.id)).size,evidence.occurrences.length);
 for(const row of evidence.occurrences){
  const doc=docs.get(row.sourceFile);assert.ok(doc,row.id);
  assert.ok(row.solutionPage>=1&&row.solutionPage<=doc.pages,row.id);
  assert.ok(row.sourceName&&row.question&&row.option,row.id);
  const events=history.events.filter(e=>e.evidenceId===row.id);assert.equal(events.length,1,row.id);
  assert.equal(events[0].sourceType,'solucionario-academia-aportado');
 }
});

test('all twenty 2023 photo answers include the two photos on the last relevant page',()=>{
 const photos=history.events.filter(e=>e.year===2023&&e.context==='fotografia-con-clave-academica');
 assert.equal(photos.length,20);
 for(const id of ['ixodes-ricinus','bolinus-brandaris']){
  const row=photos.find(e=>e.itemId===id);assert.ok(row,id);assert.equal(row.page,10);
 }
});

test('question marks and incompatible alternatives never become automatic occurrences',()=>{
 assert.equal(evidence.unresolved.length,8);
 for(const row of evidence.unresolved){
  assert.ok(!history.events.some(e=>e.evidenceId&&e.year===row.year&&e.option===row.option&&e.question===row.question));
 }
 assert.equal(priorityInfo(entry('antracita'),history.events).count,1);
 assert.equal(history.events.filter(e=>e.itemId==='antracita'&&e.year===2018).length,2);
 assert.equal(priorityInfo(entry('cuarzo'),history.events).count,3);
 assert.equal(priorityInfo(entry('sienita'),history.events).count,2);
});

test('an independently corroborated photo retains the doubtful key and the existing mineral ID',()=>{
 const row=evidence.occurrences.find(r=>r.id==='provided-2021-B-5');
 assert.equal(row.name,'Calcopirita');assert.equal(row.page,9);assert.equal(row.solutionPage,17);
 assert.equal(row.sourceType,'solucionario-academia-aportado');
 assert.deepEqual(row.photoReview.originalUncertainty.proposedNames,['Calcopirita']);
 assert.equal(row.photoReview.originalUncertainty.priorityEligible,false);
 assert.equal(row.photoReview.originalUncertainty.sourceFile,row.sourceFile);
 assert.equal(row.photoReview.originalUncertainty.solutionPage,row.solutionPage);
 assert.ok(row.photoReview.originalUncertainty.reason.includes('interrogación'));
 assert.equal(row.photoReview.reference.label,'Calcopirita');
 assert.equal(new URL(row.photoReview.reference.url).hostname,'recursos.edu.xunta.gal');
 const event=history.events.find(e=>e.evidenceId===row.id);
 assert.equal(event.itemId,'calcopirita');assert.deepEqual(event.photoReview,row.photoReview);
 assert.equal(priorityInfo(entry('calcopirita'),history.events).count,1);
 const exams=load('exams.json'),doc=exams.documents.find(d=>d.id==='andalucia-2021');
 assert.equal(doc.official,false);assert.equal(doc.uncertainAnswers.length,3);
 assert.deepEqual(exams.events.find(e=>e.evidenceId===row.id).photoReview,row.photoReview);
 assert.deepEqual(evidence.unresolved.filter(r=>r.year===2021).map(r=>[r.option,r.question]),[['A','9'],['A','10'],['A','15']]);
});

test('documented synonyms work while printed misspellings remain provenance only',()=>{
 assert.ok(answerMatches('Jacaranda ovalifolia',entry('jacaranda-mimosifolia')));
 assert.ok(answerMatches('Noctiluca miliaris',entry('noctiluca-scintillans')));
 assert.ok(!answerMatches('Sphagnum subtinens',entry('sphagnum-subnitens')));
 assert.ok(answerMatches('Sphagnum subnitens',entry('sphagnum-subnitens')));
 for(const [id,typo] of [['chalcides-striatus','Chalcides estriatus'],['eliomys-quercinus','Elyomis quercinus'],['latrodectus-tredecimguttatus','Laetrodectus tredecimguttatus']])assert.ok(!answerMatches(typo,entry(id)),id);
 assert.ok(answerMatches('Stentor',entry('stentor-sp')));
 assert.ok(!answerMatches('Stentor coeruleus',entry('stentor-sp')));
});

test('exam additions have logical study lists without fabricated original-PDF membership',()=>{
 for(const id of ['acanthus-mollis','sphagnum-subnitens','gneis-glandular']){
  const item=entry(id);assert.ok(studyLists(item).length>=2,id);
  const documents=[...evidence.documents,...load('exams.json').documents.map(d=>d.sourceMetadata).filter(Boolean)];
  assert.ok(item.sourcePages.every(p=>documents.some(d=>d.filename===p.file)),id);
 }
});

test('all documented priorities have two distinct locally stored approved image references',()=>{
 const curated=load('curated-images.json');
 for(const id of new Set(history.events.map(e=>e.itemId))){
  const images=curated[id].images.filter(im=>im.status==='approved');
  assert.ok(new Set(images.map(im=>im.key||im.page||im.originalUrl)).size>=2,id);
  assert.ok(images.every(im=>im.url.startsWith('./assets/reviewed/')),id);
 }
});
