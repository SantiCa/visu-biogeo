"""Short original descriptions of reviewed specimens and landforms."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
# No unverified linguistic origins are filled by inference from the spelling.
ROWS=r'''
abanico-aluvial-o-cono-de-deyeccion|Depósito que se abre en abanico al salir un cauce de una zona encajada.|Forma triangular o de abanico vista desde arriba.~Los pequeños canales se distribuyen desde un ápice hacia el borde del depósito.|ABANICO: busca el punto estrecho del que se abren las varillas.
arcos-marinos|Abertura en una masa rocosa costera que conserva un puente de roca por encima.|La cavidad atraviesa la roca y se abre al mar.~Comprobar el entorno litoral para distinguirlo de otros arcos naturales.|
brechas-de-falla|Roca fracturada asociada a una zona de falla.|Fragmentos angulosos dentro de una matriz triturada.~La asociación con la estructura de falla ayuda a distinguirla de una brecha sedimentaria.|
canchales-o-derrubios|Acumulaciones de fragmentos rocosos al pie de laderas y paredes.|Talud cubierto de bloques angulosos, generalmente sin redondeamiento fluvial.~Observar su posición bajo el escarpe; una pila de bloques aislada no basta.|
cascada|Salto de agua producido por un desnivel del cauce.|El agua cae por un escalón rocoso reconocible.~El tamaño de la foto no permite fijar por sí solo la magnitud del salto.|
catarata|Denominación usada para saltos de agua de gran desarrollo.|Examinar el conjunto del salto y su entorno, no solo una zona de espuma.~No hay un umbral universal visible en una foto que separe toda cascada de una catarata.|
cordon-litoral-o-barra|Acumulación alargada de sedimentos junto a la costa.|Franja de arena o grava que delimita o protege aguas interiores.~Comprobar conexiones con tierra y disposición del oleaje; no toda barra es una isla barrera.|
dolina-torca|Depresión cerrada característica de muchos paisajes kársticos.|Contorno aproximadamente circular u oval y fondo más bajo que sus bordes.~La dolina puede estar cubierta de suelo y vegetación o presentar paredes rocosas.|
estratificacion-cruzada|Laminación oblicua dentro de un conjunto sedimentario.|Láminas inclinadas respecto a los límites principales del estrato.~Buscar series y superficies que cortan otras láminas; no confundir con todo un estrato tectónicamente inclinado.|
filon-de-cuarzo|Cuerpo de cuarzo que ocupa una fractura en otra roca.|Banda o vena de cuarzo que contrasta con la roca encajante.~Seguir sus contactos y su continuidad; una zona clara aislada no confirma un filón.|
granate|Nombre de un grupo de minerales, no de una única composición.|Cristales frecuentemente equidimensionales, con caras dodecaédricas o trapezoédricas.~El rojo es frecuente, pero hay granates de otros colores; confirmar forma y contexto.|
pirolusita|Mineral de manganeso que puede presentarse en agregados oscuros.|Agregados negros, aciculares o radiados en las muestras revisadas.~Las dendritas negras en una roca pueden incluir diversos óxidos: la forma sola no prueba pirolusita.|
pirrotina|Sulfuro de hierro de composición variable, distinto de la pirita.|Color bronce a pardo y brillo metálico en las muestras revisadas.~El color aislado no permite separarlo de todos los sulfuros; contrastar propiedades de la muestra.|
playa|Acumulación de sedimentos en el borde de un cuerpo de agua.|Franja sedimentaria entre la zona sumergida y el terreno emergido.~Observar el conjunto litoral; un detalle de arena con ondulaciones no representa toda la playa.|
pliegue-anticlinal|Pliegue con materiales más antiguos hacia el núcleo, cuando la sucesión está identificada.|En el ejemplo normal de la ficha, los estratos forman un arco convexo hacia arriba.~La forma de arco sola define un antiforme: para confirmar anticlinal hay que conocer la edad de los estratos.|ANTI: imagina un arco; recuerda comprobar después qué materiales están en el centro.
pliegue-sinclinal|Pliegue con materiales más recientes hacia el núcleo, cuando la sucesión está identificada.|En el ejemplo normal de la ficha, los estratos dibujan una concavidad hacia arriba.~La geometría sola define un sinforme; confirmar la sucesión para llamarlo sinclinal.|SINCLINAL: imagina un cuenco SIN llenar y comprueba su núcleo.
pliegue-tumbado|Pliegue cuyo plano axial está próximo a la horizontal.|Charnela y flancos aparecen recostados en el afloramiento.~Seguir la continuidad de las capas para no confundirlo con estratos simplemente horizontales.|
ripples-marks|Ondulaciones pequeñas en la superficie de un sedimento.|Sucesión de crestas y surcos; observar también la simetría de los perfiles.~La asimetría puede orientar sobre la corriente; no inferir toda la génesis de una única vista.|
rio-anastomosado-o-braided|Río trenzado: varios canales se separan y vuelven a unirse entre barras sedimentarias.|Red de canales entrelazados y barras frecuentemente poco vegetadas.~No equipararlo sin más a un río anastomosado, cuyas islas y canales suelen ser más estables.|TRENZADO: sigue varios mechones de agua que se separan y vuelven a juntarse.
tillitas|Rocas formadas por la litificación de depósitos glaciares de tipo till.|Clastos de tamaños muy distintos dentro de una matriz, con mala selección.~La textura sola no demuestra origen glaciar: hacen falta contexto y evidencias adicionales.|
valle-colgado|Valle tributario que desemboca a mayor altura que el fondo del valle principal.|Desnivel visible entre ambos fondos de valle; puede existir una cascada.~La forma no obliga por sí sola a atribuir un origen glaciar a todos los ejemplos.|
valle-glaciar-valle-en-u|Valle de sección ancha y fondo relativamente abierto, modelado por hielo.|Laderas pronunciadas y sección transversal aproximadamente en U.~Examinar la sección completa y las evidencias glaciares del entorno; una garganta fluvial puede parecer ancha en perspectiva.|
xenolito|Fragmento de una roca incluido dentro de otra roca ígnea.|Inclusión con textura o color distinto del material que la engloba.~El contraste entre ambas rocas y su contacto son más útiles que el color oscuro por sí solo.|
travertino|Roca carbonatada de precipitación química, a menudo con poros y bandas.|En las muestras revisadas aparecen cavidades o laminaciones de tonos claros y pardos.~Distinguir una muestra de esta roca de una terraza de travertino en el paisaje.|
biotita|Mica oscura que se separa en láminas.|Brillo marcado en las superficies de exfoliación y hábito tabular.~Las láminas oscuras pueden formar libros o secciones aproximadamente hexagonales.|
cordierita|Silicato que puede aparecer en cristales de aspecto prismático o en masas alteradas.|En la muestra revisada, contorno prismático oscuro dentro de una matriz clara.~La identificación visual es limitada en ejemplares alterados; no confundir color oscuro con diagnóstico suficiente.|
diamante|Mineral de carbono; el aspecto natural difiere del de una gema tallada.|Buscar las caras de los cristales naturales, frecuentemente octaédricos.~Brillo y transparencia de una foto no demuestran por sí solos que una gema sea diamante.|
grafito|Mineral de carbono de aspecto gris oscuro a negro.|Brillo metálico a submetálico y agregados laminares; algunos ejemplares forman cristales de contorno hexagonal.~Una pequeña mancha negra en una matriz no es una vista suficiente para identificarlo.|
ortosa|Feldespato potásico, presente como cristales o masas en diversas rocas.|En las imágenes revisadas, cristales claros que destacan dentro de una matriz ígnea.~Color blanco o rosado por sí solo no distingue ortosa de los demás feldespatos.|
vanadinita|Mineral secundario de plomo y vanadio, de colores frecuentemente rojizos o anaranjados.|Cristales cortos, tabulares o prismáticos, con secciones hexagonales.~Brillo resinoso a adamantino; no basar la respuesta solo en el color.|VANADINITA: imagina pequeñas tuercas hexagonales rojas hechas de vanadio.
sienita|Roca plutónica dominada por feldespatos alcalinos, con minerales oscuros subordinados y poco cuarzo.|Textura granuda: buscar feldespatos y minerales máficos intercrecidos.~Una fotografía no sustituye a la estimación mineralógica; separar las variedades especializadas y las muestras de clasificación dudosa.|
'''

def main():
    cat={x['id']:x for x in json.loads((D/'species.json').read_text(encoding='utf8'))};cur=json.loads((D/'curated-images.json').read_text(encoding='utf8'));path=D/'study-notes.json';notes=json.loads(path.read_text(encoding='utf8'))
    for line in ROWS.strip().splitlines():
        id,description,diagnostics,mnemonic=line.split('|')
        images=[im for im in cur.get(id,{}).get('images',[]) if im['status']=='approved']
        if not images:continue
        sources=[{'url':u,'title':'Referencia del ejemplar o forma del relieve'} for u in dict.fromkeys(im['page'] for im in images)][:2]
        if id=='rio-anastomosado-o-braided':sources += [{'url':'https://www.nps.gov/articles/braided-stream.htm','title':'NPS: ríos trenzados'},{'url':'https://www.fs.usda.gov/biology/nsaec/fishxing/publications/PDFs/AOP_PDFs/AppendixA.pdf','title':'US Forest Service: patrones de cauce'}]
        if id=='travertino':sources.append({'url':'https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm','title':'NPS: terrazas de travertino'})
        if id=='vanadinita':sources=[{'url':'https://geology.com/minerals/vanadinite.shtml','title':'Geology.com: composición y propiedades de la vanadinita'}]
        if id=='sienita':sources=[{'url':'https://www.science.smith.edu/~jbrady/petrology/rock-library/igp-rocks/syenite/syenite.php','title':'Smith College: definición y muestras de sienita'},{'url':'https://geodil.dperkins.org/h/417.html','title':'GeoDIL: sienita de Magnet Cove'}]
        notes[id]={'description':description,'diagnostics':diagnostics.split('~'),'mnemonic':mnemonic,'sources':sources,'reviewedAt':'2026-10-25','reviewStatus':'reviewed','scope':'Resumen propio de muestras identificadas y rasgos visibles; el origen lingüístico no documentado queda pendiente.'}
        if id=='vanadinita':notes[id]['etymology']='El nombre hace referencia a su contenido en vanadio.'
    path.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8');print(len(notes),'fichas en total')

if __name__=='__main__':main()
