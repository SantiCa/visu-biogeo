"""Curated occurrence evidence. Named classification != photographic VISU.
No occurrence is inferred merely from a picture without an answer key.
"""
from pathlib import Path
import json,re,unicodedata
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
def slug(s): return re.sub('[^a-z0-9]+','-',norm(s)).strip('-')
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
urls={
2016:'https://www.precege.com/wp-content/uploads/2024/02/EXAMEN-PRaCTICO-DE-ANDALUCiA-2016-revision-2024.pdf',
2018:'https://www.precege.com/download/examen-practico-oficial-biologia-y-geologia-andalucia-2018/',
2021:'https://www.precege.com/download/examen-andalucia-2021/',
2023:'https://www.juntadeandalucia.es/educacion/portales/documents/20123/922823/590008%20BIOLOGI%C2%BFA%20Y%20GEOLOGI%C2%BFA%20P.E.S..pdf/ca83ea46-ceec-786d-44ce-764d7b30fb63',
2025:'https://www.juntadeandalucia.es/educacion/portales/documents/20123/2642358/590-008%20BIOLOGIA%20Y%20GEOLOGIA.pdf/3abbc918-c9e5-e9c0-0430-200bd7337a9a'}
catalog=json.loads((DATA/'species.json').read_text(encoding='utf8'))
events=[]
def record(year,names,page,kind,context='clasificacion',note=''):
    for name in names.split('|'):
        item=next((x for x in catalog if norm(name) in [norm(x['scientificName']),*[norm(a) for a in x.get('aliases',[])]] and x['kind']==kind),None)
        if item is None:
            item={'id':slug(name),'scientificName':name,'kind':kind,'aliases':[],'sources':[f'Examen Andalucía {year}'],'sourcePages':[], 'catalogStatus':'examen','notes':note}
            if any(x['id']==item['id'] for x in catalog): item['id']=kind+'-'+item['id']
            catalog.append(item)
        events.append({'itemId':item['id'],'name':item['scientificName'],'year':year,'page':page,'context':context,'source':urls[year],'sourceType':'reconstruccion-academia' if year==2016 else 'enunciado-oficial','note':note})

record(2016,'Marga|Diorita|Conglomerado pudinga|Ofita|Gabro|Cuarcita',4,'roca','mixto','Recuerdo parcial publicado por PRECEGE; no distingue lista escrita de fotografía.')
record(2016,'Taxus baccata|Silene sp.|Berberis thunbergii|Trivia sp.|Pecten sp.|Forficula auricularia|Graphosoma semipunctatum|Ephedra fragilis|Natica vitellus|Cistus albidus',4,'organismo','mixto','Recuerdo parcial publicado por PRECEGE; no es un solucionario oficial.')
record(2018,'Esquisto|Grauvaca|Basalto|Arcosa|Antracita|Diabasa|Dolomía|Peridotita',4,'roca')
record(2018,'Cuarzo|Berilo|Casiterita|Malaquita|Aragonito|Fluorita|Hematites|Galena',4,'mineral',note='El original usa Oligisto para Hematites.')
# Only unambiguous common-name mappings; vague names such as Abeja, Enebro,
# Garrapata and Mariquita do NOT become invented species occurrences.
record(2018,'Mantis religiosa|Abies pinsapo|Helianthus annuus|Mentha pulegium|Cercis siliquastrum|Punica granatum',5,'organismo','nombre-comun','Asignación desde nombre común del enunciado; no fotografía ni solucionario oficial.')
record(2021,'Esquisto|Gabro|Andesita|Trípoli',5,'roca',note='Diatomita en el original; sinónimo de Trípoli en el catálogo.')
record(2021,'Sillimanita|Glaucofana|Apatito|Silvina',5,'mineral')
record(2021,'Paradoxides|Hildoceras',5,'fosil',note='Hyldoceras en el original; grafía normalizada a Hildoceras.')
record(2021,'Lycopodium clavatum|Ephedra fragilis|Rubus fruticosus|Chamaerops humilis|Osmunda regalis|Quercus canariensis|Abies pinsapo|Retama monosperma|Marchantia polymorpha|Tamarix africana|Juniperus oxycedrus|Fritillaria lusitanica|Isoetes velatum|Borago officinalis|Celtis australis|Polypodium vulgare|Populus alba|Secale cereale|Taxus baccata',10,'organismo',note='Lista escrita. Se normalizan Licopodium y Osmundia. Sphagnum subtinens se deja pendiente por grafía dudosa.')
record(2023,'Azufre|Celestina|Malaquita|Silvina',5,'mineral')
record(2023,'Conglomerado brecha|Diorita|Filita|Gabro|Gneis|Granito',5,'roca')
record(2023,'Aragonito|Fluorita|Hematites|Olivino',8,'mineral')
record(2023,'Arenisca|Dolomía|Granodiorita|Mármol|Pumita|Sienita',8,'roca')
record(2025,'Fluorita|Halita|Pirita|Galena|Cuarzo|Yeso|Cinabrio|Magnetita|Baritina|Cromita',3,'mineral','formula','Identificación por fórmula química, no por imagen.')
record(2025,'Xiphias gladius|Salvia rosmarinus|Zerynthia rumina|Prunus avium|Adiantum capillus-veneris|Spatula clypeata|Genetta genetta|Actias isabellae|Upupa epops|Quercus coccifera|Pancratium maritimum|Cyanistes caeruleus|Macrolepiota procera|Oxyura leucocephala',11,'organismo','nombre-comun','Correspondencia desde nombre común; bloque IV A/B, páginas PDF 11–12. Se omiten nombres ambiguos sin clave oficial.')
for e in events:
    if e['year']==2025 and e['name'] in ['Spatula clypeata','Genetta genetta','Actias isabellae','Upupa epops','Quercus coccifera','Pancratium maritimum','Cyanistes caeruleus','Macrolepiota procera','Oxyura leucocephala']: e['page']=12
coverage={'reviewedAt':'2026-10-24','requestedPeriod':[2006,2025],'years':[{'year':y,'source':u,'coverage':'parcial: nombres escritos; fotos sin clave no contabilizadas'} for y,u in urls.items()], 'limitations':['No se ha localizado una serie completa y verificable de 2006–2025. Años no localizados no significan ausencia de convocatoria ni de especie.','Las frecuencias cuentan convocatorias distintas con evidencia nominal de reconocimiento/clasificación; NO son frecuencias de fotografías exclusivamente.','2016 es una reconstrucción parcial de academia. 2018/2021 son copias del enunciado oficial. 2023/2025 proceden de la Junta.','No se asigna nombre científico a fotos sin solucionario confirmado, ni a nombres comunes ambiguos.'], 'unresolved':['Fotos 2018 opción B','Fotos 2021 opciones A y B','Fotos 2023 opciones A y B','2021: Sphagnum subtinens','2025: tomillo, escorpión común, sapillo pintojo, chorlitejo, Alisio común, escolopendra común'], 'events':events}
if (DATA/'solved-exam-evidence.json').exists():
    from import_solved_exams import apply_evidence
    exams=json.loads((DATA/'exams.json').read_text(encoding='utf8'))
    apply_evidence(catalog,coverage,exams,json.loads((DATA/'solved-exam-evidence.json').read_text(encoding='utf8')))
    (DATA/'exams.json').write_text(json.dumps(exams,ensure_ascii=False,indent=2),encoding='utf8')
(DATA/'andalucia-priority.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
(DATA/'species.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
print(f'{len(events)} evidencias; {len(set(e["itemId"] for e in events))} fichas con historial; {len(catalog)} fichas en total')
