"""Exact recorded taxa from research-grade observations, without locality data.

Only produces candidates. Sensitive/cryptic review rules are respected and no
photo is approved without a subsequent visual and source review.
"""
from pathlib import Path
import json,time,urllib.parse
from collect_inaturalist import get,canonical
R=Path(__file__).resolve().parents[1];D=R/'data'
def main():
 load=lambda n:json.loads((D/n).read_text(encoding='utf8'))
 catalog=load('species.json');cur=load('curated-images.json');nat=load('inaturalist-images.json');rules=load('taxon-review-rules.json');target=D/'priority-additions.json';data=load(target.name)
 for item in catalog:
  id=item['id'];taxon=nat.get(id,{}).get('taxonId')
  if item['kind']!='organismo' or not taxon or any(im['status']=='approved' for im in cur.get(id,{}).get('images',[])) or data.get(id,{}).get('zeroObservationChecked'):continue
  if rules.get(id,{}).get('blockedPhotoTaxa') or id in ['podarcis-hispanicus','discoglossus-jeanneae','citrus-x-sinensis']:continue
  allowed={canonical(n) for n in [item['scientificName'],*item.get('aliases',[]),nat[id].get('acceptedName','')]};images=[]
  try:
   records=get('observations',{'taxon_id':taxon,'quality_grade':'research','photos':'true','per_page':12,'order_by':'votes','locale':'es'})
   observers=set()
   for record in records:
    t=record.get('taxon',{});name=t.get('name','')
    if canonical(name) not in allowed or record.get('quality_grade')!='research' or record.get('captive'):continue
    observer=record.get('user',{}).get('login')
    if observer in observers:continue
    for p in record.get('photos',[]):
     dimensions=p.get('original_dimensions',{})
     if min(dimensions.values() or [0])<450:continue
     url=p.get('url','').replace('/square.','/large.')
     if not url.startswith('https://'):continue
     images.append({'url':url,'key':'inat-observation-photo-'+str(p['id']),'page':'https://www.inaturalist.org/observations/'+str(record['id']),'author':p.get('attribution') or observer,'license':p.get('license_code') or 'Todos los derechos reservados · colección de estudio personal','taxonName':name,'taxonId':t.get('id'),'photoId':p['id'],'description':'Ejemplar identificado como '+name+' en observación de grado de investigación. Pendiente de revisión visual y de correspondencia.','status':'pending'});observers.add(observer);break
    if len(images)>=3:break
   entry=data.setdefault(id,{'images':[]});seen={im['url'] for im in entry['images']};entry['images'] += [im for im in images if im['url'] not in seen];entry['zeroObservationChecked']=True;target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(id,len(images),'candidates',flush=True)
  except Exception as e:
   print(id,str(e),flush=True)
   if 'RATE_LIMIT' in str(e):break
if __name__=='__main__':main()
