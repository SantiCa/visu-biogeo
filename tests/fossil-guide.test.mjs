import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {FOSSIL_GUIDES,GEOLOGICAL_INTERVALS,FOSSIL_CHALLENGES,sharedFossilIntervals} from '../fossil-guide-data.mjs';

const fossil=id=>FOSSIL_GUIDES.find(entry=>entry.id===id);
const shared=(...ids)=>sharedFossilIntervals(ids.map(fossil)).map(interval=>interval.id);

test('an empty association has no inferred age and multiple fossils narrow their common interval',()=>{
 assert.deepEqual(shared(),[]);
 assert.deepEqual(shared('trilobites','paradoxides'),['cambrian']);
 assert.deepEqual(shared('trilobites','fusulinids'),['carboniferous','permian']);
 assert.deepEqual(shared('ammonites','hippurites'),['cretaceous']);
 assert.deepEqual(shared('nummulites','trilobites'),[]);
});

test('the teaching ranges retain uncertainty rather than reducing broad taxa to their familiar age',()=>{
 assert.deepEqual(shared('nummulites'),['paleocene','eocene','oligocene']);
 assert.deepEqual(shared('monograptus'),['silurian','devonian']);
 assert.deepEqual(shared('ceratites','ammonites'),[]);
 assert.deepEqual(shared('dactylioceras','ammonites'),['jurassic']);
 const original=structuredClone(FOSSIL_GUIDES);
 sharedFossilIntervals(FOSSIL_GUIDES);
 assert.deepEqual(FOSSIL_GUIDES,original);
});

test('guide entries link to existing catalogue IDs and documented sources and intervals',async()=>{
 const catalogue=JSON.parse(await readFile(new URL('../data/species.json',import.meta.url),'utf8'));
 const catalogueIds=new Set(catalogue.map(item=>item.id));
 const intervals=new Set(GEOLOGICAL_INTERVALS.map(interval=>interval.id));
 assert.equal(new Set(FOSSIL_GUIDES.map(entry=>entry.id)).size,FOSSIL_GUIDES.length);
 for(const entry of FOSSIL_GUIDES){
  if(entry.catalogId)assert(catalogueIds.has(entry.catalogId),entry.catalogId);
  assert(entry.intervals.length>0);
  assert(entry.intervals.every(id=>intervals.has(id)),entry.id);
  assert(entry.sources.length>0);
  for(const source of entry.sources)assert.equal(new URL(source.url).protocol,'https:');
 }
 for(const question of FOSSIL_CHALLENGES){
  assert(question.fossils.every(id=>fossil(id)));
  assert(question.choices[question.answer]);
  assert(question.explanation.length>0);
 }
});
