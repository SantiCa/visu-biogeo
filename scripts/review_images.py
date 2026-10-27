"""Create contact sheets for a HUMAN visual review. Never auto-approve images."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,sys
from PIL import Image,ImageOps,ImageDraw
from collect_images import api,image_rows
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp'/'image-review'
OUT.mkdir(parents=True,exist_ok=True)
def download(url,path):
    if path.exists(): return
    req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo personal educational review'})
    with urllib.request.urlopen(req,timeout=60) as r:path.write_bytes(r.read())
def main():
    if '--book' in sys.argv:
        import fitz
        pdf=OUT/'hamburg-colour.pdf'
        download('https://www.csmc.uni-hamburg.de/en/publications/mc/files/articles/mc16-complete',pdf)
        doc=fitz.open(pdf)
        for i,page in enumerate(doc):
            if 'Yellow ochre, upper' in page.get_text():
                print('Found yellow ochre page',i+1,flush=True)
                page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(OUT/f'ochre-page-{i+1}.png')
                (OUT/'ochre-page.txt').write_text(page.get_text(),encoding='utf8')
        return
    manifest=json.loads((ROOT/'data/images.json').read_text(encoding='utf8'))
    history=json.loads((ROOT/'data/andalucia-priority.json').read_text(encoding='utf8'))
    ids={e['itemId'] for e in history['events']}|{'empusa-pennata'}
    picks=[]
    for id in sorted(ids):
        for index,im in enumerate(manifest.get(id,{}).get('images',[])[:2]):
            picks.append({'itemId':id,'index':index,'image':im})
    im={'url':'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ac/Brauneisenerz_-_Horhausen%2C_Westerwald.jpg/960px-Brauneisenerz_-_Horhausen%2C_Westerwald.jpg','page':'https://commons.wikimedia.org/wiki/File:Brauneisenerz_-_Horhausen,_Westerwald.jpg','author':"Ra’ike",'license':'CC BY-SA 3.0','licenseUrl':'https://creativecommons.org/licenses/by-sa/3.0/','description':'Limonita con ocre amarillo natural. Horhausen, Westerwald; Museo Mineralógico de Bonn.','status':'pending'}
    picks.insert(0,{'itemId':'ocre-amarillo','index':0,'image':im})
    (OUT/'picks.json').write_text(json.dumps(picks,ensure_ascii=False,indent=2),encoding='utf8')
    def get(pair):
        i,p=pair
        try: download(p['image']['url'],OUT/f'{i:03}.jpg')
        except Exception as e: print(i,str(e),flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,enumerate(picks)))
    for start in range(0,len(picks),20):
        sheet=Image.new('RGB',(1200,1100),'white');draw=ImageDraw.Draw(sheet)
        for k,p in enumerate(picks[start:start+20]):
            i=start+k;x=(k%4)*300;y=(k//4)*220
            try:
                im=Image.open(OUT/f'{i:03}.jpg').convert('RGB');im=ImageOps.contain(im,(290,180));sheet.paste(im,(x+(300-im.width)//2,y))
            except: pass
            draw.text((x+4,y+183),f"{i:03}: {p['itemId'][:37]}",fill='black')
        sheet.save(OUT/f'sheet-{start//20:02}.jpg')
    print(len(picks),'candidates',flush=True)
if __name__=='__main__':main()
