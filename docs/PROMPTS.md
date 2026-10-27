# Prompts para chats centrados en una tarea

Abrir un chat nuevo por cambio concreto dentro del proyecto cuya carpeta es `Visu BioGeo` (el repositorio real). Si habrá chats simultáneos, seleccionar **Worktree** y partir de `main` actualizado. Los worktrees separan los archivos de cada chat; los solapes se resuelven al integrar. Para trabajar en serie se puede usar Local, terminando una tarea antes de empezar la siguiente.

No crear siete chats vacíos ni mantener un chat interminable por área. Elegir el área de la tarea y sustituir el texto entre corchetes. `AGENTS.md` ya contiene las reglas de contexto, ramas, validación y PR; no hace falta pegarlo ni copiar conversaciones anteriores.

## Interfaz

```text
Área: Interfaz. Sigue AGENTS.md y la guía de esta área.
Tarea: [cambio concreto de pantalla, navegación o aspecto].
Terminado cuando: [resultado observable].
Implementa, valida lo afectado y deja un PR con un resumen breve.
```

## Aprendizaje

```text
Área: Aprendizaje. Sigue AGENTS.md y la guía de esta área.
Tarea: [cambio concreto de corrección, repasos o modo de estudio].
Ejemplo esperado: [entrada/respuesta y resultado].
Conserva el progreso y prepara un PR con las pruebas relevantes.
```

## Imágenes

```text
Área: Imágenes. Sigue AGENTS.md y la guía de esta área.
Trabaja un lote de hasta 5 entradas sin imagen de [grupo o IDs].
Busca dos vistas distintas, contrasta fuentes y revísalas visualmente.
Deja el PR con decisiones, validación y ubicación de los archivos fuera de Git. No publiques todavía.
```

## Fichas y etimologías

```text
Área: Fichas. Sigue AGENTS.md y la guía de esta área.
Completa o revisa [descripción/diagnóstico/etimología] de [hasta 5 IDs o grupo].
Documenta fuentes y deja explícitas las partes desconocidas.
Valida las fichas y prepara un PR del lote, sin publicar.
```

## Catálogo y exámenes

```text
Área: Catálogo y exámenes. Sigue AGENTS.md y la guía de esta área.
Tarea: [corrección taxonómica o evidencia de examen, con IDs/fuentes].
Conserva IDs y procedencia; no regeneres el catálogo.
Comprueba las dependencias afectadas y prepara un PR.
```

## Sincronización y uso sin conexión

```text
Área: Sincronización. Sigue AGENTS.md y la guía de esta área.
Problema: [pasos, comportamiento actual y esperado].
Corrige lo necesario preservando progreso y aislamiento entre cuentas.
Prepara un PR con la validación correspondiente.
```

## Integración

```text
Área: Integración y publicación. Sigue AGENTS.md y la guía de esta área.
Integra los PR [números/enlaces], resolviendo solapes y comprobando el resultado conjunto.
Actualiza el estado común y sincroniza main. No publiques la app todavía.
```

Para publicar una versión integrada, añadir una petición explícita: `Publica la versión integrada en el sitio actual y verifica web, medios e instalador.` La publicación requiere acceso a Sites y los archivos binarios declarados por los PR; no se consigue solo fusionando código en GitHub.

## Cuando ya existe una issue

```text
Resuelve la issue [URL] de SantiCa/visu-biogeo siguiendo AGENTS.md.
Consulta solo la guía del área y los archivos necesarios. Implementa y valida su alcance, y deja un PR que cierre esa issue.
```

## Continuar una tarea en otro chat

```text
Continúa el PR [URL]. Usa su rama y su descripción como traspaso.
Pendiente concreto: [qué falta]. Sigue AGENTS.md; comprueba el estado actual antes de modificar archivos y actualiza el mismo PR.
```

La separación por tareas limita el historial innecesario y las lecturas repetidas, pero no garantiza un porcentaje fijo de ahorro. Una tarea científica o un fallo transversal seguirá necesitando el contexto y la validación que correspondan.
