# Visu BioGeo · instrucciones del proyecto

HTML/CSS y módulos ES sin framework ni npm. Python 3.12 para mantenimiento; Node 24 para pruebas.

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

## Una tarea por chat y PR

- Trabajar en una rama `codex/area-resumen` desde `origin/main` actualizado. Si el chat ya tiene trabajo, continuar su rama. Para chats simultáneos, usar worktrees independientes; nunca cambiar de rama, limpiar o guardar con stash los cambios de otro chat en una carpeta compartida.
- Una tarea concreta, un PR. Describir resultado esperado, archivos compartidos, validación y pendientes en el PR; ese es el traspaso entre chats. No crear PR sin cambios ni tareas adicionales sin necesidad.
- Los worktrees aíslan archivos, pero no evitan conflictos al integrar el mismo JSON o módulo. Indicar esos solapes y coordinar su integración. Solo integración actualiza el resumen global `docs/ESTADO.md`; cada tarea registra sus decisiones en su PR.
- Ejecutar comprobaciones relacionadas con el cambio; no repetir suites ya correctas si no hay cambios, fallos o dudas nuevas. No añadir pruebas para cambios documentales ni réplicas del propio código. La CI cubre fuentes/datos; Windows nativo es ejecución manual.
- Respuestas breves: resultado, validación, enlace al PR y cualquier bloqueo real. Registrar solo decisiones duraderas; evitar diarios y documentación duplicada. Este criterio de economía no reduce la revisión científica ni las comprobaciones necesarias.

## Reglas comunes

Preservar IDs del catálogo, progreso y permisos. No regenerar catálogo ni ejecutar SQL por mantenimiento. No inventar taxonomía, fuentes, años o etimologías. No generar fotografías científicas con IA ni añadir reglas nemotécnicas. Mantener los servicios Supabase/Sites actuales. Las candidatas no equivalen a aprobaciones; Andalucía exige dos vistas diagnósticas y Madrid admite detalles sin una vista completa que revele la respuesta. Nunca guardar credenciales privadas, PDFs aportados, fotos, cachés o instaladores en Git.

Python local: `.venv/Scripts/python.exe` en Windows; en un worktree usar el Python disponible o crear un entorno solo si hacen falta dependencias. No descargar todo el banco de imágenes para tareas de código o documentación.
