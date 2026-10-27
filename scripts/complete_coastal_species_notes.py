"""Reviewed Spanish syntheses for the October 26 coastal and exact-name batch."""
from pathlib import Path
import json
from datetime import date

R=Path(__file__).resolve().parents[1]; D=R/'data'
NPS='https://www.nps.gov/articles/'
ROWS={
'pipa-pipa':('Sapo de Surinam; pipa',
 'Anuro sudamericano muy acuático, de cuerpo extraordinariamente aplanado. La hembra incuba los embriones en cavidades de la piel dorsal; emergen pequeñas ranas, sin una fase de renacuajo libre.',
 ['Cabeza ancha y triangular, ojos diminutos y cuerpo plano de color pardo.', 'Manos sin membrana, con extremos digitales divididos en lóbulos; pies posteriores muy palmeados.', 'Las cavidades dorsales son reproductoras y no están presentes en todos los individuos. Contrastar el conjunto corporal.'],
 'Pipa repite un nombre local de Surinam documentado por Daudin (1802), según Pipids of the World. Pipa pipa es un tautónimo: el mismo nombre se usa como género y epíteto. No deriva aquí de una pipa de fumar.',
 ['https://animaldiversity.org/accounts/Pipa_pipa/','https://pddb.org/species.php?taxon=Pipa+pipa']),
'lepiota-procera':('Parasol; apagador; matacandela',
 'Nombre histórico de la especie hoy tratada como Macrolepiota procera. Desarrolla setas grandes, de sombrero escamoso y pie esbelto. Se conserva esta entrada de la lista original sin fusionar su historial de estudio.',
 ['Sombrero con mamelón pardo central y escamas sobre fondo claro.', 'Pie largo con ornamentación parda atigrada y anillo doble móvil.', 'Las esporas o los cistidios aislados no sustituyen el examen del conjunto macroscópico.'],
 'Procera procede del latín procerus, alta o grande, por su porte. Lepiota es el género empleado en el nombre antiguo; la derivación completa de ese nombre genérico queda pendiente de contrastar. No se atribuye a Lepiota la etimología de un género distinto.',
 ['https://www.asturnatura.com/especie/macrolepiota-procera','https://www.inaturalist.org/taxa/63401']),
'platanus-hispanica':('Plátano de sombra; plátano de paseo',
 'Árbol caducifolio de gran talla, habitual en paseos. La entrada sin signo de híbrido de la lista original se relaciona con Platanus × hispanica. Su nomenclatura tiene tratamientos distintos; no se equipara sin más a Platanus orientalis.',
 ['Hojas simples, alternas y palmeadas; los arces semejantes tienen hojas opuestas.', 'Corteza que se desprende en placas, formando un mosaico de tonos claros y verdosos.', 'Infrutescencias esféricas colgantes, frecuentemente en pares. Una hoja aislada no confirma por sí sola el híbrido frente a sus parentales.'],
 'Platanus procede del nombre latino del plátano, relacionado con el griego platýs, ancho, por las hojas. Hispanica alude a variedades procedentes de España según Arbolapp; no demuestra un origen espontáneo ibérico. El signo × indica un híbrido.',
 ['https://www.arbolapp.es/especies/ficha/platanus-hispanica/','https://www.inaturalist.org/taxa/552449']),
'delta':('Delta fluvial',
 'Acumulación de sedimentos en la desembocadura de un río en el mar o en un lago. Se desarrolla cuando el aporte permite construir terreno, pese a la redistribución por oleaje, corrientes y mareas.',
 ['Canales distributarios que se ramifican hacia la desembocadura y cuerpos sedimentarios entre ellos.', 'Puede tener lóbulos o un contorno triangular, pero no todos los deltas son triángulos.', 'La foto del Misisipi usa falso color ASTER; la del Ganges-Brahmaputra es MODIS en color natural.'],
 'Delta es el nombre de la letra griega Δ. El uso geográfico compara algunos depósitos de desembocadura con su silueta triangular; la semejanza no es obligatoria en todos los ejemplos.',
 [NPS+'delta-landforms.htm','https://dle.rae.es/delta','https://science.nasa.gov/earth/earth-observatory/mississippi-river-delta-4526/','https://science.nasa.gov/earth/earth-observatory/ganges-river-delta-1326/']),
'dunas-litorales':('Dunas costeras; dunas litorales',
 'Acumulaciones de arena transportada por el viento desde la playa hacia el interior. La vegetación puede retener sedimento y estabilizar parte de los cordones dunares.',
 ['Montículos o crestas arenosas por encima de la playa, a menudo con vegetación dispersa.', 'Distinguir el relieve de una duna de las pequeñas ondulaciones superficiales de arena.', 'El contexto costero diferencia estas dunas de los campos dunares interiores.'],
 'Duna llegó del neerlandés duin, relacionado con una raíz germánica reconstruida para colina. Litoral indica su situación junto a la costa; su historia lingüística detallada queda pendiente de contrastar.',
 ['https://www.nps.gov/caco/learn/nature/sand-dunes.htm',NPS+'sandy-coast-landforms.htm','https://dle.rae.es/duna']),
'estuario':('Estuario',
 'Cuenca costera conectada con el mar donde confluyen aportes continentales y agua marina, con influencia de las mareas. Su geometría puede conservar un valle fluvial inundado, como Chesapeake.',
 ['Entrada marina que penetra tierra adentro y recibe cauces fluviales; puede presentar brazos ramificados.', 'Los bancos de sedimento y las marismas son frecuentes, pero no bastan solos para identificar el conjunto.', 'No exigir un embudo perfecto: existen varios tipos de estuarios. Distinguirlo de un delta de acumulación y de una laguna litoral.'],
 'Estuario procede del latín aestuarium. El término se relaciona con las mareas, rasgo recogido en la explicación geomorfológica del NPS.',
 [NPS+'estuary-landforms.htm','https://dle.rae.es/estuario','https://science.nasa.gov/earth/earth-observatory/sunny-mid-atlantic-4109/']),
'islas-barrera':('Islas barrera',
 'Islas bajas y alargadas construidas principalmente con arena, aproximadamente paralelas a la costa. Separan el mar abierto de aguas interiores y pueden proteger marismas y lagunas.',
 ['Franja arenosa separada de tierra firme por agua, con caras marina e interior diferenciables.', 'Las bocanas interrumpen la barrera; oleaje y viento pueden modificar su trazado.', 'Diferenciar una isla barrera de una flecha, que mantiene un extremo unido a la costa.'],
 'La expresión describe su forma insular y su función de barrera frente al oleaje. Barrera se forma sobre barra según el DLE; no es el nombre de una familia taxonómica.',
 ['https://www.nps.gov/guis/learn/nature/barrierislands.htm','https://www.nasa.gov/image-article/space-station-visits-south-padre-island/','https://dle.rae.es/barrera']),
'marisma':('Marisma costera',
 'Humedal bajo del litoral inundado por agua marina de forma periódica. Puede formar un mosaico de vegetación tolerante a la sal, superficies fangosas y canales de marea.',
 ['Terreno llano y húmedo con vegetación, surcado a menudo por pequeños canales sinuosos.', 'El contexto mareal y salino lo distingue de muchos humedales interiores.', 'No confundir el banco desnudo intermareal con toda la marisma vegetada que puede rodearlo.'],
 'Marisma procede de la expresión latina maritima ora, referida a las orillas del mar. El nombre conserva su asociación con los terrenos bajos costeros.',
 [NPS+'estuary-landforms.htm','https://www.nps.gov/subjects/geology/coastal-landforms.htm','https://dle.rae.es/marisma']),
'meandro':('Meandro fluvial',
 'Curva de un cauce fluvial sinuoso. La erosión y la deposición pueden desplazarla lateralmente y aguas abajo; algunos recodos llegan a quedar cortados del cauce activo.',
 ['Sucesión de curvas marcadas en un cauce conectado.', 'En muchos ejemplos se aprecian barras de sedimento en la orilla interna y erosión en la externa.', 'Una barra clara no es un lago abandonado: seguir la continuidad del agua antes de responder.'],
 'Meandro viene del latín Maeander y del griego Maíandros, nombre de un río de Asia Menor célebre por su curso sinuoso.',
 [NPS+'meandering-stream.htm','https://science.nasa.gov/earth/earth-observatory/meandering-in-the-amazon-84833/','https://dle.rae.es/meandro']),
'meandro-abandonado-o-encajado-lago-semilunar':('Meandro abandonado; meandro encajado; lago de meandro',
 'Esta entrada original reúne formas relacionadas, pero distintas. Un meandro abandonado queda separado del cauce; si retiene agua puede formar un lago semilunar. Un meandro encajado es una curva excavada en un valle profundo y puede seguir activa.',
 ['Lago de meandro: masa de agua curva desconectada del cauce actual; un paleocauce colmatado puede no tener agua.', 'Meandro encajado: curva fluvial entre paredes de valle o cañón, como The Loop en el Colorado.', 'El recorte del Mamoré muestra huellas de antiguos cauces junto al activo. No convertir todas las curvas en lagos abandonados.'],
 'Meandro remite al río griego Maíandros. Abandonado y encajado describen la relación con el cauce actual y el relieve; semilunar compara la silueta con una media luna, sin implicar un origen lunar.',
 [NPS+'meandering-stream.htm','https://science.nasa.gov/earth/earth-observatory/meandering-in-the-amazon-84833/','https://science.nasa.gov/earth/earth-observatory/the-loop-83875/','https://dle.rae.es/meandro']),
'tombolo':('Tómbolo',
 'Cordón de sedimentos que conecta una isla o un islote con otra masa terrestre. Puede consolidar un antiguo paso de agua y llegar a quedar vegetado o transformado por obras humanas.',
 ['Unión estrecha de sedimento entre dos sectores de tierra, con agua a ambos lados.', 'Comprobar que llega a conectar ambos extremos: una flecha libre no es todavía un tómbolo.', 'Stockton ofrece una vista aérea vegetada; Miquelon-Langlade muestra la conexión a escala orbital y en falso color ASTER.'],
 'Tómbolo llegó del italiano tombolo, procedente del latín tumulus, montón de tierra. El uso geomorfológico designa la acumulación que forma la unión.',
 [NPS+'sandy-coast-landforms.htm','https://home.nps.gov/articles/julian-bay-trail-virtual-hike-apis.htm','https://science.nasa.gov/earth/earth-observatory/saint-pierre-and-miquelon-46153/','https://dle.rae.es/tómbolo'])
}

