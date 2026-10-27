"""Explicit decisions from source + visual review of tmp/image-review sheets.
This is NOT an automatic image classifier. Do not extend the allowlist without review.
"""
from pathlib import Path
import json,hashlib,shutil
import pymupdf
from PIL import Image
from review_images import download
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tmp/image-review';ASSETS=ROOT/'assets/reviewed';ASSETS.mkdir(parents=True,exist_ok=True)
target=ROOT/'data/curated-images.json'
curated=json.loads(target.read_text(encoding='utf8')) if target.exists() else {}
def add(id,im):
    im={**im,'status':'approved','reviewedAt':'2026-10-24','reviewMethod':'Fuente identificada y revisión visual; no peritaje taxonómico.'}
    arr=curated.setdefault(id,{'images':[]})['images']
    if not any(x.get('page')==im.get('page') and (x.get('originalUrl') or x['url'])==im['url'] for x in arr):arr.append(im)
def main():
    raw=(OUT/'picks.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='e1f08a91cf77e74eabcc5f15f573a301cb89e613c016761e1cac91b810b94504', 'Contact sheet changed: review it again, do not reuse indices.'
    picks=json.loads(raw)
    allowed=[0,1,2,4,9,11,12,17,18,19,23,32,35,37,38]
    for i in [15,16,36]:
        p=picks[i]
        for im in curated.get(p['itemId'],{}).get('images',[]):
            if (im.get('originalUrl') or im['url'])==p['image']['url']: im['status']='pending'
    for i in allowed:
        p=picks[i];add(p['itemId'],p['image'])
    doc=pymupdf.open(OUT/'hamburg-colour.pdf');page=doc[94]
    # Page visually checked: only specimen, excluding the caption and nearby map.
    page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=pymupdf.Rect(48,133,277,301)).save(ASSETS/'yellow-ochre-hamburg.png')
    add('ocre-amarillo',{'url':'./assets/reviewed/yellow-ochre-hamburg.png','page':'https://www.csmc.uni-hamburg.de/en/publications/mc/files/articles/mc16-complete','author':'Mineralogical Museum Hamburg / CSMC Universität Hamburg','license':'Recorte de publicación para la colección personal; no redistribuir sin revisar condiciones','reference':'Manuscript Cultures 16 · Colour Meets Map, p. 93 (PDF p. 95), fig. 2.4.3.3-1. Muestra 8 × 7 × 6 cm, valle superior del Lahn.','description':'Muestra natural de ocre amarillo, no pintura. Recorte limitado a la fotografía del ejemplar.'})
    add('empusa-pennata',{'url':'https://upload.wikimedia.org/wikipedia/commons/b/b7/Empusa_pennata_stehend.jpg','page':'https://commons.wikimedia.org/wiki/File:Empusa_pennata_stehend.jpg','author':'Daniel Ballmer','license':'CC BY-SA 4.0','licenseUrl':'https://creativecommons.org/licenses/by-sa/4.0/','description':'Adulto de Empusa pennata. Crevillent, España. Cono cefálico, patas raptoras y lóbulos de las patas visibles.'})
    add('empusa-pennata',{'url':'https://upload.wikimedia.org/wikipedia/commons/e/ea/Empusa_pennata-.jpg','page':'https://commons.wikimedia.org/wiki/File:Empusa_pennata-.jpg','author':'Luis Nunes Alberto','license':'CC BY-SA 3.0','licenseUrl':'https://creativecommons.org/licenses/by-sa/3.0/','description':'Ninfa de Empusa pennata. Abdomen curvado, cabeza cónica y expansiones foliáceas de las patas; fotografía completa.'})
    known={p['image']['url']:OUT/f'{i:03}.jpg' for i,p in enumerate(picks)}
    known['https://upload.wikimedia.org/wikipedia/commons/b/b7/Empusa_pennata_stehend.jpg']=OUT/'empusa-spain.jpg'
    known['https://upload.wikimedia.org/wikipedia/commons/e/ea/Empusa_pennata-.jpg']=OUT/'empusa-portugal.jpg'
    for entry in curated.values():
        for im in entry['images']:
            if im['status']=='approved' and im['url'].startswith('http'):
                name=hashlib.sha256(im['url'].encode()).hexdigest()[:16]+'.jpg'
                shutil.copyfile(known[im['url']],ASSETS/name)
                im['originalUrl']=im['url'];im['url']='./assets/reviewed/'+name
    target.write_text(json.dumps(curated,ensure_ascii=False,indent=2),encoding='utf8')
    print(len(curated),'entries approved')
if __name__=='__main__':main()
