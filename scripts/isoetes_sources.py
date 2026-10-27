from pathlib import Path
import pymupdf
from review_images import download
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tmp/isoetes';OUT.mkdir(parents=True,exist_ok=True)
sources={
 'aragon':'https://www.conservacionvegetal.org/wp-content/uploads/publicaciones/Catalogo%20de%20especies%20amenazadas%20en%20Aragon.pdf',
 'flora-acuatica':'https://bibdigital.rjb.csic.es/medias/de/8d/6e/e0/de8d6ee0-a308-48e7-afd9-4cb883a336d5/files/CIR_Fl_Acu_Esp_Hidro_Vasc.pdf'
}
for name,url in sources.items():
    path=OUT/(name+'.pdf');download(url,path);doc=pymupdf.open(path)
    for i,page in enumerate(doc):
        t=page.get_text()
        if ('Isoetes velatum A. Braun subsp. velatum' in t and name=='aragon') or ('Figura 78.' in t and 'Isoetes' in t and name=='flora-acuatica'):
            page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(OUT/f'{name}-{i+1}.png')
            (OUT/f'{name}-{i+1}.txt').write_text(t,encoding='utf8')
            print(name,'PDF page',i+1,'dimensions',page.rect,flush=True)
