"""Paraphrased linguistic notes from the cited mineral handbook, retaining uncertainty."""
from pathlib import Path
import json
D=Path(__file__).resolve().parents[1]/'data'
ETYMOLOGIES='''cuarzo|El Handbook sitúa el término en la Edad Media y en la denominación de gangas de Sajonia; su origen lingüístico último es oscuro.
pirita|Procede de la raíz griega asociada al fuego: al golpearla pueden producirse chispas.
galena|Continúa el latín galena, empleado para la mena de plomo o residuos de su fundición.
halita|Nombre formado a partir de la voz griega para la sal.
silvina|Se relaciona con la antigua sal digestiva de Sylvius, nombre latinizado del médico y químico François Sylvius de le Boë.
fluorita|Del latín relacionado con fluir; alude al comportamiento de este material como fundente.
aragonito|Nombre geográfico referido a Aragón, región española asociada a su primera descripción.
magnetita|Nombre de tradición antigua; el Handbook señala como posible referencia Magnesia, en Grecia. La atribución geográfica no se presenta como segura.
hematites|De una raíz griega relacionada con la sangre, en referencia al color rojizo característico de su raya.
cinabrio|El Handbook remonta la forma latina medieval cinnabaris a una voz persa, con una interpretación vinculada a «sangre de dragón» y al rojo del mineral.
casiterita|Deriva de la palabra griega empleada para el estaño, metal del que es una mena importante.
berilo|Del griego beryllos; el sentido más antiguo de esa palabra no se conoce con seguridad.
moscovita|Del antiguo nombre del material como vidrio de Moscovia, por su empleo y procedencia histórica.
topacio|El Handbook relaciona el nombre antiguo con una isla del mar Rojo conocida por olivino, entonces llamado también topacio. Esa denominación histórica no identifica necesariamente el mineral moderno.
malaquita|De una palabra griega relacionada con la malva, por comparación con el color verde de la planta.'''
FOSSILS='''aspidiscus-cristatus|Coral colonial fósil de forma discoidal.|Cara oral con muchos coralitos y superficie inferior de crecimiento concéntrico.~Los orificios grandes de la muestra ilustrada son perforaciones de otros organismos, no los coralitos normales.
aspidiscus|Género de corales coloniales fósiles; se ilustra con ejemplares identificados como Aspidiscus cristatus.|Forma de disco y agrupación de numerosos coralitos en la cara oral.~Distinguir el relieve de los coralitos de las perforaciones ajenas que pueden afectar al fósil.
diploctenium|Coral escleractinio fósil de forma aplanada, frecuentemente semejante a un abanico.|Contorno expandido y bandas o septos radiales visibles en las caras.~La tarjeta pide el género; no atribuir una especie por el contorno aislado.
gomphotherium|Género extinto de proboscídeos representado aquí por restos mandibulares identificados.|Mandíbula alargada, con molariformes de cúspides grandes.~La forma de los dientes y la región anterior de la mandíbula aportan más información que el tamaño del resto.
exogyra|Género de bivalvos fósiles de concha desigual e irregular.|Valva muy convexa y región umbonal enrollada; ornamentación y grosor variables.~Las piezas fragmentadas pueden perder el umbo; comparar las distintas vistas del banco.
fenestella|Briozoo fósil colonial con una estructura semejante a una red fina.|Ramas conectadas por travesaños, que delimitan pequeñas ventanas repetidas.~Los poros y la arquitectura de la colonia ayudan a separarlo de una simple impresión vegetal.
hippurites|Género de rudistas, bivalvos fósiles con una valva desarrollada en forma de cono o tubo.|Concha robusta y alargada; estrías y costillas longitudinales en los ejemplares.~Para confirmar el género pueden ser necesarias secciones que muestren las estructuras internas, además de la forma externa.
micraster|Género de erizos irregulares fósiles de contorno aproximadamente acorazonado.|Cinco zonas ambulacrales, con pétalos visibles en la cara superior.~Surco anterior y silueta bilateral; comprobar ambas caras para distinguirlo de otros equinoideos.'''
def main():
 p=D/'study-notes.json';notes=json.loads(p.read_text(encoding='utf8'));cur=json.loads((D/'curated-images.json').read_text(encoding='utf8'))
 for row in ETYMOLOGIES.splitlines():
  id,text=row.split('|');notes[id]['etymology']=text;notes[id]['etymologyReviewedAt']='2026-10-26'
 for row in FOSSILS.splitlines():
  id,description,diagnostics=row.split('|');im=next(x for x in cur[id]['images'] if x['status']=='approved');notes[id]={'description':description,'diagnostics':diagnostics.split('~'),'etymology':'Origen histórico del nombre pendiente de contrastar.','sources':[{'url':im['page'],'title':'Ejemplar identificado y procedencia de colección'}],'reviewedAt':'2026-10-26','scope':'Descripción propia de rasgos visibles en ejemplares identificados; no se completa la etimología sin una fuente específica.'}
 notes['astroides-calycularis']={'commonName':'Coral naranja','description':'Coral pétreo colonial que forma masas de pólipos de color naranja sobre superficies rocosas marinas.','diagnostics':['Colonia de pequeños pólipos, cada uno con una corona de tentáculos.','Esqueleto calcáreo con numerosos cálices; vive en paredes sombreadas y extraplomos. El color solo no basta para distinguir todos los corales.'],'etymology':'Derivación histórica del binomio pendiente de contrastar.','sources':[{'url':'https://www.asturnatura.com/especie/astroides-calycularis','title':'Asturnatura · Astroides calycularis'}],'reviewedAt':'2026-10-26'}
 notes['quercus-ilex']={'commonName':'Encina','description':'Árbol perennifolio mediterráneo de hojas coriáceas y fruto en bellota.','diagnostics':['Hojas de margen variable, a veces dentado o espinoso; envés con pelos claros.','Bellota parcialmente rodeada por una cúpula. Comparar forma, nerviación y vellosidad con los taxones próximos; no basta una bellota aislada.'],'etymology':'Quercus es el nombre latino del roble; ilex es el nombre latino de la encina.','sources':[{'url':'https://www.asturnatura.com/especie/quercus-ilex','title':'Asturnatura · Quercus ilex'}],'reviewedAt':'2026-10-26'}
 p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8');print(len(notes),'profiles; 15 mineral etymologies documented')
if __name__=='__main__':main()
