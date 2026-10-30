# CONTINUAR · Visu BioGeo

Estado del traslado: **27 de octubre de 2026**, zona Europe/Madrid.

Raíz definitiva en este PC: `C:\Users\Santiago\Documents\ChatGPT\App Visu`. La aplicación y el repositorio Git están directamente en esa carpeta; ya no se utiliza la subcarpeta intermedia de la primera restauración.

Actualización de control de versiones: las fuentes se mantienen en el repositorio privado `SantiCa/visu-biogeo`. Para empezar una tarea, leer `AGENTS.md` y `docs/ESTADO.md`; para clonar y recuperar el banco de fotos, `docs/DESARROLLO.md`. Los apartados históricos de este documento describen la copia completa del ZIP: las fotos, instaladores, cachés y el checkout de Sites quedan fuera del repositorio GitHub.

## 1. Qué se entrega y por dónde empezar

Esta carpeta contiene la aplicación, los datos, las fotos locales, las herramientas de mantenimiento, los informes, las cachés de investigación y los repositorios Git. El ZIP de traslado contiene la carpeta completa, incluidos los directorios ocultos. No contiene las sesiones del navegador, las contraseñas ni la base de datos online: esos elementos viven fuera de esta carpeta.

Extrae el ZIP en una ruta corta, por ejemplo `C:\Visu\App Visu` en Windows o `~/Proyectos/App Visu` en Mac. Es un ZIP64 grande: necesitas espacio para el archivo comprimido y para aproximadamente 11 GB descomprimidos. El tamaño exacto y la comprobación del archivo aparecen en el informe `.verificacion.json` situado junto al ZIP.

Para continuar con otro asistente, abre esta carpeta como proyecto y pídele: **«Lee CONTINUAR.md, comprueba los informes actuales y continúa por las entradas sin imagen, sin modificar los identificadores ni el progreso»**.

La ruta del ordenador anterior era `C:\Users\Santi\Documents\ChatGPT\App Visu`. No debe copiarse literalmente en el nuevo ordenador: sustituirla por la nueva raíz. Algunos scripts históricos y fuentes de trabajo hacen referencia al disco `G:` o a los runtimes de Codex del ordenador anterior.

## 2. Estado actual verificado

Versión funcional y del catálogo: **8.10**. Instalador: **8.10-f64fae40aa17**.

Web publicada: <https://visu-biogeo-santica.nimblequail260.chatgpt.site/>.

| Cobertura | Estado |
|---|---:|
| Entradas del catálogo | 2602 |
| Referencias de imagen aprobadas, distintas dentro de cada entrada | 4759 |
| Entradas con alguna imagen aprobada | 2267 |
| Entradas con dos o más imágenes aprobadas | 2123 |
| Entradas pendientes de completar su pareja | **479** |
| De ellas, entradas sin imagen aprobada | **335** |
| Entradas prioritarias documentadas de Andalucía | 162, todas con pareja general |
| Entradas con dos vistas explícitamente diagnósticas para Andalucía | 111 |
| Fichas descriptivas | 440 |
| Fichas con etimología total o parcialmente pendiente | 257 |
| Notas sobre nombres de familia | 95 |
| Reglas nemotécnicas | 0, retiradas por petición del usuario |

Una referencia no equivale necesariamente a un archivo físico diferente en todo el catálogo: algunas imágenes sirven para entradas relacionadas. Tener una pareja aprobada tampoco equivale a cumplir el criterio estricto de Andalucía.

La última tanda añadió 28 referencias y 13 fichas de nubes. Las **23 entradas de nubes tienen pareja y ficha**. Se revisaron las fuentes de la OMM y SMHI, los créditos de los fotógrafos y las regiones señaladas por las anotaciones de la OMM. Cauda y flumen tienen recortes distintos de la misma tormenta; cada una tiene también otra fotografía. Las imágenes que no demuestran origen, duración o movimiento se marcan como contexto o detalle. En flumen, la fotografía OMM 5566 es de **Eric Van Lochem**, no de Steve Willington; el registro final ya está corregido.

