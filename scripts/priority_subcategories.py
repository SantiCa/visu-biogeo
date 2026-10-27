from pathlib import Path
import json,urllib.parse
from collect_commons_html import collect,soup
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';path=DATA/'commons-extra-images.json';manifest=json.loads(path.read_text(encoding='utf8'))
roots={'hildoceras':'Hildoceras','paradoxides':'Paradoxides'}
for id,category in roots.items():
    source='https://commons.wikimedia.org/wiki/Category:'+category
    s=soup(source)
    categories=[]
    for a in s.select('#mw-subcategories a[href]'):
        name=a.get_text(' ',strip=True);href=a['href']
        if category.lower() in name.lower() and '/wiki/Category:' in href:categories.append(urllib.parse.unquote(href.split('Category:',1)[1]).replace('_',' '))
    if id=='paradoxides':categories.sort(key=lambda n:'fossils' not in n.lower())
    old=manifest.setdefault(id,{'images':[]})['images'];pages={im['page'] for im in old}
    for cat in categories[:3]:
        try:r=collect(cat,6)
        except Exception as e:print(cat,e,flush=True);continue
        old.extend(im for im in r['images'] if im['page'] not in pages);pages={im['page'] for im in old}
        tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(path)
        print(cat,len(r['images']),flush=True)
