import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {examMatches,examYears,examYearLabel,studyLists,studyGroup} from '../catalogue.mjs';
import {priorityInfo} from '../engine.mjs';
const load=n=>JSON.parse(readFileSync(new URL('../data/'+n,import.meta.url)));
const catalog=load('species.json'),exams=load('exams.json'),history=load('andalucia-priority.json');
const rows=exams.events.filter(e=>e.documentId==='madrid-varios-sin-fecha');
test('Madrid selection includes the undated compilation without assigning it a year',()=>{const events=[...history.events,...exams.events.filter(e=>e.region==='Madrid')];const madrid=priorityInfo(entry('meles-meles'),events,{},'madrid');assert.equal(madrid.count,1);assert.deepEqual(madrid.years,[]);assert.equal(madrid.undated,true);assert.equal(priorityInfo(entry('meles-meles'),events,{},'andalucia').count,0);});
test('the 2002 participant list is attributed as nonofficial',()=>{const document=exams.documents.find(row=>row.id==='madrid-2002-recopilacion-foro');const events=exams.events.filter(row=>row.documentId===document.id);assert.equal(document.official,false);assert.equal(events.length,50);assert.ok(events.every(row=>row.year===2002&&row.sourceType==='recopilacion-opositor'&&row.note.includes('sin clave oficial')));assert.equal(entry('posidonia-sp').scientificName,'Posidonia sp.');assert.equal(entry('estructura-egagropila-de-rapaz-nocturna').kind,'estructura');assert(entry('peronaea-planata').aliases.includes('Tellina planata'));assert(entry('hemorrhois-hippocrepis').aliases.includes('Coluber hippocrepis'));});
const entry=id=>catalog.find(x=>x.id===id);

test('undated compilations have an explicit filter and never impersonate a dated exam',()=>{
 assert.ok(examYears(exams.documents,'Madrid').includes('undated'));
 assert.ok(!examYears(exams.documents,'Andalucía').includes('undated'));
 assert.equal(examYearLabel(null),'Varios años · sin fecha');
 const item={examEvents:[{region:'Madrid',year:null,evidenceType:'recognition'},{region:'Andalucía',year:2023,evidenceType:'recognition'}]};
 assert.ok(examMatches(item,{region:'Madrid',year:'undated'}));
 assert.ok(!examMatches(item,{region:'Madrid',year:'2023'}));
 assert.ok(!examMatches(item,{region:'Andalucía',year:'undated'}));
});

test('compilation provenance is local, undated, nonofficial, and excluded from Andalusian counts',()=>{
 assert.equal(rows.length,405);
 for(const e of rows){assert.equal(e.year,null);assert.equal(e.priorityEligible,false);assert.ok(e.page>=1&&e.page<=17);assert.ok(e.sourceName&&e.sourceFile);assert.ok(!e.source);}
 const doc=exams.documents.find(d=>d.id==='madrid-varios-sin-fecha');assert.equal(doc.official,false);assert.equal(doc.matchedEntries,396);assert.equal(doc.uncertainAnswers.length,3);
 assert.equal(priorityInfo(entry('meles-meles'),history.events).count,0);
 assert.equal(priorityInfo(entry('cuarzo'),history.events).count,3);
 assert.equal(new Set(history.events.map(e=>e.itemId)).size,163);
 assert.ok(history.events.every(e=>Number.isInteger(e.year)));
});

test('misplaced organisms are attached to their logical groups, and genera are not forced to species',()=>{
 for(const id of ['passer-domesticus','athene-noctua'])assert.ok(!entry(id).studyLists.includes('Poáceas (gramíneas)'));
 assert.ok(studyLists(entry('carex-sp')).includes('Flores'));
 assert.ok(!studyLists(entry('carex-sp')).includes('Poáceas (gramíneas)'));
 assert.ok(studyLists(entry('polytrichum-sp')).includes('Musgos y hepáticas'));
 assert.equal(entry('spirograptus').kind,'fosil');
 assert.equal(entry('colpocoryphe-sp').kind,'fosil');
 assert.notEqual(entry('colpocoryphe-sp').id,'conocoryphe');
});

test('anatomical remains keep independent IDs and never inherit whole-animal image banks',()=>{
 const part=entry('estructura-craneo-de-ovis-aries');assert.equal(part.kind,'estructura');assert.equal(part.parentTaxon,'Ovis aries');
 assert.equal(studyGroup(part),'Restos y estructuras animales');
 assert.notEqual(part.id,'ovis-orientalis-musimon');
 assert.equal(entry('estructura-huevo-de-coturnix-coturnix').parentTaxon,'Coturnix coturnix');
 assert.equal(entry('estructura-pico-de-sepia-officinalis').parentTaxon,'Sepia officinalis');
});
