import {RANK_LABELS,classificationPath,commonNameFor,formulaText} from './classification-learning.mjs';
import {norm} from './engine.mjs';

const BOOK='https://openstax.org/books/biology-2e/pages/';
const RANK_SOURCE=BOOK+'20-1-organizing-life-on-earth';
export const RANK_GUIDE={
 kingdom:{label:'Reino',text:'Agrupación amplia que contiene varios filos o divisiones.',contrast:'Está por encima del filo; no indica una forma corporal única.'},
 phylum:{label:'Filo / división',text:'Reúne clases de un gran linaje. En botánica también se emplea división.',contrast:'Una clase es una subdivisión del filo, no su equivalente.'},
 class:{label:'Clase',text:'Agrupa órdenes dentro de un filo o división.',contrast:'Aves e Insecta son clases de filos diferentes.'},
 order:{label:'Orden',text:'Agrupa familias relacionadas dentro de una clase.',contrast:'Una familia tiene un alcance menor que su orden.'},
 family:{label:'Familia',text:'Agrupa géneros relacionados.',contrast:'Es un rango; Fagaceae es un taxón concreto de ese rango.'},
 genus:{label:'Género',text:'Agrupa especies próximas y aporta la primera palabra del nombre binomial.',contrast:'Quercus es género; Quercus ilex es una especie.'},
 species:{label:'Especie',text:'Unidad de clasificación que se nombra mediante género y epíteto específico.',contrast:'El epíteto aislado no es el nombre científico completo.'}
};
const G=(name,text,contrast,source)=>({name,text,contrast,source:source.startsWith('http')?source:BOOK+source});
export const TAXON_GUIDE=Object.fromEntries([
 G('Porifera','Esponjas: sistema de poros y canales con células filtradoras llamadas coanocitos.','No tienen los cnidocitos característicos de los cnidarios.','28-1-phylum-porifera'),
 G('Cnidaria','Pólipos y medusas con cnidocitos; organización generalmente radial.','La célula urticante es más diagnóstica que el aspecto de saco o campana.','28-2-phylum-cnidaria'),
 G('Anthozoa','Anémonas y corales: organización de pólipo, solitario o colonial.','No presentan una fase de medusa en su ciclo.','28-2-phylum-cnidaria'),
 G('Arthropoda','Exoesqueleto quitinoso, apéndices articulados y crecimiento por mudas.','Frente a los anélidos, destacan los apéndices articulados y el exoesqueleto.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Hexapoda','Artrópodos con tres pares de patas torácicas.','Incluye insectos y otros hexápodos; no todos los hexápodos se clasifican como Insecta.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Chelicerata','Artrópodos con quelíceros y sin antenas.','Incluye arácnidos y otros grupos; no equivale únicamente a arañas.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Myriapoda','Artrópodos con cabeza y tronco de numerosos segmentos portadores de patas.','Comparar con los tres pares de patas torácicas de los insectos.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Insecta','Adultos con cabeza, tórax y abdomen; tres pares de patas torácicas y un par de antenas.','Los arácnidos tienen cuatro pares de patas y carecen de antenas.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Arachnida','Quelíceros, pedipalpos y, típicamente en adultos, cuatro pares de patas.','No tienen antenas. El recuento de patas puede cambiar en fases juveniles de algunos grupos.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Crustacea','Agrupación tradicional de artrópodos con dos pares de antenas y apéndices muy especializados.','Dos pares de antenas frente al par de los insectos; su rango y circunscripción varían entre fuentes.','28-6-superphylum-ecdysozoa-arthropods'),
 G('Mollusca','Cuerpo con manto, masa visceral y pie muscular modificado según el grupo.','La concha puede reducirse o faltar; no es un requisito externo universal.','28-4-superphylum-lophotrochozoa-mollusks-and-annelids'),
 G('Gastropoda','Moluscos con torsión durante el desarrollo; pie reptante en muchas formas.','La concha suele ser única y espiral, pero las babosas muestran que puede faltar.','28-4-superphylum-lophotrochozoa-mollusks-and-annelids'),
 G('Bivalvia','Dos valvas laterales articuladas y cabeza reducida.','Carecen de rádula; distinguir dos valvas de dos vueltas de una misma concha.','28-4-superphylum-lophotrochozoa-mollusks-and-annelids'),
 G('Cephalopoda','Pie transformado en brazos o tentáculos y un embudo asociado a la locomoción.','Cabeza y ojos desarrollados; la concha puede ser externa, interna o ausente.','28-4-superphylum-lophotrochozoa-mollusks-and-annelids'),
 G('Annelida','Gusanos con organización corporal segmentada.','La segmentación no implica patas articuladas ni exoesqueleto como en artrópodos.','28-4-superphylum-lophotrochozoa-mollusks-and-annelids'),
 G('Platyhelminthes','Gusanos de cuerpo aplanado dorsoventralmente; incluyen formas libres y parásitas.','No presentan la segmentación corporal de los anélidos. Las proglótides de las tenias no son metámeros equivalentes.','28-3-superphylum-lophotrochozoa-flatworms-rotifers-and-nemerteans'),
 G('Nematoda','Gusanos cilíndricos, no segmentados, con cutícula que mudan durante el crecimiento.','Frente a los platelmintos destaca la sección circular; los anillos externos no prueban segmentación interna.','28-5-superphylum-ecdysozoa-nematodes-and-tardigrades'),
 G('Echinodermata','Animales marinos con sistema ambulacral y esqueleto interno de osículos calcáreos.','Adultos frecuentemente pentarradiales; las larvas presentan simetría bilateral.','28-7-superphylum-deuterostomia'),
 G('Chordata','En alguna fase presentan notocorda, cordón nervioso dorsal hueco, hendiduras faríngeas y cola postanal.','No todos son vertebrados: también incluye tunicados y cefalocordados.','29-1-chordates'),
 G('Vertebrata','Cordados con cráneo y una organización vertebral característica.','Es una subdivisión de Chordata, no un sinónimo de todo el filo.','29-1-chordates'),
 G('Aves','Plumas y extremidades anteriores transformadas en alas.','Las plumas distinguen las aves actuales; volar no es exclusivo ni universal.','29-5-birds'),
 G('Mammalia','Pelo y glándulas mamarias; rasgos craneales y dentarios característicos.','El pelo puede ser escaso. La viviparidad no es universal: existen monotremas ovíparos.','29-6-mammals'),
 G('Amphibia','Tetrápodos de piel generalmente permeable; muchos tienen larvas acuáticas y metamorfosis.','Frente a los amniotas, no presentan el huevo amniótico; hay ciclos vitales diversos.','29-3-amphibians'),
 G('Reptilia','Agrupación tradicional de amniotas con epidermis queratinizada.','Las aves se anidan evolutivamente en los reptiles; las clasificaciones por rangos pueden mostrarlas separadas.','29-4-reptiles'),
 G('Actinopterygii','Peces óseos cuyas aletas se sostienen mediante radios.','Frente a los condrictios, predomina un esqueleto osificado; observar también las aletas.','29-2-fishes'),
 G('Chondrichthyes','Tiburones, rayas y quimeras: esqueleto principalmente cartilaginoso.','El material del esqueleto y la anatomía branquial ayudan a separarlos de los peces óseos.','29-2-fishes'),
 G('Tracheophyta','Plantas vasculares con tejidos de conducción, xilema y floema.','Incluye plantas sin semillas y con semillas; no equivale solo a plantas con flores.','25-4-seedless-vascular-plants'),
 G('Bryophyta','Musgos: domina el gametófito; el esporófito permanece unido a él.','No presentan el sistema vascular típico de las traqueófitas.','25-3-bryophytes'),
 G('Marchantiophyta','Hepáticas: gametófitos talosos o foliosos y esporófitos dependientes.','Separarlas de musgos exige observar su organización, no solo el tamaño o el hábitat húmedo.','25-3-bryophytes'),
 G('Polypodiopsida','Helechos y grupos afines según la fuente; reproducción por esporas, sin flores ni semillas.','Los soros son útiles en muchos helechos, pero no aparecen como puntos foliares en todos los grupos.','25-4-seedless-vascular-plants'),
 G('Pinopsida','Coníferas: plantas con semillas no encerradas en un ovario; suelen presentar conos.','No producen frutos verdaderos; las cubiertas carnosas de algunas no son un ovario maduro.','26-2-gymnosperms'),
 G('Liliopsida','Monocotiledóneas: un cotiledón; son frecuentes la nerviación paralela y las flores trímeras.','Combinar rasgos: hay excepciones a los patrones foliares y florales.','26-3-angiosperms'),
 G('Magnoliopsida','Nombre de clase con circunscripción variable entre sistemas, asociado aquí a numerosas dicotiledóneas.','Dos cotiledones y nerviación reticulada son orientativos; no equivale automáticamente al clado de las eudicotiledóneas.','26-3-angiosperms'),
 G('Fagaceae','Árboles con flores unisexuales y frutos asociados a cúpulas: bellotas, hayucos o castañas.','Observar el fruto y su envoltura; la hoja por sí sola no separa todos los géneros.','https://www.asturnatura.com/familia/fagaceae'),
 G('Ascomycota','Hongos con reproducción sexual mediante ascos que contienen ascosporas.','El asco es la estructura clave; el aspecto externo de una seta no basta.','24-2-classifications-of-fungi'),
 G('Basidiomycota','Hongos que producen basidios y basidiosporas en su reproducción sexual.','El basidio los diferencia de los ascomicetos; no todos forman setas con sombrero.','24-2-classifications-of-fungi'),
 G('Ígneas','Rocas originadas por solidificación de material fundido.','Comparar tamaño de cristales, textura y composición con rocas sedimentarias y metamórficas.','https://www.nps.gov/subjects/geology/rocks.htm'),
 G('Sedimentarias','Rocas formadas a partir de sedimentos o por precipitación y procesos biogénicos.','Estratos y granos son pistas frecuentes, no condiciones universales.','https://www.nps.gov/subjects/geology/rocks.htm'),
 G('Metamórficas','Rocas transformadas en estado sólido por nuevas condiciones de presión, temperatura y fluidos.','La foliación puede orientar, pero también existen rocas metamórficas no foliadas.','https://www.nps.gov/subjects/geology/rocks.htm'),
 G('Silicatos','Grupo basado en unidades estructurales de silicio y oxígeno.','La conexión entre unidades permite distinguir cadenas, láminas y redes; la fórmula y la estructura se complementan.','https://www.nps.gov/subjects/geology/minerals.htm')
].map(g=>[g.name,g]));

