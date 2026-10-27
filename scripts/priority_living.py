from pathlib import Path
import json
from collect_inaturalist import collect
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';path=DATA/'priority-additions.json'
catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));result=json.loads(path.read_text(encoding='utf8')) if path.exists() else {}
for genus,name in [('Trivia sp.','Trivia monacha'),('Pecten sp.','Pecten maximus')]:
    item=next(x for x in catalog if x['scientificName']==genus)
    value=collect({'scientificName':name,'aliases':[]})
    for im in value['images']:im['description']=f"Ejemplo identificado de {name}, incluido como representante del género solicitado ({genus}). Fuente: ficha taxonómica de iNaturalist."
    result[item['id']]=value
    print(genus,item['id'],len(value['images']),flush=True)
path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
