"""Original structural reading notes for the explicitly reviewed chemical records.

Aliases name the represented compound or the catalogue's existing vitamin class;
they never broaden NADH to NAD+ or nicotinic acid to nicotinamide.
"""
from pathlib import Path
import json

D = Path(__file__).resolve().parents[1] / 'data'
ROWS = '''
acido-graso|La clase ácido graso está representada por ácido palmítico, de 16 carbonos y sin dobles enlaces en su cadena.|Cadena hidrocarbonada larga con un carboxilo terminal.~Distinguir el COOH libre de los enlaces éster presentes en ceras, triacilglicéridos y muchos fosfolípidos.|ÁCIDO GRASO: una larga cola termina en una cabeza COOH.|ácido palmítico
cerido-cera-de-abeja|Se representa palmitato de miricilo o palmitato de triacontilo, un éster céreo asociado a la cera de abeja. La cera natural es una mezcla, no una única molécula.|Dos cadenas hidrocarbonadas largas unidas por un enlace éster.~El alcohol es de cadena larga: no hay un esqueleto de glicerol con tres ácidos grasos ni grupo fosfato.|CÉRIDO: imagina dos velas largas unidas por un único broche de éster.|cérido~cera de abeja~palmitato de miricilo~palmitato de triacontilo
fosfolipido|Se comparan dos glicerofosfolípidos: fosfatidilcolina DPPC de PubChem y fosfatidilglicerol LHG de RCSB. Sus cabezas polares son diferentes.|Esqueleto de glicerol con dos cadenas acilo y un grupo fosfato.~Buscar la cabeza polar: en DPPC incluye colina con nitrógeno cargado; en LHG contiene glicerol. No todos los fosfolípidos tienen colina.|FOSFO-LÍPIDO: dos colas grasas y una cabeza que guarda P.|
triacilglicerido|Se representa tripalmitina: glicerol esterificado con tres restos de ácido palmítico, un ejemplo de triacilglicérido.|Tres cadenas acilo unidas a los tres oxígenos del glicerol mediante enlaces éster.~Tres carbonilos y seis oxígenos en total; sin fosfato ni carboxilo libre en la estructura neutra.|TRI-ACIL-GLICÉRIDO: tres colas cuelgan de un soporte de glicerol.|triacilglicérido~triglicérido~tripalmitina
adenina|Base nitrogenada púrica presente en los ácidos nucleicos y otros nucleótidos.|Dos anillos fusionados, uno de seis y otro de cinco miembros.~Un grupo amino externo; no contiene oxígeno. Comparar con la guanina.|A de AMINO y de AUSENCIA de oxígeno: dos anillos, un amino, ningún O.|
citosina|Base nitrogenada pirimidínica del ADN y del ARN.|Un anillo de seis miembros con dos nitrógenos.~Combina un grupo amino y un carbonilo; no confundir con las dos funciones carbonilo del uracilo.|C de COMBINACIÓN: un amino y un carbonilo en un solo anillo.|
guanina|Base nitrogenada púrica del ADN y del ARN.|Dos anillos fusionados con varios nitrógenos.~Contiene un carbonilo y un grupo amino; la adenina carece de ese oxígeno.|La G de GUANINA GUARDA un O además del amino.|
timina|Base pirimidínica característica del ADN; también llamada 5-metiluracilo.|Un anillo con dos grupos carbonilo.~Un grupo metilo adicional permite distinguirla del uracilo.|T de TIENE metilo: busca el pequeño CH3 que no aparece en uracilo.|5-metiluracilo
uracilo|Base pirimidínica característica del ARN.|Anillo de seis miembros con dos nitrógenos y dos carbonilos.~No tiene el metilo de la timina ni el amino de la citosina.|URACILO: imagina que le han quitado a la timina su mochila de metilo.|
atp|Adenosín trifosfato: adenina unida a ribosa y una cadena de tres fosfatos.|Reconocer primero los dos anillos fusionados de la adenina y el anillo de ribosa.~Contar tres átomos de fósforo en la cadena; no confundir con ADP o AMP.|La T de ATP recuerda TRES fosfatos.|adenosín trifosfato~adenosintrifosfato~trifosfato de adenosina
beta-caroteno|Carotenoide hidrocarbonado. El registro representa β-caroteno, no una molécula de clorofila.|Cadena larga con dobles enlaces conjugados y un anillo en cada extremo.~Solo carbono e hidrógeno: no hay oxígeno, nitrógeno ni metal central.|BETA abre dos ruedas y una larga escalera de dobles enlaces entre ellas.|β-caroteno~betacaroteno
clorofila|Pigmento fotosintético. Las dos estructuras representan clorofila a; otras clorofilas tienen sustituyentes distintos.|Macroanillo con cuatro nitrógenos que rodean un átomo de magnesio.~Una larga cadena de fitol sale del núcleo; buscar también los grupos carbonilo y éster.|CLOROFILA: una hoja lleva una medalla de Mg y una larga cinta de fitol.|clorofila a
colesterol|Esterol con cuatro anillos fusionados, un grupo hidroxilo y una cadena hidrocarbonada lateral.|Núcleo de tres anillos de seis miembros y uno de cinco.~Un único O como hidroxilo y una cola larga lo separan de la testosterona representada.|COLESTEROL lleva COLA; compáralo con el esteroide de cola corta.|
esfingosina|Aminoalcohol de cadena larga; la estructura seleccionada es D-eritro-esfingosina.|Un grupo amino y dos hidroxilos próximos a un extremo.~Cadena hidrocarbonada larga con un doble enlace; no hay grupo carboxilo.|La ESFINGE guarda una cabeza con UN amino y DOS OH antes de su larga cola.|D-eritro-esfingosina
fructosa|Cetohexosa. Las imágenes muestran una forma cíclica del registro D-fructosa.|Seis carbonos en total; no confundir el número de carbonos con el tamaño del anillo.~El carbono anomérico deriva del C2 de la forma abierta. Puede formar anillos de tamaños distintos: no memorizar solo una silueta.|FRUCTOSA: imagina una fruta de seis piezas que puede cerrarse de más de una manera.|D-fructosa
gliceraldehido|Aldotriosa: azúcar de tres carbonos; el modelo representa D-gliceraldehído.|Cadena de tres carbonos con un aldehído terminal.~Otros dos carbonos llevan grupos hidroxilo; el modelo no es un anillo de hexosa.|GLICER-ALDEHÍDO: tres peldaños y un aldehído en la punta.|D-gliceraldehído
glucosa|Aldohexosa. El registro elegido representa D-glucosa en una forma cíclica de glucopiranosa.|Anillo de seis miembros que incluye un oxígeno: no son seis carbonos dentro del anillo.~Un grupo CH2OH queda fuera del anillo. La orientación de los OH importa para distinguir otros azúcares.|GLUCO-PIRANOSA: cuenta cinco C y un O en el aro, más un C fuera.|D-glucosa
hormona-esteroidea-testosterona|Hormona esteroidea; la entrada está representada por testosterona.|Cuatro anillos fusionados con un carbonilo en un extremo y un hidroxilo en el otro.~No presenta la larga cadena lateral característica del colesterol.|TESTOSTERONA pasa el TEST de dos O: uno carbonilo y otro OH, sin larga cola.|testosterona~hormona esteroidea
isopreno-unidad-basica-de-los-terpenos|Isopreno, 2-metilbuta-1,3-dieno: hidrocarburo de cinco carbonos relacionado con el patrón estructural de los terpenos.|Cadena principal de cuatro carbonos con dos dobles enlaces.~Un metilo ramifica la cadena: cinco carbonos en total. Las unidades biosintéticas activadas no son isopreno libre.|ISOPRENO: cuatro en fila y uno que se asoma; dos dobles enlaces.|isopreno~2-metilbuta-1,3-dieno
lactosa|Disacárido de galactosa y glucosa unidas mediante un enlace β(1→4). El registro seleccionado es β-lactosa.|Dos anillos de seis miembros unidos por un oxígeno.~Uno de los carbonos anoméricos conserva un OH libre: es un azúcar reductor. No es la pareja de anillos de seis y cinco miembros de sacarosa.|LAC de leche: dos aros grandes; uno conserva una mano anomérica libre.|β-lactosa
nadh|Forma reducida del dinucleótido de nicotinamida y adenina. No es NAD+.|Adenina y nicotinamida en extremos distintos, con dos ribosas y un puente de dos fosfatos.~El anillo de nicotinamida está reducido; el dibujo no corresponde a la forma aromática cargada de NAD+.|NAD-H: la H recuerda la forma reducida; sigue el puente de DOS fosfatos entre sus extremos.|dinucleótido de nicotinamida y adenina reducido~nicotinamida adenina dinucleótido reducido
prostaglandina|La entrada genérica está representada por prostaglandina E2, un eicosanoide. No todas las prostaglandinas tienen idénticos sustituyentes.|Anillo central de cinco carbonos con dos cadenas laterales.~Un extremo lleva carboxilo; en PGE2 aparecen un carbonilo en el anillo y grupos hidroxilo.|PROSTAGLANDINA: una plaza pentagonal con dos calles; al final de una está el COOH.|prostaglandina E2~PGE2
sacarosa|Disacárido formado por glucosa y fructosa, unidas por sus dos carbonos anoméricos.|En este dibujo, un anillo de seis miembros y otro de cinco enlazados por oxígeno.~Ambos centros anoméricos participan en el enlace: no queda un OH anomérico libre como en la lactosa.|SACAROSA se da la mano por los DOS centros: un aro grande y otro pequeño.|
vitamina-a-retinol|Las imágenes representan retinol, una forma de vitamina A; no representan retinal ni ácido retinoico.|Un anillo y una cadena de dobles enlaces conjugados.~La cadena termina en alcohol, no en aldehído ni en carboxilo.|RETIN-OL: el final OL recuerda el alcohol al final de la cola.|retinol~vitamina A
vitamina-b1-tiamina|Tiamina, vitamina B1; el registro representa el catión tiaminio.|Un anillo de seis miembros con nitrógenos se une a otro de cinco con azufre y nitrógeno.~El anillo de tiazolio lleva carga positiva; una cadena lateral termina en OH.|B1: dos aros distintos, uno guarda S y N+, y de él sale una pequeña cola con OH.|tiamina~vitamina B1
vitamina-b12-cobalamina|Familia de cobalaminas con cobalto. Se comparan una representación de cobalamina de RCSB y otra de cianocobalamina de PubChem: el ligando axial no es el mismo.|Átomo de Co dentro de un gran anillo de corrina con cuatro nitrógenos.~Numerosas cadenas amida y un apéndice nucleotídico; no confundir el cobalto con el magnesio de la clorofila.|COBALAMINA coloca Co en el centro de una corona muy adornada.|cobalamina~vitamina B12~B12
vitamina-b2-riboflavina|Riboflavina, vitamina B2: núcleo de isoaloxazina unido a una cadena de ribitilo.|Tres anillos fusionados con nitrógenos y dos carbonilos.~La cadena lateral abierta tiene varios OH; no es un anillo de ribosa ni un grupo fosfato.|RIBOFLAVINA: tres libros unidos y una cinta abierta llena de OH.|riboflavina~vitamina B2
vitamina-b3-niacina|La forma elegida de vitamina B3 es ácido nicotínico o niacina; no nicotinamida.|Anillo aromático de seis miembros con un nitrógeno.~Un grupo carboxilo en posición 3. La nicotinamida llevaría una amida en su lugar.|NIACINA tiene una N en el aro y un ÁCIDO al lado: buscar COOH, no CONH2.|niacina~ácido nicotínico~vitamina B3
vitamina-b5-acido-pantotenico|Ácido pantoténico, vitamina B5; el registro representa la forma D.|Cadena abierta con enlace amida, carboxilo terminal y grupos hidroxilo.~Dos metilos unidos al mismo carbono en uno de sus extremos; no hay núcleo aromático.|PANTOTÉNICO: imagina un pantalón con dos bolsillos de metilo junto a un cierre de amida.|ácido pantoténico~D-ácido pantoténico~vitamina B5
vitamina-b6-piridoxina|La forma seleccionada de vitamina B6 es piridoxina; no piridoxal ni piridoxamina.|Anillo de piridina con un nitrógeno y un OH directamente unido al anillo.~Dos sustituyentes CH2OH y un metilo; no hay aldehído ni grupo amino lateral.|PIRIDOXINA lleva DOS pequeñas botellas CH2OH colgadas del aro.|piridoxina~vitamina B6
vitamina-b8-biotina|Biotina, denominada vitamina B8 en la lista original; también se conoce como B7 o vitamina H.|Dos anillos de cinco miembros fusionados: uno contiene azufre y otro un grupo urea.~Una cadena lateral termina en carboxilo. La S está en un anillo, no en una larga cadena libre.|BIOTINA: BI de dos aros; una S ocupa uno y una cola ácida sale del conjunto.|biotina~vitamina B8~vitamina B7~vitamina H
vitamina-b9-acido-folico|Ácido fólico, una forma de vitamina B9; no engloba todas las estructuras de folatos.|Reconocer tres zonas: pteridina, anillo de aminobenzoato y resto de glutamato.~Varios nitrógenos en la cabeza y dos grupos carboxilo en el extremo de glutamato.|FÓLICO: imagina una hoja de tres secciones; la última termina en dos puntas ácidas.|ácido fólico~vitamina B9
vitamina-c|Ácido L-ascórbico, vitamina C.|Anillo de lactona de cinco miembros, con oxígeno en el anillo y un carbonilo.~Dos OH vecinos en el doble enlace y una pequeña cadena lateral con otros OH.|ASCÓRBICO: una pequeña cesta de cinco lados con muchos OH y un solo carbonilo.|ácido ascórbico~ácido L-ascórbico~vitamina C
vitamina-d|La estructura elegida es vitamina D3 o colecalciferol; D2 tiene otra cadena lateral.|Secoesteroide: uno de los anillos del esqueleto esteroideo se ha abierto.~Tres anillos permanecen cerrados; hay un sistema de dobles enlaces y un OH.|D3: cuenta TRES aros cerrados y busca el hueco que dejó el cuarto.|vitamina D~vitamina D3~colecalciferol
vitamina-e|La familia vitamina E está representada por α-tocoferol, no por todos los tocoferoles y tocotrienoles.|Cabeza de cromanol: anillo aromático con OH unido a un anillo que contiene oxígeno.~Cola hidrocarbonada larga y ramificada; no tiene el macroanillo metálico de la clorofila.|TOCOFEROL: imagina que TOCAS una cabeza de dos aros de la que sale una larga cuerda ramificada.|vitamina E~α-tocoferol~alfa-tocoferol~tocoferol
vitamina-k-fitomenadiona|Fitomenadiona o filoquinona, vitamina K1; no es una menaquinona de la serie K2.|Cabeza de naftoquinona: dos anillos fusionados con dos carbonilos.~Cadena lateral isoprenoide larga y ramificada. La cabeza no tiene el OH fenólico del tocoferol.|K1: imagina dos ventanas C=O en una casa de dos aros con una larga cola.|vitamina K~vitamina K1~fitomenadiona~filoquinona
colageno|Proteína estructural. Las imágenes son modelos de péptidos de tipo colágeno que muestran la triple hélice; no representan una fibra completa de tejido.|Tres cadenas polipeptídicas se enrollan en una estructura alargada.~No confundir la triple hélice con una única hélice alfa ni con un ovillo globular.|COLÁGENO es una COLA hecha con TRES cuerdas trenzadas.|
hemoglobina|Se representan hemoglobinas humanas oxigenada y desoxigenada, ambas con cuatro subunidades y grupos hemo.|Complejo globular de cuatro cadenas, con abundantes hélices alfa.~Buscar los grupos hemo entre las cadenas; el cambio de orientación no cambia su identidad.|HEMOGLOBINA: cuatro habitaciones para cuatro hemos; cada habitación tiene su propia cadena.|
inmunoglobulina|Las imágenes representan anticuerpos IgG completos: dos cadenas pesadas y dos ligeras. Otras clases pueden formar conjuntos mayores.|Dos brazos de reconocimiento y una región constante, unidos por una bisagra flexible.~Estructura rica en dominios de láminas beta; la orientación puede ocultar la silueta de Y perfecta.|INMUNOGLOBULINA: imagina una Y flexible hecha de DOS cintas largas y DOS cortas.|anticuerpo~IgG~inmunoglobulina G
'''

