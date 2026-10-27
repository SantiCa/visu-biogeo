"""Inspected museum specimens with answer labels outside the retained region."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/curated-images.json'
picks=json.loads((ROOT/'tmp/reviews/catalogo-museos-001/picks.json').read_text(encoding='utf8'));cur=json.loads(PATH.read_text(encoding='utf8'))
for n in [47,53,77]:
    p=picks[n];name='museum-specimen-'+str(n)+'-crop.jpg';shutil.copyfile(ROOT/'tmp/taxon-sources'/('crop-'+str(n)+'.jpg'),ROOT/'assets/reviewed'/name)
    im={**p['image'],'originalUrl':p['image']['url'],'url':'./assets/reviewed/'+name,'status':'approved','reviewedAt':'2026-10-24','reviewMethod':'Rótulo del ejemplar cotejado y recorte inspeccionado visualmente','reference':'Recorte del ejemplar para excluir la cartela identificativa; se conserva la referencia de la colección.'}
    arr=cur.setdefault(p['itemId'],{'images':[]})['images']
    # Replace rejection of the labelled full frame using its stable source key.
    existing=next((i for i,x in enumerate(arr) if (x.get('originalUrl') or x['url'])==p['image']['url']),None)
    if existing is None:arr.append(im)
    else:arr[existing]=im
curpath=PATH;curpath.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
