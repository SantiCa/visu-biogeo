"""Collect candidates from exact subject categories, NEVER broad text search.
Every result stays pending until a visual/source review approves it.
Resumable manifest; no request substitutes another taxon for a missing image.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request,urllib.parse,urllib.error,json,re,html,time,sys

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
PATH=DATA/'images.json'
catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'))
mapping=dict(pair.split('=',1) for pair in '''Albita=Albite
Andalucita=Andalusite
Apatito=Apatite
Aragonito=Aragonite
Arsenopirita=Arsenopyrite
Augita=Augite
Azufre=Native sulfur
Azurita=Azurite
Baritina=Barite
Bauxita=Bauxite
Berilo=Beryl
Biotita=Biotite
Bismuto=Bismuth crystals
Blenda=Sphalerite
Calcantita=Chalcanthite
Calcedonia=Chalcedony
Calcita=Calcite
Calcopirita=Chalcopyrite
Caolinita=Kaolinite
Carborundo=Silicon carbide
Carnalita=Carnallite
Casiterita=Cassiterite
Celestina=Celestine
Cianita=Kyanite
Cinabrio=Cinnabar
Clorita=Chlorite group
Cobre=Native copper
Cordierita=Cordierite
Corindón=Corundum
Crisocola=Chrysocolla
Cromita=Chromite
Cuarzo=Quartz
Diamante=Diamond crystals
Dolomita=Dolomite
Epidota=Epidote
Eritrina=Erythrite
Espinela=Spinel
Espodumena=Spodumene
Estaurolita=Staurolite
Flogopita=Phlogopite
Fluorita=Fluorite
Fuchsita=Fuchsite
Galena=Galena
Goethita=Goethite
Grafito=Graphite
Granate=Garnet
Halita=Halite
Hematites=Hematite
Hornblenda=Hornblende
Labradorita=Labradorite
Lazurita=Lazurite
Lepidolita=Lepidolite
Limonita=Limonite
Magnesita=Magnesite
Magnetita=Magnetite
Malaquita=Malachite
Marcasita=Marcasite
Moscovita=Muscovite
Olivino=Olivine
Ópalo=Opal
Oropimente=Orpiment
Ortosa=Orthoclase
Pirita=Pyrite
Pirolusita=Pyrolusite
Pirrotina=Pyrrhotite
Prehnita=Prehnite
Rejalgar=Realgar
Rodocrosita=Rhodochrosite
Rutilo=Rutile
Sepiolita=Sepiolite
Serpentina=Serpentine group
Siderita=Siderite
Silvina=Sylvite
Sodalita=Sodalite
Talco=Talc
Topacio=Topaz
Turmalina=Tourmaline
Turquesa=Turquoise
Vanadinita=Vanadinite
Wolframita=Wolframite
Yeso=Gypsum
Sillimanita=Sillimanite
Glaucofana=Glaucophane
Gabro=Gabbro
Diorita=Diorite
Granito=Granite
Gneis=Gneiss
Marga=Marl
Cuarcita=Quartzite
Basalto=Basalt
Andesita=Andesite
Filita=Phyllite
Esquisto=Schist
Sienita=Syenite
Mármol=Marble
Arenisca=Sandstone
Dolomía=Dolostone
Granodiorita=Granodiorite
Pumita=Pumice
Conglomerado brecha=Breccia
Conglomerado pudinga=Conglomerate
Grauvaca=Greywacke
Arcosa=Arkose
Antracita=Anthracite
Diabasa=Diabase
Peridotita=Peridotite'''.splitlines())
mapping.update(dict(pair.split('=',1) for pair in '''Ámbar=Amber
Anfibolita=Amphibolite
Aplita=Aplite
Arcilla=Clay
Azabache=Jet
Bomba volcánica=Volcanic bomb
Brecha volcánica=Volcanic breccia
Caliza=Limestone
Caliza litográfica=Lithographic limestone
Caliza oolítica=Oolitic limestone
Caliza pisolítica=Pisolithic limestone
Caolín=Kaolin
Cineritas=Ash tuff
Copal=Copal
Creta=Chalk
Eclogita=Eclogite
Escorias=Scoria
Granulita=Granulite
Hulla=Bituminous coal
Ignimbrita=Ignimbrite
Jumillita=Jumillite
Lapilli=Lapilli
Larviquita=Larvikite
Lava cordada=Pahoehoe
Lignito=Lignite
Micacita=Mica schist
Migmatita=Migmatite
Obsidiana=Obsidian
Pedernal=Flint
Pegmatita=Pegmatite
Petróleo=Petroleum
Pizarra=Slate
Pórfido=Porphyry
Riolita=Rhyolite
Septaria=Septarian concretion
Serpentinita=Serpentinite
Sílex=Flint
Toba calcárea=Calcareous tufa
Tobas=Tuff
Traquita=Trachyte
Turba=Peat'''.splitlines()))

def api(params):
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json',**params})
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo/2.0 (personal education; category image audit)'})
            with urllib.request.urlopen(req,timeout=25) as r: j=json.load(r)
            if 'error' in j: raise RuntimeError(j['error'])
            return j
        except urllib.error.HTTPError as error:
            if error.code==429: raise RuntimeError('RATE_LIMIT: pause collection; retry later') from error
            if attempt==2: raise
            time.sleep(3+attempt*3)
        except Exception:
            if attempt==2: raise
            time.sleep(1+attempt*2)
def clean(s): return html.unescape(re.sub('<[^>]*>','',s or '')).strip()
def image_rows(j,category):
    result=[]
    for p in j.get('query',{}).get('pages',{}).values():
        info=(p.get('imageinfo') or [{}])[0]; title=p['title']; m=info.get('extmetadata',{})
        if info.get('mime') not in ['image/jpeg','image/png','image/webp']: continue
        if min(info.get('width',0),info.get('height',0))<300: continue
        if re.search(r'logo|map\b|range|distribution|stamp|postage|painting|icon\b|coat of arms|drawing|illustration|plate\b',title,re.I): continue
        result.append({'url':info.get('thumburl') or info['url'],'page':info.get('descriptionurl',''),'title':title,'author':clean(m.get('Artist',{}).get('value','')),'license':clean(m.get('LicenseShortName',{}).get('value','')),'licenseUrl':m.get('LicenseUrl',{}).get('value',''),'description':clean(m.get('ImageDescription',{}).get('value',''))[:1200],'category':category,'status':'pending','reviewedAt':None})
    return result
def collect(x):
    name=x['scientificName']
    category=mapping.get(name) or (re.sub(r'\s+sp\.?$','',name) if x['kind']=='organismo' else None)
    if not category:return {'images':[],'status':'needs-source','reason':'Requiere una fuente específica del material/estructura.'}
    try:
        j=api({'generator':'categorymembers','gcmtitle':'Category:'+category,'gcmtype':'file','gcmlimit':8,'prop':'imageinfo','iiprop':'url|mime|size|extmetadata','iiurlwidth':800})
        images=image_rows(j,category)[:4]
        return {'images':images,'status':'pending' if images else 'needs-source','query':category}
    except Exception as e:return {'images':[],'status':'error','error':str(e)}

def main():
    manifest=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    historic=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'))
    priorities={e['itemId'] for e in historic['events']}|{'empusa-pennata','ocre-amarillo'}
    todo=[x for x in catalog if x['id'] not in manifest or manifest[x['id']].get('status')=='error']
    todo.sort(key=lambda x:x['id'] not in priorities)
    if '--priority' in sys.argv:todo=[x for x in todo if x['id'] in priorities]
    for i,x in enumerate(todo,1):
        result=collect(x);manifest[x['id']]=result
        if i%10==0 or 'RATE_LIMIT' in result.get('error',''):
            temporary=PATH.with_suffix('.tmp')
            temporary.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
            temporary.replace(PATH)
            print(f'{i}/{len(todo)} processed',flush=True)
        if 'RATE_LIMIT' in result.get('error',''):
            print('Source rate limit. Progress saved; resume later.',flush=True)
            break
        time.sleep(1.5)
    PATH.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print('Done',len(manifest),'subjects;',sum(bool(x['images']) for x in manifest.values()),'with candidates',flush=True)
if __name__=='__main__':main()
