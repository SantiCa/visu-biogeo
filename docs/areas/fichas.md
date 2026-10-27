# Fichas

Empezar con `python scripts/task_context.py notes --limit 5` para entradas sin ficha; `--pending-etymology` muestra etimologías pendientes. Consultar una ficha concreta con `python scripts/task_context.py entry ID`.

Editar solo los IDs del lote acordado en `data/study-notes.json`; notas de familia en `data/family-notes.json`. Escribir síntesis propia con descripción, rasgos diagnósticos, etimología y fuentes. Distinguir una raíz contrastada de una hipótesis; dejar explícito lo desconocido. No añadir reglas nemotécnicas ni inventar familias para estructuras.

Conservar `sources`, `reviewedAt`, `reviewStatus` y `scope` según el esquema existente. Los scripts históricos que crean tandas completas no deben ejecutarse para editar una ficha.

Validación: `python scripts/audit_study_notes.py`. Si se modifica cómo se muestra la ficha, seguir también la guía de interfaz. No ejecutar auditorías de imágenes por cambios exclusivos de texto.

Solapes: `study-notes.json`, `family-notes.json` y su auditoría. Identificar el lote por IDs en el PR; al integrar conservar las aportaciones de otros lotes y recalcular la auditoría. No cambiar el resumen global desde cada chat.
