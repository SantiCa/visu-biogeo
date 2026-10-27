import {norm,answerMatches,familyMatches} from './engine.mjs';

export const RANK_LABELS={kingdom:'Reino',phylum:'Filo',subphylum:'Subfilo',superclass:'Superclase',class:'Clase',subclass:'Subclase',infraclass:'Infraclase',superorder:'Superorden',order:'Orden',suborder:'Suborden',infraorder:'Infraorden',superfamily:'Superfamilia',family:'Familia',subfamily:'Subfamilia',tribe:'Tribu',genus:'Género',subgenus:'Subgénero',species:'Especie',subspecies:'Subespecie',variety:'Variedad'};
const ordered=Object.keys(RANK_LABELS);
export function commonNameFor(item,profile={},tax={}){return profile.commonName||tax.commonName||'';}
export function commonNamesFor(item,tax={},profile={}){return [...new Set([profile.commonName,tax.commonName,...(tax.commonNames||[])].filter(Boolean).flatMap(n=>String(n).split(/[;/,]/)).map(n=>n.trim()).filter(n=>n&&norm(n)!==norm(item.scientificName)))];}
export function commonNameMatches(answer,names){const clean=s=>norm(s).replace(/^(el|la|los|las|un|una) /,'');return !!clean(answer)&&names.some(n=>clean(n)===clean(answer));}
export function phylumLabel(tax={}){return tax.ranks?.kingdom==='Plantae'?'División':'Filo';}
export function formulaText(formula=''){return String(formula).replace(/\d/g,n=>'₀₁₂₃₄₅₆₇₈₉'[Number(n)]);}

// Case is significant: Co is cobalt, CO contains carbon and oxygen.
// Parse group multipliers and hydration; keep variable substitutions symbolic.
const normalizeFormula=value=>String(value).replace(/[₀-₉]/g,n=>String('₀₁₂₃₄₅₆₇₈₉'.indexOf(n))).replace(/\s/g,'').replace(/[⋅•]/g,'·');
function formulaAtoms(value){
 const s=normalizeFormula(value);
 if(!s||/[^A-Za-z0-9(),\[\].·]/.test(s))return null;
 const atoms={};
 for(const part of s.split(/[·.]/)){
  if(!part)return null;let i=0;const coeff=part.match(/^\d+/);if(coeff)i=coeff[0].length;
  function count(){const m=part.slice(i).match(/^\d+/);if(!m)return 1;i+=m[0].length;return Number(m[0]);}
  function parse(end){const out={};let terms=0;while(i<part.length&&part[i]!==end){let group;
   if(part[i]==='('||part[i]==='['){const close=part[i++]==='('?')':']';const rest=part.slice(i),choices=rest.match(/^([A-Z][A-Za-z0-9]*(?:,[A-Z][A-Za-z0-9]*)+)\)/);
    if(close===')'&&choices){group={['{'+choices[1].split(',').sort().join(',')+'}']:1};i+=choices[0].length;}
    else{group=parse(close);if(!group||part[i++]!==close)return null;}
   }else{const m=part.slice(i).match(/^[A-Z][a-z]?/);if(!m)return null;group={[m[0]]:1};i+=m[0].length;}
   const n=count();if(!Number.isSafeInteger(n)||n<1)return null;for(const [k,v] of Object.entries(group))out[k]=(out[k]||0)+v*n;terms++;
  }return terms?out:null;}
  const parsed=parse();if(!parsed||i!==part.length)return null;for(const[k,v]of Object.entries(parsed))atoms[k]=(atoms[k]||0)+v*Number(coeff?.[0]||1);
 }
 return Object.keys(atoms).sort().map(k=>k+':'+atoms[k]).join('|');
}
export function formulaMatches(answer,geo={}){
 if(!answer.trim()||!geo.formulaQuiz)return false;
 const a=formulaAtoms(answer);return [geo.formula,...(geo.formulaAliases||[])].some(f=>{const b=formulaAtoms(f);return a&&b?a===b:normalizeFormula(answer)===normalizeFormula(f);});
}
function scientificNames(item,tax){return [item.scientificName,...(item.aliases||[]),...(tax.matchedName?[tax.matchedName]:[])];}
export function quizFields(item,tax={},geo={},complete=true,profile={}){
 const fields=[];const ranks=tax.ranks||{},bio=['organismo','fosil'].includes(item.kind),genusOnly=tax.rank==='genus'||/\ssp\.?$/i.test(item.scientificName)||(!ranks.species&&item.scientificName.trim().split(/\s+/).length===1);
 fields.push({key:'name',label:bio?(genusOnly?'Género / nombre del taxón':complete?'Especie · epíteto o nombre completo':'Nombre científico'):'Nombre o denominación',expected:item.scientificName,required:true});
 if(bio){const names=commonNamesFor(item,tax,profile);fields.push({key:'common',label:'Nombre común',expected:names[0]||null,aliases:names,required:names.length>0});}
 if(complete&&bio&&!tax.nonTaxonomic){
  fields.push({key:'phylum',label:phylumLabel(tax),expected:ranks.phylum||null,required:!!ranks.phylum});
  fields.push({key:'family',label:'Familia',expected:ranks.family||item.family||null,required:!!(ranks.family||item.family)});
  if(!genusOnly)fields.push({key:'genus',label:'Género',expected:ranks.genus||null,required:!!ranks.genus});
 }
 if(complete&&geo.domain){
  fields.push({key:'classification',label:geo.domain==='mineral'?'Clase mineralógica · Nickel–Strunz':'Grupo por origen',expected:geo.classification||null,required:!!geo.classification});
  if(geo.formulaQuiz)fields.push({key:'formula',label:'Fórmula química',expected:geo.formula,required:true});
 }
 return fields;
}
export function evaluateIdentification(item,tax={},geo={},values={},complete=true,{reveal=false,profile={}}={}){
 const results={};const names=scientificNames(item,tax),extended={...item,aliases:names.slice(1)};
 for(const field of quizFields(item,tax,geo,complete,profile)){
  if(!field.expected){results[field.key]=null;continue;}
  const answer=String(values[field.key]||'');let ok=false;
  if(!reveal){
   if(field.key==='name'){
    ok=answerMatches(answer,extended);
    if(complete&&['organismo','fosil'].includes(item.kind)&&norm(values.genus))ok ||= names.some(n=>{const parts=norm(n).split(' ');return parts.length>=2&&parts[1]!=='sp'&&norm(answer)===parts.slice(1).join(' ')&&norm(values.genus)===parts[0];});
   }else if(field.key==='common')ok=commonNameMatches(answer,field.aliases);
   else if(field.key==='family')ok=familyMatches(answer,{...item,family:field.expected});
   else if(field.key==='genus')ok=names.some(n=>norm(n).split(' ')[0]===norm(answer))||norm(answer)===norm(field.expected);
   else if(field.key==='classification')ok=[field.expected,...(geo.classificationAliases||[])].some(n=>norm(n)===norm(answer));
   else if(field.key==='formula')ok=formulaMatches(answer,geo);
   else ok=norm(answer)===norm(field.expected);
  }
  results[field.key]=ok;
 }
 return {results,correct:results.name===true,familyCorrect:results.family??null,repeat:Object.values(results).some(v=>v===false)};
}

