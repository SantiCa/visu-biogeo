"""Prepare a small versioned Site source; approved binary media is uploaded to R2."""
from pathlib import Path
import hashlib,json,shutil,mimetypes
from prepare_release import ROOT,public_files
SITE=ROOT/'hosting/visu-biogeo-media'

def main():
    files={};total=0
    for relative in public_files():
        source=ROOT/relative;raw=source.read_bytes();hash=hashlib.sha256(raw).hexdigest();total+=len(raw)
        suffix=source.suffix.lower();mime={'.mjs':'text/javascript; charset=utf-8','.js':'text/javascript; charset=utf-8','.html':'text/html; charset=utf-8','.json':'application/json; charset=utf-8','.webmanifest':'application/manifest+json','.css':'text/css; charset=utf-8','.txt':'text/plain; charset=utf-8'}.get(suffix,mimetypes.guess_type(source)[0] or 'application/octet-stream')
        files[relative]={'hash':hash,'bytes':len(raw),'mime':mime}
        if not relative.startswith('assets/reviewed/'):
            dest=SITE/'web'/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (SITE/'media-manifest.json').write_text(json.dumps({'digest':digest,'files':files},ensure_ascii=False,separators=(',',':')),encoding='utf8')
    (SITE/'worker').mkdir(exist_ok=True);shutil.copy2(ROOT/'desktop/media-worker.mjs',SITE/'worker/index.js')
    manifest=SITE/'.openai/hosting.json';data=json.loads(manifest.read_text(encoding='utf8'));data.pop('static',None);data['r2']='BUCKET';data['d1']=None;manifest.write_text(json.dumps(data,indent=2),encoding='utf8')
    print(json.dumps({'files':len(files),'sourceBytes':sum((SITE/'web'/p).stat().st_size for p in files if not p.startswith('assets/reviewed/')),'mediaBytes':total,'digest':digest}))

if __name__=='__main__':main()
