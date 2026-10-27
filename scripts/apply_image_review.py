"""Apply explicit visual decisions; never infer approval from collection success.
Usage: python scripts/apply_image_review.py BATCH --approve 0,2,4 --reject 1,3
Or --approve-all-except N,... after every sheet of the frozen batch is inspected.
"""
from pathlib import Path
import argparse,json,hashlib,shutil,datetime
from PIL import Image
from review_crops import crop_image
from review_batch import cachepath
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';ASSETS=ROOT/'assets/reviewed';ASSETS.mkdir(parents=True,exist_ok=True)
def parse(s):return {int(n) for n in s.split(',') if n.strip()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('batch');ap.add_argument('--approve',default='');ap.add_argument('--reject',default='');ap.add_argument('--approve-all-except',default=None);ap.add_argument('--note',required=True);ap.add_argument('--crops');args=ap.parse_args()
    crops=json.loads(Path(args.crops).read_text(encoding='utf8')) if args.crops else {}
    batch=ROOT/'tmp/reviews'/args.batch;picks=json.loads((batch/'picks.json').read_text(encoding='utf8'));approved=parse(args.approve);rejected=parse(args.reject)
    if args.approve_all_except is not None:
        rejected|=parse(args.approve_all_except);approved|=set(range(len(picks)))-rejected
    if approved&rejected:raise RuntimeError('Contradictory decision')
    if (approved|rejected)-set(range(len(picks))):raise RuntimeError('Unknown image index')
    path=DATA/'curated-images.json';curated=json.loads(path.read_text(encoding='utf8'))
    decisions=[]
    for i in sorted(approved|rejected):
        p=picks[i];im={**p['image']};url=im['url'];status='approved' if i in approved else 'rejected';im.update(status=status,reviewedAt=datetime.date.today().isoformat(),reviewMethod='Correspondencia con la fuente y revisión visual',reviewNote=args.note,reviewBatch=args.batch)
        if status=='approved':
            im['description']=im.get('description','').replace('Revisión visual pendiente.','Correspondencia y encuadre revisados.').replace('Revisar rasgos diagnósticos y encuadre antes de aprobar.','Correspondencia y encuadre revisados.')
            src=cachepath(url)
            if not src.exists():raise RuntimeError(f'Image {i} was not downloaded')
            crop=crops.get(str(i));filename=hashlib.sha256((url+(json.dumps(crop,sort_keys=True) if crop else '')).encode()).hexdigest()[:20]+'.jpg'
            if crop:
                with Image.open(src) as image:crop_image(image,crop).convert('RGB').save(ASSETS/filename,quality=93)
                im.update(crop=crop,reference=(im.get('reference','')+' · Recorte docente: se conserva la región identificada y se excluyen rótulos o paneles ajenos.').strip(' ·'))
            else:shutil.copyfile(src,ASSETS/filename)
            im.update(originalUrl=url,url='./assets/reviewed/'+filename)
        arr=curated.setdefault(p['itemId'],{'images':[]})['images']
        key=lambda x:x.get('originalUrl') or x['url']
        old=next((j for j,x in enumerate(arr) if key(x)==url),None)
        if old is not None:arr[old]=im
        else:arr.append(im)
        decisions.append({'index':i,'itemId':p['itemId'],'url':url,'status':status})
    path.write_text(json.dumps(curated,ensure_ascii=False,indent=2),encoding='utf8')
    audit=DATA/'image-review-log.json';log=json.loads(audit.read_text(encoding='utf8')) if audit.exists() else []
    log.append({'batch':args.batch,'picksSha256':hashlib.sha256((batch/'picks.json').read_bytes()).hexdigest(),'date':datetime.date.today().isoformat(),'note':args.note,'decisions':decisions})
    audit.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
    print(len(approved),'approved,',len(rejected),'rejected',flush=True)
if __name__=='__main__':main()
