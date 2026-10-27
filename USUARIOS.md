# Añadir usuarios y elegir permisos

Solo la cuenta administradora ve **Ajustes > Usuarios y permisos**. Las altas públicas siguen desactivadas. Compartir el programa no autoriza a nadie en la base ni comparte tu contraseña.

1. Abre [Authentication > Users de Visu BioGeo](https://supabase.com/dashboard/project/bqyjhkrnhmrrmfceshlh/auth/users). Usa **Add user > Create new user**, introduce el correo y la contraseña que utilizará esa persona y activa **Auto Confirm User**. No hace falta enviar invitaciones ni configurar correo SMTP. La contraseña de estudio es distinta de la contraseña de administración de la base.
2. Entra con tu cuenta de estudio en Visu. Abre **Ajustes > Usuarios y permisos** e introduce ese mismo correo y el nombre que se mostrará junto a sus comentarios.
3. Marca **Cuenta autorizada** y elige por separado las capacidades de la tabla siguiente. Pulsa **Guardar usuario y permisos**. No se envía ningún correo desde ese formulario.
4. Dale el instalador o acceso a la web. Si configuras el sitio como privado, añade además esa persona en la opción de compartir del sitio en Sites; autorizarla en Supabase no cambia quién puede visitar el alojamiento. El sitio está actualmente en modo público; el catálogo base es accesible sin entrar, pero el progreso y las aportaciones siguen exigiendo una cuenta autorizada. El instalador Windows no requiere ese acceso a Sites.

| Permiso | Qué permite |
|---|---|
| Cuenta autorizada | Entrar, sincronizar su propio progreso y consultar las aportaciones compartidas. |
| Añadir imágenes nuevas | Subir archivos al banco privado o proponer una URL. Siempre quedan pendientes de aprobación. |
| Editar datos de imágenes | Corregir descripción, autor, licencia y procedencia. No cambia su aprobación. |
| Aprobar o rechazar | Decidir qué imágenes entran en el repaso compartido. No concede permiso para añadir o editar. |
| Publicar comentarios | Escribir y editar sus comentarios, o retirarlos. No permite modificar los de otra persona. |

Puedes dar solo lectura dejando desmarcadas todas las capacidades de aportación. Puedes permitir añadir y comentar sin aprobar. El administrador conserva todas las capacidades y puede retirar comentarios ajenos, pero no reescribirlos. La administración no se concede desde este formulario.

Para cambiar una cuenta, pulsa **Actualizar usuarios > Cambiar permisos** y guarda el formulario. Desmarcar **Cuenta autorizada** retira el acceso a sincronización y aportaciones. No borra su progreso ni los archivos que ya tenga descargados. Su progreso permanece privado: el formulario de administración lista permisos, no respuestas de estudio.

Los cambios se comprueban en Supabase, además de en los botones. Las aportaciones compartidas requieren Internet y solo se anuncian como guardadas cuando el servidor las acepta. Si algo falla, se muestra el error. No se ha creado ni autorizado a otras personas durante la preparación de esta versión.

Los comentarios aparecen tras resolver y en el catálogo. Su borrador se guarda solo en el navegador; **Publicar comentario** lo comparte. Las fotos privadas de versiones anteriores siguen siendo personales y se trasladan con la copia JSON. Las nuevas fotos añadidas con sesión iniciada se guardan en el bucket privado compartido; una URL externa sigue dependiendo de su fuente.
