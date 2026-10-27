export function studyNoteHTML(item,profile={},family={}, {esc,link}) {
 const biological=['organismo','fosil'].includes(item.kind);
 const sources=[...(profile.sources||[]),...(family.sources||[])].filter((s,i,a)=>s.url&&a.findIndex(x=>x.url===s.url)===i);
 return '<h2>Ficha de repaso'+(profile.commonName?' · '+esc(profile.commonName):'')+'</h2>'+
  '<p>'+esc(profile.description||'Descripción pendiente de documentar para esta entrada.')+'</p>'+
  (biological&&!profile.commonName?'<p class="help">Nombre común pendiente de documentar.</p>':'')+
  '<h3>Rasgos para reconocerla</h3>'+(profile.diagnostics?.length?'<ul>'+profile.diagnostics.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul>':'<p class="help">Rasgos diagnósticos pendientes de contrastar.</p>')+
  '<section class="etymology" aria-label="Etimología"><h3>Etimología del nombre</h3><p><strong>'+esc(item.scientificName)+':</strong> '+esc(profile.etymology||'Origen del nombre pendiente de contrastar.')+'</p>'+
  (biological?'<h3>Etimología de la familia</h3><p>'+(item.family?'<strong>'+esc(item.family)+':</strong> '+esc(family.etymology||'Etimología de la familia pendiente de contrastar.'):'Familia y etimología pendientes de documentar.')+'</p>':'')+'</section>'+
  (sources.length?'<p class="help note-sources">Fuentes: '+sources.map(s=>link(s.url,s.title||'Consultar referencia')).join(' · ')+'</p>':'');
}
