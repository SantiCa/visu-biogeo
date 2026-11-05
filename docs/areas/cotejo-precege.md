# Cotejo de listas PRECEGE

Inventario de trabajo: `data/precege-cotejo-inventario.json`. La fuente son los 51 PDF proporcionados por el usuario, cuya extracción disponible contiene 298 páginas. Los documentos originales no se incorporan al repositorio. El inventario registra nombres extraídos, archivo y página; no incluye fotografías.

## Uso por otros chats

Consultar por nombre, archivo o estado con `python scripts/consultar_cotejo_precege.py --buscar "texto"`, o mostrar los totales con `--resumen`. La búsqueda admite fragmentos sin distinguir mayúsculas ni acentos. No volcar el JSON completo en el contexto. Antes de añadir una entrada, comprobar el catálogo y los PR actuales, porque la instantánea se obtuvo sobre el commit indicado en el archivo y las ramas pueden avanzar.

Los apartados tienen significados distintos:

- `expresiones_binomiales`: expresiones detectadas automáticamente. Las coincidencias literales indican IDs y tipo de entrada del catálogo. Una expresión puede ser prosa en español, una errata o una parte de un nombre; una coincidencia con una estructura no demuestra que exista la especie completa.
- `nombres_con_saltos_o_fragmentos`: posibles nombres divididos, pendientes de comprobar en el PDF. Se incluyen algunas reconstrucciones que coinciden con el catálogo.
- `nombres_comunes_o_rotulos`: términos en mayúsculas. Incluye nombres comunes y también títulos y otros rótulos, por lo que necesita revisión contextual. Un nombre común no determina por sí solo una especie.
- `referencias_anatomicas`: referencias detectadas en texto a restos o estructuras. Una referencia como «ballena» o «mosquito» no identifica una especie; mantenerla pendiente hasta contar con evidencia suficiente.
- `cola_previa`: instantánea de 40 candidatas ya investigadas en el trabajo anterior. Sus estados son históricos, no reflejan necesariamente los PR posteriores. Comprobar las ramas y PR actuales antes de trabajar.
- `fuentes`: archivo, número de páginas y páginas sin texto. Los metadatos de procedencia permiten consultar el original local.

## Límites y próximos pasos

El inventario es un barrido automático de las 298 páginas con texto extraído. **No es un cotejo científicamente exhaustivo ni un recuento definitivo**: faltan revisión humana de las expresiones y nombres comunes, revisión visual de imágenes y comprobación de los nombres partidos que no coincidan con el catálogo. La extracción puede haber omitido texto gráfico. No interpretar el número de expresiones sin coincidencia como número de especies que faltan.

Para cada caso, revisar el original y documentar la decisión, especies o rangos implicados, fuentes taxonómicas y PR. Una identificación dudosa permanece como candidata. Al añadir especies por restos, conservar la entrada del resto e incorporar la especie solo cuando esté documentada; las fotografías requieren revisión propia según `imagenes.md`.
