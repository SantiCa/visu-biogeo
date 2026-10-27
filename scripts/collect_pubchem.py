"""Exact identified chemical records, 2D depictions and 3D conformers from PubChem."""
from urllib.parse import quote
import json
from collect_teaching import fetch,add,DATA
PATH=DATA/'pubchem-images.json'
# Entry id | unambiguous chemical record to retrieve. Generic vitamin classes are explicitly represented by one form.
ROWS='''molecula-adenina|adenine
molecula-citosina|cytosine
molecula-guanina|guanine
molecula-timina|thymine
molecula-uracilo|uracil
molecula-atp|adenosine triphosphate
molecula-beta-caroteno|beta-carotene
molecula-clorofila|chlorophyll a
molecula-colesterol|cholesterol
molecula-esfingosina|D-erythro-sphingosine
molecula-fructosa|D-fructose
molecula-gliceraldehido|D-glyceraldehyde
molecula-glucosa|D-glucose
molecula-hormona-esteroidea-testosterona|testosterone
molecula-isopreno-unidad-basica-de-los-terpenos|isoprene
molecula-lactosa|lactose
molecula-nadh|NADH
molecula-prostaglandina|prostaglandin E2
molecula-sacarosa|sucrose
molecula-vitamina-a-retinol|retinol
molecula-vitamina-b1-tiamina|thiamine
molecula-vitamina-b12-cobalamina|cyanocobalamin
molecula-vitamina-b2-riboflavina|riboflavin
molecula-vitamina-b3-niacina|niacin
molecula-vitamina-b5-acido-pantotenico|D-pantothenic acid
molecula-vitamina-b6-piridoxina|pyridoxine
molecula-vitamina-b8-biotina|biotin
molecula-vitamina-b9-acido-folico|folic acid
molecula-vitamina-c|L-ascorbic acid
molecula-vitamina-d|cholecalciferol
molecula-vitamina-e|alpha-tocopherol
molecula-vitamina-k-fitomenadiona|phylloquinone
molecula-acido-graso|palmitic acid
molecula-cerido-cera-de-abeja|myricyl palmitate
molecula-fosfolipido|1,2-dipalmitoyl-sn-glycero-3-phosphocholine
molecula-triacilglicerido|tripalmitin'''

def main():
    cat={x['id']:x for x in json.loads((DATA/'species.json').read_text(encoding='utf8'))};data=json.loads(PATH.read_text(encoding='utf8')) if PATH.exists() else {}
    for record in data.values():record['images']=[im for im in record.get('images',[]) if im.get('representation')=='3d' or 'image_size=300x300' in im['url']]
    for row in ROWS.splitlines():
        id,name=row.split('|');item=cat[id]
        if len(data.get(id,{}).get('images',[]))>=2:continue
        try:
            cids=json.loads(fetch('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+quote(name,safe='')+'/cids/JSON'))['IdentifierList']['CID']
            if len(cids)!=1:print(id,'ambiguous identifiers:',cids,flush=True);continue
            cid=cids[0];page='https://pubchem.ncbi.nlm.nih.gov/compound/'+str(cid)
            properties=json.loads(fetch(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/Title,MolecularFormula,IUPACName/JSON'))['PropertyTable']['Properties'][0]
            synonyms=json.loads(fetch(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON'))['InformationList']['Information'][0]['Synonym']
            if name.casefold() not in [s.casefold() for s in [properties.get('Title',''),*synonyms]]:raise ValueError('Query name not documented in record')
            data.setdefault(id,{'images':[]});data[id].update(queryName=name,cid=cid,properties=properties,source=page,matchedSynonym=name)
            for mode in ['2d','3d']:
                url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?record_type={mode}'+('&image_size=300x300' if mode=='2d' else '')
                try:
                    add(data,item,url,page,'PubChem / National Library of Medicine, NIH',f'Representación {mode.upper()} del registro PubChem CID {cid}, {properties["Title"]}. Fórmula: {properties["MolecularFormula"]}.','PubChem')
                    im=next(im for im in data[id]['images'] if im['url']==url);im.update(representation=mode,chemicalRecord=properties['Title'],chemicalCID=cid,license='PubChem / NLM: representación estructural del registro identificado; fuentes y condiciones en la ficha')
                except Exception as e:print(id,mode,str(e),flush=True)
            data[id]['complete']=True
            PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(item['scientificName'],cid,properties['Title'],len(data[id]['images']),flush=True)
        except Exception as error:print(id,type(error).__name__,str(error),flush=True)
if __name__=='__main__':main()
