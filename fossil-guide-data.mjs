// Ordered bins support comparison at period/epoch level, not numerical dating.
export const GEOLOGICAL_INTERVALS=[
 {id:'cambrian',name:'Cámbrico',era:'Paleozoico'},
 {id:'ordovician',name:'Ordovícico',era:'Paleozoico'},
 {id:'silurian',name:'Silúrico',era:'Paleozoico'},
 {id:'devonian',name:'Devónico',era:'Paleozoico'},
 {id:'carboniferous',name:'Carbonífero',era:'Paleozoico'},
 {id:'permian',name:'Pérmico',era:'Paleozoico'},
 {id:'triassic',name:'Triásico',era:'Mesozoico'},
 {id:'jurassic',name:'Jurásico',era:'Mesozoico'},
 {id:'cretaceous',name:'Cretácico',era:'Mesozoico'},
 {id:'paleocene',name:'Paleoceno',era:'Cenozoico'},
 {id:'eocene',name:'Eoceno',era:'Cenozoico'},
 {id:'oligocene',name:'Oligoceno',era:'Cenozoico'},
 {id:'neogene',name:'Neógeno',era:'Cenozoico'},
 {id:'quaternary',name:'Cuaternario',era:'Cenozoico'}
];

export const FOSSIL_GUIDES=[
 {
  id:'trilobites',name:'Trilobites',group:'Artrópodos',scope:'Grupo amplio',
  intervals:['cambrian','ordovician','silurian','devonian','carboniferous','permian'],
  age:'Cámbrico–Pérmico',recognition:'Exoesqueleto dividido en tres lóbulos longitudinales, con cefalón, tórax segmentado y pigidio.',
  precision:'Un trilobite sin determinar orienta al Paleozoico. Identificar el género o la especie permite afinar.',
  sources:[{title:'BGS · Trilobites',url:'https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/trilobites/'}]
 },
 {
  id:'paradoxides',name:'Paradoxides',catalogId:'paradoxides',group:'Trilobites',scope:'Género',
  intervals:['cambrian'],age:'Cámbrico medio, denominación tradicional',
  recognition:'Trilobite con tórax largo y pigidio pequeño. Compara también el cefalón y las espinas genales.',
  precision:'Acota mucho más que «trilobite». La franja señala el Cámbrico completo porque esa es la resolución del esquema.',
  sources:[{title:'Museo Geológico de la Academia Polaca de Ciencias · Paradoxides',url:'https://muzea.malopolska.pl/en/objects-list/762'}]
 },
 {
  id:'graptolites',name:'Graptolitos',group:'Colonias marinas',scope:'Grupo amplio',
  intervals:['cambrian','ordovician','silurian','devonian','carboniferous'],age:'Cámbrico–Carbonífero',
  recognition:'Marcas finas, a veces brillantes, con ramas y pequeñas tecas sucesivas.',
  precision:'Los planctónicos son especialmente útiles en Ordovícico y Silúrico. El conjunto incluye formas con un recorrido mayor.',
  sources:[{title:'BGS · Graptolites',url:'https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/graptolites/'}]
 },
 {
  id:'monograptus',name:'Monograptus',catalogId:'monograptus',group:'Graptolitos',scope:'Género en sentido tradicional',
  intervals:['silurian','devonian'],age:'Silúrico–Devónico inferior',
  recognition:'Colonia con una sola rama y una serie de tecas. Las formas pueden ser rectas o curvadas.',
  precision:'La asociación escolar con el Silúrico es orientativa. Hay monográptidos que cruzan el límite con el Devónico y la clasificación ha sido revisada.',
  sources:[{title:'BGS · Monográptidos',url:'https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/graptolites/'},{title:'Palaeontology · monográptidos silúricos y prolongación al Devónico inferior',url:'https://palass.org/sites/default/files/media/publications/palaeontology/volume_15/vol15_part4_pp579-597.pdf'}]
 },
 {
  id:'fusulinids',name:'Fusulínidos',group:'Foraminíferos',scope:'Grupo amplio',
  intervals:['carboniferous','permian'],age:'Carbonífero–Pérmico',
  recognition:'Tests de foraminíferos, frecuentemente fusiformes. Las secciones permiten estudiar cámaras y paredes.',
  precision:'Se usan en bioestratigrafía del Paleozoico superior. Para distinguir zonas hacen falta taxones concretos y contexto de facies.',
  sources:[{title:'Kansas Geological Survey · bioestratigrafía Carbonífero–Pérmico',url:'https://www.kgs.ku.edu/Current/2006/sawin/02_intro.html'}]
 },
 {
  id:'ceratites',name:'Ceratites',catalogId:'ceratites',group:'Ammonoideos',scope:'Género',
  intervals:['triassic'],age:'Triásico medio · Muschelkalk',
  recognition:'Concha enrollada y suturas ceratíticas. En un molde interno se pueden seguir los tabiques.',
  precision:'Las sucesiones de Ceratites permiten subdividir el Muschelkalk superior en biozonas. «Superior» aquí se refiere a la unidad Muschelkalk.',
  sources:[{title:'Muschelkalk Museum · cefalópodos y biozonas',url:'https://www.muschelkalkmuseum.org/en/exhibition/fossil_gallery/cephalopods/'},{title:'Muschelkalk Museum · Triásico medio',url:'https://www.muschelkalkmuseum.org/en/exhibition/muschelkalk_gallery/'}]
 },
 {
  id:'ammonites',name:'Ammonites jurásico-cretácicos',group:'Ammonoideos',scope:'Conjunto didáctico',
  intervals:['jurassic','cretaceous'],age:'Jurásico–Cretácico',
  recognition:'Conchas con cámaras, generalmente enrolladas. Costillas, sección de la vuelta y suturas ayudan a diferenciarlas.',
  precision:'Este conjunto corresponde a los ammonites tratados por BGS. Ammonoidea es más amplio e incluye formas paleozoicas y triásicas como Ceratites.',
  sources:[{title:'BGS · Ammonites',url:'https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/ammonites/'}]
 },
 {
  id:'dactylioceras',name:'Dactylioceras',catalogId:'dactylioceras',group:'Ammonites',scope:'Género',
  intervals:['jurassic'],age:'Jurásico inferior · Toarciense',
  recognition:'Concha con ombligo amplio y costillas. Revisa cómo se bifurcan y cómo cruzan el vientre.',
  precision:'El género permite afinar respecto a «ammonite». La especie y su biozona pueden precisar más dentro del Toarciense.',
  sources:[{title:'BGS · Lower Jurassic rocks, zonación toarciense',url:'https://webapps.bgs.ac.uk/memoirs/docs/B01778.html'},{title:'Ficha revisada · estudio de dactiliocerátidos toarcienses',url:'https://geojournals.pgi.gov.pl/agp/article/download/10314/8826/14665'}]
 },
 {
  id:'hippurites',name:'Hippurites',catalogId:'hippurites',group:'Bivalvos rudistas',scope:'Género',
  intervals:['cretaceous'],age:'Cretácico superior',
  recognition:'Valva robusta en forma de cono o tubo. Las estructuras internas en sección ayudan a confirmar el género.',
  precision:'El intervalo señalado corresponde a Hippurites. La forma cónica por sí sola necesita contraste con otros rudistas.',
  sources:[{title:'Smithsonian · Hippurites, Cretácico superior',url:'https://www.si.edu/object/nmnhpaleobiology_3585720'},{title:'Museums Victoria · Hippurites cornuvaccinum',url:'https://collections.museumsvictoria.com.au/specimens/1735302'}]
 },
 {
  id:'nummulites',name:'Nummulites',catalogId:'nummulites',group:'Foraminíferos',scope:'Género',
  intervals:['paleocene','eocene','oligocene'],age:'Paleoceno–Oligoceno · gran desarrollo en el Eoceno',
  recognition:'Test discoidal o lenticular. La sección ecuatorial muestra cámaras dispuestas en espiral.',
  precision:'«Nummulites = Eoceno» es una asociación frecuente, pero el género también incluye registros paleocenos y oligocenos. Precisa especie y asociación antes de excluirlos.',
  sources:[{title:'ISPRA · intervalo de las nummulitas y ejemplar oligoceno',url:'https://www.isprambiente.gov.it/it/attivita/museo/collezioni-paleontologiche/paleo-reperti/nummulites-intermedia-foraminifero'}]
 }
];

