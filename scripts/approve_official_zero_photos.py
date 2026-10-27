from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'data';OUT=R/'tmp/zero-official-oct26'
FISH='https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/2011_doadrio_et_al_seguimiento_ictiofauna_iberica_opt_tcm30-544759.pdf'
RIOJA='https://www.larioja.org/larioja-client/cm/medio-ambiente/images?idMmedia=1546871'
def main():
 p=D/'curated-images.json';data=json.loads(p.read_text(encoding='utf8'));rows=json.loads((OUT/'extracted.json').read_text(encoding='utf8'));rows.append({'id':'aphanius-baeticus','file':str(OUT/'salinete-junta.jpg'),'figure':'Hembra y macho · fotografía de la ficha oficial','junta':True});added=0
 for row in rows:
  id=row['id'];src=Path(row['file']);filehash=hashlib.sha256(src.read_bytes()).hexdigest();dest=R/'assets/reviewed'/('official-'+filehash[:20]+src.suffix);shutil.copy2(src,dest)
  page='https://www.juntadeandalucia.es/medioambiente/portal/landing-page-%C3%ADndice/-/asset_publisher/zX2ouZa4r1Rf/content/aphanius-baeticus/20151' if row.get('junta') else RIOJA if id=='androsace-rioxana' else FISH
  im={'url':'./assets/reviewed/'+dest.name,'key':'official-zero-oct26-'+filehash,'page':page,'author':'Ricardo Zaldívar / Gobierno de La Rioja' if id=='androsace-rioxana' else 'Junta de Andalucía · autor indicado en la ficha' if row.get('junta') else 'I. Doadrio / MITECO','license':'© Autor / administración editora · recorte para colección personal de estudio','reference':row['figure']+(' · PDF p. '+str(row['pdfPage']) if row.get('pdfPage') else ''),'description':'Fotografía de '+id.replace('-',' ')+', identificada en la fuente oficial. Se conserva solo la imagen del ejemplar, sin la respuesta impresa.','status':'approved','reviewedAt':'2026-10-26','reviewMethod':'Página y pie identificativo revisados junto con la fotografía; extracción del objeto de imagen original, sin reconstrucción.'}
  arr=data.setdefault(id,{'images':[]})['images']
  if not any(x.get('key')==im['key'] for x in arr):arr.append(im);added+=1
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(added,'official specimen photographs approved')
if __name__=='__main__':main()
