"""Cloud-specific exact categories. Kept separate from the fossil collector."""
from pathlib import Path
import json,urllib.error
from collect_commons_html import collect
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/cloud-images.json'
catalog=json.loads((ROOT/'data/species.json').read_text(encoding='utf8'));data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
mapping={'Asperitas':'Asperitas clouds','Cauda':'Tail clouds','Cavum':'Fallstreak holes','Contrails':'Contrails','Fluctus':'Kelvin-Helmholtz clouds','Flumen':'Beaver tails (meteorology)','Murus':'Wall clouds','Volutus o nube enrollada':'Roll clouds','Flammagenitus':'Pyrocumulus clouds'}
for item in catalog:
    if item['kind']!='nube' or item['id'] in data:continue
    name=item['scientificName'];cat=mapping.get(name,name+' clouds')
    try:result=collect(cat,4)
    except urllib.error.HTTPError as error:
        if error.code==429:print('Rate limit; stopped.',flush=True);break
        result={'images':[],'status':'needs-source','error':str(error)}
    except Exception as error:result={'images':[],'status':'needs-source','error':str(error)}
    data[item['id']]=result;PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(name,len(result['images']),flush=True)
