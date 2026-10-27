"""Source-backed original study notes for the visually reviewed histology batch."""
from pathlib import Path
import json
from datetime import date
R=Path(__file__).resolve().parents[1]
Y='https://www.medcell.org/histology/'
S='https://histology.siu.edu/'
D='https://dicciomed.usal.es/palabra/'
E=S+'eponyms.htm'
V='https://www.uv.es/histomed/medicinaEsp/01/MEsp01-06.html'
ROWS={
'seccion-de-cerebelo':('Región del encéfalo cuya corteza se pliega en folias y participa en el control y aprendizaje de los movimientos.',
 ['Las folias contienen sustancia blanca central rodeada por corteza.', 'Reconocer una capa molecular relativamente clara, una hilera de grandes células de Purkinje y una capa granulosa muy celular.', 'La organización en tres capas permite separarla de la corteza cerebral; el color depende de la tinción.'],
 'Cerebelo viene del latín cerebellum, diminutivo de cerebrum: cerebro pequeño.',[V,D+'cerebelo']),
'seccion-de-cerebelo-celulas-de-purkinje':('Neuronas grandes de la corteza cerebelosa, con un árbol dendrítico que se extiende por la capa molecular.',
 ['Somas grandes, aproximadamente piriformes, dispuestos en una hilera entre las capas molecular y granulosa.', 'Relacionar la célula con ambas capas: una neurona grande aislada no basta.', 'Los métodos de impregnación muestran más dendritas que una tinción histológica ordinaria.'],
 'Purkinje es un epónimo dedicado al anatomista bohemio Jan Purkinje. No describe una forma celular ni tiene una traducción anatómica literal.',[Y+'nervous_system_lab/purkinje_cells.php',V,E]),
'corteza-cerebral-celulas-piramidales':('Neuronas corticales llamadas piramidales por la forma de su soma y la disposición de sus prolongaciones.',
 ['Cuerpo triangular, una dendrita apical dirigida hacia la superficie y dendritas basales.', 'La imagen de impregnación conserva el contorno y las prolongaciones de una célula; no muestra todas las capas corticales.', 'Distinguirlas de las células de Purkinje usando la forma dendrítica y la organización del tejido.'],
 'Piramidal alude a la semejanza con una pirámide. La historia lingüística completa de la expresión células piramidales queda pendiente de contraste.',[Y+'nervous_system_lab/pyramidal_cell.php']),
'axon-con-vaina-de-mielina':('Prolongación neuronal rodeada por envolturas de mielina que favorecen la conducción rápida del impulso.',
 ['En sección transversal se observa el axoplasma central rodeado por láminas concéntricas de mielina.', 'El osmio oscurece los lípidos; en microscopía electrónica se distingue mejor la disposición laminar.', 'Una gota lipídica también puede teñirse de negro: buscar el axón central y la disposición de las fibras.'],
 'Axón procede del griego áxōn, eje. Mielina se forma sobre myelós, médula, con el sufijo de sustancia -ina; el nombre pasó por el alemán Myelin.',[Y+'nervous_system_lab/myelinated_axon_em.php',S+'ssb/BH006b.htm',D+'axon',D+'mielina']),
'nodo-de-ranvier':('Interrupción de la vaina de mielina entre segmentos consecutivos de un axón, relacionada con la conducción saltatoria.',
 ['En la fibra longitudinal se ve una discontinuidad corta entre dos segmentos mielínicos.', 'El axón continúa a través del nodo; no es una rotura completa del nervio.', 'Una de las vistas es una ilustración histórica de Ranvier y no una micrografía.'],
 'Ranvier es un epónimo dedicado al histólogo francés Louis Antoine Ranvier. El nombre identifica al investigador, no una raíz descriptiva de la estructura.',[Y+'nervous_system_lab/nodes_of_ranvier.php',S+'ssb/node-ranvier.htm',E]),
'sinapsis-nerviosa':('Zona de comunicación entre una neurona y otra célula. La imagen incorporada corresponde a una sinapsis química vista con microscopía electrónica.',
 ['Botón presináptico con vesículas próximo a una membrana postsináptica.', 'Buscar la hendidura y las especializaciones de membrana en la zona de contacto.', 'Las vesículas y la organización de la unión ayudan a distinguirla de dos membranas celulares simplemente próximas.'],
 'Sinapsis reúne elementos griegos relacionados con unión y contacto: sýn, junto, y la raíz de tocar, con -sis. El término se aplicó a la unión funcional neuronal.',[Y+'nervous_system_lab/synapse_em.php',D+'sinapsis']),
'retina':('Tejido nervioso fotosensible que reviste la parte interna del ojo y contiene fotorreceptores y circuitos de procesamiento visual.',
 ['Alternancia de capas nucleares densas y capas plexiformes más claras.', 'Hacia el exterior se sitúan los fotorreceptores y el epitelio pigmentario; hacia el vítreo, las células ganglionares y sus axones.', 'El grosor y la densidad de las capas cambian entre regiones de la retina. No interpretar la orientación solo por arriba y abajo de la fotografía.'],
 'Retina procede del latín medieval retina, relacionado con rete, red. Su historia es la de una denominación anatómica transmitida mediante traducciones.',[Y+'sensory_systems_lab/retina.php',S+'ssb/NM012b.htm',D+'retina']),
'ojo':('Órgano de la visión. Esta preparación muestra una sección amplia del globo ocular de un vertebrado.',
 ['Reconocer la pared del globo, el cristalino y los compartimentos del interior.', 'La relación espacial del cristalino con la pared y las cavidades permite reconocer el conjunto.', 'La retina aislada se estudia en otra entrada; no toda sección ocular muestra todas las estructuras con igual detalle.'],
 'Ojo procede del latín oculus.',[Y+'sensory_systems_lab/eye.php','https://dle.rae.es/ojo']),
'oido-interno-seccion-de-coclea-organo-de-corti':('La cóclea contiene el aparato receptor auditivo. El órgano de Corti se encuentra sobre la membrana basilar, dentro del conducto coclear.',
 ['Buscar el epitelio sensorial y el espacio del túnel de Corti bajo la membrana tectoria.', 'Las imágenes son campos de detalle del órgano de Corti; no representan toda la espiral de la cóclea.', 'Combinar el epitelio sensorial, sus apoyos y las membranas; una cavidad aislada no permite identificar la preparación.'],
 'Cóclea procede del latín cochlea y del griego kochlías, asociado a la forma de caracol. Corti conmemora al anatomista italiano Alfonso Giacomo Gaspare Corti.',[Y+'sensory_systems_lab/organ_of_corti.php',S+'ssb/EE001b.htm','https://dle.rae.es/cóclea',E]),
'piel-corpusculo-de-vater-paccini':('Receptor encapsulado de la sensibilidad mecánica, presente en regiones profundas de la piel y otros tejidos.',
 ['Láminas concéntricas alrededor de una terminación nerviosa central, con aspecto de cebolla cortada.', 'Separarlo de un folículo piloso: aquí se reconocen lamelas y no un tallo de pelo con sus vainas epiteliales.', 'La denominación habitual es corpúsculo de Vater-Pacini; se conserva la grafía de la lista original como nombre de entrada.'],
 'Vater-Pacini reúne los apellidos de Abraham Vater y Filippo Pacini, asociados a la descripción de estos receptores. Paccini, usado en la lista original, es una variante gráfica que no cambia la estructura estudiada.',[Y+'skin_lab/pacinian_corpuscle.php',S+'ssb/IN039b.htm',E]),
'foliculo-de-graaf':('Folículo ovárico maduro con un gran antro. El ovocito queda asociado a células de la granulosa en una posición excéntrica.',
 ['En la vista general, gran cavidad antral, granulosa periférica y ovocito rodeado por sus envolturas celulares.', 'Por fuera de la granulosa se sitúan las tecas.', 'El segundo campo solo muestra la pared folicular. Sin la vista general no permite demostrar por sí solo que el folículo sea preovulatorio.'],
 'Folículo viene del latín folliculum, diminutivo relacionado con una bolsa: bolsita. De Graaf es un epónimo dedicado al médico neerlandés Reinier de Graaf.',[Y+'female_reproductive_system_lab/graafian_follicle.php',S+'ssb/RE005b.htm',D+'foliculo',E]),
'vagina':('Conducto fibromuscular del aparato reproductor femenino. La preparación muestra su mucosa y parte del tejido subyacente.',
 ['Epitelio plano estratificado y tejido conjuntivo bajo la superficie plegada.', 'En humanos el epitelio es habitualmente no queratinizado; el aspecto cambia con la especie y el contexto hormonal.', 'El epitelio aislado también aparece en otros órganos: esta imagen parcial no se considera diagnóstica por sí sola para el modo Andalucía.'],
 'Vagina procede del latín vagina, vaina.',[Y+'female_reproductive_system_lab/vagina.php','https://dle.rae.es/vagina']),
'papila-lingual-corpusculos-gustativos':('Las papilas de la lengua pueden alojar botones o corpúsculos gustativos, agrupaciones de células especializadas dentro del epitelio.',
 ['Botones ovalados y relativamente claros entre las células epiteliales, con su extremo apical dirigido hacia la superficie.', 'No confundir el botón gustativo con toda la papila, que incluye un eje conjuntivo.', 'La imagen de Yale procede de una papila circunvalada; la de SIU, de una papila foliada de conejo. Ambas permiten estudiar botones gustativos.'],
 'Papila viene del latín papilla, referido a un pezón; el nombre compara una pequeña prominencia con esa forma. Gustativo indica su relación con el sentido del gusto.',[Y+'sensory_systems_lab/taste_buds.php',S+'ssb/GI048b.htm','https://dle.rae.es/papila']),
'bronquio':('Vía conductora del aparato respiratorio. La imagen corresponde a un bronquio intrapulmonar rodeado por parénquima pulmonar.',
 ['Pared con placas de cartílago y mucosa respiratoria; pueden reconocerse glándulas submucosas.', 'En la vista general, relacionar la vía aérea con el tejido pulmonar que la rodea.', 'Los bronquiolos carecen de cartílago y de glándulas submucosas. Una fotografía de bronquiolo no sustituye esta entrada.'],
 'Bronquio procede del latín tardío bronchia, tomado del plural griego brónchia.',[Y+'respiratory_system_lab/bronchus.php','https://dle.rae.es/bronquio']),
'peroxisomas':('Orgánulos rodeados por una membrana, relacionados con procesos oxidativos y con el metabolismo del peróxido de hidrógeno.',
 ['En microscopía electrónica pueden aparecer como cuerpos pequeños con matriz granular; en ciertos tejidos presentan un centro más denso.', 'Una esfera membranosa aislada no permite distinguirlos con seguridad de otros orgánulos: son importantes la identificación de la fuente y las técnicas específicas.', 'La ficha se completa, pero no se incorpora como foto de examen el esquema de reacciones del atlas.'],
 'Peroxisoma combina peróxido, por su relación con el peróxido de hidrógeno, y el elemento griego soma, cuerpo.', ['https://mmegias.webs.uvigo.es/5-celulas/6-peroxisomas.php','https://www.cun.es/diccionario-medico/terminos/peroxisoma'])
}

def main():
 p=R/'data/study-notes.json';notes=json.loads(p.read_text(encoding='utf8'))
 for suffix,(description,diagnostics,etymology,urls) in ROWS.items():
  key='estructura-'+suffix
  if key in notes:raise ValueError('Refuse to overwrite '+key)
  notes[key]={'description':description,'diagnostics':diagnostics,'etymology':etymology,'sources':[{'url':u,'title':'Etimología e historia del término' if 'dicciomed' in u or 'dle.rae' in u or u==E else 'Atlas o diccionario universitario · estructura y preparación'} for u in urls],'reviewedAt':date.today().isoformat(),'reviewStatus':'reviewed','scope':'Síntesis propia. Se distinguen órgano, tejido y detalle celular; las limitaciones de identificación y las etimologías pendientes se indican expresamente. No corresponde una familia taxonómica a una estructura histológica.'}
 p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8');print(len(ROWS),'new profiles')

if __name__=='__main__':main()
