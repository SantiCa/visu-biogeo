"""Apply reviewed answer-key facts without importing or publishing the PDFs.

Stable catalogue IDs and personal overrides are preserved. Uncertain answers
stay outside the occurrence list used by the scheduler.
"""
from pathlib import Path
import json,re,unicodedata,copy
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'[.,;:()]',' ',''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c)))).strip()

def slug(s):return re.sub('[^a-z0-9]+','-',norm(s)).strip('-')

def apply_evidence(catalog,history,exams,evidence):
    before_ids={x['id'] for x in catalog};before_pairs={(e['itemId'],e['year']) for e in history['events']}
    sources={y['year']:y['source'] for y in history['years']}
    for row in evidence['occurrences']:
        matches=[x for x in catalog if x['kind']==row['kind'] and norm(row['name']) in [norm(x['scientificName']),*[norm(a) for a in x.get('aliases',[])]]]
        if len(matches)>1:raise ValueError('Ambiguous catalogue match: '+row['name'])
        if matches:item=matches[0]
        else:
            item={'id':slug(row['name']),'scientificName':row['name'],'kind':row['kind'],'aliases':[],'sources':[],'sourcePages':[],'catalogStatus':'examen','notes':row.get('note','')}
            if any(x['id']==item['id'] for x in catalog):raise ValueError('ID collision: '+row['name'])
            catalog.append(item)
        for alias in row.get('aliases',[]):
            if alias not in item['aliases']:item['aliases'].append(alias)
        source_label='Examen Andalucía '+str(row['year'])
        if source_label not in item['sources']:item['sources'].append(source_label)
        lists=item.setdefault('studyLists',[])
        for label in row.get('studyLists',[]):
            label='Animales de la región mediterránea' if label=='Mamíferos' else label
            if label not in lists:lists.append(label)
        page={'file':row['sourceFile'],'page':row['solutionPage']}
        if page not in item['sourcePages']:item['sourcePages'].append(page)
        event={k:copy.deepcopy(v) for k,v in row.items() if k not in ['id','studyLists','aliases','kind','name']}
        event.update(itemId=item['id'],name=item['scientificName'],evidenceId=row['id'],source=sources[row['year']],note=(row.get('note','')+' Clave académica contrastada con la numeración del enunciado; no es un solucionario oficial de la administración.').strip())
        old=next((e for e in history['events'] if e.get('evidenceId')==row['id']),None)
        if not old and row['context']!='fotografia-con-clave-academica':
            old=next((e for e in history['events'] if e['itemId']==item['id'] and e['year']==row['year'] and not e.get('evidenceId')),None)
        if old:old.update(event)
        else:history['events'].append(event)
    for event in history['events']:
        if event['year']==2016:event['supportingDocuments']=[{'file':'EXAMEN PRÁCTICO DE ANDALUCÍA 2016.pdf','page':6}]
    history['reviewedAt']=evidence['reviewedAt'];history['answerKeyDocuments']=evidence['documents'];history['uncertainAnswers']=evidence['unresolved']
    history['limitations']=[
        'La serie 2006–2025 sigue siendo parcial; no localizar un año no demuestra que no hubiera convocatoria.',
        'Las frecuencias cuentan años distintos con evidencia de reconocimiento o clasificación nominal. Una misma entrada en dos opciones del mismo año cuenta una sola vez.',
        '2016 es una reconstrucción parcial. Las claves aportadas de 2018, 2021 y 2023 son académicas de PRECEGE, no solucionarios oficiales de la administración.',
        'Las identificaciones con interrogante y las alternativas incompatibles se conservan como pendientes y no aumentan la frecuencia.',
        'Se normalizan erratas y sinónimos contrastados conservando el nombre impreso, el documento y la página de la clave.'
    ]
    history['unresolved']=[f"{r['year']} {r['option']} {r['question']}: {' / '.join(r['proposedNames'])}. {r['reason']}" for r in evidence['unresolved']]+['2025: tomillo, escorpión común, sapillo pintojo, chorlitejo, Alisio común y escolopendra común: falta una clave inequívoca.']
    summaries={2016:'Recopilación parcial: 16 entradas; copia local contrastada, página 6.',2018:'Clave contrastada: 24 de las 25 fotos de B tienen una identificación única; encina B11 y cuatro nombres comunes de A conservan alternativas pendientes.',2021:'Clave contrastada: 12 de 15 seres vivos de A y 9 de 10 muestras de B identificados sin interrogante. Lista vegetal completada con Sphagnum subnitens; cuatro fotos permanecen dudosas.',2023:'Las 20 fotografías de A y B están vinculadas con la clave académica, incluidas B9 y B10 en la página 10 del enunciado.',2025:'Identificaciones nominales parciales; seis nombres comunes siguen pendientes de clave inequívoca.'}
    for year in history['years']:year['coverage']=summaries[year['year']]
    recognition=[{**e,'region':'Andalucía','evidenceType':'recognition','documentId':'andalucia-'+str(e['year'])} for e in history['events']]
    # Keep unrelated compilations in their existing position on regeneration.
    combined=[];inserted=False
    for event in exams.get('events',[]):
        if event.get('region')=='Andalucía' and event.get('evidenceType')!='context':
            if not inserted:combined.extend(recognition);inserted=True
        else:combined.append(event)
    if not inserted:combined.extend(recognition)
    exams['events']=combined
    exams['reviewedAt']=evidence['reviewedAt']
    for doc in exams['documents']:
        if doc.get('region')=='Andalucía':
            year=doc['year'];doc['coverage']=summaries[year];doc['answerKeys']=[r for r in evidence['documents'] if r['id']=='solution-'+str(year)];doc['uncertainAnswers']=[r for r in evidence['unresolved'] if r['year']==year]
            if year==2023:doc.pop('unresolved',None)
        doc['matchedEntries']=len({e['itemId'] for e in exams['events'] if e['documentId']==doc['id']})
    exams['limitations']=[s for s in exams.get('limitations',[]) if not s.startswith('Las imágenes sin clave')]
    note='Las dudas e incompatibilidades de las claves aportadas se muestran en la cobertura; no se convierten en prioridades automáticas.'
    if note not in exams['limitations']:exams['limitations'].append(note)
    pairs={(e['itemId'],e['year']) for e in history['events']}
    report={'date':evidence['reviewedAt'],'catalogEntries':len(catalog),'newEntryIds':sorted({x['id'] for x in catalog}-before_ids),'newItemYearOccurrences':len(pairs-before_pairs),'priorityEntries':len({i for i,y in pairs}),'itemYearOccurrences':len(pairs),'sourceEvidenceRows':len(history['events']),'uncertainQuestions':len(evidence['unresolved']),'years':{str(y):len({i for i,year in pairs if year==y}) for y in [2016,2018,2021,2023,2025]}}
    return report

def main():
    load=lambda name:json.loads((D/name).read_text(encoding='utf8'))
    catalog,history,exams,evidence=[load(n) for n in ['species.json','andalucia-priority.json','exams.json','solved-exam-evidence.json']]
    report=apply_evidence(catalog,history,exams,evidence)
    for name,obj in [('species.json',catalog),('andalucia-priority.json',history),('exams.json',exams)]: (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
    path=ROOT/'output/solved-exams-import.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
