# Visu BioGeo

Aplicación de estudio de biología y geología: HTML/CSS y módulos JavaScript, sin framework ni instalación npm. Python 3.12 y Node 24 para mantenimiento.

## Leer solo el contexto necesario

- Empezar por `docs/ESTADO.md` y la tarea concreta. Consultar `docs/DESARROLLO.md` para entorno, pruebas, fotos y publicación.
- `CONTINUAR.md` conserva el detalle del traslado y de la publicación 8.10; consultar sus apartados cuando hagan falta, sin releerlo entero en cada tarea.
- Consultar `data/image-audit.json` para huecos de imagen; `data/study-notes-audit.json` para fichas. Las auditorías actuales prevalecen sobre cifras históricas.
- Registrar cambios mediante commits concretos y actualizar el estado cuando cambien pendientes o decisiones. Usar ramas `codex/…` para nuevos trabajos.

## Fuentes de verdad y límites

- `data/species.json`: catálogo e IDs estables. No regenerar catálogo ni cambiar IDs al modificar imágenes o fichas; el progreso depende de ellos.
- `data/curated-images.json`: aprobaciones, créditos, recortes y uso de examen. Los otros bancos de imágenes son candidatas, no aprobaciones.
- `data/study-notes.json`, `data/family-notes.json` y `data/learning-*.json`: fichas y clasificación documentada. Indicar lo desconocido, sin inventar rangos, fuentes, años ni etimologías.
- No generar fotografías científicas con IA ni añadir reglas nemotécnicas. Revisar visualmente originales y recortes; dos recortes del mismo original no son dos fotos de una entrada.
- Andalucía exige dos vistas explícitamente diagnósticas. Madrid admite detalles y partes sin una vista completa que revele la respuesta.
- Mantener permisos, progreso y configuración Supabase/Sites. No ejecutar SQL ni cambiar políticas por una operación de mantenimiento del repositorio.
- Nunca guardar contraseñas, tokens ni claves administrativas. `config.js` contiene únicamente configuración pública. No subir PDFs aportados, cachés, fotos o instaladores a Git.

## Comprobaciones

Desde la raíz, usar `python` del entorno virtual (en este PC `.venv/Scripts/python.exe`):

```sh
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

Para imágenes: `python scripts/restore_media.py --check` y `python scripts/audit_images.py`. Tras cambiar el banco aprobado, actualizar `data/media-lock.json` con `python scripts/restore_media.py --refresh-lock`. Para fichas: `python scripts/audit_study_notes.py`.

La prueba nativa requiere Windows, el lanzador compilado y sus fotos de muestra. GitHub Actions prepara los tres. Consultar `docs/DESARROLLO.md` antes de empaquetar o publicar; GitHub controla las fuentes y Sites sigue siendo el alojamiento.
