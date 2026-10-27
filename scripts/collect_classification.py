"""Broad study groups from documented taxon lineages, never from guessed name endings."""
from pathlib import Path
import json,time
from collect_taxonomy import get,save
D=Path(__file__).resolve().parents[1]/'data';CACHE=D/'classification-source-cache.json';PATH=D/'classification.json'
GROUPS=[
 ('Mammalia','Mamíferos'),('Aves','Aves'),('Amphibia','Anfibios'),('Reptilia','Reptiles'),
 ('Actinopterygii','Peces óseos'),('Sarcopterygii','Peces óseos'),('Chondrichthyes','Peces cartilaginosos'),('Elasmobranchii','Peces cartilaginosos'),('Petromyzonti','Lampreas'),
 ('Insecta','Insectos'),('Arachnida','Arácnidos'),('Myriapoda','Miriápodos'),('Entognatha','Entognatos'),('Crustacea','Crustáceos'),
 ('Malacostraca','Crustáceos'),('Thecostraca','Crustáceos'),('Ostracoda','Crustáceos'),('Branchiopoda','Crustáceos'),('Copepoda','Crustáceos'),
 ('Mollusca','Moluscos'),('Annelida','Anélidos'),('Platyhelminthes','Platelmintos'),('Nematoda','Nematodos'),
 ('Echinodermata','Equinodermos'),('Porifera','Poríferos'),('Cnidaria','Cnidarios'),('Bryozoa','Briozoos'),('Ectoprocta','Briozoos'),
 ('Nemertea','Nemertinos'),('Nematomorpha','Nematomorfos'),('Rotifera','Rotíferos'),('Chaetognatha','Quetognatos'),('Priapulida','Priapúlidos'),('Sipuncula','Sipuncúlidos'),
 ('Tardigrada','Tardígrados'),('Onychophora','Onicóforos'),('Tunicata','Tunicados'),('Cephalochordata','Cefalocordados'),
 ('Pinopsida','Coníferas'),('Gnetopsida','Gnetófitas'),('Cycadopsida','Cícadas'),('Ginkgoopsida','Ginkgo'),
 ('Polypodiopsida','Helechos'),('Lycopodiopsida','Licófitos'),('Bryophyta','Musgos'),('Marchantiophyta','Hepáticas'),('Anthocerotophyta','Antocerotas'),
 ('Magnoliopsida','Plantas con flor'),('Liliopsida','Plantas con flor'),('Angiospermae','Plantas con flor'),
 ('Rhodophyta','Algas rojas'),('Chlorophyta','Algas verdes'),('Charophyta','Carófitas'),('Phaeophyceae','Algas pardas'),
 ('Bacillariophyta','Diatomeas'),('Bacillariophyceae','Diatomeas'),('Dinoflagellata','Dinoflagelados'),('Dinophyceae','Dinoflagelados'),
 ('Fungi','Hongos'),('Bacteria','Bacterias'),('Archaea','Arqueas'),('Arthropoda','Otros artrópodos'),
 ('Ciliophora','Ciliados'),('Apicomplexa','Apicomplejos'),('Euglenozoa','Euglenozoos'),('Amoebozoa','Amebozoos'),('Foraminifera','Foraminíferos')
]
def group(names):return next((label for name,label in GROUPS if name in names),None)

def main():
    cat=json.loads((D/'species.json').read_text(encoding='utf8'));tax=json.loads((D/'taxonomy.json').read_text(encoding='utf8'));cache=json.loads(CACHE.read_text(encoding='utf8')) if CACHE.exists() else {};data={}
    ids=sorted({str(tax[x['id']]['familyTaxonId']) for x in cat if x['kind']=='organismo' and tax.get(x['id'],{}).get('familyTaxonId')})
    missing=[id for id in ids if id not in cache]
    for start in range(0,len(missing),20):
        try:
            results=get('https://api.inaturalist.org/v1/taxa/'+','.join(missing[start:start+20]))['results']
            for t in results:
                if t.get('rank')!='family':continue
                lineage=[a['name'] for a in t.get('ancestors',[])]+[t['name']]
                cache[str(t['id'])]={'family':t['name'],'lineage':lineage,'group':group(lineage),'source':'https://www.inaturalist.org/taxa/'+str(t['id'])}
            save(CACHE,cache);print(min(start+20,len(missing)),'/',len(missing),'familias contrastadas',flush=True);time.sleep(1.5)
        except Exception as error:print('Consulta detenida:',error,flush=True);break
    for record in cache.values():record['group']=group(record['lineage'])
    save(CACHE,cache)
    for item in cat:
        if item['kind']!='organismo':continue
        t=tax.get(item['id'],{});family=cache.get(str(t.get('familyTaxonId')))
        if not family:
            matches=[r for r in cache.values() if r['family']==t.get('family') and r.get('group')]
            if len({r['group'] for r in matches})==1:family=matches[0]
        if family and family['family']==t.get('family') and family.get('group'):
            data[item['id']]={**family,'checkedAt':'2026-10-25'}
        elif 'gbif.org/species/' in t.get('source',''):
            key='gbif:'+t['source'].rsplit('/',1)[-1]
            if key not in cache:
                try:
                    result=get('https://api.gbif.org/v1/species/'+key.split(':')[1])
                    if result.get('family')==t.get('family'):
                        lineage=[result.get(k) for k in ['kingdom','phylum','class','order','family'] if result.get(k)]
                        cache[key]={'family':t['family'],'lineage':lineage,'group':group(lineage),'source':t['source']};save(CACHE,cache)
                    time.sleep(1)
                except Exception as error:print(item['scientificName'],error,flush=True)
            if cache.get(key,{}).get('group'):data[item['id']]={**cache[key],'checkedAt':'2026-10-25'}
    save(PATH,data);print(len(data),'organismos con agrupación documentada',flush=True)
if __name__=='__main__':main()
