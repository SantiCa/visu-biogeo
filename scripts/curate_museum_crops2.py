"""Second batch: inspected crops retain the fossils and remove answer labels."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/curated-images.json'
picks=json.loads((ROOT/'tmp/reviews/catalogo-museos-002/picks.json').read_text(encoding='utf8'));cur=json.loads(PATH.read_text(encoding='utf8'))
for n in [18,19,30,32,47]:
    p=picks[n];name='museum2-specimen-'+str(n)+'-crop.jpg';shutil.copyfile(ROOT/'tmp/taxon-sources'/('crop2-'+str(n)+'.jpg'),ROOT/'assets/reviewed'/name)
    im={**p['image'],'originalUrl':p['image']['url'],'url':'./assets/reviewed/'+name,'status':'approved','reviewedAt':'2026-10-24','reviewMethod':'Determinación del ejemplar cotejada y recorte inspeccionado visualmente','reference':'Recorte de la fotografía del ejemplar o grupo de ejemplares; se excluye la cartela con la respuesta.'}
    arr=cur.setdefault(p['itemId'],{'images':[]})['images'];existing=next((i for i,x in enumerate(arr) if (x.get('originalUrl') or x['url'])==p['image']['url']),None)
    if existing is None:arr.append(im)
    else:arr[existing]=im
# The photographed mammoth molar has a species-level determination in the
# source record. It also represents the separate species entry from the PDF.
source=next(im for im in cur['mammuthus']['images'] if im['status']=='approved' and im.get('recordedName','').startswith('Mammuthus primigenius'))
arr=cur.setdefault('mammuthus-primigenius',{'images':[]})['images']
if not any(x['url']==source['url'] for x in arr):arr.append({**source,'reference':'Molar determinado como Mammuthus primigenius en el registro de la colección. También representa la entrada de género Mammuthus.'})
PATH.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
