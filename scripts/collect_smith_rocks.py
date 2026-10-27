"""Identified hand specimens; thin sections and diagrams are not hand specimens."""
from urllib.parse import urljoin
from pathlib import Path
import json,re
from collect_teaching import soup,add,norm,DATA
from collect_images import mapping
PATH=DATA/'smith-images.json'
BASE='https://www.science.smith.edu/~jbrady/petrology/rock-library/'

def main():
    links=[]
    for page in ['rl-page02.php','rl-page03.php','rl-page04.php']:
        url=BASE+page;s=soup(url)
        links.extend((norm(a.get_text(' ',strip=True)),urljoin(url,a['href'])) for a in s.select('a[href]'))
    cat=json.loads((DATA/'species.json').read_text(encoding='utf8'));audit=json.loads((DATA/'image-audit.json').read_text(encoding='utf8'));zero={x['id'] for x in audit['allMissingPairs'] if x['approvedImages']==0};data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    for item in cat:
        if item['kind']!='roca' or item['id'] not in zero or item['id'] in data:continue
        term=mapping.get(item['scientificName']);pages=list(dict.fromkeys(u for text,u in links if text==norm(term or '') and '/rock-library/' in u));data.setdefault(item['id'],{'images':[]})
        for source in pages:
            try:
                s=soup(source);hand=next((a for a in s.select('a[href]') if 'Hand Sample Photos' in a.get_text(' ',strip=True)),None)
                if hand is None:continue
                page=urljoin(source,hand['href']);s=soup(page)
                for im in s.select('img.figure[src]')[:4]:
                    full=urljoin(page,im['src']);title=im.get('title','');alt=im.get('alt','')
                    add(data,item,full,page,'Smith College; créditos particulares en la fuente',item['scientificName']+' · muestra identificada de la colección de petrología; '+alt,'Smith College')
                    data[item['id']]['images'][-1].update(sourceCaption=title,license='CC BY-NC-SA 4.0 · colección docente de petrología; comprobar créditos particulares')
            except Exception as error:print(item['scientificName'],error,flush=True)
        PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(item['scientificName'],len(data[item['id']]['images']),flush=True)
if __name__=='__main__':main()
