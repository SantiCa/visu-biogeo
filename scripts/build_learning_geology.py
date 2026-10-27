"""Explicit educational mineral chemistry and rock genesis; no formula for a mixture.

The mineral tree declares its chemical/structural scheme. Species formulae are
checked against the Mineralogical Society of America's Handbook of Mineralogy.
Group formulae and nonstoichiometric materials are not marked as fixed answers.
"""
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,time,re
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';C=ROOT/'tmp/mineral-handbook';C.mkdir(exist_ok=True)
DAY=date.today().isoformat()
CLASSES={1:'Elementos nativos y afines',2:'Sulfuros y sulfosales',3:'Haluros',4:'Óxidos e hidróxidos',5:'Carbonatos y nitratos',6:'Boratos',7:'Sulfatos y afines',8:'Fosfatos, arseniatos y vanadatos',9:'Silicatos'}
# id | formula (ASCII) | principal class | structural subgroup | Handbook entry
MINERALS='''albita|NaAlSi3O8|9|Tectosilicatos / feldespatos|albite
andalucita|Al2SiO5|9|Nesosilicatos|andalusite
apatito|Ca5(PO4)3(F,Cl,OH)|8|Grupo del apatito|apatite
aragonito|CaCO3|5|Carbonatos anhidros|aragonite
arsenopirita|FeAsS|2|Sulfarseniuros|arsenopyrite
augita|(Ca,Na)(Mg,Fe,Al,Ti)(Si,Al)2O6|9|Inosilicatos / piroxenos|augite
azufre|S|1|No metales|sulfur
azurita|Cu3(CO3)2(OH)2|5|Carbonatos con aniones adicionales|azurite
baritina|BaSO4|7|Sulfatos anhidros|barite
berilo|Be3Al2Si6O18|9|Ciclosilicatos|beryl
biotita|K(Mg,Fe)3AlSi3O10(OH,F)2|9|Filosilicatos / micas|biotite
bismuto|Bi|1|Metales y semimetales|bismuth
blenda|ZnS|2|Sulfuros|sphalerite
calcantita|CuSO4·5H2O|7|Sulfatos hidratados|chalcanthite
calcedonia|SiO2|4|Sílice / variedad microcristalina de cuarzo|quartz
calcita|CaCO3|5|Carbonatos anhidros|calcite
calcopirita|CuFeS2|2|Sulfuros|chalcopyrite
caolinita|Al2Si2O5(OH)4|9|Filosilicatos / arcillas|kaolinite
carborundo|SiC|1|Carburos / material sintético|moissanite
carnalita|KMgCl3·6H2O|3|Haluros hidratados|carnallite
casiterita|SnO2|4|Óxidos|cassiterite
celestina|SrSO4|7|Sulfatos anhidros|celestine
cianita|Al2SiO5|9|Nesosilicatos|kyanite
cinabrio|HgS|2|Sulfuros|cinnabar
clorita|(Mg,Fe,Al)6(Si,Al)4O10(OH)8|9|Filosilicatos / grupo de la clorita|clinochlore
cobre|Cu|1|Metales|copper
cordierita|(Mg,Fe)2Al4Si5O18|9|Ciclosilicatos|cordierite
corindon|Al2O3|4|Óxidos|corundum
crisocola|(Cu,Al)2H2Si2O5(OH)4·nH2O|9|Silicatos de cobre hidratados|chrysocolla
cromita|FeCr2O4|4|Óxidos / grupo de la espinela|chromite
cuarzo|SiO2|4|Sílice|quartz
diamante|C|1|No metales / alótropos del carbono|diamond
dolomita|CaMg(CO3)2|5|Carbonatos anhidros|dolomite
epidota|Ca2Al2Fe(SiO4)(Si2O7)O(OH)|9|Sorosilicatos|epidote
eritrina|Co3(AsO4)2·8H2O|8|Arseniatos hidratados|erythrite
espinela|MgAl2O4|4|Óxidos / grupo de la espinela|spinel
espodumena|LiAlSi2O6|9|Inosilicatos / piroxenos|spodumene
estaurolita|Fe2Al9Si4O23(OH)|9|Nesosilicatos|staurolite
flogopita|KMg3(AlSi3O10)(OH,F)2|9|Filosilicatos / micas|phlogopite
fluorita|CaF2|3|Haluros anhidros|fluorite
fuchsita|K(Al,Cr)2(AlSi3O10)(OH)2|9|Filosilicatos / variedad cromífera de moscovita|muscovite
galena|PbS|2|Sulfuros|galena
goethita|FeO(OH)|4|Hidróxidos y oxihidróxidos|goethite
grafito|C|1|No metales / alótropos del carbono|graphite
granate|X3Y2(SiO4)3|9|Nesosilicatos / grupo del granate|almandine
halita|NaCl|3|Haluros anhidros|halite
hematites|Fe2O3|4|Óxidos|hematite
hornblenda|Variable: anfíboles cálcicos|9|Inosilicatos / anfíboles|magnesiohornblende
labradorita|(Ca,Na)(Al,Si)4O8|9|Tectosilicatos / plagioclasas|anorthite
lazurita|(Na,Ca)8(AlSiO4)6(SO4,S,Cl)2|9|Tectosilicatos / feldespatoides|lazurite
lepidolita|K(Li,Al)3(Si,Al)4O10(F,OH)2|9|Filosilicatos / micas litiníferas|polylithionite
limonita|FeO(OH)·nH2O (orientativa)|4|Mezclas de óxidos y oxihidróxidos de hierro|goethite
magnesita|MgCO3|5|Carbonatos anhidros|magnesite
magnetita|Fe3O4|4|Óxidos / grupo de la espinela|magnetite
malaquita|Cu2(CO3)(OH)2|5|Carbonatos con aniones adicionales|malachite
marcasita|FeS2|2|Sulfuros|marcasite
moscovita|KAl2(AlSi3O10)(OH)2|9|Filosilicatos / micas|muscovite
ocre-amarillo|FeO(OH) dominante; mezcla|4|Mezclas de oxihidróxidos de hierro|goethite
ocre-rojo|Fe2O3 dominante; mezcla|4|Mezclas de óxidos de hierro|hematite
olivino|(Mg,Fe)2SiO4|9|Nesosilicatos / serie forsterita–fayalita|forsterite
opalo|SiO2·nH2O|4|Sílice hidratada / mineraloide|opal
oropimente|As2S3|2|Sulfuros|orpiment
ortosa|KAlSi3O8|9|Tectosilicatos / feldespatos|orthoclase
pirita|FeS2|2|Sulfuros|pyrite
pirolusita|MnO2|4|Óxidos|pyrolusite
pirrotina|Fe(1-x)S|2|Sulfuros no estequiométricos|pyrrhotite
prehnita|Ca2Al(AlSi3O10)(OH)2|9|Inosilicatos (Strunz)|prehnite
rejalgar|As4S4|2|Sulfuros|realgar
rodocrosita|MnCO3|5|Carbonatos anhidros|rhodochrosite
rutilo|TiO2|4|Óxidos|rutile
sepiolita|Mg4Si6O15(OH)2·6H2O|9|Filosilicatos / arcillas fibrosas|sepiolite
serpentina|Mg3Si2O5(OH)4 (miembro magnésico)|9|Filosilicatos / grupo de la serpentina|lizardite
siderita|FeCO3|5|Carbonatos anhidros|siderite
silvina|KCl|3|Haluros anhidros|sylvite
sodalita|Na8(Al6Si6O24)Cl2|9|Tectosilicatos / feldespatoides|sodalite
sulfato-de-cobre|CuSO4; CuSO4·5H2O según hidratación|7|Sulfatos / compuesto con hidratación no indicada|chalcanthite
talco|Mg3Si4O10(OH)2|9|Filosilicatos|talc
topacio|Al2SiO4(F,OH)2|9|Nesosilicatos|topaz
turmalina|Variable: grupo de borosilicatos|9|Ciclosilicatos / grupo de la turmalina|schorl
turquesa|CuAl6(PO4)4(OH)8·4H2O|8|Fosfatos hidratados|turquoise
vanadinita|Pb5(VO4)3Cl|8|Vanadatos|vanadinite
wolframita|(Fe,Mn)WO4|7|Wolframatos|wolframite
yeso|CaSO4·2H2O|7|Sulfatos hidratados|gypsum
sillimanita|Al2SiO5|9|Nesosilicatos|sillimanite
glaucofana|Na2Mg3Al2Si8O22(OH)2|9|Inosilicatos / anfíboles|glaucophane
crisotilo|Mg3Si2O5(OH)4|9|Filosilicatos / grupo de la serpentina|chrysotile
estibina|Sb2S3|2|Sulfuros|stibnite
almandino|Fe3Al2(SiO4)3|9|Nesosilicatos / grupo del granate|almandine
paligorskita|(Mg,Al)2Si4O10(OH)·4H2O|9|Filosilicatos / arcillas fibrosas|palygorskite
chorlo|NaFe3Al6(BO3)3Si6O18(OH)4|9|Ciclosilicatos / grupo de la turmalina|schorl
wollastonita|CaSiO3|9|Inosilicatos / piroxenoides|wollastonite'''
VARIETIES={'agata':'calcedonia','calcita-espatica':'calcita','jacinto-de-compostela':'cuarzo','amatista':'cuarzo','estaurolita-macla-en-cruz':'estaurolita','pirolusita-dendritica':'pirolusita','yeso-fibroso':'yeso','yeso-en-punta-de-flecha':'yeso'}
VARIABLE={'apatito','augita','biotita','clorita','cordierita','crisocola','fuchsita','granate','hornblenda','labradorita','lazurita','lepidolita','limonita','ocre-amarillo','ocre-rojo','olivino','opalo','pirrotina','serpentina','sulfato-de-cobre','topacio','turmalina','wolframita','paligorskita','flogopita'}
# ids | genesis | subgroup | composition; this is not a chemical formula.
ROCKS='''granito,granodiorita|Ígneas|Plutónicas / félsicas a intermedias|Cuarzo, feldespatos y minerales ferromagnesianos en proporciones variables.
diorita|Ígneas|Plutónicas / intermedias|Plagioclasa y minerales ferromagnesianos; cuarzo variable.
gabro|Ígneas|Plutónicas / básicas|Plagioclasa cálcica, piroxenos y posibles olivino y otros minerales.
peridotita|Ígneas|Plutónicas / ultramáficas|Olivino dominante, con piroxenos y minerales accesorios.
sienita,larviquita|Ígneas|Plutónicas / ricas en feldespatos alcalinos|Feldespatos dominantes y minerales ferromagnesianos; poco cuarzo en la sienita típica.
pegmatita,pegmatita-con-andalucita,pegmatita-con-turmalina,aplita|Ígneas|Filonianas / diferenciados magmáticos|Feldespatos, cuarzo y minerales accesorios variables; grano muy grueso en pegmatitas y fino en aplitas.
basalto,basalto-con-olivino|Ígneas|Volcánicas / básicas|Plagioclasa, piroxenos y, en algunas variedades, olivino.
andesita,andesita-con-hornblenda|Ígneas|Volcánicas / intermedias|Plagioclasa y minerales ferromagnesianos; hornblenda en la variedad indicada.
dacita,riodacita-granatifera|Ígneas|Volcánicas / intermedias a félsicas|Cuarzo, feldespatos y minerales oscuros; granate en la variedad indicada.
riolita|Ígneas|Volcánicas / félsicas|Composición habitualmente rica en sílice, con cuarzo y feldespatos o vidrio equivalente.
traquita|Ígneas|Volcánicas / alcalinas|Feldespatos alcalinos dominantes y minerales oscuros variables.
jumillita|Ígneas|Volcánicas / ultrapotásicas (lamproítas)|Micas, olivino y otros silicatos en asociaciones ultrapotásicas variables.
obsidiana|Ígneas|Volcánicas / vítreas|Vidrio volcánico de composición variable, frecuentemente rica en sílice.
pumita,escorias|Ígneas|Volcánicas / vesiculares|Vidrio y cristales volcánicos; abundantes vesículas. La composición no es única.
lava-cordada|Ígneas|Volcánicas / morfología de colada|Superficie de colada con aspecto de cuerdas, habitualmente basáltica; el nombre describe una forma.
bomba-volcanica,lapilli,brecha-volcanica,tobas,cineritas,ignimbrita|Ígneas|Volcanoclásticas / piroclásticas|Fragmentos volcánicos, cenizas, cristales y/o vidrio; el tamaño, depósito y soldadura distinguen los tipos.
ofita,diabasa|Ígneas|Subvolcánicas / básicas|Plagioclasa y piroxenos; textura ofítica o dolerítica según la muestra.
porfido|Ígneas|Textura porfídica / composición no especificada|Fenocristales en una matriz más fina; el nombre no fija por sí solo una composición ni un emplazamiento.
espilita|Ígneas|Basaltos alterados hidrotermalmente|Basalto alterado, con albitización y minerales secundarios; precisar con estudio petrográfico.
arenisca,arenisca-rodeno,arcosa,grauvaca|Sedimentarias|Detríticas / arenitas|Granos de arena con cemento y/o matriz; cuarzo, feldespatos y fragmentos de roca variables.
conglomerado-brecha,conglomerado-pudinga|Sedimentarias|Detríticas / ruditas|Clastos mayores que arena en matriz o cemento; angulosos en brecha y redondeados en pudinga.
arcilla|Sedimentarias|Detríticas / lutitas y materiales finos|Minerales de arcilla y otros granos muy finos; la granulometría no determina una única especie mineral.
caliza,caliza-litografica,caliza-oolitica,caliza-pisolitica,creta,lumaquela,caliza-numulitica|Sedimentarias|Carbonatadas / calizas|Calcita y/o aragonito dominantes, con componentes accesorios; texturas y fósiles permiten distinguir las variedades.
dolomia|Sedimentarias|Carbonatadas / dolomías|Dolomita dominante, con proporciones variables de calcita y otros minerales.
marga|Sedimentarias|Mixtas / carbonato y arcilla|Mezcla de carbonatos y fracción arcillosa; sin proporción ni fórmula única fijada por el nombre.
travertino,toba-calcarea|Sedimentarias|Carbonatadas / precipitación continental|Carbonato cálcico precipitado; porosidad, laminación y restos vegetales dependen del depósito.
pedernal,silex|Sedimentarias|Silíceas / sílex|Sílice microcristalina dominante, con impurezas y posibles restos de organismos.
tripoli|Sedimentarias|Silíceas / diatomitas|Roca silícea porosa rica en frústulas de diatomeas; composición y cementación variables.
caolin|Sedimentarias|Residuales / arcillas de alteración|Caolinita y otros minerales de alteración; caolín es un material, no una especie mineral pura.
turba,lignito,hulla,azabache|Sedimentarias|Orgánicas / carbones y materiales carbonosos|Materia orgánica y fracción mineral variable; no equivalen a carbono elemental puro.
antracita|Metamórficas|De protolito orgánico / carbón de alto rango|Carbón de alto rango transformado; alto contenido en carbono, con volátiles e impurezas variables.
pizarra,filita,esquisto,micacita,esquisto-micaceo,micaesquisto-granatifero|Metamórficas|Foliadas / serie metapelítica|Micas y otros silicatos; el grado, tamaño de grano y minerales índice distinguen los tipos.
gneis,gneis-glandular|Metamórficas|Foliadas / gneises|Feldespatos, cuarzo y minerales oscuros en bandas; los ojos feldespáticos caracterizan muchas variedades glandulares.
anfibolita|Metamórficas|Ricas en anfíbol / protolitos básicos|Anfíbol y plagioclasa dominantes; posibles granate y minerales accesorios.
eclogita|Metamórficas|Alta presión / eclogitas|Granate y clinopiroxeno sódico (onfacita) como asociación característica; plagioclasa ausente en la asociación eclogítica.
granulita|Metamórficas|Alto grado / facies granulita|Composición variable según el protolito; asociaciones de alta temperatura, frecuentemente con piroxenos y feldespatos.
marmol|Metamórficas|No foliadas / carbonatadas|Calcita y/o dolomita recristalizadas, con impurezas y minerales accesorios variables.
cuarcita|Metamórficas|No foliadas / silíceas|Cuarzo recristalizado dominante; no confundir el nombre de roca con una muestra monomineral ideal.
serpentinita|Metamórficas|Hidratación de rocas ultramáficas|Minerales del grupo de la serpentina, con magnetita y otros accesorios posibles.
migmatita|Metamórficas|Anatexia / rocas mixtas|Componentes metamórficos y productos de fusión parcial, con composición y proporciones variables.
ambar,copal|Materiales orgánicos|Resinas naturales|Mezclas orgánicas de resinas; no tienen fórmula molecular única. El grado de maduración distingue copal y ámbar.
petroleo|Materiales orgánicos|Hidrocarburos líquidos|Mezcla de hidrocarburos y otros compuestos orgánicos; no es un mineral ni una roca sólida homogénea.
septaria|Materiales sedimentarios|Concreciones con grietas mineralizadas|Nódulo de composición variable, con grietas rellenas por minerales como calcita; describe una estructura.'''

