"""Import photographs downloaded through the ordinary browser, still pending review."""
from pathlib import Path
import json
from PIL import Image,ImageOps
from review_batch import cachepath
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'data/asturnatura-images.json';RAW=ROOT/'tmp/asturnatura-browser.json'
def main():
    records=json.loads(RAW.read_text(encoding='utf8'));data=json.loads(PATH.read_text(encoding='utf8'))
    for id,r in records.items():
        import re
        family=r.get('family') if re.fullmatch(r'[A-Z][a-z]+(?:aceae|idae|eae|itae)',r.get('family') or '') else None
        entry=data.setdefault(id,{'images':[]});entry.update(source=r.get('source'),matchedName=r.get('matchedName'),family=family,familySource=r.get('source'),familyReviewStatus='pending',checkedAt='2026-10-25',collectionStatus=r.get('status'))
        for im in r.get('images',[]):
            src=Path(im['downloadedFile'])
            if not src.exists():continue
            out=cachepath(im['url'])
            if not out.exists():
                with Image.open(src) as photo:ImageOps.contain(photo.convert('RGB'),(1400,1400)).save(out,quality=93)
            clean={k:v for k,v in im.items() if k!='downloadedFile'};clean.update(status='pending',provider='Asturnatura',reviewNote='Pendiente de revisión visual antes de incorporarla al repaso.')
            if not any(x['key']==clean['key'] for x in entry['images']):entry['images'].append(clean)
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print('Asturnatura:',len(data),'fichas;',sum(len(x['images']) for x in data.values()),'fotos candidatas descargadas.')
if __name__=='__main__':main()
