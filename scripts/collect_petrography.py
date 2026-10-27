"""Caption-matched PPL/XPL photographs; never mix the illumination modes."""
from pathlib import Path
from urllib.parse import urljoin
import json,re
from collect_teaching import fetch,soup,add,norm,DATA
PATH=DATA/'petrography-images.json'
def save(data):
    tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(PATH)
TRANSLATIONS={'Andalucita':'Andalusite','Andesita':'Andesite','Anfibolita':'Amphibolite','Apatito':'Apatite','Arenisca':'Sandstone','Augita (piroxeno)':'Clinopyroxene','Basalto':'Basalt','Biotita':'Biotite','Calcita':'Calcite','Caliza con bioclastos':'Bioclastic limestone','Caliza dolomítica':'Dolostone','Caliza oolítica':'Oolitic limestone','Caliza pisolítica':'Pisolithic limestone','Carbón':'Coal','Casiterita':'Cassiterite','Cianita':'Kyanite','Circón':'Zircon','Clorita':'Chlorite','Conglomerado brecha':'Breccia','Conglomerado pudinga':'Conglomerate','Corneana con andalucita':'Hornfels','Cuarcita':'Quartzite','Cuarzo':'Quartz','Epidota':'Epidote','Espinela':'Spinel','Esquisto':'Schist','Estaurolita':'Staurolite','Filita':'Phyllite','Fluorita':'Fluorite','Gabro olivínico':'Olivine gabbro','Gabro':'Gabbro','Gneis':'Gneiss','Granate':'Garnet','Granito':'Granite','Hornblenda (anfíbol)':'Amphiboles','Mármol':'Marble','Microclina':'Microcline','Moscovita':'Muscovite','Olivino':'Olivine','Ortosa':'Orthoclase','Pegmatita':'Pegmatite','Peridotita':'Peridotite','Pizarra':'Slate','Plagioclasa':'Plagioclase','Quiastolita':'Andalusite','Riolita':'Rhyolite','Serpentina':'Serpentine','Sienita':'Syenite','Sillimanita':'Sillimanite','Talco':'Talc','Traquita':'Trachyte','Turmalina':'Tourmaline'}
NARROW={'Augita (piroxeno)':'augite','Hornblenda (anfíbol)':'hornblende','Quiastolita':'chiastolite','Corneana con andalucita':'andalusite'}
def main():
    base='https://www.alexstrekeisen.it/english/';links=[]
    for section in ['meta','vulc','pluto','sedi']:
        url=base+section+'/index.php';s=soup(url)
        links.extend((norm(a.get_text(' ',strip=True)),urljoin(url,a['href'])) for a in s.select('a[href]') if not a['href'].startswith('javascript:'))
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));missing={x['id'] for x in json.loads((DATA/'image-audit.json').read_text(encoding='utf8'))['allMissingPairs']};data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    for item in catalog:
        if item['kind']!='lamina' or item['id'] not in missing or item['id'] in data:continue
        label=item['scientificName'];mineral=re.split(r'[.,]',label)[0].strip();term=TRANSLATIONS.get(mineral);mode='XPL' if 'Nícoles cruzados' in label else 'PPL'
        if not term:continue
        pages=list(dict.fromkeys(u for text,u in links if text==norm(term)));images=[]
        for page in pages:
            try:
                s=soup(page)
                for im in s.select('img[src]'):
                    anchor=im.find_parent('a');cell=im.find_parent('td');onclick=anchor.get('onclick','') if anchor else ''
                    match=re.search(r"window\.open\('([^']+\.(?:jpg|jpeg|png))'",onclick,re.I)
                    if not match or cell is None:continue
                    caption=cell.get_text(' ',strip=True)
                    modes=re.findall(r'\b(PPL|XPL)\b',caption)
                    if modes!=[mode]:continue
                    if mineral in NARROW and NARROW[mineral] not in caption.lower():continue
                    url=urljoin(page,match[1])
                    if url not in [x[0] for x in images]:images.append((url,page,caption))
                if len(images)>=3:break
            except Exception as error:print(label,error,flush=True)
        for url,page,caption in images[:3]:
            try:add(data,item,url,page,'Alex Strekeisen / colección de petrografía',label+' · '+mode+' · identificación y modo indicados en la fuente','Alex Strekeisen')
            except Exception as error:print(label,error,flush=True)
        data.setdefault(item['id'],{'images':[]});save(data);print(label,len(data[item['id']]['images']),flush=True)
if __name__=='__main__':main()
