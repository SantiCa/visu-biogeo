import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {buildStudyTree,layoutStudyTree,expandThrough,nodeAncestors,rankGuide,RANK_GUIDE,TAXON_GUIDE} from '../taxonomy-guide.mjs';
const load=async n=>JSON.parse(await readFile(new URL('../data/'+n,import.meta.url),'utf8'));
const [catalog,taxonomy,geology,profiles]=await Promise.all(['species.json','learning-taxonomy.json','learning-geology.json','study-notes.json'].map(load));
test('the study tree retains every entry once and does not turn geology into biological ranks',()=>{
 const {root,index}=buildStudyTree(catalog,taxonomy,geology,profiles,{group:'all'});
 assert.equal(root.count,catalog.length);const entries=[...index.values()].filter(n=>n.itemId);assert.equal(entries.length,catalog.length);assert.equal(new Set(entries.map(n=>n.itemId)).size,catalog.length);
 const albite=index.get('entry:albita');assert(!nodeAncestors(albite,index).some(n=>n.rank==='kingdom'||n.rank==='phylum'));assert(albite.formula.includes('₃'));
});
test('search retains the documented lineage, supports Spanish names and never fabricates a missing rank',()=>{
 const {root,index}=buildStudyTree(catalog,taxonomy,geology,profiles,{group:'plants',search:'Quercus ilex'});assert(root.count>=1);
 const entry=[...index.values()].find(n=>n.itemId&&n.name==='Quercus ilex');const ancestors=nodeAncestors(entry,index);assert(ancestors.some(n=>n.name==='Plantae'));assert(ancestors.some(n=>n.name==='Tracheophyta'));
 const arthropods=buildStudyTree(catalog,taxonomy,geology,profiles,{group:'animals',search:'artrópodos'});assert(arthropods.root.count>200);
 const missing={id:'missing',kind:'organismo',scientificName:'Unknown'};const unresolved=buildStudyTree([missing],{}, {}, {},{group:'biology'});assert(![...unresolved.index.values()].some(n=>['class','order','family'].includes(n.rank)));
});
test('all-expanded geometry has finite coordinates, unique rows for specimens, and foldable descendants',()=>{
 const tree=buildStudyTree(catalog,taxonomy,geology,profiles,{group:'all'}),all=layoutStudyTree(tree,expandThrough(tree,'all'));
 assert.equal(all.nodes.length,tree.index.size);assert(all.nodes.every(n=>Number.isFinite(n.x)&&Number.isFinite(n.y)));
 const leaves=all.nodes.filter(n=>n.itemId);assert.equal(new Set(leaves.map(n=>n.y)).size,catalog.length);assert(all.width<10000);assert(all.height<500000);
 const collapsed=layoutStudyTree(tree,new Set(['root']));assert(collapsed.nodes.length<all.nodes.length);assert.equal(new Set(all.nodes.map(n=>n.id)).size,all.nodes.length);
});
test('rank explanations distinguish rank from taxon and group facts cite primary educational sources',()=>{
 for(const rank of Object.keys(RANK_GUIDE)){const g=rankGuide(rank);assert(g.text&&g.contrast&&g.source);}
 assert(rankGuide('subfamily').text.includes('inferior'));assert(rankGuide('superfamily').text.includes('superior'));
 for(const g of Object.values(TAXON_GUIDE))assert(/^https:\/\/(openstax.org|www.nps.gov|www.asturnatura.com|genent.cals.ncsu.edu)\//.test(g.source));
});
