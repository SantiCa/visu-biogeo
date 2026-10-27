"""Use documented standard-size Commons previews rather than original large files."""
from pathlib import Path
import json,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/commons-extra-images.json'
d=json.loads(path.read_text(encoding='utf8'))
for subject in d.values():
    for im in subject['images']:
        url=im.get('originalUrl') or im['url']
        url=urllib.parse.urlunsplit(urllib.parse.urlsplit(url)._replace(query='',fragment=''))
        m=re.match(r'https://upload.wikimedia.org/wikipedia/commons/([0-9a-f])/([0-9a-f]{2})/(.+)',url)
        if m:
            a,b,name=m.groups()
            im['originalUrl']=url
            im['url']=f'https://thumb.wikimedia.org/wikipedia/commons/thumb/{a}/{b}/{name}/960px-{name}'
path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