Los informes determinantes son `data/image-audit.json`, `data/study-notes-audit.json`, `output/media-upload-v8.10.json`, `output/validation-zero-photos-v8.10.json`, `output/package-check-v8.10.json` y `output/published-clouds-v8.10.json`.

Validación: **65 pruebas JavaScript + 9 pruebas Python = 74**, sin fallos; cero archivos aprobados rotos; los 13 archivos principales publicados coinciden con los hashes locales; la activación de medios sin firma devuelve 403. El instalador coincide con los **4757 archivos públicos** de esta versión. La publicación final usa la revisión de entorno 16. La subida interrumpida se retomó y terminó antes de preparar este traslado.

## 3. Usar la app sin desarrollar

**Windows de 64 bits:** ejecuta `output/Instalar Visu BioGeo Windows.exe`. Incluye las fotos aprobadas y no necesita Python ni Node. También se puede abrir `Abrir Visu BioGeo.exe` en la raíz para servir la copia de esta carpeta. No sustituirlo por el ejecutable antiguo `Visu BioGeo.exe`: ese archivo se conserva por historial y puede no soportar todas las rutas o imágenes actuales.

**Mac:** abrir la web y añadirla al Dock desde Safari o instalarla desde Chrome. No se ha generado un binario nativo para Mac. Para usar la copia local completa sin alojamiento, seguir la alternativa con Python del apartado siguiente.

**iPhone/iPad:** Safari → Compartir → Añadir a pantalla de inicio. **Android:** Chrome → Instalar aplicación. Las imágenes web que se quieran utilizar sin conexión deben descargarse desde Ajustes; la capacidad depende del dispositivo y del navegador. El instalador Windows ya contiene el banco local.

En Ajustes, entrar con la misma cuenta de estudio y esperar a **Sincronizado**. Ver también `INSTALAR.md` y `USUARIOS.md`.

### Trasladar el progreso personal

En el navegador antiguo, esperar a que aparezca Sincronizado. Si existe progreso antiguo solo local, usar **Incorporar mi progreso local**. Exportar además una copia JSON desde Ajustes y guardarla aparte para trasladar también datos o fotos personales que sigan siendo locales.

En el ordenador nuevo, iniciar sesión con la misma cuenta; si hace falta, importar la copia JSON. La carpeta y el ZIP **no trasladan localStorage, IndexedDB, cookies ni la sesión del navegador**. Cambiar de puerto o dirección local crea otro origen de almacenamiento del navegador; el inicio de sesión y la copia JSON evitan depender del origen anterior.

No crear otro proyecto Supabase ni otra cuenta solo por cambiar de ordenador. No volver a introducir ni documentar aquí las contraseñas.

## 4. Dependencias para mantener el proyecto

La interfaz es HTML/CSS/JavaScript con módulos ES, sin framework ni servidor de aplicación que instalar. El cliente Supabase ya está incluido en `vendor/`. El Worker del alojamiento usa APIs de Cloudflare/Sites y no necesita paquetes npm para su compilación actual.

Entorno con el que se han verificado los scripts:

- Python **3.12.14**; dependencias exactas en `requirements-maintenance.txt`: Pillow, beautifulsoup4, PyMuPDF y pypdf.
- Node.js **24.22.1**, para las pruebas JS, la compilación del Worker y la subida de medios.
- PowerShell en Windows para las herramientas auxiliares.
- Compilador de .NET Framework de Windows para reconstruir el lanzador y el instalador. `build_installer.py` busca `%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe`. La generación del EXE es una tarea de Windows.

Ejemplo en Windows, desde esta carpeta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-maintenance.txt
```

Ejemplo en Mac:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-maintenance.txt
```

Los comandos siguientes usan `python` como abreviatura: usar el intérprete del entorno virtual o activarlo primero. No usar las rutas de `C:/Users/Santi/.cache/codex-runtimes/` del ordenador anterior.

