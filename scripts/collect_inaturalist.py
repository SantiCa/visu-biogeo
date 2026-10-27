"""Exact-name taxon photographs from iNaturalist; all remain pending review.
Resumable, rate-limited, preserves source/author/licence and accepted taxon.
"""
from pathlib import Path
import urllib.request,urllib.parse,urllib.error,json,time,re,sys,threading
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';PATH=DATA/'inaturalist-images.json'
RATE=threading.Lock()
last_request=0
RULES=json.loads((DATA/'taxon-review-rules.json').read_text(encoding='utf8'))
def get(path,params=None):
    global last_request
    url='https://api.inaturalist.org/v1/'+path
    if params:url+='?'+urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with RATE:
                delay=1.1-(time.monotonic()-last_request)
                if delay>0:time.sleep(delay)
                last_request=time.monotonic()
            req=urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo/3.0 educational taxon-photo review'})
            with urllib.request.urlopen(req,timeout=35) as r:result=json.load(r)
            return result['results']
        except urllib.error.HTTPError as error:
            if error.code==429:raise RuntimeError('RATE_LIMIT; resume later') from error
            if error.code==404:return []
            if attempt==2:raise
            time.sleep(4)
        except Exception:
            if attempt==2:raise
            time.sleep(4)
def canonical(n):
    return re.sub(r'\s+',' ',re.sub(r'\s*×\s*',' x ',re.sub(r'\s+sp\.?$','',n).lower())).strip()
def names(x):
    return [canonical(n) for n in [x['scientificName'],*x.get('aliases',[])]]
def resolve(x):
    accepted=names(x);taxon=None
    for name in accepted:
        matches=get('taxa',{'q':name,'is_active':'true','per_page':30})
        blocked={canonical(n) for n in RULES.get(x['id'],{}).get('blockedPhotoTaxa',[])}
        allowed=[t for t in matches if t['rank'] in ['species','subspecies','genus','variety','hybrid'] and canonical(t['name']) not in blocked]
        exact=[t for t in allowed if canonical(t['name']) in accepted]
        if not exact:exact=[t for t in allowed if canonical(t.get('matched_term','')) in accepted]
        taxon=exact[0] if len({t['id'] for t in exact})==1 else None
        if taxon:break
    return taxon
def photos(detail):
    taxon=detail;images=[];seen=set()
    for tp in detail.get('taxon_photos',[]):
        p=tp['photo']
        if p.get('flags') or p['id'] in seen:continue
        seen.add(p['id'])
        if min(p.get('original_dimensions',{}).values() or [0])<400:continue
        images.append({'url':p.get('large_url') or p['medium_url'],'page':'https://www.inaturalist.org/photos/'+str(p['id']),'taxonPage':'https://www.inaturalist.org/taxa/'+str(taxon['id']),'author':p.get('attribution_name') or p.get('attribution',''),'license':p.get('license_code') or 'Todos los derechos reservados · colección de estudio privada','description':f"Foto seleccionada en la ficha de {detail['name']} (iNaturalist taxon {taxon['id']}). Revisar rasgos diagnósticos y encuadre antes de aprobar.",'taxonName':detail['name'],'taxonRank':detail['rank'],'photoId':p['id'],'status':'pending'})
        if len(images)>=4:break
    return {'status':'pending' if images else 'needs-source','taxonId':taxon['id'],'acceptedName':detail['name'],'images':images}
def collect(x):
    taxon=resolve(x)
    if not taxon:return {'status':'needs-source','images':[],'reason':'No exact active taxon match.'}
    return photos(get('taxa/'+str(taxon['id']))[0])
def main():
    catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'))
    historic=json.loads((DATA/'andalucia-priority.json').read_text(encoding='utf8'))
    counts={}
    for e in historic['events']:counts.setdefault(e['itemId'],set()).add(e['year'])
    manifest=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    todo=[x for x in catalog if x['kind']=='organismo' and (x['id'] not in manifest or manifest[x['id']].get('status')=='error' or ('--missing' in sys.argv and not manifest[x['id']].get('images')))]
    todo.sort(key=lambda x:(-len(counts.get(x['id'],set())),x['scientificName']))
    if '--priority' in sys.argv:todo=[x for x in todo if x['id'] in counts]
    def safe_resolve(x):
        try:return x,resolve(x),None
        except Exception as e:return x,None,str(e)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for start in range(0,len(todo),15):
            batch=list(pool.map(safe_resolve,todo[start:start+15]))
            ids=[str(t['id']) for x,t,error in batch if t]
            try:details={t['id']:t for t in get('taxa/'+','.join(ids))} if ids else {}
            except Exception as e:
                print('Detail batch failed:',e,flush=True);break
            for x,t,error in batch:
                if error:result={'status':'error','images':[],'error':error}
                elif not t:result={'status':'needs-source','images':[],'reason':'No exact active taxon match.'}
                elif t['id'] not in details:result={'status':'error','images':[],'error':'Missing exact taxon detail.'}
                else:result=photos(details[t['id']])
                manifest[x['id']]=result
                print(f"{start+1}/{len(todo)} {x['scientificName']}: {len(result['images'])} candidates",flush=True)
            temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(PATH)
            if any(error and 'RATE_LIMIT' in error for x,t,error in batch):break
if __name__=='__main__':main()
