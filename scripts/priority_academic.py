"""Explicitly identified geology sources; all new photographs remain pending."""
import json,urllib.request,urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageOps
from review_batch import cachepath
from collect_commons_html import collect
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/priority-additions.json'
data=json.loads(PATH.read_text(encoding='utf8'))
def add(id,im):
    im['status']='pending';arr=data.setdefault(id,{'images':[]})['images']
    if not any(p['url']==im['url'] for p in arr):arr.append(im)
for id,name in [('ofita','ofita'),('marga','marga1'),('marga','marga2')]:
    url=f'https://www.uv.es/pardomv/avgeolog/rocas/{name}.jpg'
    local=ROOT/('tmp/uv-'+name+'.jpg')
    if local.exists():ImageOps.contain(Image.open(local).convert('RGB'),(1400,1400)).save(cachepath(url),quality=92)
    add(id,{'url':url,'page':f'https://www.uv.es/pardomv/avgeolog/rocas/_{name}.html','author':'Miguel V. Pardo Alonso y Rodolfo Gozalo / Universitat de València','license':'Colección docente · derechos de la fuente','description':'Muestra identificada en el Aula Virtual de Geología. Revisión visual pendiente.'})
page='https://www.regmurcia.com/servlet/s.Sl?r=ReP-27972-DETALLE_REPORTAJESABUELO&sit=c,365,m,108'
s=BeautifulSoup(urllib.request.urlopen(page).read(),'html.parser')
for im in s.select('img[src]'):
    if 'METHOD=VERIMAGEN_12542' in im['src'] and any(n in im['src'] for n in ['125420','125421','125423']):
        add('ofita',{'url':urllib.parse.urljoin(page,im['src']),'page':page,'key':urllib.parse.urljoin(page,im['src']),'author':'Antonio del Ramo Jiménez / Región de Murcia Digital','license':'Derechos de la fuente · colección personal','description':im.get('alt',''),'reference':im.get('alt','')})
add('tripoli',{'url':'https://geology.com/rocks/pictures/diatomite.jpg','page':'https://geology.com/rocks/diatomite.shtml','author':'Geology.com / Hobart M. King','license':'Derechos de la fuente · colección personal','description':'Diatomita blanca de Nevada, muestra de unos cinco centímetros. El listado original denomina la entrada Trípoli o diatomita.'})
try:
    for im in collect('Diatomite',6)['images']:add('tripoli',im)
except Exception as error:print('Commons:',error)
PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
