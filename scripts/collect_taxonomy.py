"""Document family ranks from the exact taxon already resolved for photographs."""
from pathlib import Path
from urllib.parse import urlencode
import json,urllib.request,urllib.error,time,re
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';PATH=DATA/'taxonomy.json';CACHE=DATA/'taxonomy-source-cache.json'
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo/4 educational taxonomy catalogue'}),timeout=50) as r:return json.load(r)
def save(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(path)
def canon(name):return re.sub(r'\s+',' ',name.replace('×','x').lower()).strip()
def main():
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));manifest=json.loads((DATA/'inaturalist-images.json').read_text(encoding='utf8'))
    data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {};cache=json.loads(CACHE.read_text(encoding='utf8')) if CACHE.exists() else {}
    ids=sorted({str(x['taxonId']) for x in manifest.values() if x.get('taxonId') and str(x['taxonId']) not in cache})
    for start in range(0,len(ids),20):
        time.sleep(1.5)
        try:results=get('https://api.inaturalist.org/v1/taxa/'+','.join(ids[start:start+20]))['results']
        except Exception as error:print('Paused:',error,flush=True);break
        for t in results:
            families=[a for a in t.get('ancestors',[]) if a.get('rank')=='family']
            if t.get('rank')=='family':families=[t]
            if len(families)==1:cache[str(t['id'])]={'family':families[0]['name'],'familyTaxonId':families[0]['id'],'matchedName':t['name'],'source':'https://www.inaturalist.org/taxa/'+str(t['id']),'checkedAt':'2026-10-25'}
        save(CACHE,cache);print(min(start+20,len(ids)),'/',len(ids),'taxa checked',flush=True)
        for item in catalog:
            taxon=manifest.get(item['id'],{}).get('taxonId');family=cache.get(str(taxon))
            if family and item['kind']=='organismo' and item['id'] not in data:data[item['id']]={**family,'aliases':[]}
        save(PATH,data)
    # Exact GBIF matches fill gaps left by the photograph source, including fossils.
    for item in catalog:
        if item['kind'] not in ['organismo','fosil'] or item['id'] in data:continue
        time.sleep(1.5)
        try:
            t=get('https://api.gbif.org/v1/species/match?'+urlencode({'name':item['scientificName'],'strict':'true'}))
            accepted={canon(n) for n in [item['scientificName'],*item.get('aliases',[])]}
            if t.get('matchType')=='EXACT' and t.get('family') and canon(t.get('canonicalName','')) in accepted:
                data[item['id']]={'family':t['family'],'aliases':[],'matchedName':t['canonicalName'],'source':'https://www.gbif.org/species/'+str(t['usageKey']),'checkedAt':'2026-10-25'}
                if item['kind']=='fosil':data[item['id']].update(reviewStatus='pending',reviewReason='Pendiente de contraste paleontológico: comprobar homónimos, rango familiar y clasificaciones históricas antes de mostrarla en el cuestionario.')
                save(PATH,data)
            print(item['scientificName'],data.get(item['id'],{}).get('family','pending'),flush=True)
        except urllib.error.HTTPError as error:
            if error.code==429:print('Rate limit: stopped.',flush=True);break
            print(item['scientificName'],error,flush=True)
        except Exception as error:print(item['scientificName'],error,flush=True)
    print('Families documented:',len(data),flush=True)
if __name__=='__main__':main()
