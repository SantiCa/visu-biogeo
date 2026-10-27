"""Exact-name fallback lookups; retain source ranks and never resolve homonyms by guess."""
from pathlib import Path
import json,urllib.parse,time
from collections import Counter
from build_learning_taxonomy import get,save,canonical,CACHE,D,DAY

def main():
 data=json.loads((D/'learning-taxonomy.json').read_text(encoding='utf8'));catalog=json.loads((D/'species.json').read_text(encoding='utf8'));items={x['id']:x for x in catalog};old=json.loads((D/'taxonomy.json').read_text(encoding='utf8'))
 # Unambiguous family records provide their own explicit, named higher ranks.
 for id,record in data.items():
  if record.get('ranks',{}).get('phylum'):continue
  family=record.get('ranks',{}).get('family');references=[r for r in data.values() if r.get('ranks',{}).get('family')==family and family and r['ranks'].get('phylum')]
  ranksets={tuple((k,r['ranks'].get(k)) for k in ['kingdom','phylum','class','order','family']) for r in references}
  if len(ranksets)==1:
   ranks={k:v for k,v in next(iter(ranksets)) if v};record['ranks']={**ranks,**record.get('ranks',{})};record['hierarchy']=[{'rank':k,'name':v} for k,v in record['ranks'].items()];record['higherRankSource']=references[0]['source'];record['reviewNote']='Rangos superiores documentados mediante la familia; identificación terminal pendiente.'
 # PBDB is primarily useful for fossils, with an explicit paleo-plant kingdom guard.
 fields={'kingdom':'kgn','phylum':'phl','class':'cll','order':'odl','family':'fml','genus':'gnl'}
 plants={'Annularia','Calamites','Sigillaria'}
 for item in catalog:
  id=item['id'];record=data.get(id)
  if not record or record.get('ranks',{}).get('phylum') or item['kind']!='fosil':continue
  name=item['scientificName'].replace(' sp.','').strip();p=CACHE/('pbdb-'+id+'.json')
  try:
   if not p.exists():save(p,get('https://paleobiodb.org/data1.2/taxa/list.json?'+urllib.parse.urlencode({'name':name,'show':'class','vocab':'pbdb'})));time.sleep(.6)
   raw=json.loads(p.read_text(encoding='utf8'));rows=raw.get('records',[]);rows=[r for r in rows if canonical(r.get('taxon_name',''))==canonical(name)]
   if name in plants:rows=[r for r in rows if r.get('kingdom')=='Plantae']
   signatures={tuple(r.get(k) for k in ['kingdom','phylum','class','order','family','genus']) for r in rows}
   if len(signatures)!=1 or not rows:continue
   row=rows[0];ranks={k:row[k] for k in fields if row.get(k)}
   if not ranks.get('phylum'):continue
   rank=row.get('taxon_rank','').lower();ranks[rank]=row['taxon_name']
   data[id]={**record,'provider':'Paleobiology Database','source':'https://paleobiodb.org/classic/basicTaxonInfo?taxon_no='+str(row['taxon_no']),'matchedName':row['taxon_name'],'rank':rank,'ranks':ranks,'hierarchy':[{'rank':k,'name':v} for k,v in ranks.items()],'status':'documented','checkedAt':DAY}
   print('Documented fossil',id,flush=True)
  except Exception as e:print('Pending',id,str(e),flush=True)
 save(D/'learning-taxonomy.json',data)
 bio=[x for x in catalog if x['kind'] in ['organismo','fosil']];report={'date':DAY,'biologicalEntries':len(bio),'rankedPhyla':sum(bool(data[x['id']]['ranks'].get('phylum')) for x in bio),'commonNames':sum(bool(data[x['id']].get('commonName')) for x in bio),'pendingIds':[x['id'] for x in bio if not data[x['id']]['ranks'].get('phylum')]};save(D/'learning-taxonomy-audit.json',report);print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
