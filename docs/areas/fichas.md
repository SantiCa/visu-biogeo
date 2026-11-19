# Fichas

Empezar con `python scripts/task_context.py notes --limit 5` para entradas sin ficha; `--pending-etymology` muestra etimologías pendientes. Consultar una ficha concreta con `python scripts/task_context.py entry ID`.

Las fichas se guardan en `data/class-notes.json`, `order-notes.json`, `family-notes.json`, `genus-notes.json` y `species-notes.json`. Los rangos intermedios van con su rango base (subclase con clase, subespecie con especie), conservando su rango exacto. `data/other-notes.json` conserva los demás rangos, las entradas sin rango documentado y las fichas no taxonómicas; no convertirlas en especies.

Cada archivo contiene `taxa`, por clave `rango:nombre`, y `entries`, por ID inalterado del catálogo. Un taxón pendiente conserva `name` y `rank`; una entrada pendiente conserva `name`, sin `profile`. Las descripciones de grupos van en `guide` (`text`, `contrast`, `source`); las notas nomenclaturales de familia, en `note`. Las fichas de entradas mantienen su contenido original dentro de `profile`, sin mezclar los IDs de sinónimos. Una descripción de especie no sirve como ficha de su género.

Seguir `docs/areas/lotes-fichas.md` para seleccionar y completar lotes. Editar solo las fichas del lote acordado. Escribir síntesis propia con descripción, rasgos diagnósticos, etimología y fuentes. Distinguir una raíz contrastada de una hipótesis; dejar explícito lo desconocido. No añadir reglas nemotécnicas ni inventar familias para estructuras.

Conservar `sources`, `reviewedAt`, `reviewStatus` y `scope` según el esquema existente. Los scripts usan `scripts/note_files.py` para leer las fichas por ID y actualizar su archivo sin borrar otras fichas, explicaciones o nombres pendientes. Tras ampliar el catálogo o su clasificación, ejecutar `python scripts/sync_note_names.py`: solo sincroniza nombres e IDs desde esos datos, sin generar contenido científico. Los scripts históricos que crean tandas completas no deben ejecutarse para editar una ficha.

Validación: `python scripts/audit_study_notes.py`; comprueba también nombres pendientes, duplicados y distribución por rango. Si se modifica la carga o visualización, ejecutar `node --test tests/taxon-notes.test.mjs tests/taxonomy-guide.test.mjs tests/study-modes.test.mjs` y `python -m unittest discover -s tests -p test_note_files.py`, y seguir la guía de interfaz. No ejecutar auditorías de imágenes por cambios exclusivos de texto.

Solapes: los archivos de notas por rango y `data/study-notes-audit.json`. Identificar el lote por IDs y taxones en el PR; al integrar conservar las aportaciones de otros lotes y recalcular la auditoría. No cambiar el resumen global desde cada chat.
