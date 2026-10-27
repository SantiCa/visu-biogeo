"""Stage identified NPS cave photographs; a separate visual review approves them."""
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json, re, urllib.request
R=Path(__file__).resolve().parents[1]; OUT=R/'tmp/nps-zero-oct26'
targets={'columna':["Wizard's Staff"], 'estalactitas-excentricas-helictitas':['Helictites'],
         'cueva-o-caverna':['Big Sky','Cave pool']}
p=R/'data/priority-additions.json'; data=json.loads(p.read_text(encoding='utf8'))
rows=json.loads((OUT/'gallery-lechuguilla.json').read_text(encoding='utf8'))
for id,titles in targets.items():
 for row in rows:
  if row['title'] not in titles: continue
  asset=row['src'].split('/GetAsset/')[1].split('/')[0]
  page='https://npgallery.nps.gov/AssetDetail/'+asset; cache=OUT/(asset+'.html')
  if not cache.exists(): cache.write_bytes(urllib.request.urlopen(page,timeout=40).read())
  soup=BeautifulSoup(cache.read_bytes(),'html.parser'); text=soup.get_text(' ',strip=True)
  link=next((a['href'] for a in soup.select('a[href]') if re.search(r'/proxymdres\.(?:jpg|png)',a['href'],re.I)),None) or next((a['href'] for a in soup.select('a[href]') if re.search(r'/original\.(?:jpg|png)',a['href'],re.I)),None)
  if not link: raise ValueError('No downloadable source rendition: '+asset)
  author=re.search(r'PhotoCredit:\s*(.*?)\s*(?:Constraints Information:|Keywords:)',text)
  image={'url':urljoin(page,link),'key':'nps-asset-'+asset,'page':page,
    'author':author.group(1) if author else 'National Park Service · crédito en la fuente',
    'license':'Dominio público · NPS (según registro de la fotografía)' if 'Public domain:Full Granting Rights' in text else 'Consultar condiciones del registro NPS; colección de estudio',
    'reference':row['title'],'description':row['alt'],'status':'pending'}
  images=data.setdefault(id,{'images':[]})['images']
  if not any(i.get('key')==image['key'] for i in images): images.append(image)
  print(id,row['title'])
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
