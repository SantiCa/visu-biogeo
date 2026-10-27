"""Geology.com article photographs, pending source and visual review."""
from pathlib import Path
import json,urllib.request,urllib.parse,re,time
from bs4 import BeautifulSoup
from collect_images import mapping
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';PATH=DATA/'geological-images.json';RAW=ROOT/'tmp/geological-sources';RAW.mkdir(parents=True,exist_ok=True)
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (VisuBioGeo personal geology study)'})
    with urllib.request.urlopen(req,timeout=35) as r:return r.read()
def main():
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));hist=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'))
    counts={}
    for e in hist['events']:counts.setdefault(e['itemId'],set()).add(e['year'])
    manifest=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    indices={}
    for section in ['minerals','rocks']:
        s=BeautifulSoup(fetch('https://geology.com/'+section+'/'),'html.parser')
        indices[section]={}
        for a in s.select('a[href]'):
            href=urllib.parse.urljoin('https://geology.com/'+section+'/',a['href'])
            if href.startswith('https://geology.com/'+section+'/') and href.endswith('.shtml'):
                indices[section][href.rsplit('/',1)[-1][:-6]]=href
    overrides={'Native sulfur':'sulfur','Native copper':'copper','Diamond crystals':'diamond','Bismuth crystals':'bismuth','Chlorite group':'chlorite','Serpentine group':'serpentine','Conglomerate':'conglomerate','Greywacke':'graywacke','Sylvite':'sylvite','Dolostone':'dolomite','Pumice':'pumice','Limonite':'limonite'}
    todo=[x for x in catalog if x['kind'] in ['mineral','roca'] and x['id'] not in manifest]
    todo.sort(key=lambda x:(-len(counts.get(x['id'],set())),x['scientificName']))
    for i,x in enumerate(todo,1):
        section='minerals' if x['kind']=='mineral' else 'rocks'
        english=mapping.get(x['scientificName'],'')
        stem=overrides.get(english,english.lower().replace(' ','-'))
        url=indices[section].get(stem)
        result={'status':'needs-source','images':[]}
        if url:
            try:
                body=fetch(url);(RAW/(x['id']+'.html')).write_bytes(body);s=BeautifulSoup(body,'html.parser');images=[]
                for im in s.select('img[src]'):
                    src=urllib.parse.urljoin(url,im['src']);alt=im.get('alt','')
                    if stem.replace('-',' ') not in alt.lower() and english.lower() not in alt.lower():continue
                    if re.search('chart|diagram|unit cell|products|map|collection|jewel|gemstone|ring|necklace',alt,re.I):continue
                    if '/photos/' not in src and not src.startswith('https://geology.com/rocks/pictures/'):continue
                    parent=im.find_parent('div');caption=parent.get_text(' ',strip=True) if parent else ''
                    # Keep detailed evidence locally for source review, not copied into app.
                    evidence={'alt':alt,'caption':caption[:2000]}
                    images.append({'url':src,'page':url,'key':src,'author':'Créditos detallados en el artículo de Geology.com','license':'Fuente de consulta privada · consultar derechos en el original','description':f"Fotografía de la ficha de {x['scientificName']} en Geology.com. Revisar muestra, escala y posibles minerales acompañantes.",'status':'pending','evidenceFile':x['id']+'.html','sourceAlt':alt})
                    if len(images)>=6:break
                result={'status':'pending' if images else 'needs-source','images':images,'source':url}
                time.sleep(.8)
            except Exception as e:result={'status':'error','images':[],'error':str(e)}
        manifest[x['id']]=result
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(PATH)
        print(f"{i}/{len(todo)} {x['scientificName']}: {len(result['images'])}",flush=True)
if __name__=='__main__':main()
