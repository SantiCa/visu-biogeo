from pathlib import Path
import urllib.request,json,pymupdf
R=Path(__file__).resolve().parents[1];OUT=R/'tmp/zero-official-oct26';OUT.mkdir(exist_ok=True)
SOURCES={'androsace-rioxana-1':'https://www.larioja.org/larioja-client/cm/medio-ambiente/images?idMmedia=1546871','androsace-rioxana-2':'https://larioja.org/larioja-client/cm/medio-ambiente/images?idMmedia=1684544','fishes':'https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/2011_doadrio_et_al_seguimiento_ictiofauna_iberica_opt_tcm30-544759.pdf'}
def main():
 for name,url in SOURCES.items():
  p=OUT/(name+'.pdf')
  if not p.exists():
   try:
    with urllib.request.urlopen(url,timeout=65) as r:raw=r.read()
    assert raw.startswith(b'%PDF');p.write_bytes(raw)
   except Exception as e:print(name,str(e),flush=True);continue
  doc=pymupdf.open(p);pages=[(i,page) for i,page in enumerate(doc) if name!='fishes' or any(s in page.get_text() for s in ['Figura 561.','Figura 577.','Figura 578.'])]
  for i,page in pages:
   page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(OUT/(name+'-p'+str(i+1)+'.png'));print(name,'PDF page',i+1,'images',page.get_images(),flush=True)
if __name__=='__main__':main()
