"""Freeze source-identified geology candidates; approval remains a separate step."""
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json,urllib.request,time,re
R=Path(__file__).resolve().parents[1];D=R/'data';OUT=R/'tmp/nps-zero-oct26'
MAP={
'arista':['Glacier Landforms: Arête, Garden Wall','Glacier Landforms: Arête & Horns, as viewed from Lake MacDonald'],
'horn':['Glacier Landforms: Horn, Flinsch Peak','Glacier Landforms: Arête & Horns, as viewed from Lake MacDonald'],
'drumlin':['Glacier Landforms: Drumlin, Spectacle Island','Spectacle Island'],
'circo-glaciar-glaciar-de-circo':['Glacier Landforms: Cirque, Muldrow Glacier','Glacier Landforms: Cirque, Granite Creek','Glacier Landforms: Cirque, Wrangell-St. Elias National Park','Types of Glaciers: Cirque Glacier, Eel Glacier'],
'abrasion-estrias-glaciares':['Glacier Landforms: Glacier Polish','Glacier Landforms: Glacier Striations, Yellowstone National Park'],
'morrena-central-de-fondo-lateral':['Glacier Landforms: Lateral Moraine, Kennicott Glacier','Glacier Landforms: Medial Moraines, Wrangell-St. Elias National Park','Glacier Landforms: Lateral Moraine, Root Glacier'],
'laguna-glaciar-ibon-antiguo-circo-glaciar':['Glacier Landforms: Tarn, Olympic National Park','Glacier Landforms: Cirque, Granite Creek'],
'iceberg':['Glacier Features: Iceberg, Pedersen Lagoon','Glacier Features: Iceberg, McBride Glacier','Glacier Features: Icebergs, Bear Glacier'],
'crevasses':['Glacier Features: Crevasses, Guyot Glacier','Glacier Features: Crevasse, Denali National Park','Glacier Features: Crevasses, Kennicott Glacier'],
'seracs':['Glacier Features: Seracs, Emmons Glacier','Glacier Features: Icefall, Stairway Icefall'],
'lengua-glaciar':['Types of Glaciers: Valley Glacier, Fraser Glacier','Types of Glaciers: Alpine Glacier, Nisqually Glacier','Glacier Features: Icebergs, Bear Glacier'],
'fiordo':['Glacier Landforms: Fjord, John Hopkins Inlet','Glacier Landforms: U-Shaped Valley, Glacier Bay National Park'],
'campo-de-bloques-erraticos':['Glacier Landforms: Glacial Erratics, Yellowstone National Park','Glacier Landforms: Glacial Landscape, Rocky Mountain National Park']}
CAVES={
'estalactitas':[('cave-speleothems','WICA-Stalactites'),('cave-speleothems','CAVE-stalactites'),('cave-jewel','/stalactite.')],
'estalagmitas':[('cave-speleothems','CAVE-stalagmites'),('cave-jewel','/stalagmite.')],
'columna':[('cave-speleothems','ORCA-grand-column'),('cave-mammoth','Violet')],
'cortina':[('cave-speleothems','TICA-cave-bacon'),('cave-jewel','cave-bacon')],
'estalactitas-excentricas-helictitas':[('cave-speleothems','TICA-helictites'),('cave-jewel','helictite_2'),('cave-mammoth','helictite')],
'perlas-o-pisolitas':[('cave-speleothems','CAVE-cave-pearls'),('cave-jewel','Cave-Chiclets')]}
def main():
 p=D/'priority-additions.json';data=json.loads(p.read_text(encoding='utf8'));rows=sum([json.loads((OUT/('gallery-page'+str(n)+'.json')).read_text(encoding='utf8')) for n in [1,2]],[]);index=json.loads((OUT/'index.json').read_text(encoding='utf8'));catalog={r['id']:r for r in json.loads((D/'species.json').read_text(encoding='utf8'))};details={}
 for id,titles in MAP.items():
  for title in titles:
   row=next((r for r in rows if r['title']==title),None)
   if not row:print('No exact gallery title',title,flush=True);continue
   asset=row['src'].split('/GetAsset/')[1].split('/')[0];url='https://npgallery.nps.gov/AssetDetail/'+asset;cache=OUT/(asset+'.html')
   if asset not in details:
    if not cache.exists():cache.write_bytes(urllib.request.urlopen(url,timeout=40).read());time.sleep(.4)
    soup=BeautifulSoup(cache.read_bytes(),'html.parser');text=soup.get_text(' ',strip=True);link=next((a['href'] for a in soup.select('a[href]') if re.search(r'/proxymdres\.(?:jpg|png)',a['href'],re.I)),None) or next((a['href'] for a in soup.select('a[href]') if re.search(r'/original\.(?:jpg|png)',a['href'],re.I)),None)
    if not link:continue
    author=re.search(r'PhotoCredit:\s*(.*?)\s*(?:Constraints Information:|Keywords:)',text);license='Dominio público · NPS (según registro de la fotografía)' if 'Public domain:Full Granting Rights' in text else 'Consultar condiciones del registro NPS; colección de estudio'
    details[asset]={'url':urljoin(url,link),'key':'nps-asset-'+asset,'page':url,'author':author.group(1) if author else 'National Park Service · crédito en la fuente','license':license,'reference':title,'status':'pending'}
   add(data,id,{**details[asset],'description':'Ejemplo identificado de '+catalog[id]['scientificName']+'. Pendiente de cotejar el rasgo y el encuadre.'})
  p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(id,'staged',flush=True)
 for id,targets in CAVES.items():
  for key,term in targets:
   source=index[key];matches=[im for im in source['images'] if term.lower() in ((im.get('src') or '')+' '+im.get('context','')).lower()]
   for im in matches:
    url=urljoin(source['url'],im['src']);credit=re.search(r'NPS\s+[Pp]hoto(?:\s+by|/)?\s*(.*)',im.get('context',''))
    author='National Park Service'+(' / '+credit.group(1) if credit and credit.group(1).strip('. ') else '')
    add(data,id,{'url':url,'key':url,'page':source['url'],'author':author,'license':'NPS · crédito y condiciones en la fuente','reference':'Fotografía del apartado correspondiente de la guía de espeleotemas NPS','description':'Ejemplo de '+catalog[id]['scientificName']+' identificado en la guía. Pendiente de revisión del encuadre.','status':'pending'})
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print('Candidate catalogue saved',flush=True)
def add(data,id,image):
 arr=data.setdefault(id,{'images':[]})['images']
 if not any(i.get('key')==image['key'] for i in arr):arr.append(image)
if __name__=='__main__':main()
