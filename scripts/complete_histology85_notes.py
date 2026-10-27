"""Original, source-backed descriptions and terminology for reviewed micrographs."""
from pathlib import Path
import json
from datetime import date

R=Path(__file__).resolve().parents[1];D=R/'data'
V='https://mmegias.webs.uvigo.es/';L='https://histology.leeds.ac.uk/home/'
B=V+'a-imagenes-grandes/sangre.php';W=L+'blood/blood_wbc/'
ROWS={
'antera':('Parte del estambre que contiene los sacos donde se forma el polen.',
 ['En el corte aprobado se reconocen dos tecas y cuatro cavidades con material polínico.', 'La antera es el conjunto; cada saco polínico es una de sus cámaras.'],
 'Antera procede del latín científico anthera, tomado del griego anthērá, florida.',
 [V+'2-organos-v/o-imagenes-grandes/flor4.php','https://dle.rae.es/antera']),
'sacos-polinicos':('Cavidades de la antera que contienen el tejido productor de microsporas y, después, los granos de polen.',
 ['Buscar las cámaras y sus paredes dentro del corte de la antera.', 'En esta preparación hay cuatro sacos. Distinguir el saco de los granos que contiene.'],
 'Polen viene del latín científico pollen y del latino pollen, pollinis, referido a harina muy fina. Polínico indica relación con el polen; saco describe la forma de una cavidad envolvente.',
 [V+'2-organos-v/guiada_o_v_flor.php','https://dle.rae.es/polen']),
'basofilos':('Leucocitos granulocíticos relacionados con respuestas inflamatorias y alérgicas.',
 ['Gránulos citoplasmáticos gruesos, muy oscuros, que pueden ocultar parte del núcleo.', 'Valorar granulación y núcleo conjuntamente; una célula oscura sin detalle no basta.'],
 'Basófilo combina base con el elemento griego philo-, afinidad. El nombre se refiere a la tinción con colorantes básicos.',
 [W,'https://webpath.med.utah.edu/HEMEHTML/HEME005.html','https://dicciomed.usal.es/palabra/basofilo-la']),
'neutrofilos':('Granulocitos sanguíneos que participan de forma destacada en la respuesta fagocitaria.',
 ['Núcleo segmentado en varios lóbulos conectados por puentes finos.', 'Citoplasma relativamente pálido con granulación fina; comparar con la granulación gruesa del basófilo.'],
 'Neutrófilo combina el latino neutrum y el griego philo-, afinidad. Ehrlich lo introdujo para una propiedad de tinción, que después dio nombre a estas células.',
 [B,W,'https://dicciomed.usal.es/palabra/neutrofilo-la']),
'monocitos':('Leucocitos grandes de la sangre; pueden pasar a tejidos y diferenciarse en células fagocitarias.',
 ['Núcleo plegado o arriñonado y citoplasma relativamente abundante.', 'Comparar el tamaño con los eritrocitos del mismo campo; una sola forma nuclear no resuelve todos los casos.'],
 'Monocito une el griego monos, único, y kyto-, célula. La denominación alude al leucocito mononuclear; no significa que los demás leucocitos carezcan de núcleo.',
 [B,W,'https://dicciomed.usal.es/palabra/monocito']),
'linfocitos':('Leucocitos que incluyen poblaciones implicadas en la defensa inmunitaria adaptativa.',
 ['Muchos linfocitos pequeños tienen núcleo redondeado y denso, con poco citoplasma visible.', 'El tamaño y la cantidad de citoplasma varían. Una tinción ordinaria no permite separar con seguridad los linfocitos B y T.'],
 'Linfocito combina el latino lympha, linfa o agua, con el elemento griego kyto-, célula.',
 [B,W,'https://dicciomed.usal.es/palabra/linfocito']),
'plaquetas':('Fragmentos citoplasmáticos procedentes de megacariocitos, implicados en la hemostasia.',
 ['Elementos pequeños, sin núcleo, mucho menores que los eritrocitos vecinos.', 'Pueden aparecer agregados. Distinguir un grupo de plaquetas de un núcleo leucocitario o de un precipitado de tinción.'],
 'Plaqueta llega del francés plaquette, relacionado con una placa pequeña. Dicciomed documenta el uso hematológico francés de Bizzozero en 1883.',
 [B,L+'blood/platelets/','https://dicciomed.usal.es/palabra/plaqueta']),
'cilios':('Prolongaciones celulares con un armazón de microtúbulos. Algunos cilios desplazan fluidos; otros actúan como estructuras sensoriales.',
 ['En las micrografías se ven prolongaciones alargadas en la superficie libre del epitelio.', 'Distinguir los cilios de las microvellosidades, que suelen ser más cortas y tienen un armazón de actina.', 'La organización 9+2 es típica de muchos cilios móviles, pero no debe exigirse a todos los tipos de cilio.'],
 'Cilio procede del latino cilium, que el DLE traduce como ceja. El nombre compara la prolongación fina con un pelo del borde ocular.',
 [V+'5-celulas/ampliaciones/7-cilio-flagelo.php','https://dle.rae.es/cilio']),
'nucleo-celular':('Compartimento de las células eucariotas que contiene la mayor parte de su ADN.',
 ['Buscar una región delimitada con cromatina; puede mostrar uno o varios nucléolos.', 'El núcleo no siempre es esférico ni único por célula. Diferenciarlo del nucléolo más pequeño que puede contener.'],
 'Núcleo viene del latín nucleus, relacionado con la parte interior de una nuez o el hueso de una fruta; es diminutivo de nux, nuez.',
 [V+'5-celulas/4-nucleo.php','https://dle.rae.es/núcleo']),
'espermatozoides':('Gametos masculinos animales. Estas micrografías muestran espermatozoides de rata en el aparato reproductor.',
 ['Reconocer las cabezas asociadas a prolongaciones flagelares muy largas.', 'Un campo de filamentos aislados puede ser ambiguo: buscar también las cabezas y el contexto de la preparación.', 'La forma de la cabeza varía entre especies; no imponer la silueta humana a la rata.'],
 'Espermatozoide reúne elementos griegos relacionados con semilla o semen, animal y semejanza. Su historia refleja que sus movimientos y su cola recordaban a un pequeño animal.',
 [V+'2-organos-a/imagenes-grandes/reproductor-tubulos.php','https://dicciomed.usal.es/palabra/espermatozoide']),
'lisosomas':('Orgánulos de degradación intracelular, con enzimas hidrolíticas y un contenido de aspecto variable.',
 ['En microscopía electrónica pueden verse cuerpos limitados por membrana y material heterogéneo o denso.', 'Una esfera oscura aislada no identifica por sí sola un lisosoma. Los campos incorporados se apoyan en la identificación explícita de la fuente.'],
 'Lisosoma combina elementos griegos relacionados con descomponer y con cuerpo o corpúsculo celular. Dicciomed documenta el término inglés en 1955.',
 [V+'5-celulas/5-lisosomas.php',L+'cell/cell_organelles/','https://dicciomed.usal.es/palabra/lisosoma']),
'membrana-plasmatica':('Límite celular formado por una bicapa lipídica con proteínas asociadas.',
 ['La micrografía muestra dos membranas celulares enfrentadas y el espacio intercelular.', 'Cada membrana puede presentar dos líneas electrodensas. Estas líneas no son dos células ni dos membranas completas.'],
 'Membrana procede del latino membrana. La raíz de plasma remite al griego plásma, forma moldeada; la historia concreta de la expresión membrana plasmática queda pendiente de contrastar.',
 [L+'cell/plasma_membrane/',V+'5-celulas/3-membrana_celular.php','https://dle.rae.es/membrana','https://dle.rae.es/plasma']),
'reticulo-endoplasmatico-liso':('Región del retículo endoplasmático sin ribosomas adheridos, relacionada con funciones como el metabolismo de lípidos.',
 ['Buscar perfiles tubulares membranosos sin el ribete de ribosomas del retículo rugoso.', 'En la imagen de Leeds se conserva la región indicada por las flechas de la fuente. La forma de un tubo aislado no basta para identificarlo.'],
 'Retículo viene del latino reticulum, referido a una red. Liso describe la ausencia de ribosomas adheridos; la derivación histórica completa de endoplasmático queda pendiente de contrastar.',
 [L+'cell/cell_organelles/',V+'5-celulas/5-reticulo.php','https://dle.rae.es/retículo']),
'ureter':('Conducto que transporta la orina desde el riñón hasta la vejiga mediante contracciones de su pared.',
 ['En el corte general se observan luz plegada, urotelio y pared muscular.', 'El detalle de urotelio procede de uréter, pero ese epitelio también existe en otras regiones urinarias. No permite reconocer el órgano sin más contexto.'],
 'Uréter procede del término griego ourētēr, recogido por el DLE. Su nombre designa el conducto entre riñón y vejiga.',
 [L+'urinary/ureter/',V+'a-imagenes-grandes/epitelio_transicion.php','https://dle.rae.es/uréter']),
'uretra':('Conducto que lleva la orina desde la vejiga hacia el exterior. Su revestimiento varía a lo largo del trayecto y según el contexto anatómico.',
 ['La preparación de Leeds conserva la luz y la pared del conducto.', 'Una luz estrellada no separa por sí sola uretra y uréter. Usar el epitelio, la pared y la procedencia de la sección.'],
 'Uretra llega del latino tardío urethra y del griego ourēthra, relacionado con oureîn, orinar.',
 [L+'urinary/urethra/','https://dle.rae.es/uretra']),
'trompa-de-falopio-oviducto':('Conducto del aparato reproductor femenino que comunica la región próxima al ovario con el útero.',
 ['En el corte general destaca una mucosa muy plegada dentro de una pared muscular.', 'El detalle muestra el epitelio de los pliegues, con células ciliadas. Para identificar el órgano hay que combinarlo con su arquitectura.'],
 'Oviducto se forma a partir de los latinos ovum, huevo, y ductus, conducto. La historia detallada del epónimo Falopio queda pendiente de contrastar.',
 [L+'female/oviduct/','https://dle.rae.es/oviducto','https://dle.rae.es/trompa']),
'vena':('Vaso sanguíneo por el que la sangre retorna hacia el corazón. Su pared y su calibre cambian con el tipo de vena.',
 ['Comparadas con arterias de calibre semejante, muchas venas tienen pared relativamente fina y luz amplia o irregular.', 'En vasos grandes puede haber músculo evidente. La forma redonda o la luz colapsada no bastan para distinguir una vena de una arteria.'],
 'Vena procede directamente del latino vena. En esta entrada tiene el sentido anatómico de vaso sanguíneo, no el mineralógico de filón.',
 [L+'circulatory/veins/','https://dle.rae.es/vena']),
'piel-glandula-sebacea':('Glándula cutánea de secreción holocrina, habitualmente asociada a un folículo piloso.',
 ['Lóbulos con células centrales grandes, claras o vacuoladas y una periferia de células más pequeñas.', 'Buscar su relación con el conducto y el folículo. La glándula sudorípara enrollada tiene una organización diferente.'],
 'Sebáceo procede del latino sebaceus y se relaciona con el sebo. El adjetivo alude a la naturaleza grasa de la secreción.',
 [L+'skin/glands/',V+'2-organos-a/imagenes-grandes/tegumento-piel-fina.php','https://dle.rae.es/sebáceo']),
'pelo-corte-transversal':('Sección perpendicular al eje de un pelo. El tallo queratinizado y las envolturas del folículo son estructuras relacionadas, pero distintas.',
 ['Comprobar la presencia del tallo y su disposición transversal antes de responder.', 'Un folículo vacío o una sección longitudinal del pelo no sustituyen la preparación transversal pedida. Las candidatas de este lote se han descartado por esa limitación.'],
 'Pelo procede del latino pilus. Transversal describe la orientación del plano de corte respecto al eje del pelo.',
 [L+'skin/hair/','https://dle.rae.es/pelo'])
}

def main():
 p=D/'study-notes.json';notes=json.loads(p.read_text(encoding='utf8'));added=[]
 for suffix,(description,diagnostics,etymology,urls) in ROWS.items():
  id='estructura-'+suffix
  if id in notes:raise ValueError('Refuse to overwrite '+id)
  notes[id]={'description':description,'diagnostics':diagnostics,'etymology':etymology,'sources':[{'url':u,'title':('Dicciomed · Universidad de Salamanca · etimología' if 'dicciomed' in u else 'DLE · origen del término' if 'dle.rae' in u else 'Atlas universitario · preparación y estructura')} for u in urls],'reviewedAt':date.today().isoformat(),'reviewStatus':'reviewed','scope':'Síntesis propia de fuentes docentes y terminológicas. Se distingue la estructura del organismo de procedencia y del nivel de detalle de la imagen. No se atribuye una familia taxonómica a un tejido u orgánulo. Las raíces pendientes se indican expresamente.'};added.append(id)
 p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8');print(len(added),'new profiles')

if __name__=='__main__':main()
