"""Collect clearly named GeoDIL teaching specimens as pending candidates.
The image index provides human-written titles, not image-search rankings.
"""
from pathlib import Path
import json,urllib.request,urllib.parse,re,time
from bs4 import BeautifulSoup
from collect_images import mapping
from review_batch import identity
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';PATH=DATA/'geodil-images.json';CACHE=ROOT/'tmp/geodil';CACHE.mkdir(parents=True,exist_ok=True)
def soup(url):
    filename=CACHE/(url.rsplit('/',1)[-1])
    if filename.exists():return BeautifulSoup(filename.read_bytes(),'html.parser')
    req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo educational geoscience collection review'})
    with urllib.request.urlopen(req,timeout=30) as r:raw=r.read()
    filename.write_bytes(raw);time.sleep(.6)
    return BeautifulSoup(raw,'html.parser')
features={'Delta':'delta','Drumlin':'drumlin','Ésker':'esker','Estuario':'estuary','Acantilado':'cliff','Cascada':'waterfall','Estalactitas':'stalactite','Estalagmitas':'stalagmite','Discordancia angular':'angular unconformity','Estromatolitos':'stromatolite','Cabalgamiento':'thrust fault','Diaclasa':'joint','Bloque errático':'glacial erratic','Canchal':'talus','Dunas litorales':'coastal dune','Falla directa':'normal fault','Falla inversa':'reverse fault','Granodiorita':'granodiorite','Trípoli':'diatomite','Marga':'marl','Ofita':'ophite','Silvina':'sylvite','Celestina':'celestite','Glaucofana':'glaucophane','Sillimanita':'sillimanite'}
features.update({'Abanico aluvial o cono de deyección':'alluvial fan','Arcos marinos':'sea arch','Arista':'arete','Banquisa':'sea ice','Berrocal':'tor','Bolos':'boulder','Brechas de falla':'fault breccia','Canchales o derrubios':'talus','Cañón. Garganta':'canyon','Catarata':'waterfall','Circo glaciar. Glaciar de circo':'cirque','Columna':'column','Cordón litoral o barra':'barrier','Crevasses':'crevasse','Cueva o caverna':'cave','Diaclasa plumosa':'plumose','Dolina. Torca':'sinkhole','Domo salino. Diapiro':'salt dome','Dropstone':'dropstone','Espejo de falla. Estrías de falla':'slickenside','Estratificación cruzada':'cross-bedding','Falla horizontal o de desgarre':'strike-slip fault','Farallones':'sea stack','Filón de cuarzo':'quartz vein','Fiordo':'fjord','Flecha':'spit','Flute casts, calcos de flauta o turboglifos':'flute','Horn':'horn','Iceberg':'iceberg','Indlandsis':'ice sheet','Islas barrera':'barrier island','Lengua glaciar':'glacier tongue','Llanuras mareales':'tidal flat','Marisma':'salt marsh','Marmitas de gigante':'pothole','Meandro':'meander','Morrena (central, de fondo, lateral)':'moraine','Permafrost':'permafrost','Piedras caballeras':'balanced rock','Playa':'beach','Playa de cantos':'pebble beach','Pliegue anticlinal':'anticline','Pliegue chevron':'chevron','Pliegue sinclinal':'syncline','Pliegue tumbado':'recumbent fold','Río anastomosado o braided':'braided','Ripples marks':'ripple','Roca aborregada':'roche moutonnee','Seracs':'serac','Sill':'sill','Suelo poligonal. Ambiente periglaciar (tundra, por ejemplo)':'polygon','Tafoni':'tafoni','Terrazas fluviales':'river terrace','Terrazas travertínicas':'travertine','Tillitas':'tillite','Tómbolo':'tombolo','Tor':'tor','Turbidita':'turbidite','Valle colgado':'hanging valley','Valle glaciar. Valle en U':'glacial valley','Varvas glaciares':'varve','Xenolito':'xenolith'})
def main():
    s=soup('https://geodil.dperkins.org/h/all.html')
    index=[{'title':im['title'],'page':urllib.parse.urljoin('https://geodil.dperkins.org/h/',im.parent['href'])} for im in s.select('a[href] img[title]') if re.match(r'^\d+\.html$',im.parent.get('href',''))]
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));hist=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'));cur=json.loads((DATA/'curated-images.json').read_text(encoding='utf8'))
    priority={e['itemId'] for e in hist['events']};manifest=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    todo=[x for x in catalog if not manifest.get(x['id'],{}).get('images') and len({identity(im) for im in cur.get(x['id'],{}).get('images',[]) if im['status']=='approved'})<2 and x['kind'] in ['mineral','roca','nube','relieve']]
    todo.sort(key=lambda x:(x['id'] not in priority,x['scientificName']))
    for x in todo:
        term=features.get(x['scientificName']) or mapping.get(x['scientificName']) or (x['scientificName'] if x['kind']=='nube' else None)
        if not term:continue
        term=term.lower().replace('native ','').replace(' crystals','').replace(' group','').replace('greywacke','graywacke')
        options=[e for e in index if re.search(r'\b'+re.escape(term)+r'\b',e['title'],re.I) and not re.search('thin.section|diagram|map|drawing|chart|structure|building|cathodoluminescence',e['title'],re.I)]
        options.sort(key=lambda e:(not e['title'].lower().startswith(term),len(e['title'])))
        images=[]
        for e in options[:5]:
            try:
                detail=soup(e['page']);rows={}
                for tr in detail.select('tr'):
                    cells=tr.select('td,th')
                    if len(cells)>=2:rows[cells[0].get_text(' ',strip=True)]=cells[1].get_text(' ',strip=True)
                if re.search(r'thin.section|cross.polari|plane.polari|PPL|XPL|photomicrograph',rows.get('Tech details',''),re.I):continue
                a=next((a for a in detail.select('a[href]') if re.search(r'/i/\d+\.jpg$',urllib.parse.urljoin(e['page'],a['href']))),None)
                im=next((im for im in detail.select('img[src]') if re.search(r'/i/\d+\.jpg$',urllib.parse.urljoin(e['page'],im['src']))),None)
                url=urllib.parse.urljoin(e['page'],a['href'] if a else im['src'] if im else '')
                if not url.endswith('.jpg'):continue
                images.append({'url':url,'page':e['page'],'key':url,'title':e['title'],'author':rows.get('Photographer','GeoDIL / University of North Dakota'),'license':'Colección docente GeoDIL · condiciones en la fuente','reference':rows.get('Collection',''),'description':f"Imagen identificada como {e['title']} en GeoDIL. Revisión visual pendiente.",'sourceDetails':rows.get('Tech details',''),'status':'pending'})
            except Exception as error:print(e['page'],error,flush=True)
            if len(images)>=4:break
        manifest[x['id']]={'images':images,'status':'pending' if images else 'needs-source','query':term}
        temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(PATH)
        print(x['scientificName'],len(images),flush=True)
if __name__=='__main__':main()
