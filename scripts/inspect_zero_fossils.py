import json
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'data';a=json.loads((D/'image-audit.json').read_text(encoding='utf8'));print([(x['id'],x['name']) for x in a['allMissingPairs'] if x['kind']=='fosil' and not x['approvedImages']])
