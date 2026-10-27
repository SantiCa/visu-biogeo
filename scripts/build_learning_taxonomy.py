"""Ranked, source-backed study taxonomy and Spanish vernaculars.

Ranks come from explicit API ranks, never guessed positions in a lineage.
The compact, resumable cache is local; only referenced factual fields ship.
"""
from pathlib import Path
from datetime import date
import json,re,time,urllib.request,urllib.parse,urllib.error,unicodedata
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';CACHE=ROOT/'tmp/learning-taxonomy';CACHE.mkdir(exist_ok=True)
DAY=date.today().isoformat()
RANKS={'kingdom','phylum','subphylum','superclass','class','subclass','infraclass','superorder','order','suborder','infraorder','superfamily','family','subfamily','tribe','genus','subgenus','species','subspecies','variety'}
def load(name):return json.loads((D/name).read_text(encoding='utf8'))
def save(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(path)
def canonical(name):
    value=''.join(c for c in unicodedata.normalize('NFD',name.casefold()) if not unicodedata.combining(c))
    return re.sub(r'\s+sp\.?$','',value.replace('×','x')).strip()
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo educational taxonomy / exact source records'}),timeout=55) as response:return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code==429:raise RuntimeError('Source rate limit; resume later') from error
            if error.code==404:return {}
            if attempt==2:raise
        time.sleep(2*(attempt+1))
def slim(t):
    return {k:t[k] for k in ['id','name','rank','is_active','iconic_taxon_name','preferred_common_name','english_common_name','extinct'] if k in t}|{
      'names':[{k:n[k] for k in ['name','locale','lexicon','is_valid'] if k in n} for n in t.get('names',[])],
      'ancestors':[{k:a[k] for k in ['id','name','rank'] if k in a} for a in t.get('ancestors',[])]}
def main():
    catalog=load('species.json');photos=load('inaturalist-images.json');old=load('taxonomy.json');notes=load('study-notes.json');rules=load('taxon-review-rules.json');output={}
    ids=sorted({int(photos[x['id']]['taxonId']) for x in catalog if x['kind']=='organismo' and photos.get(x['id'],{}).get('taxonId')})
    missing=[id for id in ids if not (CACHE/(str(id)+'.json')).exists()]
    for start in range(0,len(missing),20):
        batch=missing[start:start+20]
        try:
            result=get('https://api.inaturalist.org/v1/taxa/'+','.join(map(str,batch))+'?locale=es&all_names=true')
            for record in result.get('results',[]):save(CACHE/(str(record['id'])+'.json'),slim(record))
            print(min(start+20,len(missing)),'/',len(missing),'taxa fetched',flush=True);time.sleep(1.1)
        except Exception as error:print('Collection paused:',str(error),flush=True);break
    from collect_classification import group
    for item in catalog:
        if item['kind'] not in ['organismo','fosil']:continue
        id=item['id'];source=photos.get(id,{});path=CACHE/(str(source.get('taxonId'))+'.json');record=None
        if path.exists():
            t=json.loads(path.read_text(encoding='utf8'));blocked={canonical(n) for n in rules.get(id,{}).get('blockedPhotoTaxa',[])}
            if t.get('is_active',True) and canonical(t['name']) not in blocked:
                hierarchy=[{'rank':a['rank'],'name':a['name'],'taxonId':a['id']} for a in t['ancestors'] if a.get('rank') in RANKS]
                if t['rank'] in RANKS:hierarchy.append({'rank':t['rank'],'name':t['name'],'taxonId':t['id']})
                spanish=[n['name'] for n in t.get('names',[]) if n.get('locale')=='es' and n.get('is_valid',True)]
                record={'provider':'iNaturalist','source':'https://www.inaturalist.org/taxa/'+str(t['id']),'matchedName':t['name'],'rank':t['rank'],'hierarchy':hierarchy,'ranks':{a['rank']:a['name'] for a in hierarchy},'commonNames':list(dict.fromkeys(spanish)),'commonName':notes.get(id,{}).get('commonName') or next(iter(spanish),None),'group':group([a['name'] for a in hierarchy]),'checkedAt':DAY}
        if not record:
            reference=old.get(id,{});gbif_key=reference.get('source','').rsplit('/',1)[-1] if 'gbif.org/species/' in reference.get('source','') else None
            key=gbif_key or re.sub('[^a-z0-9]+','-',canonical(item['scientificName']));p=CACHE/('gbif-'+key+'.json')
            try:
                if not p.exists():
                    if gbif_key:t=get('https://api.gbif.org/v1/species/'+gbif_key)
                    else:t=get('https://api.gbif.org/v1/species/match?'+urllib.parse.urlencode({'name':re.sub(r'\s+sp\.?$','',item['scientificName']),'strict':'true'}))
                    save(p,t);time.sleep(.3)
                else:t=json.loads(p.read_text(encoding='utf8'))
                names={canonical(n) for n in [item['scientificName'],*item.get('aliases',[])]}
                if canonical(t.get('canonicalName','')) in names and t.get('kingdom'):
                    # Fossil plant homonyms need a declared kingdom; never use an animal Annularia.
                    plant_genera={'Annularia','Calamites','Pecopteris','Neuropteris','Alethopteris','Lepidodendron','Sigillaria','Asterophyllites','Lepidostrobus','Sphenopteris'}
                    if item['scientificName'].split()[0] in plant_genera and t['kingdom']!='Plantae':raise ValueError('Fossil plant homonym needs review')
                    ranks={k:t[k] for k in ['kingdom','phylum','class','order','family','genus'] if t.get(k)}
                    rank=t.get('rank','').lower()
                    if rank in ['species','subspecies','variety']:ranks[rank]=t['canonicalName']
                    key=t.get('usageKey') or t.get('key');source='https://www.gbif.org/species/'+str(key)
                    record={'provider':'GBIF','source':source,'matchedName':t['canonicalName'],'rank':rank,'ranks':ranks,'hierarchy':[{'rank':r,'name':n} for r,n in ranks.items()],'commonName':notes.get(id,{}).get('commonName'),'commonNames':[],'group':group(list(ranks.values())),'checkedAt':DAY}
            except Exception as error:print('Needs review',id,str(error),flush=True)
        if not record:
            record={'provider':None,'source':old.get(id,{}).get('source'),'ranks':{'family':old[id]['family']} if old.get(id,{}).get('family') and old[id].get('reviewStatus')!='pending' else {},'hierarchy':[],'commonName':notes.get(id,{}).get('commonName'),'commonNames':[],'checkedAt':DAY,'status':'pending','reviewNote':'No hay una correspondencia taxonómica inequívoca en las fuentes consultadas.'}
        record['commonNameStatus']='documented' if record.get('commonName') else 'not-documented'
        output[id]=record
    # Anatomical remains inherit only a taxon with an exact, documented parent name.
    for item in catalog:
        if not item.get('parentTaxon'):continue
        parent=canonical(item['parentTaxon']);matches=[x for x in catalog if x['kind']=='organismo' and parent in {canonical(n) for n in [x['scientificName'],*x.get('aliases',[])]}]
        records=[output[x['id']] for x in matches if output.get(x['id'],{}).get('ranks',{}).get('phylum')]
        if len(records)==1:output[item['id']]={**records[0],'subjectType':'anatomical-part','parentTaxon':item['parentTaxon'],'commonName':record_name(notes,item,records[0]),'commonNames':[]}
    save(D/'learning-taxonomy.json',output)
    report={'date':DAY,'biologicalEntries':sum(x['kind'] in ['organismo','fosil'] for x in catalog),'rankedPhyla':sum(bool(output[x['id']]['ranks'].get('phylum')) for x in catalog if x['kind'] in ['organismo','fosil']),'commonNames':sum(bool(output[x['id']].get('commonName')) for x in catalog if x['kind'] in ['organismo','fosil']),'pendingIds':[id for id,r in output.items() if r.get('status')=='pending']}
    save(D/'learning-taxonomy-audit.json',report);print(json.dumps(report,ensure_ascii=False),flush=True)
def record_name(notes,item,parent):return notes.get(item['id'],{}).get('commonName') or (('Resto de '+parent['commonName']) if parent.get('commonName') else None)
if __name__=='__main__':main()
