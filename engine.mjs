export const DAY = 86400000;
export function norm(value='') {
  return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/×/g,'x').replace(/[.,;:()]/g,' ').replace(/\s+/g,' ').trim();
}
export function answerMatches(answer, item) {
  // Illumination belongs to the specimen context, not to the mineral/rock name.
  if(item.kind==='lamina' && norm(answer)===norm(item.scientificName.split(/[.,]/)[0]))return true;
  return [item.scientificName,...(item.aliases||[])].some(name => {
    const n=norm(name); return norm(answer)===n || (/\ssp$/.test(n) && norm(answer)===n.replace(/\ssp$/,''));
  });
}
export function familyMatches(answer, item) {
  if(!item.family || !String(answer).trim()) return false;
  const traditional={Fabaceae:['Leguminosae'],Asteraceae:['Compositae'],Poaceae:['Gramineae'],Brassicaceae:['Cruciferae'],Lamiaceae:['Labiatae'],Apiaceae:['Umbelliferae'],Arecaceae:['Palmae'],Clusiaceae:['Guttiferae']};
  const group=Object.entries(traditional).find(([name,alternatives])=>[name,...alternatives].some(n=>norm(n)===norm(item.family)));
  const names=[item.family,...(item.familyAliases||[]),...(group?[group[0],...group[1]]:[])];
  return names.some(name=>norm(name)===norm(answer));
}
export function selectImagePair(images,previous=[],rng=Math.random) {
  const shuffled=[...images];
  for(let i=shuffled.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]];}
  const key=im=>im.key||im.url;
  if(shuffled.length>2 && previous.length===2 && shuffled.slice(0,2).every(im=>previous.includes(key(im)))) [shuffled[1],shuffled[2]]=[shuffled[2],shuffled[1]];
  return shuffled.slice(0,2);
}
export function priorityInfo(item, events=[], overrides={}, region='andalucia') {
  const evidence=events.filter(e=>e.itemId===item.id);
  const selected=evidence.filter(e=>region==='ambas'||(region==='madrid'?e.region==='Madrid':!e.region||e.region==='Andalucía'));
  const years=[...new Set(selected.map(e=>e.year).filter(Number.isInteger))].sort();
  const occurrences=new Set(selected.filter(e=>Number.isInteger(e.year)).map(e=>(e.region||'Andalucía')+':'+e.year));
  const undocumentedMadrid=selected.some(e=>e.region==='Madrid'&&!Number.isInteger(e.year));
  const override=overrides[item.id]?.reset ? null : overrides[item.id];
  const count=override ? Math.max(0,Math.min(30,Number(override.count)||0)) : occurrences.size+(undocumentedMadrid&&!selected.some(e=>e.region==='Madrid'&&Number.isInteger(e.year))?1:0);
  return {count,years,evidence:selected.map(e=>({...e,year:e.year??'Sin fecha',context:(e.region?e.region+' · ':'')+(e.context||'Recopilación')})),undated:undocumentedMadrid,manual:!!override,weight:1+Math.min(4,1.5*Math.log2(1+count)), retention:count ? .96 : .90};
}
export function blankRecord() { return {total:0, correct:0, lapses:0, repetitions:0, stability:1, interval:0, dueAt:0}; }
// Exponential forgetting approximation: R(t)=exp(-t/S). This is a transparent
// heuristic, not FSRS nor a fitted personal memory model. S is in days.
export function recall(record, now=Date.now()) {
  if (!record?.lastReviewed) return 0;
  const stability=record.stability || Math.max(1,(record.interval||1)/-Math.log(.90));
  return Math.exp(-Math.max(0,now-record.lastReviewed)/DAY/stability);
}
export function review(previous, {correct, familyCorrect=null, fieldResults={}, difficulty='good', priority=0, now=Date.now()}) {
  const r={...blankRecord(),...previous};
  const oldS=previous?.stability || (previous?.total ? Math.max(1,(previous.interval||1)/-Math.log(.90)) : 1);
  const retention=priority>0 ? .96 : .90;
  r.total++; r.correct+=Number(correct); r.lastReviewed=now;
  if(typeof familyCorrect==='boolean'){r.familyTotal=(r.familyTotal||0)+1;r.familyCorrect=(r.familyCorrect||0)+Number(familyCorrect);}
  r.fields=Object.fromEntries(Object.entries(r.fields||{}).map(([k,v])=>[k,{...v}]));
  for(const [key,value] of Object.entries(fieldResults))if(typeof value==='boolean'){const f=r.fields[key]||{total:0,correct:0};r.fields[key]={total:f.total+1,correct:f.correct+Number(value)};}
  if (!correct || familyCorrect===false || Object.values(fieldResults).some(v=>v===false)) {
    r.lapses++; r.repetitions=0; r.stability=Math.max(.3,oldS*.45);
    r.interval=10/1440; // Relearn after 10 minutes, not tomorrow.
  } else {
    r.repetitions++;
    r.stability=r.repetitions===1 ? 1/-Math.log(.90) : oldS*(difficulty==='easy'?2.6: difficulty==='hard'?1.25:1.9);
    r.interval=Math.min(365,Math.max(1/24,-r.stability*Math.log(retention)));
  }
  r.dueAt=now+r.interval*DAY;
  return r;
}
function weighted(items, weight, rng) {
  const weights=items.map(x=>Math.max(.001,weight(x)));
  let pick=rng()*weights.reduce((a,b)=>a+b,0);
  for(let i=0;i<items.length;i++){ pick-=weights[i]; if(pick<=0) return items[i]; }
  return items.at(-1)||null;
}
export function chooseNext(items, records, priority, {now=Date.now(),rng=Math.random,reviewCount=0,avoid=[]}={}) {
  const fresh=items.filter(x=>!records[x.id]?.total);
  const due=items.filter(x=>records[x.id]?.total && records[x.id].dueAt<=now);
  // Reserve every fifth selection for unseen subjects. Weighted sampling without
  // replacement introduces frequent exam subjects earlier but covers every new one.
  let pool=fresh.length && (reviewCount%5===0 || !due.length) ? fresh : due;
  if(!pool.length) pool=fresh;
  if(!pool.length) return null; // Never undo spacing by drawing not-yet-due cards.
  const other=pool.filter(x=>!avoid.includes(x.id)); if(other.length) pool=other;
  return weighted(pool,x=>priority(x).weight*(records[x.id]?.total ? 1+Math.min(4,1-recall(records[x.id],now)+(now-records[x.id].dueAt)/DAY) : 1),rng);
}
export function mergeRecords(local={}, remote={}) {
  const merged={...local};
  for(const [id,r] of Object.entries(remote)) if(!merged[id] || (r.lastReviewed||0)>(merged[id].lastReviewed||0)) merged[id]=r;
  return merged;
}
export function parsePriorityText(text, catalog) {
  const rows=[],errors=[];
  text.split(/\r?\n/).forEach((line,i)=>{
    if(!line.trim() || line.trim().startsWith('#')) return;
    const [name,countRaw='1',years='',source='',note='']=line.split('|').map(s=>s.trim());
    const matches=catalog.filter(x=>[x.scientificName,...(x.aliases||[])].some(n=>norm(n)===norm(name)));
    const count=Number(countRaw), ys=years?years.split(/[,; ]+/).map(Number):[];
    if(matches.length!==1) {errors.push(`Línea ${i+1}: nombre ${matches.length?'ambiguo':'no encontrado'}: ${name}`);return;}
    if(!Number.isInteger(count)||count<0||count>30||ys.some(y=>!Number.isInteger(y)||y<1900||y>2100)) {errors.push(`Línea ${i+1}: revisa frecuencia (0–30) y años.`);return;}
    rows.push({id:matches[0].id,count,years:[...new Set(ys)],source,note,updatedAt:Date.now()});
  });
  return {rows,errors};
}
