# Trabajar con Codex, Claude y Gemini

`AGENTS.md` es la fuente común de instrucciones del proyecto. `CLAUDE.md` importa ese archivo para Claude Code y `GEMINI.md` hace lo mismo para Gemini CLI. Los archivos breves evitan mantener tres copias de las reglas. Las instrucciones concretas del usuario y las restricciones del entorno también se aplican.

## Preparación

1. Abre la raíz real del repositorio. En este PC es `C:\Users\Santiago\Documents\ChatGPT\App Visu`; en otro equipo o en la nube usa la ruta de su propia copia. El repositorio de GitHub es privado: la cuenta o integración utilizada necesita acceso.
2. Comprueba que el agente puede leer `AGENTS.md` y las guías. Los imports se aplican en Claude Code y Gemini CLI con las funciones documentadas de esos productos; otras aplicaciones de Claude o Gemini pueden funcionar de otra forma. Si no cargan las instrucciones, pide expresamente que lean `AGENTS.md` y la guía del área.
3. Consulta `git status --short --branch`. Para una tarea nueva, desde la copia que contiene el repositorio común ejecuta `python scripts/start_task.py area-resumen` y trabaja en el worktree devuelto. El comando necesita acceso a Git, red para `fetch`, una raíz compartida limpia en `main` y una referencia `origin/main` válida. Si el entorno aislado no permite crear worktrees o Git no está disponible, informa del bloqueo y conserva los cambios; no fuerces ni limpies la copia. Para un PR ya abierto, continúa su worktree y su rama.
4. Mantén una tarea y un PR por cambio. Al cambiar de agente, proporciona el enlace del PR: su descripción debe recoger alcance, IDs o funciones afectados, archivos compartidos, validación, fuentes y pendientes. Comprobar el estado actual de la rama y de los demás PR antes de editar. Los agentes no comparten automáticamente su conversación.

Si dos tareas trabajan a la vez, cada una necesita su worktree. Al integrar, revisar los solapes, especialmente JSON científicos, `app.js` y los bancos de imágenes. No cambiar de rama, hacer stash ni borrar archivos de otro agente en una carpeta compartida.

## Qué viaja con Git

El código, las guías y los metadatos versionados viajan con el repositorio. Los PDF aportados, fotografías aprobadas, instaladores, cachés, credenciales y progreso personal no viajan en Git. Los PR de imágenes deben identificar la ubicación de los binarios; integración tiene que acceder a ellos y recalcular los datos con el banco combinado. Para recuperar el banco aprobado en otra copia, consulta `docs/DESARROLLO.md`; no descargues todo el banco para una tarea de código o documentación.

GitHub no publica la web. La publicación utiliza el proyecto Sites y Supabase existentes, sigue `docs/areas/publicacion.md` y se hace cuando el usuario la pide. Si el agente no dispone del plugin, acceso o archivos necesarios, puede preparar el trabajo y dejar la publicación pendiente para un entorno que sí los tenga. Nunca incluir secretos en Git, prompts, logs o PR.

## Mensajes reutilizables

Para una tarea nueva, usando cualquier agente con acceso al proyecto:

```text
Trabaja en Visu BioGeo. Lee AGENTS.md y la guía del área [área].
Tarea: [cambio concreto]. Terminado cuando: [resultado observable].
Usa el flujo de worktree del proyecto, valida lo afectado y deja un PR con fuentes, solapes y pendientes cuando corresponda.
```

Para el relevo de una tarea existente:

```text
Continúa el PR [enlace]. Lee AGENTS.md y la guía del área pertinente.
Comprueba la rama, el estado actual y la descripción del PR. Completa [pendiente], valida lo afectado y actualiza el mismo PR.
```

Para el estado global, consultar `docs/ESTADO.md`. `README.md` y `CONTINUAR.md` contienen historial: sus cifras fechadas no son recuentos actuales. Los prompts por área están en `docs/PROMPTS.md`.

Referencias de configuración: [instrucciones de Claude Code](https://code.claude.com/docs/en/memory) y [archivos de contexto de Gemini CLI](https://geminicli.com/docs/cli/gemini-md/). La disponibilidad de sus funciones depende de la versión y configuración del usuario.
