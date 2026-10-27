"""Paced exact-category candidates for fossil and cloud entries; never auto-approve."""
from pathlib import Path
import json,urllib.error
from collect_commons_html import collect
from review_batch import identity
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/commons-extra-images.json'
data=json.loads(PATH.read_text(encoding='utf8'));cur=json.loads((ROOT/'data/curated-images.json').read_text(encoding='utf8'))
catalog=json.loads((ROOT/'data/species.json').read_text(encoding='utf8'))
mapping={'Archaeopterix':'Archaeopteryx','Hiparion':'Hipparion','Parantrophus':'Paranthropus','Coprolito':'Coprolites','Icnita':'Fossil footprints','Volutus o nube enrollada':'Volutus clouds','Murus':'Wall clouds','Cauda':'Tail clouds','Cavum':'Fallstreak holes','Fluctus':'Kelvin-Helmholtz clouds','Flumen':'Beaver tails (meteorology)','Silvagenitus':'Silvagenitus clouds','Homogenitus':'Homogenitus clouds','Homomutatus':'Homomutatus clouds','Flammagenitus':'Pyrocumulus clouds','Cataractagenitus':'Cataractagenitus clouds','Carcharocles megalodon':'Otodus megalodon fossils','Stigmaria ficoides':'Stigmaria','Calamites':'Calamites (fossils)','Parkinsonia':'Parkinsonia (ammonite)'}
extant={'Balanus','Cidaris','Clypeaster','Conus','Dentalium','Encope','Equus','Fusinus','Gibbula','Globigerina','Homo','Homo sapiens','Isurus','Lamna','Myliobatis','Operculina','Ostrea','Pecten','Planorbis','Potamides','Rana','Schizaster','Strombus','Turritella','Ursus'}
for item in sorted(catalog,key=lambda x:(x['kind']!='nube',x['scientificName'])):
    id=item['id'];name=item['scientificName']
    if item['kind'] not in ['fosil','nube'] or id in data or len({identity(im) for im in cur.get(id,{}).get('images',[]) if im['status']=='approved'})>=2:continue
    category=mapping.get(name) or ('Fossil '+name if name in extant else name)
    try:result=collect(category,3)
    except urllib.error.HTTPError as error:
        if error.code==429:print('Rate limit; stopped.',flush=True);break
        result={'images':[],'status':'needs-source','error':str(error)}
    except Exception as error:result={'images':[],'status':'needs-source','error':str(error)}
    data[id]=result;tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(PATH)
    print(name,len(result['images']),flush=True)
