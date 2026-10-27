import json,pymupdf,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];OUT=R/'tmp/zero-official-oct26'
def main():
 rows=[]
 for file,id,page,xrefs,figures in [('androsace-rioxana-1','androsace-rioxana',1,[28],['Fotografía de Ricardo Zaldívar']),('fishes','aphanius-baeticus',473,[1565],['Figura 561 · hembra']),('fishes','valencia-hispanica',485,[1605,1606],['Figura 577 · macho','Figura 578 · hembra']),('fishes','parachondrostoma-arrigonis',337,[1055,1056],['Figura 336','Figura 337'])]:
  doc=pymupdf.open(OUT/(file+'.pdf'))
  for xref,figure in zip(xrefs,figures):
   im=doc.extract_image(xref);dest=OUT/(id+'-'+str(xref)+'.'+im['ext']);dest.write_bytes(im['image']);rows.append({'id':id,'file':str(dest),'pdfPage':page,'figure':figure});print(str(dest),flush=True)
 (OUT/'extracted.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
 url='https://www.juntadeandalucia.es/medioambiente/portal/landing-page-%C3%ADndice/-/asset_publisher/zX2ouZa4r1Rf/content/aphanius-baeticus/20151'
 try:
  s=BeautifulSoup(urllib.request.urlopen(url,timeout=40).read(),'html.parser');photos=[{'src':i.get('src'),'alt':i.get('alt')} for i in s.find_all('img') if 'baeticus' in str(i).lower() or 'salinete' in str(i).lower()];(OUT/'junta-images.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2),encoding='utf8');print(photos,flush=True)
 except Exception as e:print('Junta source:',str(e),flush=True)
if __name__=='__main__':main()