export function classificationPath(item,tax={},geo={}){
 if(geo.domain)return [{rank:'domain',name:geo.domain==='mineral'?'Minerales y materiales minerales':'Rocas y materiales geológicos'},...geo.path.map((name,i)=>({rank:i?'subgroup':'classification',name}))];
 if(tax.nonTaxonomic)return [{rank:'domain',name:'Otras entradas'},{rank:'group',name:'Estructuras biogénicas y trazas fósiles'}];
 if(['organismo','fosil'].includes(item.kind)||tax.subjectType){
  const ranks=tax.ranks||{};return [{rank:'domain',name:'Seres vivos y fósiles'},...ordered.filter(r=>r!=='kingdom'&&ranks[r]&&r!=='species'&&r!=='subspecies'&&r!=='variety').map(rank=>({rank,name:ranks[rank],label:rank==='phylum'?phylumLabel(tax):rank==='subphylum'&&ranks.kingdom==='Plantae'?'Subdivisión':RANK_LABELS[rank]})),...(!ranks.phylum?[{rank:'pending',name:'Filo / división pendiente de contrastar'}]:[])];
 }
 return [{rank:'domain',name:'Otras entradas'}, {rank:'group',name:item.classificationGroup||({estructura:'Estructuras e histología',lamina:'Láminas pendientes de clasificar',molecula:'Moléculas',nube:'Nubes',relieve:'Geomorfología'})[item.kind]||item.kind}];
}
export function buildClassificationForest(items,taxonomy={},geology={}){
 const root={children:[],count:0};for(const item of items){let node=root;node.count++;
  for(const part of classificationPath(item,taxonomy[item.id],geology[item.id])){
   let child=node.children.find(c=>!c.itemId&&c.rank===part.rank&&c.name===part.name);if(!child){child={...part,children:[],count:0};node.children.push(child);}child.count++;node=child;
  }node.children.push({itemId:item.id,name:item.scientificName,count:1});
 }
 function sort(node){node.children?.sort((a,b)=>(a.itemId?1:0)-(b.itemId?1:0)||a.name.localeCompare(b.name,'es'));node.children?.forEach(sort);}sort(root);return root;
}