# Each root below was read in the actual Dicciomed entry, not a search-results page.
ETYMOLOGY = {
 'adenina': ('adenina', 'De adēn, «glándula», con el sufijo químico -ina.'),
 'citosina': ('citosina', 'Se forma sobre el elemento científico cito-, «célula», con sufijos de denominación química.'),
 'guanina': ('guanina', 'Deriva de guano, voz de origen quechua: se aisló de ese material.'),
 'timina': ('timina', 'Deriva de ácido tímico, denominación relacionada con el timo.'),
 'uracilo': ('uracilo', 'Procede del alemán Uracil. Su formación precisa sigue pendiente de aclarar; Dicciomed considera posible, sin confirmarla, una relación con urea.'),
 'atp': ('adenosina', 'ATP abrevia adenosín trifosfato. Adenosina se formó a partir de adenina y ribosa; tri- indica los tres fosfatos.'),
 'beta-caroteno': ('caroteno', 'Caroteno se forma sobre el latín carota, «zanahoria», con el sufijo químico -eno. Beta distingue esta estructura de otros carotenos.'),
 'clorofila': ('clorofila', 'Del griego khlōrós, «amarilloverdoso», y phýllon, «hoja».'),
 'colesterol': ('colesterol', 'Combina raíces griegas relacionadas con «bilis» y «sólido», y -ol, terminación química de alcohol.'),
 'esfingosina': ('esfingosina', 'Se nombró por la esfinge, en alusión al carácter enigmático que se atribuía a estos compuestos.'),
 'fructosa': ('fructosa', 'Del latín fructus, «fruto», con la terminación química -osa.'),
 'glucosa': ('glucosa', 'Llegó a través del francés glucose, formado sobre el griego gleûkos, «mosto» o «vino dulce».'),
 'hormona-esteroidea-testosterona': ('testosterona', 'El nombre incorpora el latín testis, «testículo», y elementos de la nomenclatura de los esteroides.'),
 'lactosa': ('lactosa', 'Del tema latino lact-, «leche», con el sufijo químico -osa.'),
 'prostaglandina': ('prostaglandina', 'Se formó a partir de próstata y glándula. Ese origen histórico no significa que se produzcan únicamente en la próstata.'),
 'sacarosa': ('sacarosa', 'Relacionado con el griego sákkhar, «azúcar», de origen sánscrito, más la terminación química -osa.'),
 'vitamina-a-retinol': ('retinol', 'Se forma sobre retina y la terminación -ol de alcohol.'),
 'vitamina-b12-cobalamina': ('cobalamina', 'Combina el nombre del cobalto con elementos de vitamina; alude al metal de su estructura.'),
 'vitamina-b8-biotina': ('biotina', 'Se forma sobre elementos griegos relacionados con «vida» o «sustento», con el sufijo -ina.'),
 'vitamina-e': ('tocoferol', 'Combina elementos griegos relativos a «parto» y «llevar», más -ol. Es una denominación histórica ligada a estudios de reproducción.'),
 'colageno': ('colageno', 'Del griego kólla, «cola o pegamento», y un elemento que significa «que genera».'),
 'hemoglobina': ('hemoglobina', 'Forma abreviada histórica de hematoglobulina, que reúne hematina y globulina. Hemo- remite al griego «sangre».'),
 'inmunoglobulina': ('inmunoglobulina', 'Une inmuno-, relativo a inmunidad, y globulina, derivado de la familia latina de globus, «globo».'),
}