export function rankGuide(rank){
 if(RANK_GUIDE[rank])return {...RANK_GUIDE[rank],source:RANK_SOURCE};
 if(rank==='root'||rank==='domain')return {label:rank==='root'?'Catálogo':'Grupo general',text:'Punto de entrada a las ramas del catálogo. Selecciona un grupo y compara sus subdivisiones.',contrast:'Las cifras cuentan entradas de tus listas de estudio. Explorar este árbol no puntúa ni cambia tus repasos.'};
 if(rank==='pending')return {label:'Dato pendiente',text:'La fuente de esta entrada no permite completar este nivel con suficiente precisión.',contrast:'Se conserva el hueco explícito y se muestran los rangos que sí están documentados.'};
 if(rank==='tribe'||rank==='variety')return {label:rank==='tribe'?'Tribu':'Variedad',text:rank==='tribe'?'Rango subordinado a la familia y superior al género.':'Rango infraespecífico empleado en botánica.',contrast:'Los rangos intermedios dependen del sistema y de la fuente; no todos se usan en cada linaje.',source:RANK_SOURCE};
 const base=rank.replace(/^(sub|super|infra)/,'');
 if(RANK_GUIDE[base])return {label:RANK_LABELS[rank]||rank,text:`Rango intermedio ${rank.startsWith('super')?'superior':'inferior'} a ${RANK_GUIDE[base].label.toLowerCase()}.`,contrast:'Permite detallar la jerarquía; no todas las fuentes utilizan los mismos rangos intermedios.',source:RANK_SOURCE};
 return {label:RANK_LABELS[rank]||({root:'Catálogo',domain:'Grupo general',classification:'Clase / origen',subgroup:'Subgrupo',group:'Agrupación',pending:'Pendiente',entry:'Entrada',tribe:'Tribu'})[rank]||rank,text:rank==='tribe'?'Rango entre familia y género, con posibles subdivisiones.':rank==='entry'?'Ejemplar o concepto de estudio del catálogo.':'Agrupación de estudio; no equivale por sí misma a un rango biológico.',contrast:'Minerales y rocas se agrupan por criterios químicos, estructurales o de origen.'};
}
const ranks=Object.keys(RANK_LABELS);
const aliases={Arthropoda:'artrópodos',Chordata:'cordados',Mollusca:'moluscos',Annelida:'anélidos',Echinodermata:'equinodermos',Cnidaria:'cnidarios',Porifera:'poríferos esponjas',Insecta:'insectos',Arachnida:'arácnidos',Gastropoda:'gasterópodos',Bivalvia:'bivalvos',Cephalopoda:'cefalópodos',Mammalia:'mamíferos',Amphibia:'anfibios',Plantae:'plantas',Animalia:'animales',Fungi:'hongos',Tracheophyta:'plantas vasculares',Pinopsida:'coníferas',Bryophyta:'musgos'};
export function buildStudyTree(catalog,taxonomy={},geology={},profiles={},filter={}){
 const root={id:'root',rank:'root',name:'Catálogo de estudio',children:[],count:0,depth:0},index=new Map([[root.id,root]]);const term=norm(filter.search||'');
 for(const item of catalog){
  const tax=taxonomy[item.id]||{},geo=geology[item.id]||{},bio=['organismo','fosil'].includes(item.kind)&&!tax.nonTaxonomic;
  const common=commonNameFor(item,profiles[item.id],tax),group=filter.group||'biology';
  if(group==='biology'&&!bio||group==='animals'&&(!bio||tax.ranks?.kingdom!=='Animalia')||group==='plants'&&(!bio||tax.ranks?.kingdom!=='Plantae')||group==='fungi'&&(!bio||tax.ranks?.kingdom!=='Fungi')||group==='mineral'&&geo.domain!=='mineral'||group==='roca'&&geo.domain!=='roca')continue;
  let path=classificationPath(item,tax,geo);
  if(bio)path=[path[0],tax.ranks?.kingdom?{rank:'kingdom',name:tax.ranks.kingdom}:{rank:'pending',name:'Reino sin documentar en la fuente'},...path.slice(1)];
  const text=[item.scientificName,common,...path.map(p=>p.name),...path.map(p=>aliases[p.name]||''),...path.map(p=>TAXON_GUIDE[p.name]?.text||''),geo.formula].join(' ');
  if(term&&!norm(text).includes(term))continue;
  let parent=root;parent.count++;
  for(const part of path){
   const id=parent.id+'/'+encodeURIComponent(part.rank+':'+part.name);let node=index.get(id);
   if(!node){node={...part,id,parentId:parent.id,depth:parent.depth+1,count:0,children:[]};parent.children.push(node);index.set(id,node);}
   node.count++;parent=node;
  }
  const leaf={id:'entry:'+item.id,rank:'entry',name:item.scientificName,common,formula:geo.formulaQuiz?formulaText(geo.formula):geo.formula,itemId:item.id,parentId:parent.id,depth:parent.depth+1,count:1,children:[]};parent.children.push(leaf);index.set(leaf.id,leaf);
 }
 for(const node of index.values())node.children.sort((a,b)=>Number(!!a.itemId)-Number(!!b.itemId)||a.name.localeCompare(b.name,'es'));
 return {root,index};
}
export function expandThrough(tree,target='phylum'){
 const open=new Set(['root']);const limit=ranks.indexOf(target);
 for(const n of tree.index.values())if(n.children.length&&(target==='all'||n.rank==='domain'||n.rank==='kingdom'||(limit>=0&&ranks.indexOf(n.rank)>=0&&ranks.indexOf(n.rank)<limit)))open.add(n.id);
 return open;
}
export function layoutStudyTree(tree,expanded){
 const nodes=[],edges=[];let nextY=40;
 function visit(n){const children=expanded.has(n.id)?n.children:[];const p={...n,x:n.depth*272+24,y:0,visibleChildren:children.length};nodes.push(p);
  if(children.length){const ps=children.map(c=>{const q=visit(c);edges.push({from:p,to:q});return q;});p.y=(ps[0].y+ps.at(-1).y)/2;}else {p.y=nextY;nextY+=72;}
  return p;
 }visit(tree.root);return {nodes,edges,width:Math.max(300,...nodes.map(n=>n.x+250)),height:Math.max(160,nextY)};
}
export function nodeAncestors(node,index){const result=[];while(node){result.unshift(node);node=index.get(node.parentId);}return result;}
export function descendants(node,limit=6){const out=[];function visit(n){if(out.length>=limit)return;if(n.itemId)out.push(n);else for(const child of n.children)visit(child);}visit(node);return out;}

