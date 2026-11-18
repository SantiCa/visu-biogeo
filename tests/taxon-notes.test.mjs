import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {NOTE_FILES,assembleNotes,loadNotes,taxonGuide} from '../taxon-notes.mjs';
import {taxonReference} from '../taxon-reference.mjs';
import {buildStudyTree} from '../taxonomy-guide.mjs';
import {studyNoteHTML} from '../notes.mjs';

const load=async name=>JSON.parse(await readFile(new URL('../data/'+name,import.meta.url),'utf8'));
const banks=await Promise.all(NOTE_FILES.map(load));
const notes=assembleNotes(banks);
const [catalog,taxonomy,geology]=await Promise.all(['species.json','learning-taxonomy.json','learning-geology.json'].map(load));

test('every catalogue ID keeps its name, with unfilled profiles remaining unfilled',()=>{
 const entries=Object.assign({},...banks.map(bank=>bank.entries));
 assert.equal(Object.keys(entries).length,catalog.length);
 for(const item of catalog)assert.equal(entries[item.id].name,item.scientificName);
 assert(Object.keys(notes.profiles).length>=587);
 assert(Object.keys(notes.families).length>=95);
 assert.equal(entries.antracita.profile,undefined);
 const html=studyNoteHTML(catalog.find(item=>item.id==='antracita'),{}, {},{esc:String,link:()=>''});
 assert(html.includes('Descripción pendiente'));
});

test('fifteen pending PR group descriptions and the four species updates remain available',()=>{
 for(const [rank,names] of Object.entries({class:['Echinoidea','Crinoidea','Trilobita','Lycopodiopsida','Rhynchonellata'],order:['Primates','Equisetales','Ammonitida','Belemnitida','Scleractinia','Proboscidea'],family:['Poaceae','Asteraceae','Balanidae','Hominidae']})){
  for(const name of names){const guide=taxonGuide(notes.taxa,rank,name);assert(guide?.text,name);assert(guide.contrast&&guide.source,name);}
 }
 assert.equal(notes.profiles['briza-minor'].commonName,'tembladera');
 assert.equal(notes.profiles['calendula-arvensis'].commonName,'maravilla silvestre');
 assert(notes.profiles['avena-sativa'].etymology.includes('nombre latino'));
 assert(notes.profiles['hordeum-vulgare'].etymology.includes('nombre latino'));
});

test('references use the exact taxon instead of an arbitrary descendant profile',()=>{
 const context={taxa:notes.taxa,familyNotes:notes.families,profile:notes.profiles['avena-sativa']};
 assert(taxonReference('phylum','Arthropoda',context).taxonSource.includes('openstax'));
 assert.equal(taxonReference('family','Poaceae',context).taxonEtymology,notes.families.Poaceae.etymology);
 assert(taxonReference('genus','Avena',context).taxonEtymology.includes('pendiente'));
 assert(!taxonReference('genus','Avena',context).taxonEtymology.includes('Sativa'));
 assert.equal(taxonReference('species','Avena sativa',context).taxonEtymology,notes.profiles['avena-sativa'].etymology);
 assert.equal(taxonReference('genus','Balanus',context).taxonEtymology,notes.profiles.balanus.etymology);
 assert(taxonGuide(notes.taxa,'classification','Ígneas')?.text.includes('solidificación'));
});

test('tree descriptions and searches share the loaded rank files without changing entry IDs',()=>{
 const tree=buildStudyTree(catalog,taxonomy,geology,notes.profiles,{group:'biology',search:'lígula'},notes.taxa);
 assert(tree.index.has('entry:avena-sativa'));
 assert(tree.index.has('entry:briza-minor'));
 assert(taxonGuide(notes.taxa,'genus','Pecopteris').text===notes.profiles.pecopteris.description);
});

test('missing rank files fail visibly and duplicate IDs cannot overwrite another profile',async()=>{
 await assert.rejects(loadNotes(async path=>{if(path.endsWith('order-notes.json'))throw Error('missing order notes');return load(path.split('/').at(-1));}),/missing order notes/);
 assert.throws(()=>assembleNotes([{taxa:{},entries:{a:{name:'First'}}},{taxa:{},entries:{a:{name:'Second'}}}]),/duplicada/);
});
