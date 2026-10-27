import json,time,urllib.parse
from build_learning_taxonomy import get,save,CACHE,D,DAY

def main():
 t=json.loads((D/'learning-taxonomy.json').read_text(encoding='utf8'))
 for id,division in [('calamites','Pteridophyta'),('sigillaria','Lycophyta')]:
  row=json.loads((CACHE/('pbdb-'+id+'.json')).read_text(encoding='utf8'))['records'][0]
  assert row['taxon_name'].lower()==id and row['phylum']==division
  ranks={k:row[k] for k in ['phylum','class','order','family','genus'] if row.get(k) and not row[k].startswith('NO_')};ranks={'kingdom':'Plantae',**ranks}
  t[id].update(provider='Paleobiology Database',source='https://paleobiodb.org/classic/basicTaxonInfo?taxon_no='+row['taxon_no'],ranks=ranks,hierarchy=[{'rank':k,'name':v} for k,v in ranks.items()],matchedName=row['taxon_name'],rank='genus',status='documented')
 for id in ['isoetes-velatum']:
  p=CACHE/'gbif-family-Isoetaceae.json'
  if not p.exists():save(p,get('https://api.gbif.org/v1/species/match?name=Isoetaceae&rank=FAMILY&strict=true'))
  row=json.loads(p.read_text(encoding='utf8'))
  if row.get('canonicalName')=='Isoetaceae' and row.get('phylum'):
   t[id]['ranks']={k:row[k] for k in ['kingdom','phylum','class','order','family'] if row.get(k)};t[id]['hierarchy']=[{'rank':k,'name':v} for k,v in t[id]['ranks'].items()];t[id]['source']='https://www.gbif.org/species/'+str(row['usageKey']);t[id]['reviewNote']='Rangos superiores documentados a través de la familia; la grafía y circunscripción específica del listado requieren revisión.';t[id]['rank']='species'
 records=[r for r in t.values() if r.get('ranks',{}).get('genus')=='Equus' and r['ranks'].get('phylum')]
 if records:
  source=records[0];ranks={k:v for k,v in source['ranks'].items() if k not in ['species','subspecies','variety']};t['molar-de-equus']={**source,'ranks':ranks,'hierarchy':[{'rank':k,'name':v} for k,v in ranks.items()],'matchedName':'Equus','rank':'genus','subjectType':'anatomical-part','commonName':'Molar de équido','reviewNote':'Rangos del género Equus. La pieza dentaria no se atribuye a una especie concreta.'}
 for id in ['coprolito','icnita','fosil-estromatolitos']:
  t[id].update(nonTaxonomic=True,status='not-applicable',reviewNote='Estructura biogénica, no un taxón único: no se asignan filo, familia ni género por su aspecto.',ranks={},hierarchy=[])
 save(D/'learning-taxonomy.json',t)
 report=json.loads((D/'learning-taxonomy-audit.json').read_text(encoding='utf8'));report.update(rankedPhyla=sum(bool(r.get('ranks',{}).get('phylum')) for r in t.values()),commonNames=sum(bool(r.get('commonName')) for r in t.values()),pendingIds=[id for id,r in t.items() if not r.get('ranks',{}).get('phylum') and not r.get('nonTaxonomic')]);save(D/'learning-taxonomy-audit.json',report);print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
