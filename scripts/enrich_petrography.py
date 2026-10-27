"""Retain illumination and field of view from the caption of each reviewed image."""
import json,re
from urllib.parse import urljoin
from collect_teaching import DATA,soup

def main():
    path=DATA/'curated-images.json';data=json.loads(path.read_text(encoding='utf8'));pages={};count=0
    for entry in data.values():
        for im in entry['images']:
            if im.get('status')!='approved' or 'alexstrekeisen.it' not in im.get('page',''):continue
            page=im['page'];pages.setdefault(page,soup(page))
            original=im.get('originalUrl',im['url'])
            anchor=next((a for a in pages[page].select('a[onclick]') if original.rsplit('/',1)[-1] in a['onclick']),None)
            if anchor is None:raise ValueError(original)
            caption=anchor.find_parent('td').get_text(' ',strip=True)
            modes=re.findall(r'\b(PPL|XPL)\b',caption)
            if len(modes)!=1:raise ValueError(caption)
            im['optics']=modes[0]
            field=re.search(r'Field of view\s*=\s*([^)]*)',caption,re.I)
            if field:im['fieldOfView']=field.group(1).strip()
            im['author']='Colección de Alex Strekeisen; autoría de cada fotografía en la fuente'
            count+=1
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(count,'fotos con contexto óptico')

if __name__=='__main__':main()
