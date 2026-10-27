"""Second targeted pass for unresolved priority pairs, avoiding previously seen URLs."""
from pathlib import Path
import json
from collect_commons_html import collect
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
categories={'Antracita':'Anthracite','Celestina':'Celestine','Glaucofana':'Glaucophane','Granodiorita':'Granodiorite','Grauvaca':'Greywacke','Hildoceras':'Hildoceras','Marga':'Marl','Ofita':'Ophite','Paradoxides':'Paradoxides','Pecten sp.':'Pecten','Silvina':'Sylvite','Sillimanita':'Sillimanite','Trípoli':'Diatomite'}
catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));cur=json.loads((DATA/'curated-images.json').read_text(encoding='utf8'))
path=DATA/'commons-extra-images.json';manifest=json.loads(path.read_text(encoding='utf8'))
for name,category in categories.items():
    item=next(x for x in catalog if x['scientificName']==name)
    if sum(im['status']=='approved' for im in cur.get(item['id'],{}).get('images',[]))>=2:continue
    try:r=collect(category,8)
    except Exception as e:print(name,str(e),flush=True);continue
    old=manifest.setdefault(item['id'],{'images':[]})['images'];pages={i['page'] for i in old}
    old.extend(im for im in r['images'] if im['page'] not in pages)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(path)
    print(name,len(old),flush=True)
