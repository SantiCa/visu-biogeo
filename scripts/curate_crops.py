"""Explicit source-checked crops; rectangles exclude labels/other subjects."""
from pathlib import Path
import json,hashlib
import pymupdf
from PIL import Image
from review_batch import cachepath
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';ASSETS=ROOT/'assets/reviewed'
path=DATA/'curated-images.json';cur=json.loads(path.read_text(encoding='utf8'))
def add(id,im):
    im.update(status='approved',reviewedAt='2026-10-24',reviewMethod='Fuente identificada y revisión visual del recorte',reviewNote='Recorte excluye rótulos y conserva el ejemplar.')
    arr=cur.setdefault(id,{'images':[]})['images']
    if not any(x['url']==im['url'] for x in arr):arr.append(im)
def pdf_crop(id,file,pageno,rect,name,source,author,reference):
    doc=pymupdf.open(file);doc[pageno-1].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(rect)).save(ASSETS/name)
    add(id,{'url':'./assets/reviewed/'+name,'page':source,'author':author,'license':'Recorte de publicación para estudio personal · consultar condiciones del original','reference':reference})
pdf_crop('isoetes-velatum',ROOT/'tmp/isoetes/aragon.pdf',69,(35,40,547,566),'isoetes-aragon.png','https://www.conservacionvegetal.org/wp-content/uploads/publicaciones/Catalogo%20de%20especies%20amenazadas%20en%20Aragon.pdf','J. Benito / Catálogo de Especies Amenazadas en Aragón','Página impresa 68, PDF 69. Isoetes velatum subsp. velatum.')
pdf_crop('isoetes-velatum',ROOT/'tmp/isoetes/flora-acuatica.pdf',68,(239,108,397,242),'isoetes-flora-acuatica.png','https://bibdigital.rjb.csic.es/medias/de/8d/6e/e0/de8d6ee0-a308-48e7-afd9-4cb883a336d5/files/CIR_Fl_Acu_Esp_Hidro_Vasc.pdf','Santos Cirujano y colaboradores / Real Jardín Botánico, CSIC','Flora acuática española. Hidrófitos vasculares, p. 67 (PDF 68), fig. 78.')
picks=json.loads((ROOT/'tmp/reviews/andalucia-extra-4/picks.json').read_text(encoding='utf8'))
p=picks[14];im=Image.open(cachepath(p['image']['url']));w,h=im.size
im.crop((0,0,w,int(h*.79))).save(ASSETS/'celestine-museum-crop.jpg',quality=94)
add('celestina',{**p['image'],'url':'./assets/reviewed/celestine-museum-crop.jpg','originalUrl':p['image']['url'],'reference':'Recorte de la muestra del museo: se excluye la cartela inferior.'})
# A museum identification can still refer to fragments that do not make a useful quiz.
for im in cur.get('paradoxides',{}).get('images',[]):
    if '172296' in im.get('page',''):im.update(status='rejected',reviewNote='Fragmentos sin morfología completa para el reconocimiento visual.')
path.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
