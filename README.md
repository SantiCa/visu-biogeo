# Visu BioGeo

Fuentes y control de versiones en el repositorio privado [SantiCa/visu-biogeo](https://github.com/SantiCa/visu-biogeo). Para preparar una copia desde GitHub, recuperar las fotografías y ejecutar pruebas, leer [Desarrollo](docs/DESARROLLO.md). El [estado actual](docs/ESTADO.md) resume los pendientes. Los instaladores, fotos, PDFs y cachés se conservan fuera de Git; los pasos siguientes sobre el instalador corresponden a la copia completa o a un paquete generado.

Aplicación web de estudio personal para PC, Mac y móvil. El catálogo se ha reconstruido desde los 51 PDF: incluye organismos, minerales, rocas, fósiles, estructuras, moléculas y geomorfología. La importación aún puede contener nombres históricos, variantes sin desglosar y líneas que requieren depuración. El catálogo no equivale a una revisión taxonómica completa.

## Instalar y abrir

Windows: ejecuta **output/Instalar Visu BioGeo Windows.exe**. Instala el programa y el banco completo de fotos en tu usuario, crea un acceso directo y no necesita Python. El instalador ocupa aproximadamente 1,37 GB. El programa sirve sus archivos solo en 127.0.0.1 y mantiene el puerto 8081 para conservar el espacio de datos del navegador. Si ya tienes la app anterior abierta en ese puerto, se abre esa instancia; ciérrala cuando quieras usar el nuevo servidor nativo.

Mac, iPad, iPhone y Android: abre [la web privada de Visu BioGeo](https://visu-biogeo-santica.nimblequail260.chatgpt.site/). En Mac usa Safari > Archivo > Añadir al Dock o la opción Instalar de Chrome. En iPad/iPhone usa Safari > Compartir > Añadir a pantalla de inicio. En Android usa Chrome > Instalar aplicación / Añadir a pantalla de inicio. La instalación en dispositivos Apple y Android no se ha probado sobre hardware físico en esta sesión.

El alojamiento está actualmente en modo público: el catálogo base puede abrirse sin cuenta. Dentro de la app, Ajustes permite entrar con tu correo y la contraseña de estudio para acceder al progreso y a las aportaciones autorizadas. Si configuras el alojamiento como privado, se añadirá además el acceso de ChatGPT del sitio. Las imágenes originales se guardan en el almacenamiento privado del sitio; las nuevas revisiones se publican de forma incremental. El acceso a las fotos del catálogo sigue la audiencia configurada en Sites; las fotos nuevas de usuarios en Supabase requieren una cuenta autorizada.

En Windows las fotos del paquete están disponibles sin Internet. En la PWA, guarda los bloques que quieras mediante Ajustes antes de desconectarte; el navegador puede limitar o eliminar su almacenamiento y el banco completo supera 1,3 GB. La sincronización necesita conexión. No borres los datos del navegador sin exportar una copia.

Si ya estudiabas en la app anterior, abre **ese mismo navegador y dirección**, entra en tu cuenta y pulsa **Incorporar mi progreso local** cuando aparezca. Espera a Sincronizado antes de cambiar de dispositivo. La migración conserva la copia local original. El paquete distribuible no contiene cuentas, sesiones ni contraseñas.

Para desarrollo sigue disponible `python -m http.server 8080 --bind 127.0.0.1` desde esta carpeta. No es necesario para usar el instalador.

## Estudiar con los nombres visibles

En **Catálogo > Vista**, elige **Estudiar en filas · nombres visibles**. Cada fila muestra una foto aleatoria aprobada, el nombre científico, el nombre común cuando se ha documentado y la familia. **Cambiar fotos** cambia de vista cuando hay alternativas. La lectura del catálogo no registra respuestas ni cambia los intervalos de repaso. **Descripción y rasgos** abre la ficha sin tener que adivinar.

**Solo fotos guardadas** usa el mismo banco y preferencia que Estudiar: en las filas limita las entradas a las que tienen alguna foto disponible en el dispositivo. Sin conexión se aplica este criterio automáticamente.

Puedes filtrar por **Lista de estudio**, **Grupo general**, **Clasificación / grupo**, estado y prioridad; la búsqueda admite también familia y nombres comunes documentados. **Agrupar** permite ver las entradas sin agrupar, por lista, por clasificación/grupo o por familia. Una entrada puede pertenecer a varias listas.

Las 1675 entradas biológicas tienen una agrupación amplia documentada a partir de los linajes de sus familias en iNaturalist y los registros exactos de GBIF. Así se reconocen mamíferos, aves, insectos, moluscos, coníferas y otros grupos incluso en entradas que solo proceden de listas regionales. Los líquenes conservan su agrupación de estudio. Se guardan el linaje y la fuente en `data/classification.json`; estas agrupaciones prácticas no pretenden representar todos los rangos de una clasificación filogenética. En los otros bloques se conservan grupos como rocas, minerales, láminas delgadas e histología.

Las listas ya no muestran la extensión PDF. Las fichas Bonnier de Avena, Briza y Hordeum se integran en **Poáceas (gramíneas)**; Calendula, Fumaria, Lamium, Lotus y Stellaria se integran en **Flores**. Los archivos y páginas originales se conservan en la procedencia de cada entrada; no se cambian sus identificadores ni su progreso.

La opción **Revisar imágenes · vista actual** conserva el panel de revisión y admite las mismas agrupaciones. Desde una fila puedes volver a este panel con **Revisar imágenes y procedencia**.

## Revisar o sustituir imágenes

En **Catálogo** busca una entrada. Verás su procedencia, sus candidatas y su estado. Usa el filtro **Falta completar la pareja** y, si quieres, **Solo prioritarias**.

- **Aprobar** incorpora esa foto al repaso; **Rechazar** la excluye.
- Puedes pegar una URL de otra fuente o subir hasta 20 fotos a la vez, con referencia al autor, libro y página (JPG, PNG o WebP; máximo 15 MB por archivo). Cada foto se revisa y aprueba por separado.
- Los archivos locales admiten recorte porcentual y vista previa antes de aprobar.
- Solo entran en el cuestionario las fotos aprobadas. Una categoría de Wikimedia o un resultado de búsqueda no constituye por sí mismo una verificación.
- Los créditos se muestran tras responder. Las fotos conservan su encuadre con ajuste completo, sin recortar automáticamente patas, hojas o rasgos.

Las fotos revisadas que acompañan esta carpeta tienen copia local en `assets/reviewed`, con fuente, autor y condiciones en `data/curated-images.json`. Las candidatas de iNaturalist proceden de una coincidencia exacta de nombre o un sinónimo explícito y de las fotos seleccionadas en su ficha taxonómica; siguen pendientes hasta su revisión. Geology.com aporta fotos de sus artículos identificados; también se revisan, pues esas páginas incluyen usos industriales, mapas y objetos que no sirven como muestras.

La revisión ampliada incorpora GeoDIL (colección docente de la University of North Dakota), museos mediante registros de ejemplares fósiles de GBIF, WMO, NOAA/NWS, University of Waterloo, Museo Val Sanagra, Paleontological Research Institution y el material docente de Wolfgang Griem. Hay recortes identificados de publicaciones de MITECO y Generalitat Valenciana. Se conservan autores y fuentes; una descarga correcta o una ficha de museo no implica aprobación automática. Se han descartado cartelas, libros de inventario, fotografías mal vinculadas y copias de una misma foto.

`data/image-audit.json` contiene el recuento verificable y **todas las entradas a las que aún falta completar la pareja**. `data/image-review-log.json` conserva las decisiones de cada lote. La definición de revisada es correspondencia documental y examen visual; no certificación taxonómica especializada de especies crípticas. El catálogo completo sigue en revisión. El filtro **Falta completar la pareja** de la app muestra exactamente los huecos.

Los casos delicados de sinonimia/población se anotan en `data/taxon-review-rules.json`, para evitar reintroducir candidatas demasiado amplias en futuras búsquedas. Por ejemplo, la lagartija de Columbretes utiliza fotos de procedencia insular documentada, y P. velascoi no se sustituye por P. carascalensis. Los sinónimos documentados sirven como respuestas válidas; se han corregido además las grafías Archaeopteryx, Hipparion y Paranthropus conservando los identificadores de progreso.

Asturnatura aporta nuevas vistas descargadas desde sus fichas de fotografía, comprobando el taxón asociado y conservando el autor y el enlace de cada foto. No se presupone que tenga fotografías de todas las especies. Las candidatas están en `data/asturnatura-images.json`; solo las aprobadas, copiadas en `assets/reviewed`, entran en el repaso. Se descartan árboles lejanos, imágenes poco diagnósticas y asignaciones dudosas de cultivares. Las fotos de Asturnatura conservan las condiciones de sus autores y se incorporan a esta colección de estudio personal.

Se han añadido imágenes del Atlas de Histología de la Universidad de Vigo, la colección de petrografía de Alex Strekeisen y la colección de rocas de Smith College. Se comprueban la región identificada, el modo de iluminación y el pie de foto. Los recortes excluyen rótulos con la respuesta o paneles que no correspondan. En las láminas delgadas aparece la iluminación y, cuando la fuente lo indica, el campo de visión; se admite como respuesta el nombre del mineral o roca sin escribir la iluminación.

La agpaíta señalada por el usuario se ha excluido de la ficha general de sienita; se incorporan muestras de sienita identificadas en GeoDIL y Smith College. Las exclusiones particulares muestran su motivo en la revisión. La antigua entrada «Río anastomosado o braided» se ha precisado como **Río trenzado (braided)**: ambos patrones no se consideran sinónimos. Se conserva el identificador original para mantener el progreso.

## Varias vistas, familias y uso sin conexión

Cada tarjeta sortea **dos imágenes distintas entre todas las aprobadas disponibles**. Cuando hay más de dos, evita repetir la misma pareja consecutiva. Puedes ampliar el banco de cualquier entrada desde Catálogo; el número de fotografías por especie no está limitado a dos. Si una entrada solo tiene una aprobada, se muestra esa vista mientras se completa la pareja.

Tras contestar se muestra la **familia científica y su fuente**, cuando está documentada. Activa **Estudiar > Practicar también la familia** para escribirla: es opcional y dejarla en blanco no penaliza. Se aceptan las denominaciones botánicas alternativas tradicionales, como Poaceae/Gramineae. Si aciertas la especie y fallas una familia escrita, se mantiene el acierto del nombre y la entrada vuelve a los 10 minutos. Los aciertos de familia tienen su propio contador en Progreso.

Las familias se documentan en `data/taxonomy.json` mediante los ancestros de rango familia de iNaturalist y coincidencias exactas de GBIF; se conservan sus referencias. Las asignaciones automáticas de fósiles quedan pendientes de contraste paleontológico y se ocultan hasta documentarlas con una fuente adecuada: un homónimo o una clasificación histórica no se convierte automáticamente en respuesta. Cuando falta información se muestra «Familia pendiente de documentar».

La revisión acumulada al 26/10/2026 suma **4470 referencias de imagen aprobadas**, distintas dentro de cada entrada: **2007 entradas tienen pareja**, **595 parejas siguen incompletas** y **469 entradas aún no tienen foto aprobada**, sobre un catálogo ampliado a 2602 fichas. Las **162 entradas del histórico andaluz disponible tienen pareja**. La recopilación de Madrid ha añadido 132 fichas, 142 referencias de imagen revisadas y 12 perfiles descriptivos: 53 de sus 54 nuevas entradas de organismos ya tienen pareja. Las 1745 entradas de organismos tienen familia documentada, pero el alcance histórico de Podarcis hispanicus requiere contraste antes de incorporar fotos. Hay 264 fichas descriptivas y 81 notas de construcción de nombres de familia; las etimologías sin contraste se señalan como pendientes y no se añaden reglas nemotécnicas. Los recuentos y huecos están en `data/image-audit.json` y `data/study-notes-audit.json`.

Las estructuras químicas proceden de registros identificados de [PubChem / NLM](https://pubchem.ncbi.nlm.nih.gov/) y [RCSB PDB](https://www.rcsb.org/). Se conservan los identificadores CID, CCD y PDB y se distinguen diagramas 2D, conformeros 3D y modelos proteicos. Las entradas genéricas explican qué formas se representan: por ejemplo, clorofila a, vitamina D3 y dos glicerofosfolípidos con cabezas diferentes. Los modelos de colágeno muestran péptidos de triple hélice, no fibras de tejido completas. La cera de abeja conserva por ahora una sola estructura aprobada; no se cuenta como pareja. Los nombres químicos breves documentados se aceptan como respuesta sin aceptar compuestos distintos, como nicotinamida por ácido nicotínico. Las rocas se han contrastado también con GeoDIL, Smith College, USGS, INGV, Arizona Geological Survey y WHOI. Las etimologías nuevas se apoyan en Dicciomed de la Universidad de Salamanca y, para obsidiana, CNRTL.

## Fichas de repaso y etimologías

Tras responder se muestra la descripción, los rasgos y la etimología del nombre y de la familia directamente, sin desplegarla. Las mnemotecnias se han retirado a petición del propietario. Cuando falta una etimología se indica explícitamente. La ficha se guarda con el programa y puede abrirse desde las filas del catálogo.

Hay **233 fichas descriptivas**: las 223 anteriores y diez de géneros de nubes, con etimologías de la OMM y descripción de NOAA/NWS. La etimología de Baculites se ha contrastado con Battison (2009). Hay notas nomenclaturales para 60 familias. En 178 fichas la etimología sigue parcial o totalmente pendiente y quedan 2219 entradas sin ficha. Los recuentos están en data/study-notes-audit.json.

## Cómo se programa el repaso

Se aproxima el olvido con R(t) = exp(−t/S). Es una heurística transparente, no FSRS ni una estimación personal validada. Los aciertos elevan la estabilidad, según el esfuerzo; los errores vuelven a los 10 minutos. La dificultad nunca convierte una respuesta incorrecta en acierto.

La frecuencia aplica peso `1 + min(4, 1.5 × log2(1 + frecuencia))` a la selección. Además, se usa un objetivo orientativo de recuerdo del 96% para las prioritarias y del 90% para las demás, por lo que las primeras se repasan antes a igual rendimiento. Los intervalos ya programados se recalculan al responder.

Si quedan entradas nuevas, al menos una selección de cada cinco se reserva para ellas. Las nuevas se eligen sin reemplazo a medida que las contestas; saltar sin puntuar no cuenta como aprendizaje. Solo se sortean nuevas o vencidas: si no hay ninguna, se muestra que has terminado por ahora. No se adelantan las tarjetas futuras para llenar una sesión.

## Sincronización y separación de usuarios

El proyecto gratuito **Visu BioGeo** ya está configurado. La app incluye únicamente la URL del proyecto y su clave pública publishable en config.js. La contraseña de la base de datos y las claves administrativas no forman parte de la app ni de los paquetes. En Ajustes accede con la cuenta de estudio creada y tu contraseña; se limpia el campo después del intento.

Las altas públicas están desactivadas. Además de autenticar, la base exige pertenecer a la tabla privada de miembros autorizados. Solo está habilitada la cuenta de estudio del propietario. La seguridad por filas permite leer y actualizar exclusivamente el progreso de ese usuario, y la función de sincronización vuelve a comprobar la pertenencia. Copiar la app no autoriza acceso a estos datos: otra persona puede estudiar en local o configurar su propio proyecto.

Se sincronizan progreso, prioridades, decisiones sobre imágenes y preferencias. Se reintenta al recuperar conexión, volver a la ventana o pulsar Sincronizar. Los registros de una misma entrada se combinan por su fecha de repaso más reciente; dos sesiones simultáneas no suman sus contadores. Las prioridades se combinan por entrada y fecha. Cada cuenta tiene también su espacio local separado y una petición tardía de otra cuenta no puede escribir en él.

Las fotos privadas que añadas desde la interfaz permanecen en ese navegador; no se suben a Supabase. Usa **Ajustes > Descargar copia JSON** para trasladarlas. Las imágenes aprobadas del catálogo distribuido sí acompañan a Windows y al banco privado de la web.

Se ha comprobado el acceso real con la cuenta de estudio, confirmado por el propietario. El script supabase/verify-isolation.sql pasó 11 comprobaciones en la base real: aislamiento entre cuentas, bloqueo de un usuario sin membresía, denegación anónima y combinación de fechas, con reversión de los datos sintéticos de prueba. Las políticas están en supabase/schema.sql. El script de creación de tablas no autoriza automáticamente ninguna cuenta: eso se hace explícitamente desde el administrador del proyecto.

Si compartes el código para que otra persona configure su propia base, debe crear su proyecto, ejecutar el esquema, desactivar altas públicas, crear su cuenta desde el panel y autorizar su UUID en visu_members. Debe cambiar config.js por su propia URL y clave pública; nunca usar service_role ni una clave secreta en el cliente.

## Copia de seguridad y comprobaciones

La copia JSON incluye progreso, prioridades, decisiones y fotos privadas. La restauración combina los registros por fecha y conserva fotos distintas. Los datos antiguos de localStorage no se borran durante la migración.

```powershell
node --test tests/*.test.mjs
node --check app.js
```

Los recolectores de `scripts/` son reanudables y guardan candidatas pendientes. `review_batch.py` congela hojas de contacto, y `apply_image_review.py` aplica decisiones explícitas con trazabilidad en `data/image-review-log.json`. Nunca se aprueban todas las fotos por el mero hecho de que su descarga funcione. No vuelvas a ejecutar el importador antiguo `extract_species.py --verify-gbif` directamente sobre el catálogo nuevo: perdería los grupos no taxonómicos.

La ampliación de instalación incorpora seis imágenes revisadas para cuatro entradas previamente sin foto: Annularia, Baculites, Calceola y Gryphaea. Calceola y Gryphaea completan pareja. Se añaden cuatro fichas descriptivas y dos familias fósiles contrastadas. Las láminas históricas se identifican como ilustraciones, con sus fuentes; las etimologías no contrastadas permanecen pendientes. La revisión posterior completa también la pareja de Baculites y retira las mnemotecnias.

## Botones, aportaciones y usuarios

Saltar sin puntuar pasa a otra tarjeta sin registrar la respuesta ni cambiar su intervalo, incluso si ya se ha mostrado la solución. Revisar / corregir imágenes abre esa entrada en el catálogo sin puntuarla. Al resolver todavía falta pulsar Con esfuerzo, Bien, Fácil o Continuar para guardar el resultado; el último botón queda debajo de No lo sé. Todos los botones tienen una explicación al pasar el ratón y una descripción accesible.

El progreso, prioridades y preferencias de estudio siguen siendo personales y se sincronizan con la misma cuenta. Las decisiones personales anteriores se conservan. Con sesión iniciada, las nuevas fotos, ediciones de su procedencia y aprobaciones son aportaciones compartidas y requieren conexión. Las fotos nuevas se guardan en un bucket privado de Supabase, separado del banco original del programa; también se pueden añadir URLs externas. Sin sesión, las nuevas fotos y revisiones quedan solo en ese navegador y su copia JSON.

Las capacidades de añadir fotos, editar datos, aprobar/rechazar y comentar se conceden por separado y se comprueban en la base. Añadir nunca aprueba una foto automáticamente. Editar sus datos nunca cambia su estado. Los comentarios se muestran únicamente al resolver o en el catálogo, permiten editar los propios y retirarlos; el administrador puede retirarlos. Los borradores se conservan en ese navegador, pero no se publican sin pulsar el botón. No contienen progreso de otros usuarios.

Para añadir usuarios, consulta USUARIOS.md. No se ha autorizado ninguna cuenta nueva durante esta actualización. Se conserva la audiencia configurada en Sites, actualmente pública. La ruta de actualización del banco verifica firmas ECDSA con una clave pública configurada por el propietario; la clave de firma permanece solo en la memoria del proceso actualizador.

## Exámenes anteriores

Catálogo y Estudiar ofrecen Exámenes anteriores, con comunidad (Andalucía o Madrid), año o todos y uso en el examen. El banco conserva 11 documentos: cinco años andaluces y seis documentos oficiales madrileños de 2018, 2021, 2023 y 2025. Se han vinculado 53 apariciones adicionales de nombres en problemas, además de las evidencias nominales anteriores.

El filtro distingue reconocimiento/clasificación nominal de materiales nombrados en problemas. Una leyenda de corte no se presenta como una fotografía de visu ni aumenta automáticamente la frecuencia andaluza. Los solucionarios de PRECEGE aportados de 2018, 2021 y 2023 permiten añadir 78 apariciones de entrada por año y ampliar el histórico de 95 a 162 entradas. Las 20 fotos andaluzas de 2023 tienen correspondencia con la clave académica, incluidas B9 y B10 en la página 10 del enunciado. Se conservan nueve preguntas dudosas o con alternativas incompatibles fuera de las prioridades automáticas; también siguen pendientes seis nombres comunes ambiguos de 2025. Las claves académicas no se presentan como soluciones oficiales de la Junta. Cada referencia conserva año, opción, pregunta, nombre impreso, documento y página de solución. Los PDF completos y las páginas extraídas permanecen locales y no entran en la distribución. La serie de dos décadas sigue siendo parcial. `data/exams.json` y `data/solved-exam-evidence.json` conservan la procedencia; `output/solved-exams-import.json` resume esta importación.

## Recopilación de Madrid sin fechas

El documento aportado `VISUS DE MADRID DE VARIOS AÑOS.pdf` se revisó en sus 17 páginas. Sus 406 líneas nominales tienen una decisión explícita: 403 admitidas (dos contienen dos variedades expresas) y tres pendientes: Cytisus purgans sin autor, Blaps mortisaga/lusitanica y Diorita o granodiorita. Se vinculan 396 entradas distintas mediante 405 referencias de procedencia. No se asigna año ni frecuencia por convocatoria.

En **Catálogo o Estudiar → Exámenes anteriores → Comunidad de Madrid → Año: Varios años · sin fecha** aparecen las entradas de esta recopilación. Se conservan la página, el nombre impreso y la sección original. Las erratas no se convierten en respuestas aceptadas; los sinónimos contrastados sí se documentan. Los restos anatómicos tienen fichas independientes, sin heredar fotos del animal completo. El histórico y las prioridades de Andalucía no cambian.

La importación reproducible usa `scripts/import_madrid_compilation.py` y sus decisiones nominales en `data/madrid-compilation-evidence.json`. El PDF original y sus páginas no se distribuyen con la web ni el instalador. Resumen de esta ampliación: `output/madrid-compilation-import.json`.


## Clasificación y repaso por campos · versión 8.0

La pestaña **Clasificación**, junto a Catálogo, incluye todas las entradas. Despliega las ramas y después el nombre para ver dos fotos aprobadas y la ficha. Permite buscar nombres científicos o comunes, rangos y fórmulas. Las fichas sin imágenes o datos documentados indican el pendiente; no se ocultan entradas para aparentar cobertura completa.

**Practicar clasificación completa** está activado de inicio. En organismos y fósiles taxonómicos se responde nombre, filo o división, familia y género cuando están documentados. Para géneros sin especie determinada no se inventa un epíteto. Puedes contestar el nombre binomial o, si escribes el género por separado, el epíteto específico. Los nombres comunes documentados aparecen como pista, según lo solicitado. Después se muestra también clase y orden, con la fuente de la clasificación.

En minerales se pregunta la clase principal de Nickel–Strunz 9 y la fórmula cuando hay una fórmula evaluable. La ecuación acepta subíndices, agrupaciones equivalentes y agua de hidratación; distingue Co de CO. Las composiciones generales se indican expresamente. En este esquema el cuarzo se incluye en óxidos; esto no sustituye otros esquemas estructurales usados en docencia. En rocas se pregunta el grupo por origen y se muestra su composición: no se exige una fórmula química única. Asbesto y bauxita explican su naturaleza de hábito o mezcla.

Un fallo en cualquiera de los campos evaluados programa repaso a los diez minutos cuando pulsas **Continuar**. Los aciertos del nombre y de cada campo se conservan por separado en Progreso; se sincronizan en la misma cuenta. Los campos documentales pendientes no penalizan. La lectura del árbol no puntúa y no cambia la planificación.

Los rangos biológicos proceden de registros explícitos de iNaturalist, GBIF y Paleobiology Database, con enlaces por entrada. Las diferencias de circunscripción o nombre aceptado se muestran en la ficha; los rangos no se deducen de la posición en una lista. Los nombres vernáculos no son universales y pueden faltar. Las trazas, coprolitos y estromatolitos no se fuerzan a una clasificación corporal de un único productor.

## Árboles de estudio y modos de fotografía · versión 8.3

La nueva pestaña Árboles de estudio conserva todas las entradas del catálogo. Incluye un árbol por ramas y un mapa SVG con desplazamiento, zoom, teclado y minimapa. Los niveles y grupos tienen explicaciones contrastadas cuando existen; los rasgos y raíces pendientes se indican. No representa distancias o fechas evolutivas. La clasificación de cada ejemplar sigue enlazada a su registro de procedencia.

El nombre común documentado se pregunta también cuando se desactiva la clasificación completa. Admite las alternativas registradas y normaliza artículos, mayúsculas y tildes. Los nombres comunes pendientes no penalizan. Un fallo en cualquier campo programa el repaso en diez minutos; los resultados de nombre común se conservan en fields.common y se sincronizan con el resto del progreso.

En Estudiar puedes elegir Andalucía, Madrid o General. Andalucía exige dos imágenes con evaluación visual diagnóstica y no sustituye las que faltan por vistas sin evaluar. La primera evaluación cubre 324 fotografías de las 162 prioridades, con 66 entradas que cumplen la pareja. Madrid alterna vistas de ejemplares y detalles; una pregunta de partes no se acompaña de la vista completa como pista. Solo partes y detalles aislados permite limitarse a las 35 vistas marcadas, repartidas en 26 entradas. General conserva el catálogo aprobado.

Catálogo → Uso para estudiar permite valorar cada vista para tu cuenta. Se guarda en preferences.imageStudy y se sincroniza; no modifica la aprobación de fotos ni los permisos compartidos. Las fotos nuevas empiezan sin evaluar para el modo estricto.

Los nombres del cuadro taxonómico de la solución abren información con ratón, foco o toque. El clic o toque fija el cuadro; Esc o × lo cierran. Se puede abrir ese grupo directamente en el nuevo mapa. Se distingue la etimología del término del rango (filo, clase, familia…) de la del nombre concreto del taxón. Las raíces no documentadas se muestran como pendientes; no se han rellenado por semejanza de palabras.

## Revisión de fotografías y fichas · versión 8.4

Se incorporan 26 referencias de imagen revisadas y guardadas localmente. Once entradas que estaban sin foto completan pareja: Lepiota procera (sinónimo histórico de Macrolepiota procera), Pipa pipa, Platanus hispanica, delta, dunas litorales, estuario, islas barrera, marisma, meandro, la entrada compuesta de meandros abandonados o encajados y tómbolo. Las fuentes nuevas incluyen iNaturalist, NPS y NASA. Las imágenes orbitales en falso color se identifican como tales y los topónimos no se interpretan como rasgos geológicos.

Se añaden 12 fichas descriptivas, incluida la entrada separada Platanus × hispanica, y se documenta el origen de Pipidae y Platanaceae. Se conservan los ID y los historiales de estudio; no se fusionan las entradas sinónimas. Se distinguen meandro encajado, meandro abandonado y lago semilunar; no son sinónimos. Las raíces lingüísticas no contrastadas siguen explícitamente pendientes y no se añaden mnemotecnias.

Recuento tras la revisión: 4593 referencias aprobadas, 2184 entradas con foto y 2057 con pareja; faltan 545 parejas, de las que 418 no tienen foto. Hay 350 fichas descriptivas y 95 notas de construcción u origen de familia. La web y el instalador 8.4 contienen los mismos 4597 archivos públicos; 65 pruebas JS y 9 de Python superadas, sin archivos aprobados rotos ni discrepancias de empaquetado. El informe de publicación y la captura están en output/published-curation-v8.4.json y output/visu-fichas-v8.4.png.

## Micrografías y terminología · versión 8.5

Se añaden 32 referencias aprobadas de micrografías para 18 entradas que estaban sin foto, con fuentes de Vigo, Leeds y Utah. Trece completan pareja. Hay 4625 referencias aprobadas, 2202 entradas con foto y 2070 con pareja: quedan 532 parejas incompletas y 400 entradas sin imagen aprobada. Se añaden 19 fichas con diagnóstico y etimología; el catálogo contiene 369 fichas descriptivas. Tres de las nuevas etimologías conservan partes pendientes explícitas.

Los recortes aíslan los tipos celulares nombrados por el mapa del atlas sanguíneo y excluyen los rótulos. Se revisa expresamente un recorte de lisosomas anteriormente rechazado por su etiqueta. La identidad de la preparación no convierte automáticamente un detalle en una vista diagnóstica para Andalucía: los campos de contexto, los detalles epiteliales y los orgánulos que requieren información de la fuente conservan esa limitación. Se mantienen las fuentes, los derechos y la técnica de microscopía.

La entrada pelo, corte transversal sigue sin foto: se han descartado folículos sin tallo inequívoco y vistas longitudinales. Su nueva ficha explica esa diferencia. No se han incorporado imágenes nuevas del atlas PDF inspeccionado. Los datos y sesiones personales no se incluyen en el paquete distribuible.

## Muestras geológicas y fichas · versión 8.6

Se añaden 33 referencias aprobadas, con copia local, para 15 entradas que estaban sin foto. Catorce completan pareja: ágata, almandino, amatista, asbesto, azabache, chorlo, crisotilo, dacita, estaurolita con macla en cruz, estibina, ignimbrita, micaesquisto granatífero, paligorskita y wollastonita. Migmatita recibe una primera vista útil. Las fuentes incluyen GeoDIL, Geology.com, National Park Service y National Museum of Wales, con sus autores y derechos. Se excluyen gemas talladas, hábitos poco útiles y una toba cuya atribución a ignimbrita no queda demostrada por su fuente.

Las 15 fichas nuevas explican rasgos diagnósticos y etimología; las hipótesis sobre el origen último de chorlo se presentan como inciertas. Asbesto se explica como una denominación colectiva, y azabache como material de origen orgánico. Las imágenes correctamente identificadas por su fuente que no separan inequívocamente especies o litologías semejantes siguen disponibles en el catálogo general y quedan fuera de Andalucía estricto. Las evaluaciones del lote dejan 87 entradas elegibles en ese modo.

El catálogo contiene 4658 referencias aprobadas, 2217 entradas con foto y 2084 con pareja; quedan 518 parejas incompletas y 385 entradas sin foto aprobada. Hay 384 fichas descriptivas y 95 notas de familia. La web y el instalador 8.6-4dc322d6ba8d incluyen los mismos 4659 archivos públicos. Pasan 65 pruebas JS y 9 de Python, sin archivos aprobados rotos ni discrepancias de empaquetado. El informe es output/published-geology-v8.6.json y la captura output/visu-geologia-v8.6.png.

## Formas del relieve y fichas · versión 8.7

Se incorporan 23 referencias aprobadas con copia local para 14 entradas que estaban sin foto. Nueve completan pareja: pilas, tafoni, roca aborregada, ésker, varvas glaciares, farallones, cañón o garganta, llanuras mareales y terrazas travertínicas. Acantilado, dropstone, playa de cantos, plataforma de abrasión y la entrada compuesta de zona de ablación o frente glaciar reciben una primera vista. Las fuentes son NPS, NOAA, Géologie Québec y AntarcticGlaciers.org, con sus créditos. Se revisan las tres láminas y los recortes; se excluyen rótulos, vistas lejanas, un montaje insuficiente de grus y una costa rocosa publicada en una página de playa de cantos que no mostraba bien el depósito.

Se añaden 15 fichas descriptivas, incluida grus, que conserva cero fotos aprobadas. Siete fichas nuevas conservan partes etimológicas pendientes expresas; el origen discutido de farallón y el origen probablemente prerromano de tafone no se convierten en certezas inventadas. Se distingue una pila de meteorización de una marmita fluvial, la laminación de su demostración como varva anual y una plataforma de abrasión de una rasa elevada o una sucesión flysch. Los detalles de sedimentos que requieren contexto se separan de las vistas diagnósticas. Andalucía estricto queda con 94 entradas elegibles.

Hay 4681 referencias de imagen aprobadas, 2231 entradas con foto y 2093 con pareja: quedan 509 parejas incompletas y 371 entradas sin foto. El catálogo contiene 399 fichas descriptivas y 95 notas de familia. Web e instalador 8.7-7249299cd044 incluyen los mismos 4681 archivos públicos; pasan las 65 pruebas JS y las 9 de Python, los 13 archivos principales publicados coinciden con sus hashes y la activación sin firma sigue rechazada. No se alteran historiales ni permisos personales. Informe: output/published-landforms-v8.7.json. Captura: output/visu-relieve-v8.7.png.

## Preparaciones histológicas · versión 8.8

Se incorporan 25 imágenes revisadas de Yale, Southern Illinois University y Universitat de València: 14 entradas antes vacías reciben imágenes y 9 alcanzan una pareja. Se conservan créditos y marcas de procedencia; los recortes excluyen nombres impresos. La ilustración histórica del nodo de Ranvier se identifica expresamente como dibujo. Los campos de detalle de Corti, pared folicular y botones gustativos no se convierten en una vista inequívoca del órgano completo. La vagina parcial tampoco pasa el criterio estricto de Andalucía. Se descartan cortes longitudinales de pelo, un archivo truncado y preparaciones rotuladas o ambiguas.

Hay 4706 referencias aprobadas, 2245 entradas con imagen y 2102 con pareja: quedan 500 parejas incompletas y 357 entradas sin imagen. Hay 414 fichas descriptivas, 15 nuevas, incluyendo peroxisomas sin atribuir al esquema del atlas el valor de micrografía. Una de las nuevas etimologías queda parcialmente pendiente; el total de fichas con alguna raíz pendiente es 255. No se añaden reglas nemotécnicas. Son 99 las entradas con dos vistas calificadas explícitamente como diagnósticas; esta cifra es distinta de la cobertura general de imágenes.

Web e instalador 8.8-c66fe4ce540f contienen los mismos 4706 archivos públicos. Pasan 65 pruebas JS, 9 de Python, la verificación de hashes de 13 archivos principales publicados y la comprobación de que la activación sin firma sigue rechazada. Informe: output/published-histology-v8.8.json. Captura: output/visu-histologia-v8.8.png.

## Preparaciones botánicas · versión 8.9

Se añaden 25 referencias de imagen aprobadas (23 archivos nuevos, con dos imágenes compartidas entre entradas relacionadas): polen de Lilium y Pinus, polen genérico, germinación polínica, almidón, cristales de oxalato, célula vegetal, placas cribosas, soros y esporangios, mitosis radicular, saco embrionario y contexto del embrión de Lilium. Doce entradas antes vacías reciben imágenes y once completan una pareja. Se preservan los créditos, las marcas CNRS y el copyright específico de Mullendore et al. / ASPB en la serie de calosa. Las imágenes rotuladas se recortan tras revisión visual; se descartan los esquemas del saco embrionario y de esporangios, la comparación mixta de elementos conductores y el campo de meristemo sin mitosis reconocible.

Las 13 fichas nuevas distinguen Lilium de otros lirios, pino de otras coníferas bisacadas, soro de esporangio, saco embrionario de embrión, y grano de almidón de plasto. La ficha de centrosoma se completa sin añadir un esquema rotulado al examen. Dos nuevas etimologías conservan raíces parcialmente pendientes. No se incorporan reglas nemotécnicas ni familias ficticias para tejidos.

El catálogo tiene 4731 referencias aprobadas, 2257 entradas con imagen y 2113 con pareja; quedan 489 parejas incompletas y 345 entradas sin imagen. Son 427 fichas descriptivas, con 257 etimologías total o parcialmente pendientes. Hay 105 entradas con dos vistas expresamente consideradas diagnósticas para el modo Andalucía. La cobertura general no se confunde con ese criterio estricto.

Web e instalador 8.9-b66e63b5d23b incluyen los mismos 4729 archivos públicos. Pasan 65 pruebas JS y 9 de Python, la comprobación de integridad del instalador, los hashes de los 13 archivos principales publicados y el rechazo de activación sin firma. Informe: output/published-botany-v8.9.json. Captura: output/visu-botanica-v8.9.png.

## Nubes y traslado · versión 8.10

La tanda añade 28 referencias de imagen y 13 fichas con fuentes OMM y SMHI. Las diez entradas de nubes antes vacías reciben dos o más fotografías; las 23 entradas de nubes tienen pareja y ficha. Los recortes de cauda y flumen se cotejan con las regiones anotadas por la OMM y conservan créditos y límites de identificación. Las historias causales o de movimiento no se infieren de una foto fija. La foto OMM 5566 corresponde a Eric Van Lochem.

Hay 4759 referencias aprobadas, 2267 entradas con alguna imagen y 2123 con pareja. Quedan 479 parejas incompletas, de ellas 335 entradas sin imagen. El catálogo contiene 440 fichas, 257 etimologías con alguna parte pendiente, 95 notas de familia y cero reglas nemotécnicas. Son 111 las entradas con dos vistas calificadas como diagnósticas para Andalucía.

Web e instalador 8.10-f64fae40aa17 comparten los mismos 4757 archivos públicos. Pasan 65 pruebas JS, 9 de Python, integridad del paquete, 13 hashes de archivos principales publicados y rechazo 403 de activación sin firma. La subida interrumpida se retomó y se activó con revisión de entorno 16. Informe: output/published-clouds-v8.10.json.

Para continuar en otro ordenador, leer CONTINUAR.md. Las dependencias de mantenimiento están en requirements-maintenance.txt. El ZIP de traslado conserva la carpeta completa y se guarda fuera de ella.
