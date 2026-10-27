"""Freeze a labelled review batch; approval uses stable URL keys, never positions."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,sys,hashlib,urllib.request,urllib.error,time,argparse,threading
from urllib.parse import unquote
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';CACHE=ROOT/'tmp/photo-cache';CACHE.mkdir(parents=True,exist_ok=True)
STOP_COMMONS=threading.Event()
def identity(im):
    page=im.get('page','')
    if 'commons.wikimedia.org/wiki/File' in page:return unquote(page).replace('_',' ')
    return im.get('key') or im.get('page') or im.get('originalUrl') or im['url']
def cachepath(url):return CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.jpg')
def fetch_image(url):
    path=cachepath(url)
    if path.exists():return path
    if 'wikimedia.org' in url and STOP_COMMONS.is_set():raise RuntimeError('Wikimedia paused after rate limit')
    for attempt in range(2):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 VisuBioGeo personal educational review'})
            with urllib.request.urlopen(req,timeout=40) as r:raw=r.read()
            import io
            im=Image.open(io.BytesIO(raw)).convert('RGB')
            im.thumbnail((1400,1400))
            im.save(path,quality=92)
            return path
        except urllib.error.HTTPError as e:
            if e.code==429:
                if 'wikimedia.org' in url:STOP_COMMONS.set()
                raise
            if attempt:raise
            time.sleep(2)
        except Exception as e:
            if attempt:raise
            time.sleep(2)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('batch');ap.add_argument('--source',choices=['naturalist','geology','commons','extra','additions','geodil','clouds','asturnatura','teaching','petrography','smith','pubchem'],default='naturalist');ap.add_argument('--priority',action='store_true');ap.add_argument('--limit',type=int,default=100);ap.add_argument('--per-item',type=int,default=2);ap.add_argument('--offset',type=int,default=0);ap.add_argument('--ids',default='');ap.add_argument('--exclude-batches',default='');ap.add_argument('--target-images',type=int,default=2);args=ap.parse_args()
    out=ROOT/'tmp/reviews'/args.batch;out.mkdir(parents=True,exist_ok=True)
    if (out/'picks.json').exists():raise RuntimeError('Batch already frozen; choose a new name.')
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'));historic=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'));curated=json.loads((DATA/'curated-images.json').read_text(encoding='utf8'))
    manifest=json.loads((DATA/{'naturalist':'inaturalist-images.json','geology':'geological-images.json','commons':'images.json','extra':'commons-extra-images.json','additions':'priority-additions.json','geodil':'geodil-images.json','clouds':'cloud-images.json','asturnatura':'asturnatura-images.json','teaching':'teaching-images.json','petrography':'petrography-images.json','smith':'smith-images.json','pubchem':'pubchem-images.json'}[args.source]).read_text(encoding='utf8'))
    counts={}
    previously_attempted=set()
    for batch_name in args.exclude_batches.split(','):
        if batch_name:
            old=json.loads((ROOT/'tmp/reviews'/batch_name/'picks.json').read_text(encoding='utf8'))
            previously_attempted.update(identity(p['image']) for p in old)
    for e in historic['events']:counts.setdefault(e['itemId'],set()).add(e['year'])
    candidates=[]
    for item in sorted(catalog,key=lambda x:(-len(counts.get(x['id'],set())),x['scientificName'])):
        if args.priority and item['id'] not in counts:continue
        if args.ids and item['id'] not in args.ids.split(','):continue
        approved=[im for im in curated.get(item['id'],{}).get('images',[]) if im['status']=='approved']
        if len({identity(im) for im in approved})>=args.target_images:continue
        decided_urls={identity(im) for im in curated.get(item['id'],{}).get('images',[]) if im['status'] in ['approved','rejected']}
        pics=[im for im in manifest.get(item['id'],{}).get('images',[]) if identity(im) not in decided_urls and identity(im) not in previously_attempted]
        if pics:candidates.append((item,pics))
    picks=[]
    for item,pics in candidates[args.offset:args.offset+args.limit]:
        for im in pics[:args.per_item]:picks.append({'itemId':item['id'],'name':item['scientificName'],'image':im})
    (out/'picks.json').write_text(json.dumps(picks,ensure_ascii=False,indent=2),encoding='utf8')
    def load(pair):
        i,p=pair
        try:fetch_image(p['image']['url'])
        except Exception as e:print('Failed',i,p['name'],e,flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(load,enumerate(picks)))
    fontpath=Path('C:/Windows/Fonts/arial.ttf');font=ImageFont.truetype(str(fontpath),16)
    for start in range(0,len(picks),16):
        sheet=Image.new('RGB',(1440,1320),'#f3f1eb');draw=ImageDraw.Draw(sheet)
        for k,p in enumerate(picks[start:start+16]):
            i=start+k;x=k%4*360;y=k//4*330
            try:
                im=Image.open(cachepath(p['image']['url']));im=ImageOps.contain(im,(350,286));sheet.paste(im,(x+(360-im.width)//2,y+(286-im.height)//2))
            except:pass
            draw.text((x+4,y+290),str(i)+': '+p['name'][:32],font=font,fill='black')
            draw.text((x+4,y+311),(p['image'].get('sourceAlt') or p['image'].get('taxonName') or '')[:40],font=font,fill='#555555')
        sheet.save(out/f'sheet-{start//16:03}.jpg',quality=90)
    print(args.batch,len(picks),'photos,',len(candidates[args.offset:args.offset+args.limit]),'entries. Batch frozen.',flush=True)
if __name__=='__main__':main()
