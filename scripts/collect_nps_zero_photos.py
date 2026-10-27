from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json,urllib.request,time
R=Path(__file__).resolve().parents[1];D=R/'data';OUT=R/'tmp/nps-zero-oct26';OUT.mkdir(exist_ok=True)
SERIES='https://www.nps.gov/articles/series.htm?id=F6B94C83-1DD8-B71B-0B7447F900839E48'
def fetch(url,name):
 p=OUT/(name+'.html')
 if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=40).read());time.sleep(.4)
 return BeautifulSoup(p.read_bytes(),'html.parser')
def main():
 data=json.loads((D/'priority-additions.json').read_text(encoding='utf8'));index=json.loads((OUT/'index.json').read_text(encoding='utf8'))
 soup=fetch(SERIES,'glacier-series')
 for i,a in enumerate(soup.select('a[href]')):
  title=a.get_text(' ',strip=True)
  if not title.startswith('Article '):continue
  url=urljoin(SERIES,a['href']);name='glacial-'+str(i);s=fetch(url,name);images=[]
  for im in s.select('figure img'):
   parent=im.find_parent('figure');images.append({'src':im.get('src'),'alt':im.get('alt'),'context':parent.get_text(' ',strip=True)})
  index[name]={'url':url,'title':title,'images':images};print(title,len(images),flush=True)
 url='https://www.nps.gov/media/photo/gallery-item.htm?gid=915CCD1D-B609-4C34-9364-0B3F83301C66&id=d4ea1d99-8052-4354-8b62-0a77b3863a76'
 s=fetch(url,'mcdonald-peaks');index['mcdonald-peaks']={'url':url,'images':[{'src':i.get('src'),'alt':i.get('alt'),'context':(i.find_parent('figure') or i.parent.parent).get_text(' ',strip=True)} for i in s.select('img') if 'glacier' in str(i).lower() or 'image' in str(i.get('src','')).lower()]}
 (OUT/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
 print('Glacial photo contexts:',json.dumps({k:v for k,v in index.items() if k.startswith('glacial-') and k!='glacial-gallery'},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
