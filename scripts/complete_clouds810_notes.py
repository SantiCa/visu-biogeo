"""Original, source-backed notes: cloud taxa, features and generating factors."""
from pathlib import Path
from datetime import date
import json
R=Path(__file__).resolve().parents[1];O=R/'tmp/clouds810'
def source(k):return json.loads((O/(k+'.json')).read_text(encoding='utf8'))['url']
E=source('wmo-etymology')
ROWS={
'cataractagenitus':('Nube que se forma en el entorno de una gran cascada por las condiciones de humedad y circulación del aire generadas allí. Las fotos corresponden a Stratus cataractagenitus en las cataratas del Niágara.',
 ['Combinar la presencia de la cascada con jirones nubosos que se condensan por encima de la zona de agua pulverizada.', 'El aerosol de la cascada y la nube condensada son fenómenos relacionados, pero distintos. No llamar nube a toda la columna de salpicaduras.', 'Una sola foto puede no separar con claridad ambos; las fichas de la OMM documentan qué zonas corresponden a nube.'],
 'Cataractagenitus combina los latinos cataracta, cascada, y genitus, generado.', ['wmo-cataracta','wmo-special-8']),
'cauda':('Rasgo suplementario de Cumulonimbus: una prolongación nubosa baja y horizontal en forma de cola que suele conectar con el murus.',
 ['Buscar una cola aproximadamente horizontal que une la región de precipitación con la nube de muro.', 'A diferencia de una tuba, no es un embudo descendente. El recorte conserva la región identificada por la anotación de la OMM.', 'Se diferencia del flumen por su unión con el murus y por su nivel. Una imagen recortada puede mostrar la cola sin toda la estructura de la tormenta.'],
 'Cauda es el nombre latino de la cola.', ['wmo-cauda','wmo-cauda-other','wmo-cauda-4']),
'cavum':('Hueco bien delimitado en una capa delgada de nubes de gotitas de agua subfundidas. Puede ser redondeado o alargado y suele contener precipitación de cristales que se ve como virga.',
 ['Buscar una abertura definida y, con frecuencia, filamentos de hielo que descienden de su interior.', 'La perspectiva puede hacer ovalado un hueco circular. También existen formas lineales asociadas al paso de una aeronave.', 'No confundirlo con cualquier claro irregular de una capa fragmentada. Puede aparecer en Altocumulus, Cirrocumulus y, con menor frecuencia, Stratocumulus.'],
 'El latín cavum significa hueco, cavidad u orificio.', ['wmo-cavum','wmo-cavum-4']),
'flammagenitus':('Nube cuyo desarrollo está ligado a la convección intensa producida por un incendio o una fuente natural de calor semejante. Las imágenes documentan cúmulos generados sobre incendios.',
 ['La nube condensada, con formas cumuliformes, debe diferenciarse de la columna de humo.', 'Valorar la relación con la fuente de calor y la continuidad de la pluma ascendente.', 'Un cúmulo aislado puede parecer igual que otro de origen ordinario: la fuente y la observación del episodio son esenciales para afirmar el origen.'],
 'Flammagenitus une los latinos flamma, fuego, y genitus, generado.', ['wmo-flamma','wmo-special-4']),
'fluctus':('Rasgo suplementario formado por ondulaciones de aspecto rizado o de ola rompiente, habitualmente en la parte superior de una nube.',
 ['Crestas sucesivas que se curvan como rompientes; no basta con que la nube tenga una superficie ondulada.', 'Se asocia a ondas de Kelvin–Helmholtz y suele durar poco.', 'Distinguirlo de undulatus, con bandas u ondulaciones más regulares, y de asperitas, donde destaca la rugosidad de la base.'],
 'Fluctus es el término latino para ola u oleaje.', ['wmo-fluctus','wmo-fluctus-4']),
'flumen':('Nube accesoria de una supercélula que aparece como una banda de entrada de aire hacia su corriente ascendente. Una forma ancha y plana recibe el nombre de cola de castor.',
 ['Banda nubosa relativamente baja que converge hacia la zona ascendente de la tormenta.', 'Su base queda más alta que el murus y no está unida a este como la cauda. Los recortes conservan las regiones señaladas en las fotos de la OMM.', 'El movimiento de entrada es parte de la identificación, pero una fotografía fija no lo demuestra. Por ello estas vistas se tratan como detalles de apoyo.'],
 'Flumen alude en latín a una corriente, río o arroyo.', ['wmo-flumen','wmo-murus-detail','wmo-flumen-4']),
'homogenitus':('Calificador de origen para nubes formadas por actividad humana. El catálogo muestra ejemplos vinculados a plumas industriales, fuegos de origen humano y estelas de aeronaves.',
 ['Combinar la nube condensada con la fuente que la genera; humo y nube no son equivalentes.', 'Las estelas persistentes de aeronaves se denominan Cirrus homogenitus en el atlas de la OMM.', 'No es un género nuboso ni una forma única. Si el origen no está documentado, el aspecto aislado no basta para distinguirla de una nube natural.'],
 'Homogenitus combina el latín homo, ser humano, y genitus, generado. Homo no es aquí el griego de semejante.', ['wmo-homogen','wmo-special-5','wmo-contrails']),
'homomutatus':('Calificador de una nube originada por actividad humana que ha evolucionado hasta adoptar el aspecto de una nube de otra categoría. Las imágenes incluyen estelas extendidas y transformadas en cirros.',
 ['Pueden verse filamentos o mechones que han perdido la geometría rectilínea inicial de una estela.', 'Los dos campos de la secuencia de la OMM muestran momentos diferentes de una misma evolución, además de otro ejemplo independiente.', 'Un cirro natural puede presentar el mismo aspecto. Para afirmar homomutatus hay que conocer o documentar la evolución desde la nube artificial.'],
 'Homomutatus combina los latinos homo, ser humano, y mutatus, cambiado.', ['wmo-homomut','wmo-special-7']),
'silvagenitus':('Nube que se desarrolla sobre un bosque en relación con el aire húmedo aportado por evaporación y evapotranspiración. Los ejemplos de la OMM muestran jirones de Stratus junto al dosel forestal.',
 ['Jirones nubosos próximos al bosque, en un contexto favorable de humedad y movimientos locales del aire.', 'No toda niebla sobre un bosque es automáticamente silvagenitus. Es necesario relacionar la formación de la nube con el ambiente forestal.', 'La secuencia de la fuente distingue disipación de niebla y formación posterior de nuevos jirones; la fotografía fija solo conserva una fase.'],
 'Silvagenitus combina los latinos silva, bosque, y genitus, generado.', ['wmo-silva','wmo-special-9']),
'volutus-o-nube-enrollada':('Especie nubosa que forma una masa alargada y horizontal, con aspecto de rodillo y separada de otras nubes. Aparece sobre todo en Stratocumulus y, con menor frecuencia, en Altocumulus.',
 ['Contorno tubular largo y aislado; comprobar que no sea solo el borde de una nube mayor.', 'Un arcus está ligado a la nube madre; la separación es un criterio importante del volutus.', 'Las dos fotos documentan Altocumulus volutus en Australia y un volutus identificado por SMHI en Suecia. La rotación aparente requiere observar el movimiento.'],
 'Volutus significa enrollado en latín y describe su forma de rodillo.', ['wmo-volutus','wmo-volutus-4','smhi-stratocumulus']),
'asperitas':('Rasgo suplementario con ondulaciones irregulares y una base de aspecto rugoso, semejante a una superficie marina agitada vista desde abajo.',
 ['Relieve caótico de la base, con ondulaciones de tamaño y forma variables.', 'El juego de luces realza la textura, pero el color oscuro o el aspecto amenazante por sí solos no identifican asperitas.', 'Comparar con undulatus, más organizado, y con las crestas de ola rompiente del fluctus. Se observa especialmente en Altocumulus y Stratocumulus.'],
 'Asperitas es el sustantivo latino que expresa rugosidad.', ['wmo-asperitas','wmo-asperitas-detail']),
'murus':('Rasgo suplementario de Cumulonimbus: descenso localizado y persistente de la base de la nube, con aspecto de muro bajo la zona ascendente de una tormenta.',
 ['Buscar una base descendida respecto a la nube que la rodea, con su relación espacial con la zona de precipitación.', 'No confundir el murus con todo el frente de racha o arcus.', 'Puede presentar movimientos intensos, pero una foto fija no demuestra rotación. Un murus no implica por sí solo que haya un tornado.'],
 'Murus significa muro en latín; alude al descenso abrupto de la base.', ['wmo-murus','wmo-murus-detail']),
'contrails':('Estelas de condensación asociadas a aeronaves. Pueden ser breves o persistir y evolucionar, según las condiciones atmosféricas.',
 ['Trazos alargados asociados al paso de aeronaves; su anchura y continuidad cambian con el tiempo.', 'La OMM denomina Cirrus homogenitus a las estelas que han persistido al menos diez minutos.', 'Si se transforman y pierden su aspecto de estela, puede corresponder homomutatus. Una fotografía no permite medir por sí sola la duración.'],
 'Contrails corresponde al inglés condensation trails, estelas de condensación. Cirrus significa mechón en latín.', ['wmo-contrails','wmo-special-6'])
}
def main():
 p=R/'data/study-notes.json';notes=json.loads(p.read_text(encoding='utf8'));cat={x['id'] for x in json.loads((R/'data/species.json').read_text(encoding='utf8'))}
 for id,(description,diagnostics,etymology,keys) in ROWS.items():
  if id not in cat or id in notes:raise ValueError('Unknown or existing profile: '+id)
  urls=list(dict.fromkeys([source(k) for k in keys]+[E]))
  notes[id]={'description':description,'diagnostics':diagnostics,'etymology':etymology,'sources':[{'url':u,'title':'OMM · etimología de los nombres latinos' if u==E else 'SMHI · fotografía y clasificación' if 'smhi.se' in u else 'OMM · definición o fotografía comentada'} for u in urls],'reviewedAt':date.today().isoformat(),'reviewStatus':'reviewed','scope':'Síntesis propia de fuentes meteorológicas. Se distingue género, especie, rasgo suplementario, nube accesoria y origen; no son rangos biológicos ni tienen familia taxonómica. No se deducen duración, rotación o historia causal a partir de una foto fija.'}
 p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8');print(len(ROWS),'new profiles')
if __name__=='__main__':main()
