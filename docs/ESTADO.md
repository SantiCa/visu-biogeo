# Estado del proyecto

Actualizado el 5 de noviembre de 2026. Base funcional y de catálogo: **8.15**.

Repositorio: `https://github.com/SantiCa/visu-biogeo` (privado). GitHub controla fuentes y cambios. La aplicación está publicada en `https://visu-biogeo-santica.santic1290.chatgpt.site/`; la dirección anterior de nimblequail260 redirige a ella. El proyecto de Sites y el de Supabase se conservan.

La versión 8.15 integra los PR #36–#45: 19 especies, cuatro géneros y dos formas larvarias de PRECEGE, además de una procedencia y un inventario de cotejo. El catálogo tiene 2.641 entradas y 503 fichas. Las 25 altas carecen de imágenes aprobadas; Andalucía exige dos vistas diagnósticas. El cotejo nominal de crustáceos está cerrado; los demás PDF no tienen cierre completo acreditado. La cola histórica conocida conserva 19 consultas pendientes de revisión, sin representar el total de posibles omisiones.

Publicación: versión 23 de Sites, fuente `ef189cca6e832a5e1561626448b5c3426541517b`, manifiesto activo `bef002db2e17e69972bfa0077c383ffce753b6997a423bbf549c2e5aed644402`, 4.804 archivos. Banco combinado de 4.750 archivos físicos aprobados y 4.805 referencias, con 2.289 entradas ilustradas, 2.143 con pareja y 352 sin imagen. Se verificaron los hashes del banco, 71 pruebas JavaScript, 15 Python incluida la prueba nativa y el paquete Windows 8.15. Tras la activación se verificaron 13 archivos principales y el rechazo de activaciones sin firma. Supabase y la audiencia pública se conservan; la sincronización con cuentas reales queda pendiente de comprobación manual.

Siguen pendientes los casos A9, A10 y A15 de Andalucía 2021, los rangos de las cinco entradas nuevas de Castilla-La Mancha y la revisión científica de la cola PRECEGE. El historial madrileño es incompleto; las 50 correspondencias de Madrid 2002 se atribuyen a un opositor, sin clave oficial. Los importadores conservan la fecha más reciente y la posición de documentos y eventos al reaplicar evidencia. Las tareas nuevas arrancan con `scripts/start_task.py` desde una raíz limpia y una copia actualizada de `origin/main`.

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
