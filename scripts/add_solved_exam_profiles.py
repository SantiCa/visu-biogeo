"""Original, bounded study summaries for entries documented in the supplied keys.

Unverified word origins stay explicitly pending. No mnemonic fields are created.
"""
from pathlib import Path
import json
D=Path(__file__).resolve().parents[1]/'data'

def main():
    notes=json.loads((D/'study-notes.json').read_text(encoding='utf8'))
    families=json.loads((D/'family-notes.json').read_text(encoding='utf8'))
    taxonomy=json.loads((D/'taxonomy.json').read_text(encoding='utf8'))
    curated=json.loads((D/'curated-images.json').read_text(encoding='utf8'))
    rows=[
      ('acanthus-mollis','Acanto','Hierba perenne de grandes hojas basales y espigas florales erguidas.',
       ['Hojas anchas, profundamente divididas, agrupadas en la base.','Flores claras con brácteas y cálices de tonos purpúreos; observar la espiga y las hojas conjuntamente.'],
       'Acanthus procede del nombre grecolatino del acanto, relacionado con la palabra griega para espina. Mollis significa blando o suave en latín.',
       'https://www.asturnatura.com/especie/acanthus-mollis'),
      ('bougainvillea-spectabilis','Buganvilla','Trepadora leñosa ornamental, con ramas espinosas y brácteas vistosas alrededor de flores pequeñas.',
       ['Las piezas grandes y coloreadas son brácteas; las flores verdaderas son pequeñas y tubulares.','La pilosidad de las hojas ayuda frente a B. glabra; el color por sí solo no identifica la especie.'],
       'La dedicatoria del género y el significado exacto del epíteto están pendientes de contraste documental.',
       'https://www.asturnatura.com/fotografia/flora-ornamental/bougainvillea-spectabilis-1/26122.html'),
      ('clavelina-lepadiformis','Clavelina','Ascidia colonial con pequeños individuos transparentes unidos por la base.',
       ['Colonias de zooides con aspecto de botellitas transparentes.','Líneas blancas recorren los individuos y rodean los sifones próximos entre sí.'],
       'Origen de Clavelina y lepadiformis pendiente de contraste; no se deduce solo de su aspecto.',
       'https://www.asturnatura.com/especie/clavelina-lepadiformis'),
      ('dama-dama','Gamo','Cérvido con manchas claras frecuentes en el pelaje estival y astas palmeadas en los machos adultos.',
       ['El extremo de las astas del macho adulto forma una pala ancha; las hembras carecen de astas.','Escudo anal blanco con borde oscuro y cola relativamente larga. El moteado varía con la estación y el individuo.'],
       'La repetición Dama dama es un tautónimo zoológico. El origen lingüístico de dama está pendiente de contraste.',
       'https://www.asturnatura.com/especie/dama-dama'),
      ('daphnia-pulex','Pulga de agua','Pequeño crustáceo de agua dulce, de cuerpo lateralmente comprimido y carapacho transparente.',
       ['Ojo oscuro conspicuo y antenas natatorias ramificadas; pueden verse huevos en la cámara dorsal.','La silueta permite reconocer Daphnia, pero separar especies del complejo pulex requiere caracteres microscópicos y una clave.'],
       'Origen de Daphnia y pulex pendiente de contraste documental.',
       'https://animaldiversity.org/accounts/Daphnia_pulex/'),
      ('eliomys-quercinus','Lirón careto','Pequeño roedor con antifaz oscuro y cola peluda rematada por un pincel contrastado.',
       ['Banda negra alrededor de los ojos que continúa hacia las orejas.','Orejas grandes, vientre claro y extremo de la cola con pelos largos blancos y negros.'],
       'Origen de Eliomys y quercinus pendiente de contraste documental.',
       'https://www.asturnatura.com/especie/eliomys-quercinus'),
      ('espilita','Espilita','Roca volcánica básica alterada, habitualmente derivada de basaltos con transformación de las plagioclasas hacia albita.',
       ['Puede presentar color verdoso, amígdalas rellenas y venas claras de minerales secundarios.','No todo basalto verde es espilita: la textura externa orienta, pero su identificación precisa necesita mineralogía y contexto.'],
       'El origen lingüístico del término espilita está pendiente de contraste. No es una especie y no tiene familia taxonómica.',
       'https://www.mindat.org/min-50065.html'),
      ('fomes-fomentarius','Yesquero','Hongo de madera con cuerpos fructíferos perennes, duros y de aspecto de casco.',
       ['Sombrero grueso, generalmente grisáceo, con bandas o surcos concéntricos.','Cara inferior con poros finos, sin láminas. Comparar con otros políporos y no identificar por el árbol hospedador solamente.'],
       'Fomes significa yesca en latín; fomentarius alude al uso como yesca. Ambos elementos remiten al aprovechamiento tradicional de su tejido seco.',
       'https://www.first-nature.com/fungi/fomes-fomentarius.php'),
      ('gneis-glandular','Gneis glandular u ocelar','Roca metamórfica foliada con grandes cristales o agregados lenticulares que destacan en una matriz bandeada.',
       ['Los ojos, a menudo feldespáticos, son rodeados por bandas de minerales más oscuros.','Debe verse la relación entre los ojos y la foliación; un granito con cristales grandes sin esa estructura no basta.'],
       'La denominación inglesa augen gneiss incorpora el alemán Augen, ojos, en referencia a sus agregados ocelados. El origen remoto de gneis queda pendiente de contraste.',
       'https://geodil.dperkins.org/h/338.html'),
      ('ixodes-hexagonus','Garrapata del erizo','Garrapata dura asociada a erizos y otros mamíferos; su aspecto cambia mucho al alimentarse.',
       ['Adultos y ninfas con cuatro pares de patas; no usar el tamaño de una hembra engordada como diagnóstico.','La confirmación frente a otros Ixodes requiere observar estructuras del capítulo y de la cara ventral con una clave; la foto general no las sustituye.'],
       'Origen de Ixodes y hexagonus pendiente de contraste documental.',
       'https://pmc.ncbi.nlm.nih.gov/articles/PMC5670724/'),
      ('jacaranda-mimosifolia','Jacaranda','Árbol ornamental con hojas muy divididas y floración azul violácea.',
       ['Hojas bipinnadas con numerosos folíolos pequeños.','Flores tubulares acampanadas y frutos leñosos aplanados, aproximadamente redondeados.'],
       'Mimosifolia significa con hojas semejantes a las de Mimosa; es una comparación foliar, no un parentesco cercano. El origen de Jacaranda queda pendiente de contraste.',
       'https://plants.ces.ncsu.edu/plants/jacaranda-mimosifolia/common-name/jacaranda/'),
      ('latrodectus-tredecimguttatus','Viuda negra mediterránea','Araña de abdomen redondeado; las hembras fotografiadas muestran manchas rojizas sobre fondo negro.',
       ['Abdomen voluminoso y patas relativamente finas.','El patrón rojo puede orientar, pero varía con el desarrollo; confirmar especies próximas mediante una clave especializada.'],
       'El nombre original documentado por Rossi se escribió Aranea 13-guttata y alude a trece manchas. La etimología de Latrodectus queda pendiente de contraste.',
       'https://www.wsc.nmbe.ch/spec-data/45689/species'),
      ('noctiluca-scintillans','Noctiluca','Dinoflagelado marino de célula grande y aproximadamente globosa; algunas poblaciones producen bioluminiscencia.',
       ['En aumento se observa una célula globosa, con una región oral y un tentáculo conspicuo.','Una fotografía del mar iluminado no basta para identificar la especie; estudiar las imágenes celulares.'],
       'La explicación lingüística precisa de Noctiluca y scintillans está pendiente de contraste documental.',
       'https://www.anbg.gov.au/abrs/Dinoflagellates/Species/Noctiluca_scintillans.pdf'),
      ('ovis-orientalis-musimon','Muflón','Ovino silvestre cuyo macho adulto suele portar grandes cuernos curvados.',
       ['Cuernos permanentes curvados a ambos lados de la cabeza, sin las ramificaciones de las astas de los cérvidos.','El pelaje y la mancha clara del costado varían con sexo, edad y época; no identificarlos por un único macho.'],
       'El origen lingüístico de los tres elementos queda pendiente de contraste. Se conserva el nombre del examen; la fuente fotográfica emplea Ovis aries musimon para este taxón.',
       None),
      ('porcellio-scaber','Cochinilla de la humedad','Isópodo terrestre de cuerpo aplanado y dorso fuertemente granuloso.',
       ['Dorso tuberculado, de color gris frecuente pero con variaciones y ejemplares moteados.','Flagelo antenal con dos segmentos y dos pares de pulmones pleopodales; estos caracteres ayudan frente a otras cochinillas.'],
       'Origen de Porcellio y scaber pendiente de contraste documental.',
       'https://bmig.org.uk/species/porcellio-scaber'),
      ('sphagnum-subnitens','Esfagno (nombre del género)','Musgo de ambientes húmedos con ramas agrupadas y un capítulo terminal compacto.',
       ['En formas iluminadas puede verse un centro verde y una periferia rojiza en el capítulo; las formas de sombra pueden ser verdes.','Las hojas secas pueden mostrar brillo plateado. El color no basta: confirmar con una clave y caracteres microscópicos.'],
       'Origen de Sphagnum y subnitens pendiente de contraste documental. Subtinens es una errata del enunciado, no un sinónimo aceptado.',
       'https://www.britishbryologicalsociety.org.uk/learning/species-finder/sphagnum-subnitens-var-subnitens/'),
      ('stentor-sp','Ciliado trompeta (nombre descriptivo)','Género de ciliados unicelulares que pueden adoptar forma de trompeta al extenderse.',
       ['Extremo anterior ensanchado con zona oral ciliada; extremo posterior estrecho de fijación.','Se contrae y cambia de forma. El examen solo identifica el género: no exigir una especie concreta ni un color único.'],
       'La procedencia del nombre Stentor está pendiente de contraste. Sp. indica una especie no determinada del género, no forma parte de su nombre específico.',
       'https://www.wfoissner.at/data_prot/Foissner_2002_561-566.pdf'),
      ('yucca-gigantea','Yuca gigante','Planta arborescente ornamental, de tronco grueso y rosetas terminales de hojas alargadas.',
       ['Hojas dispuestas en roseta en el extremo de tallos leñosos, con puntas menos punzantes que otras yucas.','Puede tener la base del tronco ensanchada y flores claras acampanadas en inflorescencias elevadas.'],
       'El sinónimo Yucca elephantipes alude al tronco semejante a una pata de elefante. La etimología de Yucca y del epíteto gigantea queda pendiente de contraste.',
       'https://plants.ces.ncsu.edu/plants/yucca-gigantea/common-name/spineless-yucca/'),
      ('globigerina','Globigerina (foraminífero)','Género de foraminíferos planctónicos con concha formada por cámaras globosas; se estudia también entre los microfósiles.',
       ['Concha de cámaras redondeadas en una espiral baja y abertura hacia la región umbilical.','Las imágenes representan G. bulloides como ejemplo del género. Diferenciarla de otros géneros exige observar el número de cámaras, la abertura y la pared.'],
       'Origen de Globigerina pendiente de contraste documental; no se asigna una raíz por semejanza de palabras.',
       'https://www.mikrotax.org/pforams/index.php?module=pf_neogene&taxon=Globigerina+bulloides'),
    ]
    for id,common,desc,traits,etym,source in rows:
        sources=[]
        if source:sources.append({'url':source,'title':'Ficha y caracteres de referencia'})
        if id in taxonomy:sources.append({'url':taxonomy[id]['source'],'title':'Correspondencia taxonómica de la entrada'})
        for im in curated.get(id,{}).get('images',[]):
            if im['status']=='approved' and im.get('page') not in [s['url'] for s in sources]:
                sources.append({'url':im['page'],'title':'Ejemplar identificado y rasgos visuales'})
                break
        notes[id]={'commonName':common,'description':desc,'diagnostics':traits,'etymology':etym,'sources':sources,'reviewedAt':'2026-10-26','reviewStatus':'reviewed','scope':'Resumen propio de caracteres documentados y visibles; los límites de identificación y los orígenes lingüísticos pendientes se indican expresamente.'}
    construction={
      'Acanthaceae':('Acanthus','botanical'),'Nyctaginaceae':('Nyctago','botanical'),
      'Clavelinidae':('Clavelina','zoological'),'Cervidae':('Cervus','zoological'),
      'Daphniidae':('Daphnia','zoological'),'Gliridae':('Glis','zoological'),
      'Polyporaceae':('Polyporus','botanical'),'Ixodidae':('Ixodes','zoological'),
      'Bignoniaceae':('Bignonia','botanical'),'Theridiidae':('Theridion','zoological'),
      'Noctilucaceae':('Noctiluca','botanical'),'Bovidae':('Bos','zoological'),
      'Porcellionidae':('Porcellio','zoological'),'Sphagnaceae':('Sphagnum','botanical'),
      'Stentoridae':('Stentor','zoological'),'Globigerinidae':('Globigerina','zoological')}
    for name,(genus,code) in construction.items():
        if name in families:continue
        ending='-aceae' if code=='botanical' else '-idae'
        url='https://iapt-taxon.org/melbourne/main.php?page=art18' if code=='botanical' else 'https://code.iczn.org/formation-and-treatment-of-names/article-29-family-group-names/'
        families[name]={'etymology':f'Nombre construido sobre el género tipo {genus}, con la terminación familiar {ending}. La raíz lingüística remota del género queda pendiente de contraste.','typeGenus':genus,'sources':[{'url':url,'title':'Construcción nomenclatural de los nombres de familia'}],'reviewedAt':'2026-10-26'}
    taxonomy['globigerina']={'family':'Globigerinidae','matchedName':'Globigerina','source':'https://www.mikrotax.org/pforams/index.php?module=pf_neogene&taxon=Globigerina+bulloides','checkedAt':'2026-10-26','aliases':[]}
    for name,obj in [('study-notes.json',notes),('family-notes.json',families),('taxonomy.json',taxonomy)]:
        (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{len(rows)} perfiles revisados; {len(notes)} perfiles en total; {len(families)} notas de familia; sin reglas nemotécnicas añadidas.')

if __name__=='__main__':main()
