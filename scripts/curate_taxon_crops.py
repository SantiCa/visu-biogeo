"""Explicitly identified book photographs, after visual inspection of each crop."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/curated-images.json'
cur=json.loads(PATH.read_text(encoding='utf8'))
specs=[
 ('pyrenaearia-velascoi','pyrenaearia','https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/Pyrenaearia_velascoi_tcm30-198464.pdf','Arantzazu Elejalde / Atlas y Libro Rojo de los Invertebrados Amenazados de España','Página impresa 928, PDF 1. Tres vistas de la misma concha; se cuenta como una imagen.'),
 ('podarcis-atrata','podarcis','https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/reptil_39_tcm30-98944.pdf','L. J. Barbadillo / Atlas y Libro Rojo de los Anfibios y Reptiles de España','Página impresa 238, PDF 1. Macho, Islas Columbretes. Recorte excluye título y mapa.'),
 ('podarcis-atrata','podarcis-gva','https://parquesnaturales.gva.es/documents/80302789/174100595/Folleto%2BGVA%2BColumbretesCast.pdf/ac63b362-f4b5-4511-aef4-adec83a5424c','B. Albiach Galán / Generalitat Valenciana','Folleto del parque natural de las Islas Columbretes, PDF 8. Foto identificada como Podarcis atrata. Recorte excluye pie con respuesta y conserva crédito.'),
]
for item,name,source,author,reference in specs:
    filename=name+'-source-crop.png';shutil.copyfile(ROOT/'tmp/taxon-sources'/(name+'-crop.png'),ROOT/'assets/reviewed'/filename)
    im={'url':'./assets/reviewed/'+filename,'page':source,'author':author,'license':'Recorte de publicación para estudio personal · consultar condiciones del original','reference':reference,'status':'approved','reviewedAt':'2026-10-24','reviewMethod':'Página y determinación de la fuente cotejadas; recorte inspeccionado visualmente'}
    arr=cur.setdefault(item,{'images':[]})['images']
    if not any(x['url']==im['url'] for x in arr):arr.append(im)
PATH.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
