"""Fallback to ordinary exact Commons category pages, with pacing.
No API retries against a rate limit; stop immediately on 429.
Reads specimen file descriptions and keeps everything pending visual review.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json,urllib.request,urllib.parse,urllib.error,time,re
from collect_images import mapping
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';PATH=DATA/'commons-extra-images.json'
def soup(url):
    time.sleep(1.2)
    req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo educational specimen-source review'})
    with urllib.request.urlopen(req,timeout=35) as r:return BeautifulSoup(r.read(),'html.parser')
def text(s):return s.get_text(' ',strip=True) if s else ''
def collect(category,limit=4):
    source='https://commons.wikimedia.org/wiki/Category:'+urllib.parse.quote(category.replace(' ','_'))
    s=soup(source);files=[]
    for box in s.select('.gallerybox'):
        a=box.select_one('.gallerytext a');img=box.select_one('img')
        if not a or not img:continue
        title=a.get('title') or text(a);page=urllib.parse.urljoin(source,a['href'])
        if re.search(r'painting|pigment|map|chart|drawing|structure|diagram|stamp|postage|building|museum.*0|scheme|logo|thin.section|plan--|railroad|coal.pockets|axon|triangle|SEM|plate|sch[eé]ma|insect',title,re.I):continue
        if not re.search(r'\.(jpg|jpeg|png)$',title,re.I):continue
        files.append((title,page))
    files.sort(key=lambda t:(not re.match(r'File:'+re.escape(category)+r'[ _(-]',t[0],re.I),len(t[0])))
    images=[]
    for title,page in files[:max(8,limit)]:
        p=soup(page);a=p.select_one('.fullMedia a') or p.select_one('.fullImageLink a')
        if not a:continue
        preview=p.select_one('.fullImageLink img')
        src=urllib.parse.urljoin(page,preview['src'] if preview and preview.get('src') else a.get('href',''));author=p.select_one('#fileinfotpl_aut+td')
        desc=p.select_one('#fileinfotpl_desc+td') or p.select_one('.description')
        licences=[text(t) for t in p.select('.licensetpl_short')]
        artist=text(author)[:200] or 'Créditos en Wikimedia Commons'
        description=text(desc)[:800]
        images.append({'url':src,'page':page,'key':src,'title':title,'author':artist,'license':' / '.join(licences) or 'Consultar licencia en fuente','description':description,'category':category,'status':'pending'})
        if len(images)>=limit:break
    return {'images':images,'status':'pending' if images else 'needs-source','source':source}
def main():
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));hist=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'));cur=json.loads((DATA/'curated-images.json').read_text(encoding='utf8'))
    priority={e['itemId'] for e in hist['events']};manifest=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    extra={'Paradoxides':'Paradoxides','Hildoceras':'Hildoceras','Ofita':'Ophite','Trípoli':'Diatomite','Marga':'Marl','Silvina':'Sylvite','Sienita':'Syenite','Sillimanita':'Sillimanite','Glaucofana':'Glaucophane','Celestina':'Celestine','Arcosa':'Arkose','Antracita':'Anthracite','Grauvaca':'Greywacke','Granodiorita':'Granodiorite','Trivia sp.':'Trivia (genus)','Isoetes velatum':'Isoetes velatum'}
    todo=[x for x in catalog if x['id'] in priority and sum(im['status']=='approved' for im in cur.get(x['id'],{}).get('images',[]))<2 and x['id'] not in manifest]
    for x in todo:
        category=extra.get(x['scientificName']) or mapping.get(x['scientificName']) or x['scientificName'].replace(' sp.','')
        try:result=collect(category)
        except Exception as e:
            result={'status':'error','images':[],'error':str(e)}
            if isinstance(e,urllib.error.HTTPError) and e.code==429:print('Rate limit: stopped.',flush=True);break
        manifest[x['id']]=result;temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(PATH)
        print(x['scientificName'],len(result['images']),flush=True)
if __name__=='__main__':main()
