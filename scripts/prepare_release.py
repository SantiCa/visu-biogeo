"""Copy only distributable app files; no browser accounts, backups or credentials.

The public Supabase key is expected in config.js. Session tokens are never files
in this package and project-admin files are not part of the web directory.
"""
import argparse,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def public_files():
    files=set(re.findall(r'''['"]\./([^'"\n]+)['"]''',(ROOT/'sw.js').read_text(encoding='utf8')))
    files.update(['sw.js','icons/icon.ico','vendor/LICENSE-supabase.txt','vendor/sources.json'])
    for row in json.loads((ROOT/'data/curated-images.json').read_text(encoding='utf8')).values():
        for im in row.get('images',[]):
            if im['status']=='approved' and im['url'].startswith('./assets/reviewed/'):
                files.add(im['url'][2:])
    return sorted(files)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--target',required=True);args=parser.parse_args()
    destination=Path(args.target).resolve()
    if ROOT not in destination.parents or destination==ROOT:raise ValueError('Release must be a distinct project subdirectory')
    files=public_files();copied=0
    for relative in files:
        source=(ROOT/relative).resolve()
        if ROOT not in source.parents or not source.is_file():raise ValueError('Missing or invalid app file: '+relative)
        target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and target.stat().st_size==source.stat().st_size and target.stat().st_mtime_ns==source.stat().st_mtime_ns:continue
        shutil.copy2(source,target);copied+=1
    print(json.dumps({'files':len(files),'copied':copied,'target':str(destination),'bytes':sum((ROOT/f).stat().st_size for f in files)}))

if __name__=='__main__':main()