export const FOSSIL_CHALLENGES=[
 {fossils:['paradoxides','trilobites'],prompt:'El estrato contiene Paradoxides y otros trilobites. ¿Qué intervalo puedes proponer?',choices:['Cámbrico','Paleozoico completo','Jurásico'],answer:0,explanation:'Paradoxides acota la identificación al Cámbrico medio tradicional. El grupo Trilobita, por sí solo, tendría un recorrido mucho mayor.'},
 {fossils:['dactylioceras'],prompt:'Has confirmado Dactylioceras. ¿Qué edad es la más precisa de estas opciones?',choices:['Mesozoico completo','Jurásico inferior · Toarciense','Cretácico superior'],answer:1,explanation:'La identificación del género permite proponer el Toarciense. «Ammonite» sin más detalle dejaría una incertidumbre mayor.'},
 {fossils:['ceratites'],prompt:'La leyenda del corte indica Ceratites del Muschelkalk. ¿Dónde lo sitúas?',choices:['Devónico','Triásico medio','Jurásico superior'],answer:1,explanation:'Ceratites es un ammonoideo del Triásico medio. Muschelkalk superior designa una parte de esa unidad, no el Triásico superior.'},
 {fossils:['nummulites'],prompt:'La única identificación es Nummulites. ¿Qué respuesta respeta la precisión disponible?',choices:['Eoceno obligatorio','Paleógeno, con el Eoceno como asociación frecuente','Cretácico'],answer:1,explanation:'El intervalo de trabajo es Paleoceno–Oligoceno. El Eoceno es especialmente característico, pero el género por sí solo no excluye las otras épocas.'},
 {fossils:['monograptus'],prompt:'¿Puedes asegurar «solo Silúrico» con Monograptus en sentido tradicional?',choices:['Sí, siempre','No, hay registros que alcanzan el Devónico inferior'],answer:1,explanation:'Hay monográptidos que atraviesan el límite Silúrico–Devónico. La especie y la biozona son las que permiten afinar.'},
 {fossils:['trilobites','fusulinids'],prompt:'Sin determinar más los fósiles, ¿qué intervalo común queda a escala de períodos?',choices:['Cámbrico–Silúrico','Carbonífero–Pérmico','Triásico–Cretácico'],answer:1,explanation:'Se conserva la intersección de ambos recorridos. La asociación aún abarca dos períodos y necesita una determinación más precisa.'},
 {fossils:['trilobites','nummulites'],prompt:'En una muestra aparecen ambos grupos. ¿Cómo lo razonas?',choices:['Promedio entre las dos edades','Asigno directamente Eoceno','Reviso identificación, procedencia y posible retrabajamiento'],answer:2,explanation:'No hay intervalo común en este esquema. Un fósil antiguo puede haber sido erosionado y redepositado en sedimentos más jóvenes. No se promedian edades.'},
 {fossils:['hippurites','ammonites'],prompt:'¿Qué período comparten estos intervalos de trabajo?',choices:['Jurásico','Cretácico','Paleógeno'],answer:1,explanation:'Hippurites sitúa el conjunto en el Cretácico y su ficha precisa Cretácico superior. Haría falta determinar el ammonite para proponer una biozona.'}
];

export function sharedFossilIntervals(fossils){
 if(!fossils.length)return [];
 return GEOLOGICAL_INTERVALS.filter(interval=>fossils.every(fossil=>fossil.intervals.includes(interval.id)));
}
