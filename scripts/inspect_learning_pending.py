from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parents[1];D=R/'data'
load=lambda p:json.loads((D/p).read_text(encoding='utf8'))
catalog=load('species.json');cur=load('curated-images.json');audit=load('image-audit.json');notes=load('study-notes.json');tax=load('learning-taxonomy.json')
print('Missing notes priorities',[(i['id'],i['scientificName']) for i in catalog if i['id'] in {e['itemId'] for e in load('andalucia-priority.json')['events']} and not notes.get(i['id'],{}).get('description')])
for source in ['asturnatura-images.json','inaturalist-images.json','priority-additions.json','teaching-images.json']:
 data=load(source);rows=[]
 for item in catalog:
  approved=[im for im in cur.get(item['id'],{}).get('images',[]) if im['status']=='approved'];decided={im.get('originalUrl') or im['url'] for im in cur.get(item['id'],{}).get('images',[]) if im['status'] in ['approved','rejected']}
  candidates=[im for im in data.get(item['id'],{}).get('images',[]) if im['url'] not in decided]
  if not approved and candidates:rows.append((item['id'],len(candidates)))
 print(source,'zero-photo candidates',len(rows),rows[:24])
print('Missing phylum',[(i['id'],i['scientificName'],tax.get(i['id'],{}).get('ranks')) for i in catalog if i['id'] in load('learning-taxonomy-audit.json')['pendingIds']])
