"""Accept explicit taxonomic synonyms resolved by the exact-name collector."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/species.json'
catalog=json.loads(PATH.read_text(encoding='utf8'));manifest=json.loads((ROOT/'data/inaturalist-images.json').read_text(encoding='utf8'));changes=[]
rules=json.loads((ROOT/'data/taxon-review-rules.json').read_text(encoding='utf8'))
for item in catalog:
    rejected=rules.get(item['id'],{}).get('rejectedAliases',[])
    item['aliases']=[a for a in item.get('aliases',[]) if a not in rejected]
    if 'aliasSources' in item:item['aliasSources']=[s for s in item['aliasSources'] if s['name'] not in rejected]
    source=manifest.get(item['id'],{});accepted=source.get('acceptedName')
    if accepted in rejected:continue
    if item['kind']!='organismo' or not accepted or not source.get('images') or accepted==item['scientificName'] or accepted in item.get('aliases',[]):continue
    item.setdefault('aliases',[]).append(accepted)
    item.setdefault('aliasSources',[]).append({'name':accepted,'source':'https://www.inaturalist.org/taxa/'+str(source['taxonId']),'method':'Coincidencia exacta del nombre o sinónimo explícito en la fuente; no búsqueda aproximada.'})
    changes.append(item['scientificName']+' = '+accepted)
PATH.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8');print('\n'.join(changes));print(len(changes),'alias additions')
