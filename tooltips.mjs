const help={
 'check-answer':'Comprueba el nombre y los campos de clasificación activos. Al elegir la valoración o Continuar se guarda cada resultado; cualquier error programa repaso en 10 minutos.',
 'classification-collapse':'Pliega todas las ramas del árbol sin cambiar tu progreso.',
 reveal:'Muestra la respuesta como no recordada. Pulsa después Continuar para guardar el error y programar el repaso en 10 minutos.',
 skip:'Pasa a otra entrada sin guardar esta respuesta ni cambiar su próximo repaso, incluso si ya has visto la solución.',
 report:'Abre esta entrada en el catálogo para consultar las fuentes y revisar o añadir imágenes según tus permisos. No guarda una respuesta de estudio.',
 'sync-now':'Combina tu progreso local con el de tu cuenta y actualiza las aportaciones compartidas. Requiere conexión.',
 'sign-in':'Accede a tu cuenta de estudio autorizada. Tu progreso queda separado del de otros usuarios.',
 'sign-out':'Cierra la sesión de este dispositivo. Conserva los datos locales y no cierra tus otros dispositivos.',
 'sign-in-link':'Solicita un enlace de acceso para tu cuenta existente; no crea otra cuenta.',
 'transfer-local':'Combina el estudio local anterior con tu cuenta y conserva la copia local original.',
 'backup-export':'Descarga una copia JSON del progreso, preferencias, decisiones y fotos privadas locales de esta cuenta.',
 'backup-import':'Combina una copia con los datos actuales; conserva el repaso más reciente de cada entrada.',
 'catalog-shuffle':'Sortea otra fotografía aprobada para cada fila, cuando hay varias disponibles.',
 'catalog-more':'Muestra más entradas que cumplen los filtros actuales.',
 'priority-more':'Muestra más entradas de la lista de prioridades.',
 'priority-apply':'Valida todas las líneas y guarda tus prioridades personales si no hay errores.',
 'priority-export':'Descarga tus prioridades personales en un archivo JSON.',
 'offline-download':'Guarda en este dispositivo las fotos aprobadas del bloque seleccionado. Puedes reanudar sin repetir las ya guardadas.',
 'offline-stop':'Detiene esta descarga conservando todas las fotos que ya se han guardado.',
 'install-app':'Muestra la instalación como aplicación o las instrucciones de tu navegador.',
 'member-refresh':'Consulta las cuentas autorizadas y sus permisos actuales.',
};
export function buttonHelp(button){
 if(button.dataset.taxHelp)return 'Muestra rasgos, significado del nivel y etimologías de este taxón. También se puede consultar con ratón o toque.';
 if(button.dataset.help)return button.dataset.help;
 if(button.dataset.view==='taxonomy-study')return 'Explora rangos, rasgos y ejemplares en un árbol desplegable o un mapa que puedes ampliar y recorrer. No puntúa.';
 if(button.dataset.select||button.dataset.mapSelect)return 'Muestra la explicación de este grupo o la ficha del ejemplar; no registra respuestas.';
 if(button.dataset.toggle||button.dataset.mapToggle)return 'Abre o pliega las ramas de este grupo.';
 if(button.dataset.rankGuide)return 'Explica qué significa este rango taxonómico y cómo se distingue de los demás.';
 if(help[button.id])return help[button.id];
 if(button.dataset.view)return 'Abre '+({study:'el repaso con imágenes',catalog:'el catálogo y la lectura libre',classification:'los árboles de taxonomía, minerales y rocas',priorities:'tus especies prioritarias',progress:'el resumen de tu aprendizaje',settings:'la cuenta, instalación y copias de seguridad'}[button.dataset.view]||'esta sección')+'.';
 if(button.dataset.grade)return button.dataset.grade==='again'?'Guarda esta respuesta y pasa a otra entrada. Programa el siguiente repaso en 10 minutos.':'Guarda el resultado y adapta el intervalo al esfuerzo elegido. Después muestra otra entrada.';
 if(button.dataset.decision)return button.dataset.decision==='approved'?'Aprueba esta foto para el repaso. En una cuenta autorizada, la decisión se comparte con los demás usuarios.':'Excluye esta foto del repaso. En una cuenta autorizada, la decisión se comparte con los demás usuarios.';
 if(button.hasAttribute('data-save-priority'))return 'Guarda tu frecuencia y referencia personal para esta entrada; no modifica la prioridad de otros usuarios.';
 if(button.hasAttribute('data-reset-priority'))return 'Restaura la frecuencia documentada de Andalucía para esta entrada en tu cuenta.';
 if(button.dataset.item)return button.classList.contains('catalog-entry')?'Abre las imágenes y procedencia de esta entrada. No registra una respuesta.':'Abre la revisión de imágenes de esta entrada. No registra una respuesta.';
 if(button.dataset.member)return 'Carga los permisos de esta cuenta en el formulario. Los cambios solo se aplican al pulsar Guardar usuario y permisos.';
 if(button.dataset.commentAction)return ({edit:'Edita tu comentario guardado.',remove:'Retira el comentario de la conversación sin borrar el registro de forma permanente.'})[button.dataset.commentAction];
 if(button.type==='submit')return button.form?.classList.contains('comment-form')?'Publica este comentario para los usuarios autorizados. Requiere conexión.':button.form?.id==='add-image'?'Añade las fotos como pendientes de revisión. Las compartidas solo entran en el repaso después de aprobarlas.':button.form?.classList.contains('image-metadata')?'Guarda la descripción y procedencia de esta imagen según tus permisos.':button.form?.id==='member-form'?'Autoriza una cuenta ya creada en Supabase con los permisos seleccionados. No envía correos ni cambia contraseñas.':'Guarda los datos de este formulario.';
 return 'Abre '+button.textContent.trim().toLowerCase()+'.';
}
export function setupButtonHelp(root=document){
 const decorate=()=>root.querySelectorAll('button').forEach(b=>{const text=buttonHelp(b);if(text){b.title=text;b.setAttribute('aria-description',text);}});
 decorate();new MutationObserver(decorate).observe(root.body||root,{childList:true,subtree:true});
}