def fetch_handbook(slug):
    p=C/(slug+'.pdf');url='https://handbookofmineralogy.org/pdfs/'+slug+'.pdf'
    if p.exists():return slug,True
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VisuBioGeo educational mineral chemistry reference'}),timeout=25) as r:raw=r.read()
        if not raw.startswith(b'%PDF'):return slug,False
        p.write_bytes(raw);time.sleep(.1);return slug,True
    except Exception:return slug,False
def main():
    catalog=json.loads((D/'species.json').read_text(encoding='utf8'));result={};rows=[line.split('|') for line in MINERALS.splitlines()]
    with ThreadPoolExecutor(max_workers=4) as pool:availability=dict(pool.map(fetch_handbook,sorted({r[4] for r in rows})))
    for id,formula,number,subgroup,entry in rows:
        path=[CLASSES[int(number)],*subgroup.split(' / ')];source='https://handbookofmineralogy.org/pdfs/'+entry+'.pdf'
        refs=[{'url':'https://www.mindat.org/strunz9.php','title':'Clases principales de Nickel–Strunz, 9.ª edición'}]
        if availability.get(entry):refs.append({'url':source,'title':'Handbook of Mineralogy · '+entry})
        result[id]={'domain':'mineral','path':path,'classification':path[0],'classificationAliases':{'4':['Óxidos','Hidróxidos'],'1':['Elementos nativos'],'7':['Sulfatos'],'8':['Fosfatos'],'5':['Carbonatos']}.get(number,[]),'formula':formula,'formulaKind':'general-or-variable' if id in VARIABLE else 'ideal','formulaQuiz':id not in VARIABLE,'composition':formula,'description':'Entrada mineralógica clasificada por composición química y estructura. '+('Es un grupo, variedad, mezcla o composición variable; no se exige una fórmula única.' if id in VARIABLE else 'La fórmula representa la composición ideal; las muestras naturales pueden incorporar sustituciones o impurezas.'),'scheme':'Clases principales de Nickel–Strunz 9; agrupaciones estructurales con fines de estudio.','sources':refs,'checkedAt':DAY}
    for id,parent in VARIETIES.items():result[id]={**result[parent],'varietyOf':parent,'description':'Variedad o hábito de '+next(x['scientificName'] for x in catalog if x['id']==parent)+'. '+result[parent]['description']}
    result['asbesto']={'domain':'mineral','path':['Silicatos','Hábito asbestiforme / varios grupos'],'classification':'Silicatos','formula':'Sin fórmula única: crisotilo o anfíboles asbestiformes','formulaKind':'mixture-or-habit','formulaQuiz':False,'composition':'El nombre describe un hábito fibroso en minerales distintos, no una única especie.','description':'Asbesto designa variedades fibrosas de ciertos silicatos. La fórmula depende del mineral determinado.','sources':[{'url':'https://www.usgs.gov/centers/national-minerals-information-center/asbestos-statistics-and-information','title':'USGS · Asbestos'}],'checkedAt':DAY}
    result['bauxita']={'domain':'mineral','path':['Mezclas y materiales','Agregados de hidróxidos de aluminio'],'classification':'Mezclas y materiales','classificationAliases':['Roca residual','Sedimentaria residual'],'formula':'Sin fórmula única','formulaKind':'mixture','formulaQuiz':False,'composition':'Mezcla de hidróxidos y oxihidróxidos de Al, con óxidos de hierro, arcillas y otros componentes.','description':'La bauxita es una roca o material residual, no una especie mineral pura, aunque figure entre minerales del listado original.','sources':[{'url':'https://www.usgs.gov/centers/national-minerals-information-center/bauxite-and-alumina-statistics-and-information','title':'USGS · Bauxite and Alumina'}],'checkedAt':DAY}
    for line in ROCKS.splitlines():
        ids,origin,subgroup,composition=line.split('|')
        for id in ids.split(','):
            result[id]={'domain':'roca','path':[origin,*subgroup.split(' / ')],'classification':origin,'classificationAliases':['Magmáticas'] if origin=='Ígneas' else [],'formula':None,'formulaKind':'no-fixed-formula','formulaQuiz':False,'composition':composition,'description':'Clasificación por origen y características petrográficas. '+composition,'sources':[{'url':'https://www.bgs.ac.uk/technologies/bgs-rock-classification-scheme/','title':'BGS · Rock Classification Scheme'}],'checkedAt':DAY}
    result['antracita']['classificationAliases']=['Carbón de alto rango','Sedimentarias']
    result['antracita']['description']+=' Se agrupa con los carbones sedimentarios en algunos esquemas docentes; aquí se explicita su transformación y se admiten ambas convenciones al responder.'
    for item in catalog:
        if item['kind']=='lamina':
            base=item['scientificName'].split('.')[0].split(',')[0].strip().casefold()
            matches=[x for x in catalog if x['kind'] in ['mineral','roca'] and x['scientificName'].casefold()==base and x['id'] in result]
            if len(matches)==1:result[item['id']]={**result[matches[0]['id']],'representation':'Lámina delgada','parentMaterialId':matches[0]['id']}
    missing=[x['id'] for x in catalog if x['kind'] in ['mineral','roca'] and x['id'] not in result]
    if missing:raise ValueError('Unclassified geological entries: '+','.join(missing))
    (D/'learning-geology.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'entries':len(result),'mineralsAndRocks':181,'missing':missing,'handbookVerified':sum(availability.values()),'handbookMissing':[s for s,ok in availability.items() if not ok]},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
