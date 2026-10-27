from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'app.js';s=p.read_text(encoding='utf8');s=s.replace("$('#source-progress').innerHTML=Object.entries(groups)", "$('#progress-metrics').innerHTML+=Object.entries({phylum:'Filo / división',genus:'Género',classification:'Clase mineral / origen',formula:'Fórmula química'}).map(([key,label])=>{const total=records.reduce((n,r)=>n+(r.fields?.[key]?.total||0),0),good=records.reduce((n,r)=>n+(r.fields?.[key]?.correct||0),0);return '<article><span>'+label+': aciertos / respuestas</span><strong>'+good+' / '+total+'</strong></article>';}).join('');$('#source-progress').innerHTML=Object.entries(groups)")
s=s.replace("const term=norm($('#classification-search').value)","const term=norm($('#classification-search').value.normalize('NFKC'))");s=s.replace("g?.formula].filter(Boolean).join(' ')).includes(term)","g?.formula].filter(Boolean).join(' ').normalize('NFKC')).includes(term)");p.write_text(s,encoding='utf8')
p=R/'data/learning-taxonomy.json';t=json.loads(p.read_text(encoding='utf8'));t['cruziana'].update(nonTaxonomic=True,status='not-applicable',reviewNote='Icnogénero: describe una traza fósil atribuida principalmente a actividad de trilobites, no el cuerpo de una especie. No se exige un filo del productor como si fuera un taxón corporal.',ranks={},hierarchy=[]);p.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
p=R/'data/curated-images.json';cur=json.loads(p.read_text(encoding='utf8'));source=cur['aspidiscus-cristatus']['images'];target=cur.setdefault('aspidiscus',{'images':[]})['images'];seen={im.get('originalUrl') or im['url'] for im in target}
for im in source:
 if im['status']=='approved' and (im.get('originalUrl') or im['url']) not in seen:target.append({**im,'reviewNote':im.get('reviewNote','')+' Ejemplo documentado de Aspidiscus cristatus para la entrada de género Aspidiscus.'})
p.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
print('Progress and source-backed genus example saved')