def main():
    path=D/'study-notes.json';notes=json.loads(path.read_text(encoding='utf8'))
    catpath=D/'species.json';catalog=json.loads(catpath.read_text(encoding='utf8'));cat={x['id']:x for x in catalog}
    cur=json.loads((D/'curated-images.json').read_text(encoding='utf8'))
    count=0
    for line in ROWS.strip().splitlines():
        suffix,description,diagnostics,mnemonic,aliases=line.split('|');id='molecula-'+suffix
        images=[im for im in cur.get(id,{}).get('images',[]) if im['status']=='approved']
        if len(images)<(1 if suffix=='cerido-cera-de-abeja' else 2):raise ValueError('Missing reviewed structural images: '+id)
        sources=[{'url':url,'title':'Registro químico o modelo de estructura identificado'} for url in dict.fromkeys(im['page'] for im in images)]
        note={'description':description,'diagnostics':diagnostics.split('~'),'mnemonic':mnemonic,'sources':sources,'reviewedAt':'2026-10-25','reviewStatus':'reviewed','scope':'Lectura estructural propia de registros identificados y revisión visual. La mnemotecnia es inventada; las clases genéricas se delimitan a las formas representadas.'}
        if suffix in ETYMOLOGY:
            term,etymology=ETYMOLOGY[suffix];note['etymology']=etymology
            sources.append({'url':'https://dicciomed.usal.es/palabra/'+term,'title':'Universidad de Salamanca · Dicciomed: origen del término'})
        elif suffix=='nadh':note['etymology']='La sigla reúne nicotinamida, adenina y dinucleótido; H distingue la forma reducida. La historia de las raíces remotas queda pendiente de contraste.'
        notes[id]=note
        if aliases:
            cat[id]['aliases']=list(dict.fromkeys([*cat[id].get('aliases',[]),*aliases.split('~')]))
        count+=1
    path.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8')
    catpath.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
    print(count,'fichas químicas añadidas;',len(notes),'fichas en total')

if __name__=='__main__':main()
