"""Named blood cells, collected from their specific atlas pages."""
import json
from urllib.parse import urljoin
from collect_teaching import soup,add,norm,DATA
TARGETS={'estructura-basofilos':'basofilo','estructura-neutrofilos':'neutrofilo','estructura-monocitos':'monocito','estructura-plaquetas':'plaqueta','estructura-linfocitos':'linfocito'}
def main():
    cat={x['id']:x for x in json.loads((DATA/'species.json').read_text(encoding='utf8'))};data={}
    for id,name in TARGETS.items():
        page='https://mmegias.webs.uvigo.es/8-tipos-celulares/'+name+'.php'
        try:
            s=soup(page)
            for im in s.select('img[src]'):
                label=im.get('alt','')+' '+im.get('title','');src=im['src']
                if name not in norm(label+' '+src) or not src.lower().endswith(('.png','.jpg','.jpeg')):continue
                add(data,cat[id],urljoin(page,src),page,'Atlas de Histología / Universidad de Vigo; autoría de cada figura en la fuente',label or cat[id]['scientificName'],'Universidad de Vigo')
        except Exception as error:print(name,str(error),flush=True)
        print(name,len(data.get(id,{}).get('images',[])),flush=True)
    (DATA/'vigo-cells-images.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
