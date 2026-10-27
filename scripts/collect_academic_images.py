"""Identified photographs from WMO and museum/teaching collections.
Collection only creates pending candidates. A visual review is still required.
"""
from pathlib import Path
from urllib.parse import urljoin
import urllib.request,json,re,time
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/priority-additions.json'
catalog=json.loads((ROOT/'data/species.json').read_text(encoding='utf8'))
data=json.loads(PATH.read_text(encoding='utf8'))
def page(url):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 VisuBioGeo educational catalogue'}),timeout=30).read(),'html.parser')
def add(item,url,source,author,description):
    arr=data.setdefault(item['id'],{'images':[]})['images']
    if any(im['url']==url for im in arr):return
    arr.append({'url':url,'key':url,'page':source,'author':author,'license':'Fuente identificada · consultar condiciones del original · colección personal','description':description,'sourceAlt':description,'status':'pending'})
def save():PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def exact(text,term):return bool(re.search(r'(?<![a-z])'+re.escape(term)+r'(?![a-z])',text,re.I))
def main():
    wmo='https://public.wmo.int/world-meteorological-day-2017/classifying-clouds'
    s=page(wmo)
    for heading in s.find_all('h4'):
        name=heading.get_text(' ',strip=True).split(' ')[0]
        item=next((i for i in catalog if i['kind']=='nube' and i['scientificName']==name),None)
        im=heading.find_next('img')
        if item and im:
            figure=im.find_parent('figure');credit=figure.get_text(' ',strip=True) if figure else 'World Meteorological Organization'
            add(item,urljoin(wmo,im['src']),wmo,credit,'WMO: '+heading.get_text(' ',strip=True)+'. '+im.get('alt',''))
    save()
    sources=[
      ('https://valsanagra.it/en/inventory/fossil-fern-6/','Museo Val Sanagra'),
      ('https://uwaterloo.ca/earth-sciences-museum/resources/history-life/carboniferous-period/pennsylvanian-sub-period/fern-fossils','Earth Sciences Museum, University of Waterloo'),
      ('https://www.digitalatlasofancientlife.org/learn/cnidaria/anthozoa/tabulata/','Paleontological Research Institution / Digital Atlas of Ancient Life'),
    ]
    for url,author in sources:
        try:
            s=page(url)
            for im in s.find_all('img'):
                alt=im.get('alt','');src=im.get('src','')
                if 'image_gallery_square' in src or not src:continue
                for item in catalog:
                    if item['kind']=='fosil' and exact(alt,item['scientificName']):add(item,urljoin(url,src),url,author,alt)
            save();print(url,'collected',flush=True)
        except Exception as error:print(url,str(error),flush=True)
    seed='https://geovirtual2.cl/Museovirtual/0633a1ge.htm';s=page(seed)
    pages={seed}
    for a in s.find_all('a',href=True):
        if any(i['kind']=='fosil' and exact(a.get_text(' ',strip=True),i['scientificName']) for i in catalog):
            link=urljoin(seed,a['href'])
            if link.startswith('https://geovirtual2.cl/') and '.htm' in link:pages.add(link)
    for url in sorted(pages):
        try:
            s=page(url)
            for im in s.find_all('img'):
                alt=im.get('alt','');src=im.get('src','')
                if not src or not ('Fotos/' in src or 'fotos/' in src):continue
                for item in catalog:
                    if item['kind']=='fosil' and exact(alt,item['scientificName']):add(item,urljoin(url,src),url,'Wolfgang Griem / Museo Virtual Geovirtual2',alt)
            save();print(url,'collected',flush=True);time.sleep(.8)
        except Exception as error:print(url,str(error),flush=True)
    print('Collection finished; candidates remain pending.',flush=True)
if __name__=='__main__':main()