Los scripts de hojas de contacto usan actualmente `C:/Windows/Fonts/arial.ttf`. Para generar hojas en Mac, adaptar esa ruta a una fuente instalada; esto no afecta al funcionamiento de la app.

### Ejecutar la copia local en Mac o durante desarrollo

Preparar un directorio con los archivos públicos y arrancar un servidor HTTP solo en loopback:

```sh
python scripts/prepare_release.py --target output/local-app
python -m http.server 8083 --bind 127.0.0.1 --directory output/local-app
```

Abrir <http://127.0.0.1:8083/>. El primer comando copia el banco público y necesita espacio adicional. No abrir `index.html` con `file://`: los módulos y la carga de datos necesitan HTTP. No publicar la raíz completa del proyecto, que también contiene cachés, SQL y material de trabajo.

## 5. Estructura y archivos que son fuente de verdad

| Ruta | Función |
|---|---|
| `index.html`, `app.js`, `styles.css` | Interfaz principal |
| `engine.mjs` | Planificación de repasos y respuestas |
| `classification-learning.mjs` | Preguntas y corrección por campos |
| `exam-photos.mjs` | Elegibilidad de imágenes por comunidad |
| `taxonomy-guide.mjs`, `taxon-reference.mjs` | Árbol interactivo, explicaciones y etimologías de taxones |
| `cloud.mjs`, `community.mjs`, `storage.mjs` | Sincronización, permisos y almacenamiento |
| `offline.mjs`, `sw.js` | Descargas y cachés offline |
| `data/species.json` | Catálogo e identificadores estables |
| `data/curated-images.json` | Decisiones finales de imagen, fuente, crédito, recorte y uso de examen |
| `assets/reviewed/` | Fotos locales aprobadas y sus recortes |
| `data/image-review-log.json` | Trazabilidad de lotes y decisiones |
| `data/study-notes.json`, `data/family-notes.json` | Descripciones, diagnósticos, etimologías y fuentes |
| `data/learning-taxonomy.json`, `data/learning-geology.json` | Clasificación biológica, minerales, fórmulas y rocas |
| `data/andalucia-priority.json` | Evidencias de exámenes, años y prioridades |
| `supabase/` | SQL de esquema, colaboración y comprobaciones de aislamiento |
| `desktop/` | C# del lanzador, instalador y Worker de medios |
| `hosting/visu-biogeo-media/` | Checkout separado de Sites, manifiesto de medios y salida compilada |
| `output/` | Instalador, archivos de publicación e informes de validación |
| `tmp/reviews/` | Candidatas congeladas, hojas de contacto y vistas de recortes |
| `tmp/photo-cache/` | Copias normalizadas descargadas para revisión |
| `.git/` y el `.git/` del checkout de alojamiento | Historiales separados; ambos se conservan en el traslado |

Los JSON de recolectores (`images.json`, `teaching-images.json`, etc.) contienen **candidatas**, no aprobaciones. Para la app mandan las decisiones en `curated-images.json` y las aportaciones personales/compartidas que se cargan al entrar.

Los PDFs originales que estaban fuera de `App Visu`, por ejemplo en Google Drive `G:` o en una carpeta temporal de Windows, **no forman parte de este ZIP**. El catálogo y los resultados ya extraídos sí están aquí. Para reextraer un PDF habrá que copiarlo o indicar su nueva ruta. `extract_species.py` conserva una ruta por defecto al `G:` antiguo; `build_catalog.py` la importa. No regenerar el catálogo sin necesidad ni cambiar IDs, porque el progreso está asociado a ellos.

## 6. Base de datos y permisos

Se reutiliza el proyecto Supabase de **Visu BioGeo**. URL y clave **publicable** en `config.js`. Referencia del proyecto: `bqyjhkrnhmrrmfceshlh`.

Panel: <https://supabase.com/dashboard/project/bqyjhkrnhmrrmfceshlh>.

