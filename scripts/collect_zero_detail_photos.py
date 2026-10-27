from pathlib import Path
import json
from collect_inaturalist import get
D=Path(__file__).resolve().parents[1]/'data'
def main():
 p=D/'priority-additions.json';data=json.loads(p.read_text(encoding='utf8'));batch=json.loads((D.parent/'tmp/reviews/living-zero-observations-oct26/picks.json').read_text(encoding='utf8'));ids={'aphanius-baeticus','valencia-hispanica','androsace-rioxana','leptosiphonia-brodiei'}
 for id in ids:
  pages=list(dict.fromkeys(r['image']['page'] for r in batch if r['itemId']==id));seen={im.get('photoId') for im in data[id]['images']};added=0
  for page in pages:
   for rec in get('observations/'+page.rsplit('/',1)[-1]):
    for photo in rec.get('photos',[]):
     if photo['id'] in seen:continue
     if min(photo.get('original_dimensions',{}).values() or [0])<450:continue
     data[id]['images'].append({'url':photo['url'].replace('/square.','/large.'),'key':'inat-observation-photo-'+str(photo['id']),'page':page,'author':photo.get('attribution') or rec['user']['login'],'license':photo.get('license_code') or 'Todos los derechos reservados · colección personal','taxonName':rec['taxon']['name'],'photoId':photo['id'],'description':'Otra vista de la misma observación identificada; revisar encuadre y correspondencia.','status':'pending'});seen.add(photo['id']);added+=1
  print(id,added,'additional views',flush=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
