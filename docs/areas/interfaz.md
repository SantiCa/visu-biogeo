# Interfaz

Alcance: aspecto, navegación, filtros, accesibilidad y presentación. Confirmar el comportamiento concreto pedido; no rediseñar otras pantallas.

Archivos habituales: `index.html`, `styles.css`, funciones relacionadas de `app.js`; para catálogo `catalogue.mjs`, para fichas `notes.mjs` y `tooltips.mjs`. Localizar con `rg` antes de leer módulos grandes. Los árboles usan `taxonomy-guide.mjs` y `taxon-reference.mjs`.

Validación: comprobar la pantalla y estados afectados (tamaño móvil, teclado o foco cuando proceda). Ejecutar `tests/catalogue.test.mjs`, `tests/study-modes.test.mjs` o `tests/taxonomy-guide.test.mjs` solo si se cambia la lógica que cubren. Un ajuste CSS simple requiere inspección visual, no nuevas pruebas automáticas.

Solapes: `app.js` y `styles.css` pueden cambiar en varios chats. Señalar las funciones o selectores afectados en el PR. No tocar datos, intervalos, cuentas ni permisos salvo que la tarea los incluya.
