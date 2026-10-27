from pathlib import Path
from collections import Counter
from datetime import date
import json,urllib.parse
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));cur=json.loads((DATA/'curated-images.json').read_text(encoding='utf8'));history=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'));priority={e['itemId'] for e in history['events']}
def identity(im):
    if 'commons.wikimedia.org/wiki/File' in im.get('page',''):return urllib.parse.unquote(im['page'].split('?')[0]).replace('_',' ')
    return im.get('key') or im.get('page') or im.get('originalUrl') or im['url']
counts={};errors=[];sources=Counter();decisions=Counter()
for item in catalog:
    seen=set()
    for im in cur.get(item['id'],{}).get('images',[]):
        decisions[im['status']]+=1
        if im['status']!='approved' or identity(im) in seen:continue
        seen.add(identity(im));sources[urllib.parse.urlsplit(im.get('page','')).hostname or 'referencia local']+=1
        if im['url'].startswith('./'):
            path=ROOT/im['url'][2:]
            try:
                with Image.open(path) as pic:pic.verify()
            except Exception as e:errors.append({'itemId':item['id'],'image':im['url'],'error':str(e)})
    counts[item['id']]=len(seen)
missing=[{'id':x['id'],'name':x['scientificName'],'kind':x['kind'],'approvedImages':counts[x['id']],'priority':x['id'] in priority} for x in catalog if counts[x['id']]<2]
audit={'date':date.today().isoformat(),'catalogEntries':len(catalog),'entriesWithApprovedImage':sum(n>0 for n in counts.values()),'entriesWithPair':sum(n>=2 for n in counts.values()),'approvedImages':sum(counts.values()),'priorityEntries':len(priority),'priorityWithPair':sum(counts[id]>=2 for id in priority),'decisions':dict(decisions),'imageSources':dict(sources),'brokenApprovedFiles':errors,'priorityMissingPairs':[x for x in missing if x['priority']],'allMissingPairs':missing,'reviewDefinition':'Correspondencia con fuente identificada y revisión visual; no peritaje taxonómico ni garantía de identificación de especies crípticas.'}
(DATA/'image-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
labels={'organismo':'Organismos','mineral':'Minerales','roca':'Rocas','fosil':'Fósiles','estructura':'Estructuras e histología','lamina':'Lámina delgada','molecula':'Moléculas','nube':'Nubes','relieve':'Geomorfología'}
report=['# Estado de la revisión de imágenes','',f"Fecha: {audit['date']}. Catálogo: {len(catalog)} entradas.",'',f"- {audit['approvedImages']} imágenes aprobadas y {audit['entriesWithPair']} entradas con al menos dos imágenes distintas según su referencia.",f"- {audit['priorityWithPair']}/{len(priority)} prioritarias del histórico disponible con pareja. El histórico es parcial: no cubre todos los exámenes de las últimas dos décadas.",f"- {len(missing)} entradas pendientes de completar la pareja; {len(catalog)-audit['entriesWithApprovedImage']} sin imagen aprobada.",f"- Archivos aprobados no legibles: {len(errors)}.",'','| Grupo | Entradas | Con pareja aprobada | Pendientes de pareja |','|---|---:|---:|---:|']
for kind,label in labels.items():
    items=[i for i in catalog if i['kind']==kind];paired=sum(counts[i['id']]>=2 for i in items)
    report.append(f'| {label} | {len(items)} | {paired} | {len(items)-paired} |')
report+=['','## Alcance y pendientes','','Las aprobadas se han cotejado con la identificación de su fuente y examinado visualmente. Esto no equivale a certificación especializada de especies crípticas. Los ejemplares parciales, moldes y secciones conservan su referencia de procedencia. Se han apartado fotos ambiguas, inventarios, cartelas con respuestas y duplicados detectados.','','El listado completo de huecos está en [image-audit.json](image-audit.json), campo `allMissingPairs`. En la app se puede consultar con **Catálogo → Estado → Falta completar la pareja**. Las decisiones por lote están en [image-review-log.json](image-review-log.json). Los casos de sinonimia o procedencia que requieren cuidado están en [taxon-review-rules.json](taxon-review-rules.json).','','Fuentes y autores de cada imagen: [curated-images.json](curated-images.json). Las fotografías aprobadas tienen copia local en `assets/reviewed`. Las candidatas no aprobadas no entran en el cuestionario.']
(DATA/'image-review-report.md').write_text('\n'.join(report)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in audit.items() if k not in ['allMissingPairs','reviewDefinition']},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
