const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function memberPermissions(member){
 const enabled=member?.enabled===true,admin=enabled&&member.is_admin===true;
 return {member:enabled,admin,add:enabled&&(admin||member.can_add_images===true),edit:enabled&&(admin||member.can_edit_images===true),review:enabled&&(admin||member.can_review_images===true),comment:enabled&&(admin||member.can_comment===true)};
}
const unwrap=result=>{if(result.error)throw result.error;return result.data;};
export async function fetchCommunity(client,{userId,isCurrent,previous={}}){
 const member=unwrap(await client.from('visu_members').select('*').eq('user_id',userId).maybeSingle());
 if(!isCurrent())return null;
 if(!memberPermissions(member).member)return {member:null,images:[],edits:[]};
 const readAll=async table=>{const rows=[];for(let start=0;;start+=500){const part=unwrap(await client.from(table).select('*').order(table==='visu_shared_images'?'id':'image_key').range(start,start+499));if(!isCurrent())return null;rows.push(...part);if(part.length<500)return rows;}};
 const images=await readAll('visu_shared_images');if(!images)return null;
 const edits=await readAll('visu_image_edits');if(!edits)return null;
 const old=new Map((previous.images||[]).map(row=>[row.id,row]));
 for(const image of images){
  if(image.external_url){image.url=image.external_url;continue;}
  const cached=old.get(image.id);
  if(cached?.url&&cached.urlExpires>Date.now()+300000){image.url=cached.url;image.urlExpires=cached.urlExpires;continue;}
  const signed=unwrap(await client.storage.from('visu-user-images').createSignedUrl(image.object_path,3600));
  if(!isCurrent())return null;image.url=signed.signedUrl;image.urlExpires=Date.now()+3500000;
 }
 return isCurrent()?{member,images,edits}:null;
}
export class Community {
 constructor({getClient,getIdentity,read,write,changed,notify}){Object.assign(this,{getClient,getIdentity,read,write,changed,notify});this.state={member:null,images:[],edits:[]};this.serial=0;}
 get permissions(){return memberPermissions(this.state.member);}
 get personal(){return this.getIdentity().account==='guest';}
 can(cap){return this.personal?['add','edit','review'].includes(cap):this.permissions[cap];}
 imageRows(itemId){return this.state.images.filter(row=>row.item_id===itemId).map(row=>({key:'shared:'+row.id,url:row.url,page:row.source_url,description:row.description,author:row.author,license:row.license,reference:row.reference,status:'pending',sharedId:row.id}));}
 imageEdit(itemId,key){return this.state.edits.find(row=>row.item_id===itemId&&row.image_key===key);}
 async activate(){const serial=++this.serial,id=this.getIdentity().account;this.state={member:null,images:[],edits:[]};if(id!=='guest'){const saved=await this.read('community:'+id,null);if(serial===this.serial&&id===this.getIdentity().account&&saved)this.state=saved;}this.renderPermissions();}
 async refresh(){
  if(this.personal||!this.getClient())return;
  const identity=this.getIdentity(),serial=++this.serial,isCurrent=()=>serial===this.serial&&identity.account===this.getIdentity().account&&identity.revision===this.getIdentity().revision;
  const result=await fetchCommunity(this.getClient(),{userId:identity.account,isCurrent,previous:this.state});if(!result||!isCurrent())return;
  const changed=JSON.stringify(result)!==JSON.stringify(this.state);this.state=result;await this.write('community:'+identity.account,result);if(!isCurrent())return;this.renderPermissions();if(changed)this.changed();
 }
 require(cap){if(this.personal)throw Error('Accede a una cuenta autorizada para usar las aportaciones compartidas.');if(!navigator.onLine)throw Error('Esta aportación compartida necesita conexión. No se ha enviado.');if(!this.permissions[cap])throw Error('Tu cuenta no tiene permiso para esta acción.');return this.getIdentity().account;}
 async rpc(name,args,cap){const actor=this.require(cap);unwrap(await this.getClient().rpc('visu_dispatch',{p_actor:actor,p_action:name,p_payload:args}));}
 async setStatus(itemId,key,status){await this.rpc('visu_set_image_status',{p_item:itemId,p_key:key,p_status:status},'review');await this.refresh();}
 async edit(itemId,key,metadata){await this.rpc('visu_edit_image_metadata',{p_item:itemId,p_key:key,p_metadata:metadata},'edit');await this.refresh();}
 async addImages(itemId,images){
  const userId=this.require('add');let completed=0;
  try{for(const image of images){
   if(userId!==this.getIdentity().account)throw Error('La cuenta ha cambiado; se ha detenido el envío.');
   const payload={reference:image.reference,source_url:image.page,license:image.license,description:image.description||''};
   if(image.url.startsWith('data:')){
    const blob=await (await fetch(image.url)).blob();const extension=({'image/jpeg':'jpg','image/png':'png','image/webp':'webp'})[blob.type];if(!extension||blob.size>15728640)throw Error('La imagen debe ser JPG, PNG o WebP y ocupar como máximo 15 MB.');
    if(userId!==this.getIdentity().account)throw Error('La cuenta ha cambiado; se ha detenido el envío.');
    payload.object_path=userId+'/'+crypto.randomUUID()+'.'+extension;
    unwrap(await this.getClient().storage.from('visu-user-images').upload(payload.object_path,blob,{contentType:blob.type,upsert:false}));
   }else payload.external_url=image.url;
   if(userId!==this.getIdentity().account)throw Error('La cuenta ha cambiado; se ha detenido el envío.');
   await this.rpc('visu_add_image',{p_item:itemId,p_image:payload},'add');completed++;
  }}catch(error){error.message=completed+' de '+images.length+' imágenes añadidas. '+error.message;throw error;}
  finally{await this.refresh();}
 }
 renderPermissions(){
  const node=document.querySelector('#community-status');if(!node)return;
  const p=this.permissions;node.textContent=this.personal?'Modo local: tus revisiones y fotos son personales. Accede para ver y publicar aportaciones compartidas.':!p.member?'Esta cuenta no tiene una autorización vigente para las aportaciones compartidas.':'Aportaciones compartidas · '+['add','edit','review','comment'].map((cap,i)=>(['Añadir fotos','Editar datos','Aprobar / rechazar','Comentar'][i])+': '+(p[cap]?'sí':'no')).join(' · ');
  const panel=document.querySelector('#member-admin');if(panel)panel.hidden=!p.admin;
 }
 async mountComments(container,itemId){
  if(!container)return;const account=this.getIdentity().account,revision=this.getIdentity().revision,token=crypto.randomUUID();container.dataset.request=token;
  const current=()=>container.isConnected&&container.dataset.request===token&&account===this.getIdentity().account&&revision===this.getIdentity().revision;
  container.innerHTML='<h3>Comentarios</h3>';
  if(!this.permissions.member){container.insertAdjacentHTML('beforeend','<p class="help">Accede con una cuenta autorizada para ver los comentarios compartidos.</p>');return;}
  if(!navigator.onLine){container.insertAdjacentHTML('beforeend','<p class="help">Conéctate para consultar y publicar comentarios. No se han enviado cambios.</p>');return;}
  try{
   const rows=unwrap(await this.getClient().from('visu_comments').select('*').eq('item_id',itemId).eq('removed',false).order('created_at',{ascending:false}).limit(51));if(!current())return;
   container.innerHTML='<h3>Comentarios</h3><p class="help">Compartidos con las cuentas autorizadas. Se muestran después de resolver, nunca durante la pregunta.</p>'+
    (rows.length?rows.slice(0,50).map(row=>'<article class="comment" data-comment="'+escape(row.id)+'"><p><strong>'+escape(row.author_name)+'</strong> · <time>'+escape(new Date(row.created_at).toLocaleString())+'</time></p><p class="comment-body">'+escape(row.body)+'</p>'+((row.author_id===account||this.permissions.admin)?'<div class="actions">'+(row.author_id===account?'<button class="text-button" data-comment-action="edit">Editar</button>':'')+'<button class="text-button" data-comment-action="remove">Retirar</button></div>':'')+'</article>').join(''):'<p>Todavía no hay comentarios para esta entrada.</p>')+
    (rows.length>50?'<p class="help">Se muestran los 50 comentarios más recientes.</p>':'')+
    (this.permissions.comment?'<form class="comment-form"><label>Tu comentario<textarea name="body" maxlength="2000" rows="3" required></textarea></label><input name="comment-id" type="hidden"><button class="primary-button" type="submit">Publicar comentario</button><p class="help comment-result" role="status"></p></form>':'<p class="help">Tu cuenta puede leer los comentarios, pero no publicarlos.</p>');
   const form=container.querySelector('form');
   if(form){const draft=await this.read('comment-draft:'+account+':'+itemId,'');if(!current())return;form.elements.body.value=draft;form.elements.body.oninput=()=>{void this.write('comment-draft:'+account+':'+itemId,form.elements.body.value);};
    form.onsubmit=async event=>{event.preventDefault();const button=form.querySelector('button');button.disabled=true;try{if(!current())return;await this.rpc('visu_write_comment',{p_item:itemId,p_body:form.elements.body.value,p_id:form.elements['comment-id'].value||null,p_removed:false},'comment');await this.write('comment-draft:'+account+':'+itemId,'');if(current())await this.mountComments(container,itemId);}catch(error){if(current())form.querySelector('.comment-result').textContent='No se ha publicado: '+error.message;}finally{button.disabled=false;}};
   }
   container.querySelectorAll('[data-comment-action]').forEach(button=>button.onclick=async()=>{const row=rows.find(r=>r.id===button.closest('[data-comment]').dataset.comment);try{if(!current())return;if(button.dataset.commentAction==='edit'){form.elements.body.value=row.body;form.elements['comment-id'].value=row.id;form.querySelector('button').textContent='Guardar comentario';form.elements.body.focus();}else{await this.rpc('visu_write_comment',{p_item:itemId,p_body:'',p_id:row.id,p_removed:true},'comment');if(current())await this.mountComments(container,itemId);}}catch(error){this.notify(error.message);}});
  }catch(error){if(current())container.innerHTML='<h3>Comentarios</h3><p class="help">No se pudieron cargar: '+escape(error.message)+'</p>';}
 }
 async renderAdmin(){
  const list=document.querySelector('#member-list');if(!list||!this.permissions.admin)return;
  try{this.require('admin');const account=this.getIdentity().account,rows=unwrap(await this.getClient().rpc('visu_list_members'));if(account!==this.getIdentity().account||!this.permissions.admin)return;
   list.innerHTML=rows.map(row=>'<article class="member-row"><strong>'+escape(row.display_name)+'</strong><p>'+escape(row.email)+'</p><p class="help">'+(row.is_admin?'Administrador':(row.enabled?'Autorizado':'Desactivado')+' · Añadir: '+(row.can_add_images?'sí':'no')+' · Editar: '+(row.can_edit_images?'sí':'no')+' · Aprobar: '+(row.can_review_images?'sí':'no')+' · Comentar: '+(row.can_comment?'sí':'no'))+'</p>'+(!row.is_admin?'<button type="button" data-member="'+escape(row.user_id)+'" class="secondary-button">Cambiar permisos</button>':'')+'</article>').join('');
   list.querySelectorAll('[data-member]').forEach(button=>button.onclick=()=>{const row=rows.find(r=>r.user_id===button.dataset.member),form=document.querySelector('#member-form');form.elements.email.value=row.email;form.elements.name.value=row.display_name;for(const [field,key] of [['enabled','enabled'],['add','can_add_images'],['edit','can_edit_images'],['review','can_review_images'],['comment','can_comment']])form.elements[field].checked=row[key];form.scrollIntoView({block:'center',behavior:'smooth'});});
  }catch(error){list.textContent=error.message;}
 }
 bindAdmin(){
  document.querySelector('#member-refresh').onclick=()=>this.renderAdmin();
  const form=document.querySelector('#member-form');form.onsubmit=async event=>{event.preventDefault();const button=form.querySelector('button');button.disabled=true;try{await this.rpc('visu_set_member',{p_email:form.elements.email.value.trim(),p_name:form.elements.name.value.trim(),p_enabled:form.elements.enabled.checked,p_add:form.elements.add.checked,p_edit:form.elements.edit.checked,p_review:form.elements.review.checked,p_comment:form.elements.comment.checked},'admin');form.querySelector('[role=status]').textContent='Permisos guardados. No se ha enviado ningún correo.';await this.renderAdmin();}catch(error){form.querySelector('[role=status]').textContent='No se han guardado: '+error.message;}finally{button.disabled=false;}};
 }
}
