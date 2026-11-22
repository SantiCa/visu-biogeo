# Visu BioGeo · instrucciones del proyecto

HTML/CSS y módulos ES sin framework ni npm. Python 3.12 para mantenimiento; Node 24 para pruebas.

Al escribir o modificar código, incluidos scripts y pruebas, aplicar los principios de Clean Code adaptados al lenguaje: nombres claros, responsabilidades coherentes, diseño sencillo, validación en los límites y errores útiles. Mantener el comportamiento y los contratos existentes salvo petición expresa; verificar los cambios con las comprobaciones pertinentes.

## Cómo colaborar con Santiago

- Aplicar estas instrucciones con cualquier agente. La petición concreta del usuario prevalece sobre las preferencias generales del proyecto; no asumir que otro agente conoce esta conversación o dispone de las mismas herramientas y archivos.
- Avanzar hasta completar la tarea autorizada; resolver decisiones rutinarias sin pedir confirmaciones innecesarias. Comunicar resultados y bloqueos de forma clara y breve, indicando qué se ha comprobado y qué queda pendiente.
- Reducir consumo de contexto: reutilizar fuentes, resultados y scripts válidos, buscar solo lo necesario y evitar repetir extracciones de PDF, investigaciones o pruebas sin cambios relevantes. Esto no sustituye la revisión científica ni justifica dar por terminada una tarea incompleta.
- Preferir una tarea activa cada vez; si el usuario quiere trabajo simultáneo, aislar las tareas y coordinar los archivos compartidos. Ajustar el tamaño de los lotes a la petición y a las fuentes disponibles; para fichas, aplicar `docs/areas/lotes-fichas.md`.
- Al continuar «el siguiente lote», usar el último PR y comprobar el catálogo y los PR actuales para evitar duplicados. En el cierre, distinguir las altas verificadas, las propuestas aún sin integrar y los casos pendientes; un recuento parcial debe identificarse como tal.

## Contexto mínimo

1. Identificar la tarea y revisar `git status --short --branch`. Leer **solo la guía del área** de la tabla. Consultar `docs/ESTADO.md` si hacen falta versión o pendientes globales.
2. Buscar con `rg` y leer funciones/rangos relevantes. No volcar bancos JSON, README o historial completos. Usar `python scripts/task_context.py images`, `notes` o `entry ID` para consultas pequeñas.
3. Ampliar contexto cuando la tarea lo requiera. `CONTINUAR.md` es referencia histórica; `docs/DESARROLLO.md`, guía de entorno. No releerlos por rutina ni recuperar conversaciones antiguas para una tarea autocontenida.

| Área indicada por el usuario | Guía a leer |
|---|---|
| Interfaz | `docs/areas/interfaz.md` |
| Aprendizaje | `docs/areas/aprendizaje.md` |
| Imágenes | `docs/areas/imagenes.md` |
| Fichas | `docs/areas/fichas.md` |
| Catálogo y exámenes | `docs/areas/catalogo.md` |
| Sincronización | `docs/areas/sincronizacion.md` |
| Integración y publicación | `docs/areas/publicacion.md` |

Para crear o completar fichas, seguir también `docs/areas/lotes-fichas.md` y avanzar en lotes amplios cuando las fuentes lo permitan.
Para cotejar los PDF de PRECEGE, consultar además `docs/areas/cotejo-precege.md` y reutilizar el inventario compartido. Sus resultados automáticos no son un cotejo exhaustivo ni un recuento definitivo.

## Una tarea por chat y PR

- Trabajar en una rama `codex/area-resumen` desde `origin/main` actualizado. Si el chat ya tiene trabajo, continuar su rama. Para chats simultáneos, usar worktrees independientes; nunca cambiar de rama, limpiar o guardar con stash los cambios de otro chat en una carpeta compartida.
- Para cada tarea nueva, incluso dentro de un chat reutilizado, ejecutar `python scripts/start_task.py area-resumen` y trabajar en la ruta devuelta. Comprueba que la raíz esté limpia, actualiza `main` solo por avance rápido y crea una rama/worktree nuevos desde `origin/main`. Si la tarea tiene un PR abierto, continuar su worktree. Los worktrees de tareas integradas se conservan como referencia y no se reutilizan para cambios distintos. `python scripts/start_task.py --check` comprueba la raíz común.
- Una tarea concreta, un PR. Describir resultado esperado, archivos compartidos, validación y pendientes en el PR; ese es el traspaso entre chats. No crear PR sin cambios ni tareas adicionales sin necesidad.
- Estas reglas se aplican también a Claude y Gemini. Los archivos `CLAUDE.md` y `GEMINI.md` remiten aquí; si el entorno no los carga o no tiene acceso al repositorio, consultar `docs/AGENTES-IA.md`. Un agente no hereda automáticamente las herramientas, credenciales o archivos locales de otro.
- Los worktrees aíslan archivos, pero no evitan conflictos al integrar el mismo JSON o módulo. Indicar esos solapes y coordinar su integración. Solo integración actualiza el resumen global `docs/ESTADO.md`; cada tarea registra sus decisiones en su PR.
- Las tareas ordinarias dejan el PR preparado. Integración revisa los cambios, coordina su fusión y actualiza `main` cuando el usuario lo solicita. GitHub no publica la web: para desplegar, seguir `docs/areas/publicacion.md` cuando la publicación forme parte de la petición. Si faltan acceso o binarios, informar de lo pendiente.
- Ejecutar comprobaciones relacionadas con el cambio; no repetir suites ya correctas si no hay cambios, fallos o dudas nuevas. No añadir pruebas para cambios documentales ni réplicas del propio código. La CI cubre fuentes/datos; Windows nativo es ejecución manual.
- Respuestas breves: resultado, validación, enlace al PR y cualquier bloqueo real. Registrar solo decisiones duraderas; evitar diarios y documentación duplicada. Este criterio de economía no reduce la revisión científica ni las comprobaciones necesarias.

## Reglas comunes

Preservar IDs del catálogo, progreso y permisos. No regenerar catálogo ni ejecutar SQL por mantenimiento. No inventar taxonomía, fuentes, años o etimologías. No generar fotografías científicas con IA ni añadir reglas nemotécnicas. Mantener los servicios Supabase/Sites actuales. Las candidatas no equivalen a aprobaciones; Andalucía exige dos vistas diagnósticas y Madrid admite detalles sin una vista completa que revele la respuesta. Nunca guardar credenciales privadas, PDFs aportados, fotos, cachés o instaladores en Git.

El objetivo de los listados PRECEGE es incorporar las especies documentadas que falten, con procedencia y clasificación verificadas. Si el PDF muestra un resto anatómico atribuible a una especie, conservar la entrada del resto y preparar también la entrada del organismo completo, su ubicación taxonómica y fotografías del animal cuando la identificación y las fuentes lo permitan. Una ficha presente en el catálogo no equivale a una especie estudiable con fotografías aprobadas. No asignar una especie concreta a un nombre común, género o resto ambiguo sin evidencia.

Python local: `.venv/Scripts/python.exe` en Windows; en un worktree usar el Python disponible o crear un entorno solo si hacen falta dependencias. No descargar todo el banco de imágenes para tareas de código o documentación.
