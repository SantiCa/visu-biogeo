# Imágenes

Empezar con `python scripts/task_context.py images --limit 5`; añadir `--kind fosil` u otro tipo si la tarea lo especifica. Por defecto muestra entradas sin imagen aprobada, priorizadas. `--missing-pairs` incluye las parejas incompletas. Para una entrada: `python scripts/task_context.py entry ID`.

Fuente final: `data/curated-images.json`; decisiones: `data/image-review-log.json`; archivos: `assets/reviewed/` fuera de Git. Los otros bancos contienen candidatas. Trabajar un lote pequeño con IDs explícitos y nombre nuevo en `tmp/reviews/LOTE/`; no repetir recolectores globales ni scripts de lotes ya aplicados.

Buscar fuentes exactas, revisar visualmente originales y recortes, conservar autor y licencia. Dos recortes de un original no son dos fotografías de la misma entrada. Marcar `examUse` según lo que la vista demuestre. Consultar `CONTINUAR.md`, apartados 8–9, solo si se necesita el procedimiento detallado.

Validación: `python scripts/audit_images.py`; tras cambios de archivos aprobados, `python scripts/restore_media.py --refresh-lock` y `--check`. No regenerar el lock con un banco incompleto. En un worktree recuperar solo los originales necesarios o usar la copia completa como fuente; no cambiar la copia de otro chat. Cada foto nueva debe conservarse localmente hasta publicarla y respaldarla.

Solapes: el JSON de aprobaciones, el log, la auditoría y el lock son compartidos. Coordinar lotes y resolver por ID al integrar; no sobrescribir el banco con una copia antigua. Los binarios no viajan en el PR: declarar en él las rutas y cómo acceder a ellos. La integración debe obtener esos archivos y volver a calcular auditoría/lock sobre el banco combinado. La subida a GitHub no publica fotos en Sites.
