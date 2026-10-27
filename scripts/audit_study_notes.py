"""Validate note coverage and distinguish filled fields from complete etymological research."""
import json,re
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date
D=Path(__file__).resolve().parents[1]/'data'
catalog={x['id']:x for x in json.loads((D/'species.json').read_text(encoding='utf8'))}
notes=json.loads((D/'study-notes.json').read_text(encoding='utf8'));families=json.loads((D/'family-notes.json').read_text(encoding='utf8'))
priority={x['itemId'] for x in json.loads((D/'andalucia-priority.json').read_text(encoding='utf8'))['events']}
biological={id for id in priority if catalog[id]['kind']=='organismo'}
errors=[]
for id,note in notes.items():
    if id not in catalog:errors.append('Unknown entry: '+id)
    if not note.get('description') or not note.get('diagnostics') or not note.get('sources'):errors.append('Incomplete descriptive note: '+id)
    for s in note.get('sources',[]):
        if urlsplit(s.get('url','')).scheme not in ['http','https']:errors.append('Invalid source: '+id)
pending=[id for id,n in notes.items() if not n.get('etymology') or re.search('pendiente|contrastar|requiere contraste',n['etymology'],re.I)]
audit={'date':date.today().isoformat(),'catalogEntries':len(catalog),'descriptiveProfiles':len(notes),'withoutDescriptiveProfile':len(catalog)-len(notes),'biologicalPriorityProfiles':len(biological&notes.keys()),'biologicalPriorityEntries':len(biological),'profilesWithCommonName':sum(bool(n.get('commonName')) for n in notes.values()),'profilesWithMnemonic':sum(bool(n.get('mnemonic')) for n in notes.values()),'familyNameConstructionNotes':len(families),'profilesWithWhollyOrPartlyPendingEtymology':len(pending),'etymologyPendingIds':pending,'errors':errors,'scope':'Una ficha descriptiva no implica etimología completa. El texto indica las partes pendientes y no convierte asociaciones de memoria en explicaciones lingüísticas. Las notas de familia explican su construcción nomenclatural; las raíces remotas solo se completan con referencia.'}
(D/'study-notes-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in audit.items() if k!='etymologyPendingIds'},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
