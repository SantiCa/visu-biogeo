import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {sourceLabel,studyLists,listMatches,groupCatalog,studyGroup,familyLabel,classificationFor} from '../catalogue.mjs';

test('Bonnier species join the existing lists and retain their original provenance',()=>{
 const item={id:'avena',sources:['Avena sativa. Bonnier.pdf','Listado de visu de Poáceas (Gramíneas).pdf']};
 assert.deepEqual(studyLists(item),['Poáceas (gramíneas)']);
 assert.ok(listMatches(item,'Poáceas (gramíneas)'));
 assert.equal(sourceLabel('Lotus corniculatus. BONNIER.pdf'),'Flores');
 assert.equal(item.sources[0],'Avena sativa. Bonnier.pdf');
});
test('all real catalogue lists have friendly labels without PDF extensions or Bonnier entries',()=>{
 const catalog=JSON.parse(readFileSync(new URL('../data/species.json',import.meta.url)));
 const labels=catalog.flatMap(studyLists);
 assert.ok(labels.length>0);assert.ok(labels.every(s=>!/(\.pdf|bonnier|^listado)/i.test(s)));
 assert.equal(sourceLabel('Listado de visu  de minerales y rocas lamina delgada.pdf'),'Minerales y rocas en lámina delgada');
});
test('grouping by list preserves multiple memberships and grouping by family uses documented families',()=>{
 const item={id:'a',scientificName:'Abies pinsapo',kind:'organismo',family:'Pinaceae',sources:['Listado de ÁRBOLES Y ARBUSTOS.pdf','Examen Andalucía 2021']};
 assert.equal(groupCatalog([item],'lists').length,2);assert.equal(groupCatalog([item],'family')[0].label,'Pinaceae');assert.equal(studyGroup(item),'Árboles y arbustos');
 assert.equal(familyLabel({kind:'roca'}),'No procede');
 assert.equal(groupCatalog([{id:'r',scientificName:'Granito',kind:'roca'}],'family')[0].label,'Rocas');
});
test('documented lineages classify regional-only entries, while lichens retain their study group',()=>{
 assert.equal(studyGroup({kind:'organismo',classificationGroup:'Mamíferos',sources:['Listado de animales de la región eurosiberiana.pdf']}),'Mamíferos');
 assert.equal(studyGroup({kind:'organismo',classificationGroup:'Hongos',sources:['Listado de VISU DE LÍQUENES.pdf']}),'Líquenes');
});
test('classification needs a matching documented family and safely ignores rocks and missing records',()=>{
 assert.equal(classificationFor({kind:'roca'},undefined),null);
 assert.equal(classificationFor({kind:'organismo',family:'Felidae'},undefined),null);
 assert.equal(classificationFor({kind:'organismo',family:'Felidae'},{family:'Canidae',group:'Mamíferos'}),null);
 const record={family:'Felidae',group:'Mamíferos'};assert.equal(classificationFor({kind:'organismo',family:'Felidae'},record),record);
});
