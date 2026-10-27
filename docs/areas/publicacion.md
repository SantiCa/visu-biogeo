# Integración y publicación

Empezar por los PR concretos indicados y `docs/ESTADO.md`; leer `docs/DESARROLLO.md` para entorno. Integrar solo cambios terminados y compatibles; las tareas normales preparan PR, esta área coordina la versión común.

Comprobar rama base y diff, resultados de CI y solapes de archivos. Resolver por ID los JSON científicos compartidos. Las fotos quedan fuera de Git: obtener los archivos declarados en cada PR antes de integrar lotes de imagen. Recalcular auditorías y `data/media-lock.json` desde el banco combinado completo. Integrar por orden y comprobar el resultado conjunto.

Actualizar `docs/ESTADO.md` solo con versión, decisiones duraderas, cobertura y pendientes reales. La CI ejecuta fuentes/datos cuando cambian código o datos; las ediciones solo documentales no disparan esa suite. La integración Windows está disponible mediante `workflow_dispatch`.

Publicar en Sites únicamente cuando forme parte de la petición. Reutilizar el sitio y Supabase existentes; consultar `CONTINUAR.md` apartados 10–11 y la habilidad Sites vigente. Actualizar versión de `sw.js` e instalador de forma coordinada antes de publicar cambios públicos; no cambiar innecesariamente la caché persistente de fotos.

Fuentes: `desktop/media-worker.mjs`, `scripts/prepare_release.py`, `scripts/prepare_media_site.py`, `scripts/build_installer.py`, `scripts/check_learning_package.py` y `scripts/validate_live_learning.mjs`. El checkout `hosting/` es separado y no viaja en GitHub. El empaquetado requiere el banco local; Windows requiere el compilador .NET. No iniciar reconstrucciones o subidas ajenas a la tarea.
