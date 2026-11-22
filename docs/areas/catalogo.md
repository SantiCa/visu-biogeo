# Catálogo y exámenes

Alcance: clasificación documentada, nombres, sinónimos y evidencias de exámenes. Consultar `python scripts/task_context.py entry ID` antes de editar una entrada.

Fuentes de verdad: `data/species.json` (IDs y procedencia), `data/learning-taxonomy.json`, `data/learning-geology.json`, `data/taxonomy.json` y `data/classification.json`. Exámenes: `data/exams.json`, `data/andalucia-priority.json`, `data/solved-exam-evidence.json` y `data/madrid-compilation-evidence.json`.

No regenerar el catálogo ni cambiar IDs para corregir nombres o añadir evidencia. Conservar variantes históricas y procedencia. No asignar especies/rangos por intuición. Distinguir documentos oficiales de soluciones académicas; una recopilación sin fecha no crea frecuencias por año. Los PDFs se mantienen fuera de Git.

Al trabajar con los listados PRECEGE, seguir también `cotejo-precege.md`. Comprobar especies ya existentes y PR en curso antes de añadir. Los restos identificados a especie conservan su entrada y pueden dar lugar a una entrada separada del organismo completo, con clasificación y fotos verificadas; no convertir un resto ambiguo en especie por suposición. Señalar por separado inclusiones, imágenes pendientes y dudas.

Validación: tests de catálogo, clasificación, `tests/solved-exams.test.mjs`, `tests/madrid-compilation.test.mjs` y sus módulos Python según los datos modificados. Los importadores han de conservar IDs, campos personales y ser idempotentes. No reimportar globalmente para una corrección local.

Solapes: catálogo, clasificación y exámenes son JSON compartidos; enumerar IDs y evidencias afectados en el PR. Un cambio en una entrada puede afectar imágenes/fichas relacionadas: comprobar esas dependencias concretas.
