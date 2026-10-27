"""Restore non-taxonomic VISU subjects, preserving original IDs/progress.
Never feed mineral, histology, landscape or fossil-genus names to GBIF.
Outputs source page references and an explicit audit report.
"""
from pathlib import Path
import json, re, unicodedata
from pypdf import PdfReader
from extract_species import PDF_DIRECTORY

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))
def slug(s): return re.sub('[^a-z0-9]+', '-', norm(s)).strip('-')
def write(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

seed = DATA / 'taxa-baseline.json'
if not seed.exists(): write(seed, json.loads((DATA/'species.json').read_text(encoding='utf-8')))
items = {x['id']: {**x, 'kind':'organismo', 'aliases':[], 'sourcePages':[], 'catalogStatus':'importado'} for x in json.loads(seed.read_text(encoding='utf-8'))}
pages_by_file = {f.name:[p.extract_text() or '' for p in PdfReader(f).pages] for f in PDF_DIRECTORY.glob('*.pdf')}
for x in items.values():
    for source in x['sources']:
        for i, text in enumerate(pages_by_file.get(source, [])):
            if norm(x['scientificName']) in norm(re.sub(r'\s+', ' ',text)):
                x['sourcePages'].append({'file':source,'page':i+1})

def add(name, kind, file, page, aliases=None, notes=''):
    name=re.sub(r'\s+', ' ',name).strip(' .,:;')
    if not name: return
    id=slug(name) if kind not in ('lamina','estructura','molecula') else slug(kind+'-'+name)
    if id in items and items[id]['kind']!=kind: id=kind+'-'+id
    x=items.setdefault(id, {'id':id,'scientificName':name,'kind':kind,'aliases':aliases or [],'sources':[], 'sourcePages':[], 'notes':notes,'catalogStatus':'importado'})
    if file not in x['sources']: x['sources'].append(file)
    ref={'file':file,'page':page}
    if ref not in x['sourcePages']: x['sourcePages'].append(ref)

minerals='Listado MINERALES VISU I II III.pdf'
for p,text in enumerate(pages_by_file[minerals],1):
    for m in re.finditer(r'^\s*-\s*([^\n]+)',text,re.M):
        head=re.split(r'[.(,:]|\s+(?:α-|Ca5|Pb5)',m[1])[0].strip()
        parts=re.split(r'\s+o\s+',head)
        add(parts[0],'mineral',minerals,p,parts[1:])
add('Ocre amarillo','mineral',minerals,2,notes='Material terroso natural de limonita y goethita; no es una especie mineral única. La ficha debe mostrar la muestra geológica, no pintura ni objetos de ese color.')
add('Ocre rojo','mineral',minerals,2,notes='Material terroso ferruginoso; agregado, no una especie mineral única.')

rockfile='Listado visu de rocas.pdf'
for p,text in enumerate(pages_by_file[rockfile],1):
    for m in re.finditer(r'^\s*\*\.?\s*(.+)',text,re.M):
        head=re.split(r'[.(]|,\s*variedad',m[1])[0].strip(' .')
        if head.startswith('Conglomerado,'): head=head.replace('Conglomerado,','Conglomerado')
        parts=re.split(r'\s+o\s+|,',head)
        add(parts[0],'roca',rockfile,p,[s.strip() for s in parts[1:]])

for filename,pages in pages_by_file.items():
    lower=norm(filename)
    if 'lamina delgada' in lower: kind='lamina'
    elif 'geomorfologia' in lower: kind='relieve'
    elif 'nubes' in lower: kind='nube'
    elif 'histologia' in lower or 'estructuras microscopicas' in lower or 'estructuras de insectos' in lower: kind='estructura'
    elif 'moleculas' in lower: kind='molecula'
    else: continue
    for p,text in enumerate(pages,1):
        for raw in text.splitlines():
            name=raw.strip()
            if not name or re.match(r'^(\d+\s*$|www\.|LISTADO|VISU|GEOMORFOLOG)',name,re.I): continue
            if name.isupper() and name not in {'ATP','NADH','FADH','GUANINA','CITOSINA','URACILO','TIMINA','ADENINA'}: continue
            if kind=='lamina':
                if not re.match(r'^\d+\.',name): continue
                name=re.sub(r'^\d+\.\s*','',name)
            if name.startswith(('ribosómico)', 'Transcripción de los genes')): continue
            add(name,kind,filename,p)
    if 'estructuras microscopicas' in lower:
        add('Transcripción de genes del organizador nucleolar','estructura',filename,1)

fossil='Listado de visu de fósiles.pdf'
for p,text in enumerate(pages_by_file[fossil],1):
    for genus in re.findall(r'\bG\.\s*([A-Z][a-z]+)',text): add(genus,'fosil',fossil,p)
for name,p in [('Estromatolitos',1),('Cruziana',4),('Anomalocaris',4),('Tiktaalik',5),('Icnita',8),('Coprolito',8)]: add(name,'fosil',fossil,p)
for x in items.values():
    if x['kind']=='organismo' and x['sources']==[fossil]: x['kind']='fosil'

# Explicitly accepted scientific synonyms, not fuzzy spelling acceptance.
aliases={'Salvia rosmarinus':['Rosmarinus officinalis'], 'Actias isabellae':['Graellsia isabellae'], 'Spatula clypeata':['Anas clypeata'], 'Cyanistes caeruleus':['Parus caeruleus']}
for x in items.values(): x['aliases']=list(dict.fromkeys(x['aliases']+aliases.get(x['scientificName'],[])))

write(DATA/'species.json',sorted(items.values(),key=lambda x:norm(x['scientificName'])))
counts={k:sum(x['kind']==k for x in items.values()) for k in sorted({x['kind'] for x in items.values()})}
report={'generated':'2026-10-24','sourceFiles':len(pages_by_file),'entries':len(items),'byKind':counts,'note':'Taxones heredados de extracción previa; no equivale a revisión taxonómica exhaustiva ni de imágenes. Los sujetos no taxonómicos se importan de sus listas por separado. Variantes dentro de descripciones pueden requerir fichas adicionales.', 'sourceCoverage':{f:sum(f in x['sources'] for x in items.values()) for f in pages_by_file}}
write(DATA/'catalog-audit.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
