export function setupInstallUI() {
 const button=document.querySelector('#install-app'),help=document.querySelector('#install-help');
 let prompt=null;
 const standalone=()=>matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
 const update=()=>{button.hidden=standalone();if(standalone())help.textContent='Visu BioGeo ya está abierta como aplicación en este dispositivo.';};
 const apple=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
 help.textContent=apple?'En Safari: Compartir → Añadir a pantalla de inicio. Después, abre Visu BioGeo desde su icono.':/Mac/.test(navigator.platform)?'En Safari: Archivo → Añadir al Dock. En Chrome o Edge: menú → Instalar Visu BioGeo.':'Instala Visu BioGeo desde este botón o desde el menú de Chrome o Edge. Las fotos se guardan por separado en cada dispositivo.';
 window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();prompt=event;button.textContent='Instalar Visu BioGeo';update();});
 window.addEventListener('appinstalled',()=>{prompt=null;update();});
 button.addEventListener('click',async()=>{if(prompt){const selected=prompt;prompt=null;await selected.prompt();await selected.userChoice;update();}else help.focus();});
 update();
}
