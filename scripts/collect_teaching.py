"""Named teaching collections. Candidates require a separate visual approval."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
import argparse,json,re,time,hashlib,urllib.request,urllib.error,ssl,subprocess,unicodedata
from PIL import Image,ImageOps
from review_batch import cachepath
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';CACHE=ROOT/'tmp/teaching-sources';CACHE.mkdir(exist_ok=True);PATH=DATA/'teaching-images.json'
def norm(s):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()).strip()
def fetch(url):
    path=CACHE/hashlib.sha256(url.encode()).hexdigest()
    if path.exists():return path.read_bytes()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo personal educational collection'}),timeout=35) as r:raw=r.read()
        path.write_bytes(raw)
    except urllib.error.URLError as error:
        if not isinstance(error.reason,ssl.SSLCertVerificationError):raise
        subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'scripts/fetch_public_file.ps1'),'-Uri',url,'-Destination',str(path)],check=True,capture_output=True)
    time.sleep(.25);return path.read_bytes()
def soup(url):return BeautifulSoup(fetch(url),'html.parser')
def save(data):
    tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(PATH)
def add(data,item,url,page,author,label,provider):
    arr=data.setdefault(item['id'],{'images':[]})['images']
    if any(im['url']==url for im in arr):return
    import io
    out=cachepath(url)
    if not out.exists():
        with Image.open(io.BytesIO(fetch(url))) as im:
            image=im.convert('RGB');image.thumbnail((1400,1400));image.save(out,quality=93)
    arr.append({'url':url,'key':url,'page':page,'author':author,'license':'Colección docente identificada · consultar condiciones de la fuente · estudio personal','provider':provider,'description':label,'sourceAlt':label,'status':'pending'})

VIGO={
'Alveolos pulmonares':['Pulmón'],'Aparato de Golgi':['Aparato de Golgi'],'Arteria':['Arteria elástica'],'Astrocitos':['Astrocito'],
'Axón con vaina de mielina':['Mielina'],'Canal resinífero de gimnosperma':['Canales resiníferos'],'Centrosoma, Centríolos, Diplosoma':['Centrosoma'],
'Cilios':['Cilios'],'Citoesqueleto':['Citoesqueleto'],'Cloroplasto':['Cloroplastos'],'Corte de esófago':['Esófago'],
'Corte de hoja':['hoja-transv.php'],'Corte de hoja de gimnosperma':['hoja-pino.php'],'Corte de lengua':['Lengua'],'Corte de riñón':['excretor-rinon.php'],
'Cromatina':['Cromatina'],'Cromoplastos':['Plastos'],'Desmosomas':['Complejos de unión'],'Eosinófilos':['Eosinofilo'],
'Epidermis':['proteccion_epidermis.php'],'Epidermis con estomas':['Epidermis: estomas'],'Epitelio ciliado, tráquea':['Tráquea'],
'Eritrocitos':['Eritrocito'],'Esclerénquima, fibras, esclereidas':['Esclerénquima: Fibras','Esclerénquima: Esclereidas'],
'Estómago, corte transversal':['Estómago'],'Exocitosis':['Exocitosis'],'Floema, placas cribosas':['conduccion_xilema.php'],
'Folículo de Graaf':['Folículos'],'Fruto':['Pericarpo (manzana)','Pericarpo (naranja)'],'Glándula tiroides':['Tiroides'],
'Glomérulos renales- Cápsula de Bowman':['La nefrona'],'Hipófisis (pituitaria)':['Hipófisis'],'Intestino delgado':['Intestino delgado'],
'Intestino grueso':['Intestino grueso'],'Lenticela':['Peridermis'],'Linfocitos':['Linfocito'],'Lisosomas':['Lisosomas'],
'Lóbulo del hígado':['Hígado'],'Membrana plasmática':['3. Membrana celular ▸'],'Meristemo apical de raíz':['Primario apical radical'],
'Microtúbulos':['Microtúbulos'],'Mitocondria':['Mitocondrias'],'Neurona':['Neurona'],'Neurona multipolar':['Neurona'],
'Núcleo celular':['4. Núcleo ▸'],'Nucleolo':['Nucléolo'],'Ovario':['reproductor-ovario.php'],'Ovocito':['Folículos'],
'Páncreas, islotes de Langerhans':['digestivo-pancreas.php'],'Parénquima acuífero':['Acuífero'],'Parénquima aerífero':['Aerífero'],
'Parénquima clorofílico':['Clorofílico'],'Parénquima de reserva':['Reserva'],'Peroxisomas':['Peroxisomas'],'Piel':['Piel fina','Piel gruesa'],
'Raíz de Monocotiledónea':['raiz-primaria-m.php'],'Raíz primaria de Dicotiledónea':['raiz-primaria-d.php'],'Raíz secundaria de Dicotiledónea':['raiz-secundaria-d.php'],
'Retículo endoplasmático':['Retículo endoplasmático'],'Retículo endoplasmático liso':['Retículo endoplasmático'],'Retículo endoplasmático rugoso':['Retículo endoplasmático'],
'Sangre humana':['sangre.php'],'Sección de un diente':['Diente'],'Sección de una flor':['flor2.php'],
'Sección transversal de un nervio':['nervioso-nervio.php'],'Tallo de Gimnosperma':['tallo-secundario-g.php'],
'Tallo de Monocotiledónea':['tallo-primario-m.php'],'Tallo primario de Dicotiledónea':['tallo-primario-d2.php'],
'Tallo secundario de Dicotiledónea':['tallo-secundario-d.php'],'Tejido adiposo':['adiposo_blanco.php','adiposo_pardo.php'],
'Tejido cartilaginoso':['Hialino','Elástico','Fibrocartílago'],'Tejido conjuntivo denso':['Denso regular','Denso irregular'],
'Tejido conjuntivo fibroso':['Denso regular'],'Tejido conjuntivo laxo':['Laxo','Laxo 2'],
'Tejido epitelial plano, monoestratificado. Tejido endotelial':['Simple plano','Endotelial'],
'Tejido muscular cardíaco':['Cardiaco'],'Tejido muscular estriado':['Esquelético'],'Tejido muscular liso':['Liso'],
'Tejido nervioso, médula espinal':['Neurona-glía'],'Tejido óseo compacto':['Hueso compacto'],'Tejido óseo esponjoso':['Hueso trabecular'],
'Tejido pulmonar':['Pulmón'],'Testículo, túbulos seminíferos':['Túbulos seminíferos'],'Tricoma':['Epidermis: tricomas'],
'Túbulos renales':['La nefrona'],'Vacuola vegetal':['Vacuolas'],'Vellosidades intestinales':['Intestino delgado'],'Xilema':['conduccion_xilema.php']}

def vigo(catalog,data):
    base='https://mmegias.webs.uvigo.es/';index=soup(base+'mapa.php');links=[(a.get_text(' ',strip=True),urljoin(base,a['href'])) for a in index.select('a[href]')]
    for item in catalog:
        if item['kind']!='estructura' or item['id'] in data:continue
        terms=VIGO.get(item['scientificName'],[item['scientificName']]);pages=[]
        for term in terms:
            matches=[u for text,u in links if norm(text)==norm(term) or (term.endswith('.php') and urlsplit(u).path.endswith('/'+term))]
            matches.sort(key=lambda u:('imagenes-grandes' not in u,len(u)))
            pages.extend(matches[:2])
        if not pages:continue
        for page in dict.fromkeys(pages):
            try:
                s=soup(page);candidates=[]
                for im in s.select('img[src]'):
                    src=im['src'];url=urljoin(page,src)
                    if not re.search(r'\.(jpg|jpeg|png)$',src,re.I) or any(w in src for w in ['modelos/','icon','bandera','logo']):continue
                    if im.find_parent(['nav','header','footer']):continue
                    label=im.get('alt') or im.get('title') or ''
                    if 'imagenes-grandes' not in page and not im.find_parent('figure'):continue
                    # Detailed tissue pages supply their own labels; general pages need an identified organelle.
                    if 'imagenes-grandes' not in page and not any(norm(t).rstrip('s') in norm(label) for t in [item['scientificName'],*terms]):continue
                    candidates.append((url,label))
                for url,label in dict.fromkeys(candidates):
                    if len(data.get(item['id'],{}).get('images',[]))>=4:break
                    add(data,item,url,page,'Atlas de Histología / Universidad de Vigo; autoría de cada figura en la fuente','Atlas de Histología: '+item['scientificName']+' · '+label[:55],'Universidad de Vigo')
            except Exception as error:print(item['scientificName'],str(error),flush=True)
        data.setdefault(item['id'],{'images':[]});save(data);print(item['scientificName'],len(data[item['id']]['images']),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',choices=['vigo']);args=ap.parse_args()
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));audit=json.loads((DATA/'image-audit.json').read_text(encoding='utf8'));missing={x['id']:x['approvedImages'] for x in audit['allMissingPairs']};catalog=[x for x in catalog if x['id'] in missing];catalog.sort(key=lambda x:(missing[x['id']]>0,x['scientificName']))
    data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {};vigo(catalog,data)
if __name__=='__main__':main()