const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const svgNS='http://www.w3.org/2000/svg';
export function createTaxonomyStudy(host,options){
 let tree,expanded=new Set(),selected='root',mode='explore',layout,view={x:0,y:0,w:1000,h:650},ready=false;
 const $=s=>host.querySelector(s);
 host.innerHTML=`<p class="eyebrow">ENTENDER ANTES DE MEMORIZAR</p><h1>Árboles de estudio</h1><p class="muted">Del grupo general al ejemplar: abre ramas, compara sus rasgos y recorre el mapa.</p>
 <details class="rank-intro"><summary>Cómo se leen los niveles de clasificación</summary><p>Un rango es un nivel; un taxón es un grupo con nombre. Este esquema organiza el catálogo, sin representar fechas ni distancias evolutivas. El mismo rango no implica idéntica diversidad o antigüedad.</p><div class="rank-ribbon">${Object.entries(RANK_GUIDE).map(([k,g])=>`<button data-rank-guide="${k}" type="button">${esc(g.label)}</button>`).join('<span aria-hidden="true">→</span>')}</div><p>De izquierda a derecha disminuye el alcance. Los rangos intermedios se conservan cuando están documentados. La ausencia de un rango no significa que no exista.</p><p class="help"><a href="${RANK_SOURCE}" target="_blank" rel="noopener noreferrer">Fuente: OpenStax · organización de la diversidad</a></p></details>
 <div class="filters tree-study-filters"><label>Buscar grupo o ejemplar<input id="guide-search" type="search" placeholder="Artrópodos, Aves, encina…"></label><label>Contenido<select id="guide-group"><option value="biology">Seres vivos y fósiles</option><option value="animals">Animales</option><option value="plants">Plantas</option><option value="fungi">Hongos</option><option value="mineral">Minerales</option><option value="roca">Rocas</option><option value="all">Todo el catálogo</option></select></label><label>Desplegar hasta<select id="guide-depth"><option value="phylum">Filo / división</option><option value="class">Clase</option><option value="order">Orden</option><option value="family">Familia</option><option value="genus">Género</option><option value="all">Todas las entradas</option></select></label></div>
 <div class="tree-study-toolbar"><div class="tree-mode" role="group" aria-label="Vista del árbol"><button id="guide-explore" aria-pressed="true">Árbol desplegable</button><button id="guide-map" aria-pressed="false">Mapa gigante</button></div><button id="guide-reset" class="text-button">Volver al inicio</button><button id="guide-focus" class="text-button">Centrar selección</button></div><p id="guide-count" class="help" role="status"></p>
 <div class="tree-study-workspace"><div class="tree-study-navigation"><div id="guide-outline" class="guide-outline" aria-label="Ramas de clasificación"></div><div id="guide-map-wrap" hidden><div class="map-controls"><button id="guide-zoom-in" aria-label="Acercar mapa">＋</button><button id="guide-zoom-out" aria-label="Alejar mapa">−</button><button id="guide-fit">Ver todo</button><span id="guide-zoom" class="help"></span></div><svg id="guide-canvas" class="guide-canvas" role="group" aria-label="Mapa de clasificación. Arrastra o usa las flechas para moverte; más y menos para ampliar; Inicio para ver todo." tabindex="0"></svg><svg id="guide-mini" class="guide-mini" role="img" aria-label="Minimapa. Pulsa para ir a esa zona"></svg><p class="help map-help">Arrastra para moverte · rueda o pellizco para ampliar · flechas, + y − con el mapa enfocado. Selecciona un nodo para leerlo; usa su signo para abrir ramas.</p></div></div><aside id="guide-detail" class="guide-detail" aria-label="Explicación del grupo seleccionado"></aside></div>`;
 const tip=(id,text)=>{$(id).dataset.help=text;$(id).title=text;};
 tip('#guide-reset','Restablece filtros, ramas y selección. No modifica tu progreso.');tip('#guide-focus','Lleva la vista al grupo seleccionado.');tip('#guide-fit','Ajusta todas las ramas actualmente desplegadas al mapa.');tip('#guide-zoom-in','Amplía alrededor del centro del mapa.');tip('#guide-zoom-out','Reduce la escala del mapa.');
 function build(){const data=options.getData();tree=buildStudyTree(data.catalog,data.taxonomy,data.geology,data.profiles,{group:$('#guide-group').value,search:$('#guide-search').value});expanded=expandThrough(tree,$('#guide-depth').value);selected=tree.index.has(selected)?selected:'root';ready=true;render(true);}
 function drawOutline(){
  const rows=[];function row(n,depth=0){const branch=n.children.length>0;rows.push(`<div class="guide-row${selected===n.id?' selected':''}" style="--tree-depth:${Math.min(depth,12)}"><button class="guide-toggle" ${branch?`data-toggle="${esc(n.id)}" aria-expanded="${expanded.has(n.id)}"`:'disabled'} aria-label="${branch?(expanded.has(n.id)?'Plegar ':'Desplegar '):'Entrada '}${esc(n.name)}">${branch?(expanded.has(n.id)?'−':'+'):'·'}</button><button class="guide-select" data-select="${esc(n.id)}" ${selected===n.id?'aria-current="true"':''}><small>${esc(n.label||rankGuide(n.rank).label)}</small><span>${esc(n.name)}</span>${n.common?`<small>${esc(n.common)}</small>`:''}<em>${n.itemId?'Ficha':n.count+' entradas'}</em></button></div>`);if(expanded.has(n.id))n.children.forEach(c=>row(c,depth+1));}row(tree.root);$('#guide-outline').innerHTML=rows.join('');
 }
 function detail(node){
  const data=options.getData(),g=rankGuide(node.rank),profile=TAXON_GUIDE[node.name],anc=nodeAncestors(node,tree.index);
  let html=`<div class="guide-breadcrumb" aria-label="Ruta">${anc.map(n=>`<button data-select="${esc(n.id)}">${esc(n.name)}</button>`).join('<span>›</span>')}</div><p class="eyebrow">${esc(node.label||g.label)}</p><h2>${esc(node.name)}</h2>`;
  if(node.itemId){html+=options.entryHTML(node.itemId);}
  else{
   html+=`<p>${node.count} entradas en esta selección.</p><section class="guide-rank-card"><h3>Qué significa este nivel</h3><p>${esc(g.text)}</p><p class="help">${esc(g.contrast)}</p></section>`;
   if(profile)html+=`<h3>Qué caracteriza al grupo</h3><p>${esc(profile.text)}</p><h3>En qué fijarte para distinguirlo</h3><p>${esc(profile.contrast)}</p><p class="help"><a href="${esc(profile.source)}" target="_blank" rel="noopener noreferrer">Fuente de la explicación</a></p>`;
   else if(node.rank!=='root'&&node.rank!=='domain')html+='<p class="help">Los rasgos propios de este grupo aún no tienen una ficha explicativa. Puedes estudiar sus ejemplares y consultar la fuente de su clasificación.</p>';
   if(options.referenceHTML)html+=options.referenceHTML(node.rank,node.name,descendants(node,1)[0]?.itemId);
   const sample=descendants(node,1)[0],tax=sample&&data.taxonomy[sample.itemId],geo=sample&&data.geology[sample.itemId];const source=geo?.sources?.[0]?.url||tax?.source;
   if(source&&node.rank!=='root'&&node.rank!=='domain')html+=`<p class="help"><a href="${esc(source)}" target="_blank" rel="noopener noreferrer">Registro de clasificación de un ejemplar de esta rama</a></p>`;
   if(node.children.length)html+=`<h3>Comparar las ramas siguientes</h3><div class="guide-compare">${node.children.map(child=>{const p=TAXON_GUIDE[child.name];return `<button data-select="${esc(child.id)}"><strong>${esc(child.name)}</strong><small>${esc(child.label||rankGuide(child.rank).label)} · ${child.count} entradas</small><span>${esc(p?.text||'Abrir posición, subgrupos y ejemplares de esta rama.')}</span></button>`;}).join('')}</div>`;
   const examples=descendants(node,4);if(examples.length)html+=`<h3>Ejemplares de esta rama</h3><div class="guide-examples">${examples.map(n=>`<button data-select="${esc(n.id)}">${esc(n.name)}${n.common?' · '+esc(n.common):''}</button>`).join('')}</div>`;
  }
  $('#guide-detail').innerHTML=html;
 }
 function select(id,focus=false){if(!tree.index.has(id))return;selected=id;const n=tree.index.get(id);nodeAncestors(n,tree.index).slice(0,-1).forEach(a=>expanded.add(a.id));render(false);if(focus)focusSelected();if(matchMedia('(max-width:800px)').matches)$('#guide-detail').scrollIntoView({block:'start',behavior:'smooth'});}
 function toggle(id){expanded.has(id)?expanded.delete(id):expanded.add(id);render(false);}
 function render(fit=false){layout=layoutStudyTree(tree,expanded);$('#guide-count').textContent=`${tree.root.count} entradas · ${layout.nodes.length} nodos desplegados · las cantidades se refieren a este catálogo, no a toda la biodiversidad.`;drawOutline();detail(tree.index.get(selected)||tree.root);if(fit)fitMap();else drawMap();}
 function fitMap(){const svg=$('#guide-canvas'),ratio=(svg.clientWidth||650)/(svg.clientHeight||600);view={x:-20,y:-20,w:Math.max(layout.width+40,(layout.height+40)*ratio),h:Math.max(layout.height+40,(layout.width+40)/ratio)};drawMap();}
 function focusSelected(){const n=layout.nodes.find(n=>n.id===selected);if(!n)return;if(mode==='map'){view.x=n.x+110-view.w/2;view.y=n.y-view.h/2;drawMap();}else{$('#guide-outline').querySelector('[aria-current="true"]')?.scrollIntoView({block:'center',behavior:'smooth'});}}
 function svgEl(tag,attrs={},text){const e=document.createElementNS(svgNS,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text)e.textContent=text;return e;}
 function drawMap(){if(!layout)return;const svg=$('#guide-canvas');svg.setAttribute('preserveAspectRatio','none');svg.setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);svg.replaceChildren();const ratio=(svg.clientWidth||650)/view.w,showLabels=ratio>.28;
  const visible=n=>n.x+250>view.x&&n.x<view.x+view.w&&n.y+28>view.y&&n.y-28<view.y+view.h;
  for(const e of layout.edges){if(Math.max(e.from.y,e.to.y)+30<view.y||Math.min(e.from.y,e.to.y)-30>view.y+view.h||e.to.x<view.x||e.from.x>view.x+view.w)continue;svg.append(svgEl('path',{d:`M${e.from.x+236},${e.from.y} H${e.from.x+252} V${e.to.y} H${e.to.x}`,fill:'none',stroke:'#b4cbbd','stroke-width':2}));}
  for(const n of layout.nodes.filter(visible)){
   const group=svgEl('g',{'data-map-select':n.id,role:'button',tabindex:showLabels?'0':'-1','aria-label':n.name+' · '+n.count+' entradas',class:'map-node'+(n.id===selected?' selected':'')});group.append(svgEl('title',{},n.name+' · '+(TAXON_GUIDE[n.name]?.text||rankGuide(n.rank).text)));group.append(svgEl('rect',{x:n.x,y:n.y-25,width:236,height:50,rx:9,fill:n.id===selected?'#123c32':n.itemId?'#f7edda':'#fffefa',stroke:'#7c9c89'}));
   if(showLabels){group.append(svgEl('text',{x:n.x+10,y:n.y-5,fill:n.id===selected?'#fff':'#567366','font-size':10},(n.label||rankGuide(n.rank).label)+' · '+n.count));const name=n.name.length>27?n.name.slice(0,25)+'…':n.name;group.append(svgEl('text',{x:n.x+10,y:n.y+13,fill:n.id===selected?'#fff':'#17251f','font-size':13,'font-weight':600},name));if(n.children.length){const t=svgEl('text',{x:n.x+216,y:n.y+8,fill:n.id===selected?'#fff':'#123c32','font-size':22,'data-map-toggle':n.id,role:'button',tabindex:'0','aria-label':(expanded.has(n.id)?'Plegar ':'Desplegar ')+n.name},expanded.has(n.id)?'−':'+');group.append(t);}}
   svg.append(group);
  }
  $('#guide-zoom').textContent=Math.round(ratio*100)+'%';const mini=$('#guide-mini');mini.replaceChildren();const miniRatio=150/110;const mw=Math.max(layout.width,layout.height*miniRatio),mh=mw/miniRatio;mini.setAttribute('viewBox',`0 0 ${mw} ${mh}`);
  for(const n of layout.nodes)mini.append(svgEl('rect',{x:n.x,y:n.y-12,width:220,height:24,fill:n.id===selected?'#c37a24':'#6a9680'}));mini.append(svgEl('rect',{x:view.x,y:view.y,width:view.w,height:view.h,fill:'#e8a94025',stroke:'#b57720','stroke-width':Math.max(4,mw/100)}));
 }
 function zoom(factor,point){const svg=$('#guide-canvas'),rect=svg.getBoundingClientRect();const px=point?(point.x-rect.left)/rect.width:.5,py=point?(point.y-rect.top)/rect.height:.5;const w=Math.max(280,Math.min(layout.width+layout.height*3,view.w*factor)),f=w/view.w;view={x:view.x+view.w*px*(1-f),y:view.y+view.h*py*(1-f),w,h:view.h*f};drawMap();}
 function switchMode(value){mode=value;$('#guide-outline').hidden=mode==='map';$('#guide-map-wrap').hidden=mode!=='map';$('#guide-explore').setAttribute('aria-pressed',mode==='explore');$('#guide-map').setAttribute('aria-pressed',mode==='map');if(mode==='map'){if(selected==='root'){const preferred=['Arthropoda','Tracheophyta','Fungi','Silicatos','Ígneas'].map(name=>[...tree.index.values()].find(n=>n.name===name)).find(Boolean);if(preferred)select(preferred.id);}fitMap();const svg=$('#guide-canvas'),width=svg.clientWidth||650,height=svg.clientHeight||580;view.w=width/.6;view.h=height/.6;focusSelected();}}
 host.addEventListener('click',e=>{const button=e.target.closest('[data-select],[data-toggle],[data-rank-guide],[data-map-select],[data-map-toggle]');if(!button)return;if(button.dataset.toggle)toggle(button.dataset.toggle);else if(button.dataset.mapToggle){e.stopPropagation();toggle(button.dataset.mapToggle);}else if(button.dataset.rankGuide){const g=rankGuide(button.dataset.rankGuide);$('#guide-detail').innerHTML=`<p class="eyebrow">NIVEL TAXONÓMICO</p><h2>${esc(g.label)}</h2><p>${esc(g.text)}</p><h3>Cómo se distingue</h3><p>${esc(g.contrast)}</p>${options.referenceHTML?options.referenceHTML(button.dataset.rankGuide,'',null):''}<p><a href="${g.source}" target="_blank" rel="noopener noreferrer">Fuente</a></p>`;}else select(button.dataset.select||button.dataset.mapSelect,!!button.dataset.select);});
 $('#guide-search').addEventListener('input',build);$('#guide-group').addEventListener('change',build);$('#guide-depth').addEventListener('change',()=>{expanded=expandThrough(tree,$('#guide-depth').value);render(true);});$('#guide-explore').onclick=()=>switchMode('explore');$('#guide-map').onclick=()=>switchMode('map');$('#guide-focus').onclick=focusSelected;$('#guide-reset').onclick=()=>{$('#guide-search').value='';$('#guide-group').value='biology';$('#guide-depth').value='phylum';selected='root';build();};$('#guide-fit').onclick=fitMap;$('#guide-zoom-in').onclick=()=>zoom(.75);$('#guide-zoom-out').onclick=()=>zoom(1/.75);
 const svg=$('#guide-canvas'),pointers=new Map();let last=null,moved=false,suppressClick=false;
 svg.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY>0?1.15:1/1.15,{x:e.clientX,y:e.clientY});},{passive:false});
 svg.addEventListener('pointerdown',e=>{pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});last={x:e.clientX,y:e.clientY};moved=false;suppressClick=false;});
 svg.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const old=[...pointers.values()];pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const current=[...pointers.values()];if(current.length===2&&old.length===2){const distance=a=>Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);if(distance(current)>5)zoom(distance(old)/distance(current),{x:(current[0].x+current[1].x)/2,y:(current[0].y+current[1].y)/2});moved=true;}else if(last){const dx=e.clientX-last.x,dy=e.clientY-last.y;if(!moved&&Math.abs(dx)+Math.abs(dy)<5)return;moved=true;svg.setPointerCapture(e.pointerId);const rect=svg.getBoundingClientRect();view.x-=dx*view.w/rect.width;view.y-=dy*view.h/rect.height;drawMap();}last={x:e.clientX,y:e.clientY};});
 const end=e=>{pointers.delete(e.pointerId);last=null;if(moved)suppressClick=true;};svg.addEventListener('pointerup',end);svg.addEventListener('pointercancel',end);svg.addEventListener('click',e=>{if(suppressClick){e.stopPropagation();suppressClick=false;}},true);
 svg.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)&&e.target!==svg){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));return;}if(['+','=','-','Home','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();if(e.key==='Home')fitMap();else if(e.key==='+'||e.key==='=')zoom(.75);else if(e.key==='-')zoom(1/.75);else{view.x+=(e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0)*view.w*.12;view.y+=(e.key==='ArrowDown'?1:e.key==='ArrowUp'?-1:0)*view.h*.12;drawMap();}}});
 $('#guide-mini').addEventListener('click',e=>{const r=e.currentTarget.getBoundingClientRect(),b=e.currentTarget.viewBox.baseVal;view.x=(e.clientX-r.left)/r.width*b.width-view.w/2;view.y=(e.clientY-r.top)/r.height*b.height-view.h/2;drawMap();});
 return {show(){if(!ready)build();else if(mode==='map')drawMap();},refresh:build,openTaxon(rank,name){$('#guide-search').value=name;$('#guide-group').value='all';build();const n=[...tree.index.values()].find(n=>n.rank===rank&&n.name===name);if(n){select(n.id);switchMode('map');}}};
}
