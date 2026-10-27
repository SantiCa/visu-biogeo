import {norm} from './engine.mjs';

export const KIND_LABELS={organismo:'Organismos',mineral:'Minerales',roca:'Rocas',fosil:'Fósiles',estructura:'Estructuras e histología',molecula:'Moléculas',nube:'Nubes',relieve:'Geomorfología',lamina:'Lámina delgada'};
const SUBJECTS=[
 ['poaceas','Poáceas (gramíneas)'],['gramineas','Poáceas (gramíneas)'],['arboles y arbustos','Árboles y arbustos'],
 ['estructuras de insectos','Estructuras de insectos'],['aracnidos y otros artropodos','Arácnidos y otros artrópodos'],
 ['aracnidos y otros artopodos','Arácnidos y otros artrópodos'],
 ['insectos','Insectos'],['crustaceos','Crustáceos'],['anfibios y reptiles','Anfibios y reptiles'],
 ['citologia e histologia animal','Citología e histología animal'],['histologia vegetal','Histología vegetal'],
 ['bacterias, virus y protozoos','Bacterias, virus y protozoos'],['organismos unicelurares','Organismos unicelulares'],
 ['estructuras microscopicas','Estructuras microscópicas'],['tipos de frutos','Tipos de frutos'],
 ['minerales y rocas lamina delgada','Minerales y rocas en lámina delgada'],['minerales visu','Minerales'],
 ['geomorfologia fluvial y costera','Geomorfología fluvial y costera'],['geomorfologia granitica','Geomorfología granítica'],
 ['geomorfologia karstica','Geomorfología kárstica'],['geomorfologia glacial','Geomorfología glacial'],
 ['tectonica y varios geomorfologia','Tectónica y otras formas del relieve'],['musgos y hepaticas','Musgos y hepáticas'],
 ['picnogonidos, poriferos','Picnogónidos, poríferos y otros invertebrados'],['phylum cnidaria','Cnidarios'],
 ['restos de arribazon','Restos de arribazón'],['restos y estructuras animales','Restos y estructuras animales'],['especies de baleares','Especies de Baleares'],
 ['animales de la region eurosiberiana','Animales de la región eurosiberiana'],['animales de la region mediterranea','Animales de la región mediterránea'],
 ['vegetales de la region eurosiberiana','Plantas de la región eurosiberiana'],['plantas de la region mediterranea','Plantas de la región mediterránea'],
 ['helechos','Helechos'],['hongos','Hongos'],['liquenes','Líquenes'],['moluscos','Moluscos'],['peces','Peces'],['algas','Algas'],['gusanos','Gusanos'],
 ['fosiles','Fósiles'],['aves','Aves'],['flores','Flores'],['rocas','Rocas'],['moleculas','Moléculas'],['nubes','Nubes']
];

export function sourceLabel(source){
 const clean=String(source).replace(/\.pdf$/i,'').replace(/\s+/g,' ').trim();
 if(/bonnier/i.test(clean))return /^(Avena|Briza|Hordeum)\b/i.test(clean)?'Poáceas (gramíneas)':'Flores';
 const n=norm(clean);
 if(/^examen (andalucia|madrid)/.test(n))return 'Exámenes anteriores';
 return SUBJECTS.find(([key])=>n.includes(norm(key)))?.[1]||clean;
}
export function studyLists(item){return [...new Set([...(item.sources||[]).map(sourceLabel),...(item.studyLists||[]),...(item.examEvents?.length?['Exámenes anteriores']:[])])];}
export function listMatches(item,label){return !label||studyLists(item).includes(label);}

export function examMatches(item,{region='',year='',evidenceType=''}={}){
 return (item.examEvents||[]).some(e=>(!region||e.region===region)&&(!year||(year==='undated'?e.year==null:String(e.year)===String(year)))&&(!evidenceType||e.evidenceType===evidenceType));
}
export function examYears(documents,region='') {
 const selected=documents.filter(d=>!region||d.region===region);
 const years=[...new Set(selected.map(d=>d.year).filter(y=>Number.isInteger(y)&&y>0))].sort((a,b)=>b-a);
 return selected.some(d=>d.year==null)?[...years,'undated']:years;
}
export function examYearLabel(year){return year==null||year==='undated'?'Varios años · sin fecha':String(year);}

const BIO_GROUPS=['Poáceas (gramíneas)','Helechos','Musgos y hepáticas','Algas','Hongos','Líquenes','Árboles y arbustos','Flores','Aves','Anfibios y reptiles','Peces','Insectos','Arácnidos y otros artrópodos','Crustáceos','Moluscos','Gusanos','Cnidarios','Picnogónidos, poríferos y otros invertebrados','Bacterias, virus y protozoos','Organismos unicelulares'];
export function studyGroup(item){
 const lists=studyLists(item);
 if(item.kind==='organismo'&&item.classificationGroup)return lists.includes('Líquenes')?'Líquenes':item.classificationGroup;
 if(item.kind==='organismo')return BIO_GROUPS.find(label=>lists.includes(label))||'Otros organismos';
 if(item.kind==='estructura')return ['Restos y estructuras animales','Histología vegetal','Citología e histología animal','Estructuras de insectos','Estructuras microscópicas','Tipos de frutos'].find(label=>lists.includes(label))||KIND_LABELS[item.kind];
 if(item.kind==='relieve')return lists.find(label=>label.startsWith('Geomorfología')||label.startsWith('Tectónica'))||KIND_LABELS[item.kind];
 return KIND_LABELS[item.kind]||item.kind;
}
export function familyLabel(item){return ['organismo','fosil'].includes(item.kind)?item.family||'Familia pendiente de documentar':'No procede';}
export function classificationFor(item,record){return item.kind==='organismo'&&item.family&&record?.family===item.family&&record.group?record:null;}
export function groupCatalog(items,mode){
 const groups=new Map();
 for(const item of items){
  const labels=mode==='lists'?studyLists(item):[mode==='group'?studyGroup(item):mode==='family'?(['organismo','fosil'].includes(item.kind)?familyLabel(item):KIND_LABELS[item.kind]):''];
  for(const label of labels.length?labels:['Sin lista asignada']){if(!groups.has(label))groups.set(label,[]);groups.get(label).push(item);}
 }
 return [...groups].sort(([a],[b])=>a.localeCompare(b,'es')).map(([label,items])=>({label,items:[...items].sort((a,b)=>a.scientificName.localeCompare(b.scientificName,'es'))}));
}
