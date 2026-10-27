from pathlib import Path
from urllib.parse import urljoin
import json,urllib.request
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];D=R/'data';OUT=R/'tmp/zero-cdc-oct26';OUT.mkdir(exist_ok=True)
def main():
 p=D/'priority-additions.json';data=json.loads(p.read_text(encoding='utf8'))
 for id,url,files in [('toxoplasma-gondii','https://www.cdc.gov/dpdx/toxoplasmosis/index.html',['T_gondii_tachy.jpg','T_gondii_cyst_brain.jpg','T_gondii_cyst_unstained.jpg']),('plasmodium-falciparum','https://www.cdc.gov/dpdx/malaria/index.html',['Pf_rings_thinA.jpg','Pf_rings_thinD.jpg','Pf_gametocyte_thinB.jpg'])]:
  with urllib.request.urlopen(url,timeout=40) as response:raw=response.read()
  s=BeautifulSoup(raw,'html.parser');images=[]
  for im in s.find_all('img'):
   src=urljoin(url,im.get('src',''));name=src.rsplit('/',1)[-1].split('?')[0]
   if name.lower() not in {n.lower() for n in files}:continue
   caption=im.find_parent('figure') or im.find_parent(class_='card');caption=caption.get_text(' ',strip=True) if caption else im.parent.get_text(' ',strip=True)
   images.append({'url':src,'key':src,'page':url,'author':'CDC / DPDx · créditos de cada figura en la fuente','license':'Condiciones de CDC/DPDx; referencia educativa conservada','description':caption or im.get('alt',name),'sourceAlt':im.get('alt',name),'status':'pending'})
  entry=data.setdefault(id,{'images':[]});seen={i['url'] for i in entry['images']};entry['images'] += [i for i in images if i['url'] not in seen];print(id,images,flush=True)
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
