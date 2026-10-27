# Desarrollo y control de versiones

## Preparar una copia

```sh
git clone https://github.com/SantiCa/visu-biogeo.git
cd visu-biogeo
python -m venv .venv
```

Activar `.venv` con el procedimiento del sistema e instalar `python -m pip install -r requirements-maintenance.txt` para las herramientas de mantenimiento. Requiere Python 3.12; Node 24 ejecuta las pruebas y herramientas JavaScript sin instalar paquetes npm. La interfaz no necesita compilación.

## Fotografías fuera de Git

```sh
python scripts/restore_media.py
python scripts/restore_media.py --check
```

La primera orden descarga únicamente los archivos ausentes del banco aprobado, desde el alojamiento actual. Comprueba tamaño y SHA-256 antes de crear cada archivo. Un archivo local modificado provoca un error y se conserva. La segunda orden solo comprueba la copia local. Se puede interrumpir y volver a ejecutar; los archivos correctos se reutilizan. La descarga completa ronda 1,4 GB.

`--sample` selecciona solo las tres fotografías que usa la prueba nativa (JPEG, PNG y JPG); sirve para CI o una comprobación rápida. `--workers 1` limita la concurrencia. Un error HTTP se informa sin intentar eludir restricciones. Los originales, créditos, licencias y usos permitidos siguen en `data/curated-images.json`; el manifiesto no cambia esos derechos.

Después de aprobar o modificar fotografías locales, ejecutar `python scripts/restore_media.py --refresh-lock` y registrar el nuevo manifiesto junto con las decisiones. El comando calcula hashes desde los archivos locales y no publica nada. Para que otras copias puedan recuperar las nuevas fotos, completar primero la publicación de medios de Sites. Los recortes y originales aprobados deben seguir disponibles en la copia local y su respaldo.

## Ejecutar la app

Con el banco recuperado:

```sh
python scripts/prepare_release.py --target output/local-app
python -m http.server 8083 --bind 127.0.0.1 --directory output/local-app
```

Abrir `http://127.0.0.1:8083/`. No servir la raíz completa del repositorio ni abrir `index.html` como `file://`. En Windows se puede compilar el lanzador y abrirlo:

```powershell
.\scripts\build_desktop.ps1 -Destination (Join-Path (Get-Location) 'Abrir Visu BioGeo.exe')
```

El progreso personal se recupera entrando con la misma cuenta y esperando a **Sincronizado**. Git no guarda sesiones ni progreso del navegador. Los datos exclusivamente locales necesitan su exportación JSON.

## Pruebas

```sh
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

Las pruebas de lógica no requieren el banco completo. La prueba nativa se omite si no existe el EXE; para ejecutarla en Windows compilar el lanzador y recuperar `--sample`. Su fixture histórico de importación está en `tests/fixtures/solved-exams-import.json`, no en una salida de trabajo ignorada por Git.

GitHub Actions ejecuta las pruebas de fuentes en Ubuntu para cada push y pull request. En `workflow_dispatch` ejecuta además la integración Windows, que compila el lanzador y recupera las tres fotos de muestra. Así las comprobaciones habituales no dependen de la disponibilidad del alojamiento de fotos. La suite de medios prueba integridad, rechazo de rutas y preservación de archivos locales con respuestas simuladas.

Para cambios de imágenes o fichas, ejecutar además las auditorías correspondientes de `AGENTS.md`. El empaquetado completo requiere el banco local y Windows: ver `CONTINUAR.md`, apartado 10.

## Forma de trabajar

- `main` conserva la versión integrada; usar ramas `codex/descripcion-breve` para cada tarea nueva.
- Commits que expliquen el cambio y su propósito; comprobar el diff antes de subir y no añadir archivos temporales.
- Mantener `docs/ESTADO.md` breve y actualizado. Llevar a cada tarea solo la información y los archivos que necesita.
- No guardar credenciales en archivos o remotos Git. El código mantiene únicamente la clave publicable de Supabase.

## Publicación y respaldo

GitHub no sustituye Sites ni Supabase, ni ejecuta despliegues automáticos. `desktop/media-worker.mjs` es la fuente del Worker; `scripts/prepare_media_site.py` prepara el checkout de Sites. Ese checkout es una copia separada y queda fuera de GitHub. Antes de publicar, usar el plugin Sites con el proyecto existente y consultar `CONTINUAR.md`, apartado 11. No crear otro sitio ni otra base de datos.

El ZIP de traslado conserva el estado completo, las fotos, los PDFs locales, las cachés y el checkout histórico de alojamiento. Mantener un respaldo de esos materiales: el repositorio de fuentes y el alojamiento activo no sustituyen una copia de seguridad independiente.
