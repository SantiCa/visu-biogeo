"""Resolve exact Latin names with rank filters; stage only, never approve."""
from pathlib import Path
import json,sys
from collect_inaturalist import get,canonical,photos
R=Path(__file__).resolve().parents[1];D=R/'data';OUT=R/'tmp/exact-zero-next';OUT.mkdir(exist_ok=True)
load=lambda name:json.loads((D/name).read_text(encoding='utf8'))
cat={x['id']:x for x in load('species.json')};audit=load('image-audit.json');nat=load('inaturalist-images.json');rules=load('taxon-review-rules.json');p=D/'priority-additions.json';data=load(p.name)
skip={'arion-rufus','citrus-x-sinensis','discoglossus-jeanneae','podarcis-hispanicus','penicillium-chrysogenum','proteus-anguinus','taraxacum-officinarum'}
known={'pipa-pipa':25462,'lepiota-procera':63401,'platanus-hispanica':552449}
for row in audit['allMissingPairs']:
 id=row['id'];item=cat[id]
 if row['approvedImages'] or item['kind']!='organismo' or id in skip or rules.get(id,{}).get('blockedPhotoTaxa'):continue
 cache=OUT/(id+'.json')
 try:
  if cache.exists():result=json.loads(cache.read_text(encoding='utf8'))
  else:
   allowed={canonical(n) for n in [item['scientificName'],*item.get('aliases',[]),nat.get(id,{}).get('acceptedName','')]}
   if id in known:matches=get('taxa/'+str(known[id]))
   else:
    rows=get('taxa',{'q':item['scientificName'],'rank':'species,subspecies,hybrid','per_page':100,'is_active':'true'})
    exact=[t for t in rows if canonical(t['name']) in allowed]
    matches=get('taxa/'+str(exact[0]['id'])) if len({t['id'] for t in exact})==1 else []
   result=photos(matches[0]) if matches else {'images':[],'reason':'No unique exact-name match'}
   cache.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
  entry=data.setdefault(id,{'images':[]});seen={im.get('photoId') for im in entry['images']}
  for im in result['images']:
   if im['photoId'] not in seen:
    entry['images'].append({**im,'key':'inat-photo-'+str(im['photoId']),'reference':'Nombre exacto en ficha taxonómica; revisión de encuadre pendiente.'});seen.add(im['photoId'])
  p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(id,len(result['images']),'candidates',flush=True)
 except Exception as e:
  print(id,str(e),flush=True)
  if 'RATE_LIMIT' in str(e):break
