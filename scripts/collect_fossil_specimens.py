"""Museum fossil specimens via GBIF. Exact recorded taxon, no automatic approval."""
from pathlib import Path
from urllib.parse import urlencode
import urllib.request,json,re,time
from review_batch import identity
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/priority-additions.json'
CORRECTIONS={'Archaeopterix':'Archaeopteryx','Hiparion':'Hipparion','Parantrophus':'Paranthropus','Carcharocles':'Otodus','Paranthropus boisei':'Paranthropus boisei'}
def collect(item):
    name=CORRECTIONS.get(item['scientificName'],item['scientificName'])
    url='https://api.gbif.org/v1/occurrence/search?'+urlencode({'scientificName':name,'mediaType':'StillImage','basisOfRecord':'FOSSIL_SPECIMEN','limit':30})
    req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo educational specimen catalogue'})
    records=json.load(urllib.request.urlopen(req,timeout=40));images=[];seen=set()
    for rec in records['results']:
        recorded=rec.get('scientificName','');raw=rec.get('verbatim',{}).get('scientificName',recorded)
        if not re.match(r'^'+re.escape(name)+r'(?:\s|$)',recorded,re.I):continue
        if rec.get('basisOfRecord')!='FOSSIL_SPECIMEN':continue
        if len(name.split())>1 and (rec.get('identificationQualifier') or '?' in raw or ' cf.' in raw or ' aff.' in raw):continue
        for im in rec.get('media',[]):
            photo=im.get('identifier','');title=im.get('title','')
            if im.get('type')!='StillImage' or not photo.startswith('http') or photo in seen:continue
            if any(word in title.lower() for word in ['label','ledger','register','inventory book']) or 'label' in photo.lower():continue
            seen.add(photo)
            images.append({'url':photo,'key':photo,'page':'https://www.gbif.org/occurrence/'+str(rec['key']),'author':im.get('creator') or rec.get('institutionCode') or rec.get('datasetName','Museo de procedencia'),'license':im.get('license') or rec.get('license') or 'Consultar condiciones de la colección','sourceAlt':recorded+' · '+str(rec.get('catalogNumber','')),'description':title or recorded,'recordedName':recorded,'specimen':rec.get('catalogNumber'),'institution':rec.get('institutionCode'),'basisOfRecord':'FOSSIL_SPECIMEN','recordSource':rec.get('references'),'status':'pending'})
            if len(images)>=3:return images
    return images
def main():
    catalog=json.loads((ROOT/'data/species.json').read_text(encoding='utf8'));cur=json.loads((ROOT/'data/curated-images.json').read_text(encoding='utf8'));data=json.loads(PATH.read_text(encoding='utf8'))
    todo=[x for x in catalog if x['kind']=='fosil' and len({identity(im) for im in cur.get(x['id'],{}).get('images',[]) if im['status']=='approved'})<2 and not data.get(x['id'],{}).get('gbifChecked')]
    def safe(item):
        try:return item,collect(item),None
        except Exception as error:return item,[],str(error)
    for item in todo:
        time.sleep(1.5)
        item,images,error=safe(item)
        entry=data.setdefault(item['id'],{'images':[]});seen={im['url'] for im in entry['images']}
        entry['images'] += [im for im in images if im['url'] not in seen]
        entry.update(gbifChecked=not bool(error),gbifError=error)
        temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(PATH)
        print(item['scientificName'],len(images),error or '',flush=True)
        if error and '429' in error:
            print('Rate limit: stopped. Resume in a later session.',flush=True)
            break
if __name__=='__main__':main()
