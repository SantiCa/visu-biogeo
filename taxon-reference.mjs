import {rankGuide,TAXON_GUIDE} from './taxonomy-guide.mjs';
export const RANK_ETYMOLOGIES={
 kingdom:['Reino procede del latín regnum.','reino'],
 phylum:['Filo, en su acepción biológica, procede del griego phŷlon, raza o estirpe. División procede del latín divisio, -onis.','filo'],
 class:['Clase procede del latín classis.','clase'],order:['Orden procede del latín ordo, -inis.','orden'],
 family:['Familia procede del latín familia.','familia'],genus:['Género procede del latín genus, -eris.','género'],
 species:['Especie procede del latín species.','especie']
};
const TAXON_ETYMOLOGIES={
 Aves:['Aves es el plural latino de avis, ave.','https://dle.rae.es/ave'],
 Amphibia:['Se relaciona con el griego amphíbios y el latín amphibion, referido a un animal que vive en tierra y agua. Es el sentido histórico del nombre, no una regla sin excepciones sobre su ciclo.','https://dle.rae.es/anfibio'],
 Reptilia:['La base remite al latín reptilis, de donde procede reptil. El nombre se asocia tradicionalmente al desplazamiento reptante.','https://dle.rae.es/reptil'],
 Chordata:['El nombre alude a la notocorda. La raíz chord- corresponde al griego chordḗ, cuerda, documentada en notocordio.','https://dle.rae.es/notocordio'],
 Mammalia:['La base mamm- remite al latín mamma, mama; se relaciona con las glándulas mamarias. La historia completa de la formación Mammalia queda pendiente.','https://dle.rae.es/mamífero'],
 Bivalvia:['El nombre expresa la presencia de dos valvas: bi- y valva.','https://dle.rae.es/bivalvo'],
 Cephalopoda:['Formado sobre raíces griegas que remiten a cabeza y pie: kephalḗ y -podos.','https://dle.rae.es/cefalópodo'],
 Insecta:['La base latina insectum alude a las divisiones del cuerpo. El término latino es un calco de una voz griega relacionada con incisión o sección.','https://dle.rae.es/insecto'],
 Arachnida:['La raíz arachn- remite al griego aráchnē, araña; el DLE documenta esa raíz en arácnido.','https://dle.rae.es/arácnido'],
 Annelida:['La base annel- remite al latín anellus, anillo pequeño; alude a la organización anillada del cuerpo.','https://dle.rae.es/anélido'],
 Cnidaria:['La base cnid- corresponde al griego knídē, ortiga, relacionado con las células urticantes.','https://dle.rae.es/cnidario'],
 Echinodermata:['La raíz echin- remite al griego echînos, erizo. El nombre del grupo se relaciona con su cubierta espinosa; la derivación completa del nombre científico queda pendiente.','https://dle.rae.es/equinodermo'],
 Porifera:['Alude a los poros: el nombre se explica como portadores de poros.','https://openstax.org/books/biology-2e/pages/28-1-phylum-porifera'],
 Arthropoda:['El nombre alude a los apéndices articulados: pies articulados.','https://openstax.org/books/biology-2e/pages/28-6-superphylum-ecdysozoa-arthropods'],
 Mollusca:['El nombre alude al cuerpo blando de estos animales.','https://openstax.org/books/biology-2e/pages/28-4-superphylum-lophotrochozoa-mollusks-and-annelids'],
 Nematoda:['El nombre se relaciona con la idea de hilo, por el cuerpo alargado.','https://openstax.org/books/biology-2e/pages/28-5-superphylum-ecdysozoa-nematodes-and-tardigrades']
};
export function taxonReference(rank,name,{familyNotes={},profile={}}={}){
 const base=rank.replace(/^(sub|super|infra)/,''),entry=RANK_ETYMOLOGIES[base];
 const prefix=rank!==base?`${rank.startsWith('super')?'Super- indica posición superior; ':rank.startsWith('infra')?'Infra- indica posición inferior; ':'Sub- indica subordinación; '}`:'';
 const rankEtymology=entry?prefix+entry[0]:'Etimología de este rango pendiente de contrastar.';
 let taxonEtymology=TAXON_ETYMOLOGIES[name]?.[0]||'',source=TAXON_ETYMOLOGIES[name]?.[1]||'';
 if(rank==='family'&&familyNotes[name]?.etymology){taxonEtymology=familyNotes[name].etymology;source=familyNotes[name].sources?.[0]?.url||'';}
 if(['genus','species','subspecies','variety'].includes(rank)&&profile.etymology){taxonEtymology='Nota del nombre del ejemplar de esta rama: '+profile.etymology;source=profile.sources?.[0]?.url||'';}
 return {rank:rankGuide(rank),group:TAXON_GUIDE[name],rankEtymology,rankSource:entry?'https://dle.rae.es/'+entry[1]:'',taxonEtymology:taxonEtymology||'Origen del nombre de este taxón pendiente de contrastar. No se deduce solo de su terminación.',taxonSource:source};
}
export function referenceHTML(rank,name,context,{esc,link}){const r=taxonReference(rank,name,context);return '<section class="taxon-etymology"><h3>Etimología del nivel</h3><p>'+esc(r.rankEtymology)+'</p>'+(r.rankSource?'<p class="help">'+link(r.rankSource,'DLE · origen del término')+(rank==='phylum'?' · '+link('https://dle.rae.es/división','División'):'')+'</p>':'')+(name?'<h3>Etimología de '+esc(name)+'</h3><p>'+esc(r.taxonEtymology)+'</p>'+(r.taxonSource?'<p class="help">'+link(r.taxonSource,'Referencia del nombre')+'</p>':''):'')+'</section>';}
export function setupTaxonHelp({getContext,openTree,esc,link}){
 const panel=document.createElement('aside');panel.id='taxon-popover';panel.className='taxon-popover';panel.hidden=true;panel.setAttribute('role','dialog');panel.setAttribute('aria-label','Información del taxón');document.body.append(panel);
 let trigger=null,pinned=false,timer;
 const hide=()=>{clearTimeout(timer);panel.hidden=true;trigger?.setAttribute('aria-expanded','false');trigger=null;pinned=false;};
 function show(button){clearTimeout(timer);if(trigger===button&&!panel.hidden)return;trigger?.setAttribute('aria-expanded','false');trigger=button;pinned=false;const {rank,name,item}=button.dataset,context=getContext(item),r=taxonReference(rank,name,context);button.setAttribute('aria-expanded','true');button.setAttribute('aria-controls',panel.id);
  panel.innerHTML='<button class="taxon-close" aria-label="Cerrar información del taxón">×</button><p class="eyebrow">'+esc(r.rank.label)+'</p><h2>'+esc(name)+'</h2><p>'+esc(r.rank.text)+'</p>'+(r.group?'<h3>Rasgos del grupo</h3><p>'+esc(r.group.text)+'</p><p>'+esc(r.group.contrast)+'</p>':'<p class="help">Los rasgos propios de este taxón aún no tienen ficha explicativa.</p>')+referenceHTML(rank,name,context,{esc,link})+'<button class="secondary-button taxon-open-tree">Explorar este grupo en el árbol</button><p class="help">Toque o clic para fijar · Esc o × para cerrar.</p>';
  panel.hidden=false;const rect=button.getBoundingClientRect(),width=Math.min(380,window.innerWidth-24);panel.style.width=width+'px';panel.style.left=Math.max(12,Math.min(window.innerWidth-width-12,rect.left))+'px';const desiredHeight=Math.min(560,window.innerHeight-24),top=window.innerHeight-rect.bottom>300?rect.bottom+8:rect.top-desiredHeight-8;panel.style.top=Math.max(12,Math.min(window.innerHeight-190,top))+'px';panel.style.maxHeight=Math.max(150,window.innerHeight-parseFloat(panel.style.top)-12)+'px';
  panel.querySelector('.taxon-close').onclick=hide;panel.querySelector('.taxon-open-tree').onclick=()=>{hide();openTree(rank,name);};
 }
 const leave=()=>{clearTimeout(timer);if(!pinned)timer=setTimeout(hide,220);};
 document.addEventListener('pointerover',e=>{const b=e.target.closest('[data-tax-help]');if(b)show(b);else if(!panel.contains(e.target))leave();});
 panel.addEventListener('pointerenter',()=>clearTimeout(timer));panel.addEventListener('pointerleave',leave);
 document.addEventListener('focusin',e=>{const b=e.target.closest('[data-tax-help]');if(b)show(b);});
 document.addEventListener('click',e=>{const b=e.target.closest('[data-tax-help]');if(b){show(b);pinned=true;}else if(!panel.contains(e.target))hide();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')hide();});
 return {hide};
}
