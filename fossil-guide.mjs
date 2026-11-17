import {FOSSIL_GUIDES,GEOLOGICAL_INTERVALS,FOSSIL_CHALLENGES,sharedFossilIntervals} from './fossil-guide-data.mjs';

export function createFossilGuide(host,{esc,link,getPhoto,getEvidence,openCatalog}){
 const fossilById=new Map(FOSSIL_GUIDES.map(fossil=>[fossil.id,fossil]));
 const selected=new Set(['dactylioceras']);
 let questionIndex=0,checked=0,correct=0,detailId='dactylioceras';

 host.innerHTML=`
  <p class="eyebrow">DEL FÓSIL A LA EDAD DEL ESTRATO</p>
  <h1>Fósiles guía</h1>
  <p class="muted">Practica la lectura de cortes de Madrid. Sitúa un fósil en el tiempo, combina hallazgos y justifica hasta dónde puedes precisar.</p>
  <div class="fossil-method">
   <p><strong>1. Identifica.</strong> Distingue grupo, género y especie.</p>
   <p><strong>2. Acota.</strong> Busca el intervalo común de los fósiles del mismo estrato.</p>
   <p><strong>3. Comprueba.</strong> Contrasta la asociación, la facies y la posible presencia de fósiles retrabajados.</p>
  </div>
  <div class="fossil-modes" role="group" aria-label="Forma de estudiar fósiles guía">
   <button type="button" data-fossil-mode="explore" aria-pressed="true">Explorar intervalos</button>
   <button type="button" data-fossil-mode="practice" aria-pressed="false">Practicar cortes</button>
  </div>
  <div id="fossil-explore">
   <h2>Un grupo orienta. Un taxón preciso acota.</h2>
   <p class="help">Paleozoico · Cámbrico–Pérmico. Mesozoico · Triásico–Cretácico. Cenozoico · desde el Paleoceno.</p>
   <p class="help" id="fossil-scale-help">De más antiguo a más reciente →. Franjas por períodos y épocas, de anchura uniforme. Su tamaño no representa duración. Una franja coloreada indica presencia en alguna parte del intervalo, no en toda su extensión.</p>
   <div class="fossil-timeline" role="region" aria-label="Tabla de intervalos fósiles, desplazable horizontalmente" aria-describedby="fossil-scale-help" tabindex="0">
    <table>
     <caption>Selecciona fósiles con las casillas para construir un estrato. Pulsa un nombre para consultar su ficha.</caption>
     <thead><tr><th scope="col">Fósil del estrato</th>${GEOLOGICAL_INTERVALS.map(interval=>`<th scope="col" class="fossil-era-${interval.era.toLowerCase()}"><span>${interval.name}</span><small>${interval.era}</small></th>`).join('')}</tr></thead>
     <tbody>${FOSSIL_GUIDES.map(fossil=>`<tr data-fossil-row="${fossil.id}">
      <th scope="row"><div class="fossil-name"><label><input type="checkbox" data-fossil-pick="${fossil.id}" aria-label="Añadir ${esc(fossil.name)} al estrato" ${selected.has(fossil.id)?'checked':''}></label><button type="button" data-fossil-detail="${fossil.id}">${esc(fossil.name)}<small>${esc(fossil.scope)}</small></button></div></th>
      ${GEOLOGICAL_INTERVALS.map(interval=>`<td class="${fossil.intervals.includes(interval.id)?'fossil-presence':''}"><span class="sr-only">${fossil.intervals.includes(interval.id)?'Presencia documentada':'Fuera del intervalo de trabajo'}</span>${fossil.intervals.includes(interval.id)?'<span aria-hidden="true">●</span>':''}</td>`).join('')}
     </tr>`).join('')}</tbody>
    </table>
   </div>
   <div class="fossil-workspace">
    <section class="fossil-panel" aria-label="Laboratorio de un estrato">
     <p class="eyebrow">TU ESTRATO · ASOCIACIÓN SIMULADA</p>
     <h2>¿Qué edad comparten?</h2>
     <p class="help">Supón que los fósiles seleccionados proceden del mismo depósito y no han sido retrabajados. La comparación se calcula a la resolución de la tabla.</p>
     <div id="fossil-association" role="status" aria-live="polite"></div>
     <button type="button" id="fossil-clear" class="text-button">Vaciar el estrato</button>
    </section>
    <article class="fossil-panel" id="fossil-detail" aria-label="Ficha del fósil seleccionado"></article>
   </div>
  </div>
  <section id="fossil-practice" class="fossil-panel" hidden aria-label="Ejercicios de datación">
   <p class="eyebrow">ENTRENA EL RAZONAMIENTO</p>
   <p id="fossil-score" class="help" role="status"></p>
   <div id="fossil-question"></div>
   <div class="fossil-actions"><button type="button" id="fossil-check" class="primary-button">Comprobar</button><button type="button" id="fossil-reveal" class="text-button">Ver explicación</button><button type="button" id="fossil-next" class="secondary-button" hidden>Siguiente caso</button></div>
   <p id="fossil-feedback" role="status" aria-live="polite"></p>
  </section>
  <details class="fossil-sources">
   <summary>Cómo usar los intervalos y de dónde proceden</summary>
   <p>Un buen fósil guía combina un recorrido temporal breve con distribución amplia y posibilidad de identificación. Las fichas reúnen grupos orientativos y géneros más precisos. Para asignar una biozona hacen falta una determinación suficiente y una zonación contrastada.</p>
   <p>Si dos intervalos no se solapan, revisa la identificación y la procedencia. El retrabajamiento puede incorporar fósiles antiguos a un sedimento más joven. La edad del fósil y la del depósito que lo contiene pueden ser distintas.</p>
   <p>En el Cenozoico, la tabla desglosa el Paleógeno en Paleoceno, Eoceno y Oligoceno. Las franjas son una síntesis didáctica. Las precisiones de cada ficha prevalecen sobre la amplitud de la celda.</p>
   <p>El material PRECEGE ya cotejado en la app ayuda a elegir los taxones de estudio. Las menciones de Madrid se muestran con su procedencia y distinguen el contexto de un problema de una lista de reconocimiento. Cada ficha enlaza las fuentes geológicas de su intervalo.</p>
   <p>${link('https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/','BGS · fósiles y tiempo geológico')} · ${link('https://www.kgs.ku.edu/Current/2006/sawin/02_intro.html','Kansas Geological Survey · facies y retrabajamiento')}</p>
   <p class="help">Los casos prácticos son ejercicios didácticos propios. Los resultados duran esta sesión de práctica.</p>
  </details>`;

 function showDetail(id){
  detailId=id;
  const fossil=fossilById.get(id);
  const photo=fossil.catalogId&&getPhoto(fossil.catalogId);
  const evidence=fossil.catalogId?getEvidence(fossil.catalogId):[];
  const panel=host.querySelector('#fossil-detail');
  panel.innerHTML=`<p class="eyebrow">${esc(fossil.group)} · ${esc(fossil.scope)}</p>
   <h2>${esc(fossil.name)}</h2>
   <p class="fossil-age">${esc(fossil.age)}</p>
   ${photo?`<figure class="fossil-photo"><img src="${esc(photo.url)}" alt="Ejemplar de ${esc(fossil.name)}" loading="lazy"><figcaption>${photo.source?link(photo.source,photo.credit||'Procedencia de la fotografía'):esc(photo.credit)}</figcaption></figure>`:''}
   <h3>En qué fijarte</h3><p>${esc(fossil.recognition)}</p>
   <h3>Hasta dónde puedes precisar</h3><p>${esc(fossil.precision)}</p>
   ${fossil.catalogId?`<button type="button" class="text-button" data-fossil-catalog="${fossil.catalogId}">Abrir ficha y fotografías del catálogo</button>`:''}
   ${evidence.length?`<h3>En los materiales de Madrid</h3><ul>${evidence.map(event=>`<li>${esc(event.year||'Sin fecha')} · ${event.evidenceType==='context'?'contexto de problema':'lista de reconocimiento'} · ${event.sourceFile?esc(event.sourceFile)+' · pág. '+esc(event.sourcePage??event.page):link(event.source,'Enunciado / procedencia')}<small class="help">${esc(event.sourceType==='enunciado-oficial'?'Enunciado oficial':event.sourceType==='recopilacion-academia-sin-fecha'?'Recopilación académica sin atribución a un año':'Recopilación académica')}</small></li>`).join('')}</ul>`:''}
   <p class="help">${fossil.sources.map(source=>link(source.url,source.title)).join(' · ')}</p>`;
  panel.querySelector('img')?.addEventListener('error',event=>{
   event.target.closest('figure').replaceChildren(document.createTextNode('La fotografía no está disponible en este dispositivo. Puedes consultar la ficha del catálogo.'));
  },{once:true});
  host.querySelectorAll('[data-fossil-detail]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.fossilDetail===id)));
 }

 function updateAssociation(){
  const fossils=FOSSIL_GUIDES.filter(fossil=>selected.has(fossil.id));
  const shared=sharedFossilIntervals(fossils);
  const panel=host.querySelector('#fossil-association');
  if(!fossils.length){
   panel.innerHTML='<p>Marca al menos un fósil en la tabla para empezar.</p>';
  }else{
   panel.innerHTML=`<p><strong>${fossils.map(fossil=>esc(fossil.name)).join(' + ')}</strong></p>${shared.length?`<p class="fossil-age">${shared.map(interval=>interval.name).join(' · ')}</p><p>Este es el intervalo común a escala de la tabla. Consulta las fichas para afinar dentro de cada período.</p>`:'<p class="fossil-conflict"><strong>Sin intervalo común en este esquema.</strong> Revisa identificación, mezcla de muestras y posible retrabajamiento antes de asignar una edad.</p>'}`;
  }
  host.querySelectorAll('[data-fossil-row]').forEach(row=>row.classList.toggle('fossil-row-selected',selected.has(row.dataset.fossilRow)));
 }

 function updateScore(){
  host.querySelector('#fossil-score').textContent=`Caso ${questionIndex+1} de ${FOSSIL_CHALLENGES.length} · ${correct} aciertos de ${checked} respuestas comprobadas`;
 }

 function showQuestion(){
  const question=FOSSIL_CHALLENGES[questionIndex];
  host.querySelector('#fossil-question').innerHTML=`<p class="fossil-specimens">Muestra · ${question.fossils.map(id=>esc(fossilById.get(id).name)).join(' + ')}</p>
   <fieldset><legend tabindex="-1">${esc(question.prompt)}</legend>${question.choices.map((choice,index)=>`<label class="fossil-choice"><input type="radio" name="fossil-answer" value="${index}"> <span>${esc(choice)}</span></label>`).join('')}</fieldset>`;
  host.querySelector('#fossil-feedback').textContent='';
  host.querySelector('#fossil-next').hidden=true;
  host.querySelector('#fossil-next').textContent=questionIndex===FOSSIL_CHALLENGES.length-1?'Volver a empezar':'Siguiente caso';
  host.querySelector('#fossil-check').disabled=false;
  host.querySelector('#fossil-reveal').disabled=false;
  updateScore();
 }

 function answerQuestion(reveal){
  if(host.querySelector('#fossil-check').disabled)return;
  const question=FOSSIL_CHALLENGES[questionIndex];
  const answer=host.querySelector('[name="fossil-answer"]:checked');
  const feedback=host.querySelector('#fossil-feedback');
  if(!answer&&!reveal){
   feedback.textContent='Elige una respuesta o pulsa «Ver explicación».';
   return;
  }
  const success=!reveal&&Number(answer.value)===question.answer;
  if(!reveal){checked++;if(success)correct++;}
  feedback.textContent=`${reveal?'Solución':success?'Correcto':'Repasa este razonamiento'}. ${question.choices[question.answer]}. ${question.explanation}`;
  host.querySelectorAll('[name="fossil-answer"]').forEach(input=>input.disabled=true);
  host.querySelector('#fossil-check').disabled=true;
  host.querySelector('#fossil-reveal').disabled=true;
  host.querySelector('#fossil-next').hidden=false;
  updateScore();
 }

 host.addEventListener('click',event=>{
  const modeButton=event.target.closest('[data-fossil-mode]');
  if(modeButton){
   const practice=modeButton.dataset.fossilMode==='practice';
   host.querySelector('#fossil-explore').hidden=practice;
   host.querySelector('#fossil-practice').hidden=!practice;
   host.querySelectorAll('[data-fossil-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button===modeButton)));
  }
  const detailButton=event.target.closest('[data-fossil-detail]');
  if(detailButton)showDetail(detailButton.dataset.fossilDetail);
  const catalogButton=event.target.closest('[data-fossil-catalog]');
  if(catalogButton)openCatalog(catalogButton.dataset.fossilCatalog);
 });
 host.addEventListener('change',event=>{
  const id=event.target.dataset.fossilPick;
  if(!id)return;
  if(event.target.checked)selected.add(id);else selected.delete(id);
  updateAssociation();
 });
 host.querySelector('#fossil-clear').onclick=()=>{
  selected.clear();
  host.querySelectorAll('[data-fossil-pick]').forEach(input=>input.checked=false);
  updateAssociation();
 };
 host.querySelector('#fossil-check').onclick=()=>answerQuestion(false);
 host.querySelector('#fossil-reveal').onclick=()=>answerQuestion(true);
 host.querySelector('#fossil-next').onclick=()=>{
  questionIndex++;
  if(questionIndex===FOSSIL_CHALLENGES.length){questionIndex=0;checked=0;correct=0;}
  showQuestion();
  host.querySelector('legend').focus();
 };
 showDetail('dactylioceras');
 updateAssociation();
 showQuestion();
 return {refresh:()=>showDetail(detailId)};
}
