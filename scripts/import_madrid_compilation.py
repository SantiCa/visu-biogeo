"""Import reviewed factual names from a local, undated academic compilation.

No PDF content, invented years, frequencies, or fuzzy taxon matches are shipped.
"""
from pathlib import Path
import json,re,unicodedata,copy
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
DOCUMENT_ID='madrid-varios-sin-fecha'

def norm(value):
    value=''.join(c for c in unicodedata.normalize('NFD',value.casefold()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',re.sub(r'[.,;:()]',' ',value)).strip()

def key(value):return re.sub(r'\s+sp$','',norm(value))
def slug(value):return re.sub('[^a-z0-9]+','-',norm(value)).strip('-')

def apply_compilation(catalog,exams,evidence):
    before={x['id'] for x in catalog};events=[];unresolved=[]
    for row in evidence['rows']:
        if row['status']!='accepted':unresolved.append(copy.deepcopy(row));continue
        for target in row['targets']:
            matches=[x for x in catalog if x['kind']==target['kind'] and key(target['name']) in [key(n) for n in [x['scientificName'],*x.get('aliases',[])]]]
            literal=[x for x in matches if norm(x['scientificName'])==norm(target['name'])]
            if len(literal)==1:matches=literal
            if target.get('existingId'):matches=[x for x in catalog if x['id']==target['existingId']]
            if len(matches)>1:raise ValueError('Ambiguous reviewed target '+target['name'])
            if matches:item=matches[0]
            else:
                id=('estructura-' if target['kind']=='estructura' else '')+slug(target['name'])
                if any(x['id']==id for x in catalog):raise ValueError('ID collision: '+id)
                item={'id':id,'scientificName':target['name'],'kind':target['kind'],'aliases':[],'sources':[],'sourcePages':[],'catalogStatus':'recopilacion-sin-fecha','notes':target.get('note','')}
                catalog.append(item)
            if target.get('correctExistingName'):item['scientificName']=target['name']
            for alias in target.get('aliases',[]):
                if alias not in item['aliases']:item['aliases'].append(alias)
            source='Examen Madrid · recopilación sin fecha'
            if source not in item['sources']:item['sources'].append(source)
            page={'file':evidence['document']['filename'],'page':row['page']}
            if page not in item['sourcePages']:item['sourcePages'].append(page)
            lists=item.setdefault('studyLists',[])
            for label in target['studyLists']:
                if label not in lists:lists.append(label)
            if target.get('parentTaxon'):item['parentTaxon']=target['parentTaxon']
            event={'documentId':DOCUMENT_ID,'itemId':item['id'],'name':item['scientificName'],'region':'Madrid','year':None,'evidenceType':'recognition','sourceType':'recopilacion-academia-sin-fecha','context':'recopilacion-nominal-sin-fecha','page':row['page'],'sourcePage':row['page'],'sourceFile':evidence['document']['filename'],'sourceName':row['raw'],'sourceSection':row['section'],'evidenceId':row['id']+'::'+item['id'],'priorityEligible':False,'note':row.get('note','')}
            events.append(event)
    exams['events']=[e for e in exams['events'] if e['documentId']!=DOCUMENT_ID]+events
    doc={'id':DOCUMENT_ID,'region':'Madrid','year':None,'variant':'Recopilación académica','official':False,'sourceType':'recopilacion-academia-sin-fecha','sourceFile':evidence['document']['filename'],'sourceMetadata':evidence['document'],'matchedEntries':len({e['itemId'] for e in events}),'coverage':f"Recopilación PRECEGE de varios años, sin fechas ni atribución por convocatoria. {len({e['itemId'] for e in events})} entradas vinculadas con página de procedencia; no permite calcular frecuencias. {len(unresolved)} denominaciones ambiguas se mantienen pendientes.",'uncertainAnswers':unresolved}
    exams['documents']=[d for d in exams['documents'] if d['id']!=DOCUMENT_ID]+[doc]
    exams['reviewedAt']=evidence['reviewedAt']
    note='La recopilación de Madrid sin fecha no acredita años concretos ni frecuencias; los restos anatómicos se estudian como entradas independientes.'
    if note not in exams['limitations']:exams['limitations'].append(note)
    return {'date':evidence['reviewedAt'],'sourceRows':len(evidence['rows']),'acceptedSourceRows':sum(r['status']=='accepted' for r in evidence['rows']),'unresolvedRows':len(unresolved),'evidenceRows':len(events),'matchedEntries':doc['matchedEntries'],'newEntryIds':sorted({x['id'] for x in catalog}-before),'catalogEntries':len(catalog),'datedOccurrencesAdded':0,'andaluciaPriorityChanged':False}

def main():
    load=lambda name:json.loads((D/name).read_text(encoding='utf8'))
    catalog,exams,evidence=[load(n) for n in ['species.json','exams.json','madrid-compilation-evidence.json']]
    report=apply_compilation(catalog,exams,evidence)
    for name,obj in [('species.json',catalog),('exams.json',exams)]:
        (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
    (ROOT/'output/madrid-compilation-import.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