El progreso se guarda por usuario y las políticas RLS/membresía aíslan los datos. Las altas públicas están cerradas. La clave publicable no sustituye la autorización del usuario ni es una clave administrativa. El banco privado de aportaciones y los permisos de añadir, editar, aprobar y comentar se gestionan según `USUARIOS.md` y `supabase/collaboration.sql`.

No ejecutar de nuevo SQL ni cambiar políticas para un simple traslado. No poner contraseñas, claves service-role o tokens de sesión en archivos, commits, comandos o documentación. El nuevo ordenador necesita iniciar sesión por sí mismo en Supabase/Sites cuando se vayan a administrar esos servicios. Las credenciales temporales del asistente no son parte del proyecto ni se pueden recuperar del ZIP.

## 7. Comportamiento que debe conservarse

- Preguntar nombre común además de nombre científico cuando esté documentado; no revelarlo antes de responder.
- Preguntar filo/división, familia, género y especie cuando proceda y exista información. No inventar rangos ni penalizar campos desconocidos.
- Minerales: clasificación y fórmula; rocas: grupo y composición, sin imponer una fórmula única.
- Andalucía: usar dos imágenes explícitamente diagnósticas, sin rellenar con vistas ambiguas o sin evaluar.
- Madrid: permitir partes y detalles sin acompañarlos de una vista completa que revele la respuesta.
- Mostrar etimología y ficha al resolver; permitir explorar taxones al pasar el ratón, enfocar o tocar.
- Estudio por filas, agrupaciones/listas, exámenes de Andalucía y Madrid, selección por año, árboles de clasificación y Árboles de estudio.
- Comentarios solo tras resolver o en catálogo; respetar los permisos del servidor.
- Mantener IDs, progreso, autorizaciones y correcciones personales. Las valoraciones personales del uso de imagen no cambian automáticamente la aprobación compartida.
- **No añadir reglas nemotécnicas ni generar fotografías científicas con IA.**

## 8. Trabajo pendiente

1. Continuar con **479 entradas pendientes de pareja**, empezando por las **335 sin ninguna imagen**. La lista exacta, con ID, nombre, tipo y prioridad, es `data/image-audit.json → allMissingPairs`. Filtrar primero `approvedImages == 0`.
2. Buscar, cotejar y revisar visualmente dos vistas distintas de cada entrada. Emplear Asturnatura y otras fuentes identificadas cuando sea útil. Conservar los archivos dentro del programa y la procedencia, autor y licencia conocidos.
3. Quedan sin foto especialmente estructuras animales, relieve y fósiles; también organismos difíciles, láminas petrográficas, rocas, minerales y modelos moleculares. El grupo de nubes ya tiene cobertura general completa.
4. Completar las descripciones que faltan: **2162 entradas sin ficha descriptiva**. Que exista clasificación o foto no significa que ya exista una ficha.
5. Completar o revisar las **257 etimologías total o parcialmente pendientes**, además de los nombres taxonómicos aún sin raíz documentada. Indicar lo desconocido en lugar de inventarlo. Las notas de familia no garantizan que esté contrastada la raíz del género tipo.
6. Revisar de forma continua la correspondencia y utilidad de imágenes ya aprobadas, especialmente entradas compuestas, especies parecidas, partes aisladas y material geológico. La auditoría informática no es una verificación taxonómica exhaustiva.
7. Ampliar evidencias de exámenes anteriores de Andalucía y Madrid cuando haya fuentes oficiales o documentación aportada. No inventar frecuencias ni años. Preservar por separado las fuentes oficiales y las reconstrucciones/soluciones de academias.

Casos históricos importantes: el ocre debe mostrar material geológico, no pintura; una roca alcalina especial o una escultura no sustituye una sienita representativa; un corte longitudinal de pelo o un folículo vacío no sustituye pelo en corte transversal. Hay sinonimias o complejos difíciles como Arion rufus, Podarcis y Discoglossus que requieren más que una búsqueda por nombre.

No volver a intentar sortear errores 429 de Wikimedia, retos de seguridad, 403 o certificados inválidos. Cambiar de fuente. No confundir una imagen encontrada con una imagen aprobada.