def main():
 p=D/'study-notes.json';notes=json.loads(p.read_text(encoding='utf8'));added=[]
 for id,(common,description,diagnostics,etymology,urls) in ROWS.items():
  if id in notes:raise ValueError('Existing profile: '+id)
  notes[id]={'commonName':common,'description':description,'diagnostics':diagnostics,'etymology':etymology,'sources':[{'url':u,'title':'Fuente de descripción, identificación o etimología'} for u in urls],'reviewedAt':date.today().isoformat(),'reviewStatus':'reviewed','scope':'Síntesis propia de fuentes identificadas y revisión visual. Se distinguen las limitaciones de una fotografía, los sinónimos históricos y las etimologías pendientes. Sin reglas nemotécnicas.'};added.append(id)
 # A separate catalogue ID remains separate for user progress and overrides.
 notes['platanus-x-hispanica']={**notes['platanus-hispanica'],'description':'Plátano de sombra tratado como híbrido entre Platanus occidentalis y P. orientalis en la ficha taxonómica de iNaturalist. Árbol caducifolio de gran talla muy plantado en paseos; su nomenclatura se ha tratado de distintas maneras.'}
 added.append('platanus-x-hispanica')
 p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8')
 p=D/'family-notes.json';fam=json.loads(p.read_text(encoding='utf8'))
 for name,genus,text,url in [
  ('Pipidae','Pipa','Pipidae se forma sobre Pipa con el sufijo zoológico -idae. Pipa conserva el nombre local surinamés referido por Daudin (1802), según Pipids of the World.','https://pddb.org/species.php?taxon=Pipa+pipa'),
  ('Platanaceae','Platanus','Platanaceae se forma sobre Platanus con la terminación botánica -aceae. Platanus se relaciona con el griego platýs, ancho, por la extensión de las hojas, según Arbolapp.','https://www.arbolapp.es/especies/ficha/platanus-hispanica/')]:
  old=fam.get(name,{})
  fam[name]={**old,'etymology':text,'typeGenus':genus,'sources':[*old.get('sources',[]),{'url':url,'title':'Origen del género que da nombre a la familia'}],'reviewedAt':date.today().isoformat()}
 p.write_text(json.dumps(fam,ensure_ascii=False,indent=2),encoding='utf8')
 print(len(added),'new profiles; 2 family etymologies documented')

if __name__=='__main__':main()
