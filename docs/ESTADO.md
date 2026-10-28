# Estado del proyecto

Actualizado el 28 de octubre de 2026. Base funcional y de catálogo: **8.11**.

Repositorio: `https://github.com/SantiCa/visu-biogeo` (privado). GitHub controla fuentes y cambios. La aplicación publicada sigue en `https://visu-biogeo-santica.nimblequail260.chatgpt.site/`; la sincronización sigue en el mismo proyecto Supabase.

La versión 8.11 incorpora 15 fichas prioritarias (455 en total, 85 de 103 prioritarias), el modo oscuro configurable y la aparición corroborada de calcopirita en Andalucía 2021. La tanda de foraminíferos permanece en el PR #5 en borrador y no está publicada. Los casos A9, A10 y A15 de Andalucía 2021 siguen pendientes.

Publicación: versión 18 de Sites, manifiesto activo `60ac4bca9615f5ae3498949f209195853c6775ba6ea29a66a5aa5c3c969131dd`, 4.758 archivos. Se verificaron 4.704 imágenes locales, 66 pruebas JavaScript, 15 Python, los archivos públicos de aprendizaje y el paquete Windows. La revisión visual móvil y la sincronización con cuentas reales quedan pendientes de comprobación manual.

La raíz local definitiva es **`C:\Users\Santiago\Documents\ChatGPT\App Visu`**, coincidiendo con el proyecto que ya estaba abierto en Codex. Los archivos y `.git` están directamente en esa carpeta; la subcarpeta intermedia `Visu BioGeo` de la restauración se retiró. `traslado-local/` conserva los respaldos e informes históricos con sus rutas originales y queda fuera de Git.

## Estado validado al importar

- 2.602 entradas; 2.267 con imagen aprobada, 2.123 con pareja.
- 4.759 referencias aprobadas distintas dentro de cada entrada; cero archivos aprobados rotos.
- 479 entradas pendientes de pareja; **335 sin imagen**, el siguiente grupo prioritario si el usuario pide continuar las imágenes.
- 440 fichas descriptivas; 2.162 entradas sin ficha y 257 etimologías total o parcialmente pendientes.
- Las 23 entradas de nubes tienen pareja y ficha; no repetir los scripts de la tanda `clouds810`.
- Antes de preparar GitHub pasaron 65 pruebas JavaScript y 9 Python, incluida la prueba nativa Windows.
- Preparación para GitHub: 65 pruebas JavaScript y 15 Python correctas, con seis pruebas nuevas de integridad y recuperación de medios. Una copia limpia pasó la suite de fuentes (la prueba nativa se omite hasta compilar el EXE); se descargaron las tres fotos de muestra, se compiló el lanzador y su integración pasó también.
- El manifiesto recuperable fija 4.704 archivos físicos aprobados, 1.461.724.788 bytes, todos comprobados contra la copia local. La diferencia con el recuento de referencias se debe a reutilización entre entradas.

Las listas exactas y actualizadas están en `data/image-audit.json` y `data/study-notes-audit.json`. No deducir aprobación taxonómica o elegibilidad Andalucía de un simple recuento.

## Próximo trabajo

La organización por tareas está en `AGENTS.md`, `docs/areas/` y `docs/PROMPTS.md`. Hay formularios de issue/PR para describir un cambio y traspasarlo entre chats. Cada tarea usa su rama; la integración coordina archivos compartidos y el resumen global. Las consultas de `scripts/task_context.py` muestran listas pequeñas o una sola entrada sin volcar bancos completos.

El traslado a GitHub no inicia una tanda de investigación ni una publicación. Al recibir una tarea, trabajar solo su alcance y dejar un commit y una nota del resultado. Para imágenes, elegir IDs desde la auditoría; congelar un lote nuevo, guardar fuentes, revisar visualmente y aplicar decisiones explícitas. Para historia detallada, consultar `CONTINUAR.md` y `README.md`.

## Portabilidad

El código, los datos y las instrucciones viajan con Git. El banco binario se recupera desde el alojamiento existente con `scripts/restore_media.py`; su contenido se verifica con `data/media-lock.json`. Las cachés de investigación, PDFs, instaladores y checkouts generados permanecen en la copia local y el ZIP original.

El repositorio principal del ZIP no tenía commits de rama; contenía objetos/checkpoints de Codex. La primera versión de GitHub parte del estado validado 8.10. Se conserva el checkout histórico de Sites en la copia local, separado de este repositorio.
