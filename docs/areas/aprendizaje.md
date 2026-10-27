# Aprendizaje

Alcance: respuestas, clasificación por campos, prioridades, intervalos y selección de imágenes. `engine.mjs` planifica; `classification-learning.mjs` corrige; `exam-photos.mjs` decide elegibilidad; `app.js` conecta la interfaz.

Preservar aciertos y contadores por campo. Los campos desconocidos no penalizan; un fallo evaluado mantiene la repetición a diez minutos. Los nombres comunes se preguntan sin mostrarlos antes de responder. No cambiar estas reglas por un arreglo ajeno a ellas.

Consultar una entrada con `python scripts/task_context.py entry ID`. Clasificación documentada: `data/learning-taxonomy.json`, `data/learning-geology.json`; no cargar bancos completos en la conversación.

Validación: elegir entre `tests/engine.test.mjs`, `tests/classification-learning.test.mjs`, `tests/chemical-answers.test.mjs`, `tests/study-modes.test.mjs` y los tests de árboles según el comportamiento modificado. Ejecutar los elegidos con `node --test RUTAS`.

Solapes: `engine.mjs`, `app.js` y clasificación. Explicar en el PR cualquier cambio de comportamiento que afecte al progreso o a otro modo de estudio.
