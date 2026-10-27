# Sincronización

Alcance: progreso, cuentas, aportaciones compartidas, almacenamiento y uso sin conexión. Archivos: `cloud.mjs`, `community.mjs`, `storage.mjs`, `offline.mjs`, `sw.js` y funciones relevantes de `app.js`. Configuración pública en `config.js`.

Mantener aislamiento entre usuarios, validación de membresía y permisos separados de añadir/editar/aprobar/comentar. Cambiar de cuenta durante una operación no puede mezclar ni subir datos del usuario anterior. Las fotos personales no se convierten en fotos públicas al sincronizar progreso.

Validación según alcance: `tests/cloud.test.mjs`, `tests/community.test.mjs`, `tests/offline.test.mjs`, `tests/service-worker.test.mjs`. Las comprobaciones de SQL están en `supabase/`, pero no ejecutar cambios de esquema o políticas salvo que sean parte explícita de la tarea. No usar credenciales reales en fixtures ni registros.

Solapes: `sw.js`, `app.js` y almacenamiento. Coordinar versiones de caché con integración; no incrementar cada chat de forma independiente. No modificar Supabase ni Sites para resolver un cambio puramente local.