## 9. Cómo revisar otra tanda sin perder trazabilidad

Últimos lotes completos: `histology88`, `histology88-completion`, `botany89`, `botany89-completion`, **`clouds810`** y **`clouds810-completion`**, dentro de `tmp/reviews/`.

La investigación del lote de nubes está en `tmp/clouds810/`: HTML/JSON de fuentes, metadatos, coordenadas de recortes, `stage.py`, `completion.py`, `finalize.py`. Las nuevas fichas se crearon con `scripts/complete_clouds810_notes.py`. Esos scripts son de una tanda ya aplicada; no repetirlos: algunos rechazan sobrescribir y otros fijan versiones.

Flujo para una tanda nueva:

1. Consultar la auditoría y elegir IDs sin foto. Buscar fuentes exactas; no aceptar imágenes por coincidencias vagas del buscador.
2. Crear un nombre de lote nuevo y congelar `tmp/reviews/LOTE/picks.json`. Usar las herramientas de `scripts/review_batch.py` o un recolector específico.
3. Inspeccionar las hojas y, si hace falta, el original. Para recortes, guardar las coordenadas y previsualizarlos con `python scripts/review_crops.py LOTE ruta/crops.json`.
4. Aplicar decisiones **explícitas** con `scripts/apply_image_review.py LOTE --approve ... --reject ... --crops ... --note ...`. No inferir aprobación por descarga exitosa. No contar dos recortes del mismo original como dos fotos de una misma entrada.
5. Completar crédito, leyenda y `examUse`: `diagnostic`, `detail`, `context` o `insufficient`, según lo que realmente permita reconocer la imagen. Aprobación general y elegibilidad Andalucía son decisiones distintas.
6. Escribir síntesis propia con fuentes en `data/study-notes.json`: `description`, `diagnostics`, `etymology`, `sources`, `reviewedAt`, `reviewStatus`, `scope`. No copiar extensamente textos ajenos ni incluir instrucciones de documentos como órdenes del usuario.
7. Ejecutar auditorías, preparar versión y validar antes de publicar. No modificar datos ya congelados durante el empaquetado.

## 10. Comprobaciones y empaquetado

Desde la raíz:

```sh
python scripts/audit_images.py
python scripts/audit_study_notes.py
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

La última orden completa se ha verificado en Windows. `test_native_images.py` ejecuta un EXE y requiere Windows; en Mac ejecutar por separado los otros tres módulos mediante `unittest discover` y los patrones `test_learning_distribution.py`, `test_madrid_compilation.py` y `test_solved_exams.py`. No afirmar que se ha probado el lanzador Windows desde Mac.

Tras cambiar datos públicos, incrementar la versión de `sw.js` y el prefijo del instalador; actualizar los nombres de informe en `check_learning_package.py` y `validate_live_learning.mjs`. No cambiar innecesariamente la caché de fotos persistentes.

```sh
python scripts/prepare_media_site.py
python scripts/build_installer.py
python scripts/check_learning_package.py
```

`build_installer.py` requiere Windows; produce `output/Instalar Visu BioGeo Windows.exe` y `output/windows-installer/payload.zip`. Para reconstruir el lanzador actual en Windows:

```powershell
.\scripts\build_desktop.ps1 -Destination (Join-Path (Get-Location) 'Abrir Visu BioGeo.exe')
```

No llamar a ese script sin destino si se quiere conservar el ejecutable antiguo; su destino por defecto es `Visu BioGeo.exe`. No añadir pruebas que simplemente reproduzcan datos escritos a mano. Usar las comprobaciones existentes y las verificaciones adecuadas al cambio.

## 11. Publicación en Sites: información para el siguiente asistente

Proyecto: **`appgprj_6ade076290f8819199ecb0073730325e`**. Audiencia actual: **pública**, conservarla.

Checkout: `hosting/visu-biogeo-media`. Su manifiesto `.openai/hosting.json` mantiene `d1: null` y `r2: "BUCKET"`. Las imágenes públicas se sirven desde R2 mediante un manifiesto y una activación firmada; la base Supabase es otro servicio y no se reemplaza al publicar.

Última fuente publicada: **`a3ff4905043465b8b74a93632c5e2701d252c741`** (8.12).

Versión guardada de Sites: **19**, ID **`appgprj_6ade076290f8819199ecb0073730325e~appgver_f26a0abb83b08191bac760699e9489ce`**.

Archivo de publicación: `worktrees/prioridades-madrid/output/visu-v8.12.tar.gz`. Es el pequeño artefacto del Worker, **no** una copia completa del proyecto ni el banco de fotos.

Revisión de entorno final: **18**. Despliegue final: **`appgdep_6ae3ecf402308191bfc91d08cfb69fdd`**.

Manifiesto activo: **`aa3bc42ca0d5cb23f0756b8040ee6d4cf1b736dc703ab4457674e174ce926737`**, 4758 archivos públicos.

En otro ordenador, instalar/conectar el plugin Sites con la cuenta del propietario y leer su `SKILL.md` vigente. La ruta del helper cambia con la instalación: no copiar la ruta de caché de Codex del ordenador anterior. El helper de fuente se llama `scripts/site-workflow.mjs` dentro del plugin Sites. Primero obtener `get_site` y credencial de escritura para este mismo proyecto, y abrir el checkout con el helper antes de editarlo. Mantener las credenciales solo en memoria y pasarlas por **stdin oculto**, nunca en argumentos o archivos.

Esta implementación compila con estos argumentos, **sin bash**:

```json
[["node", "scripts/build.mjs"], ["node", "scripts/validate-artifact.mjs"]]
```

El README heredado del starter y `npm run build` mencionan `build.sh`; para este proyecto usar los comandos anteriores. `prepare_media_site.py` copia los datos públicos y genera `media-manifest.json`. La fuente principal de `worker/index.js` sigue siendo `desktop/media-worker.mjs`.

Para subir/activar medios, arrancar `node scripts/upload_site_media.mjs` en una sesión TTY retenida. Muestra una clave **pública** de verificación y espera un JSON por stdin oculto. Su clave privada de firma existe solo en ese proceso; si el proceso o la conversación se pierde, arrancar otro uploader, actualizar únicamente `VISU_MEDIA_PUBLIC_KEY`, desplegar con esa revisión de entorno y retomar los blobs que falten. No debilitar la firma ni publicar contraseñas.

Después de preparar el manifiesto y la clave pública, publicar con el flujo de Sites para la audiencia actual, utilizando los IDs y el commit devueltos por sus herramientas. El uploader recibe `root`, `coreRoot`, `manifest`, `origin`, `serviceToken` y `report` por stdin; obtener `serviceToken` de la respuesta autorizada de `get_site`, sin imprimirlo. `coreRoot` es `hosting/visu-biogeo-media/web`; `root` es esta carpeta. Esperar a `phase: active` y al informe de subida. Un despliegue del Worker por sí solo no activa los datos nuevos.

Comprobar después `node scripts/validate_live_learning.mjs`, la integridad del instalador y la interfaz. Actualizar informe de publicación y este documento con las cifras reales. No crear un sitio nuevo ni sustituir Supabase. En un asistente sin acceso a Sites se puede seguir trabajando y usar la app local; la publicación debe quedar expresamente pendiente hasta recuperar esa conexión.

## 12. Continuar sin rehacer trabajo terminado

Las anteriores tandas publicadas están documentadas al final de `README.md` y en `output/published-*.json`. Las auditorías actuales prevalecen sobre los números de mensajes antiguos. No reejecutar recolectores o importadores globales para una simple continuación: pueden sobrescribir información o repetir búsquedas fallidas.

No hay tareas de generación de imágenes o subidas que deban quedar ejecutándose al finalizar el traslado. El ZIP se creó después de cerrar la actualización 8.10. El primer paso de trabajo en el ordenador nuevo es comprobar los informes y elegir una nueva tanda entre las 335 entradas aún sin foto.
