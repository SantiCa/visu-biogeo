"""Reviewed crop: the blue glaucophane-bearing specimen, excluding its label."""
from pathlib import Path
import json
from PIL import Image
from review_batch import cachepath
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'tmp/reviews/andalucia-extra-4/picks.json').read_text(encoding='utf8'))[19]
Image.open(cachepath(p['image']['url'])).crop((100,755,880,1155)).save(ROOT/'assets/reviewed/glaucophane-sonoma-crop.jpg',quality=94)
path=ROOT/'data/curated-images.json';cur=json.loads(path.read_text(encoding='utf8'))
im={**p['image'],'url':'./assets/reviewed/glaucophane-sonoma-crop.jpg','originalUrl':p['image']['url'],'status':'approved','reviewedAt':'2026-10-24','reference':'Recorte de la muestra azul 96, Sonoma County. Esquisto con glaucofana; no muestra de mineral puro. Se excluyen cartela y otra roca superior.','reviewMethod':'Fuente y muestra rotulada cotejadas; revisión visual del recorte'}
arr=cur.setdefault('glaucofana',{'images':[]})['images']
if not any(i['url']==im['url'] for i in arr):arr.append(im)
path.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
