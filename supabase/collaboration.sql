-- Run after schema.sql. Keeps personal progress private; contributions are shared.
alter table public.visu_members add column if not exists display_name text not null default 'Estudiante';
alter table public.visu_members add column if not exists is_admin boolean not null default false;
alter table public.visu_members add column if not exists can_add_images boolean not null default false;
alter table public.visu_members add column if not exists can_edit_images boolean not null default false;
alter table public.visu_members add column if not exists can_review_images boolean not null default false;
alter table public.visu_members add column if not exists can_comment boolean not null default true;

create or replace function public.visu_allowed(cap text)
returns boolean language sql stable security definer set search_path=public,pg_temp as $$
 select exists(select 1 from public.visu_members m where m.user_id=auth.uid() and m.enabled and
 (m.is_admin or case cap when 'member' then true when 'add' then m.can_add_images
 when 'edit' then m.can_edit_images when 'review' then m.can_review_images
 when 'comment' then m.can_comment else false end));
$$;
revoke all on function public.visu_allowed(text) from public,anon;
grant execute on function public.visu_allowed(text) to authenticated;

create table if not exists public.visu_shared_images (
 id uuid primary key default gen_random_uuid(), item_id text not null check(length(item_id) between 1 and 250),
 object_path text, external_url text, reference text not null check(length(reference) between 1 and 1000),
 source_url text not null default '', author text not null default '', license text not null default '',
 description text not null default '', created_by uuid not null references auth.users(id),
 created_at timestamptz not null default now(),
 check((object_path is null)<>(external_url is null)),
 check(external_url is null or (external_url ~ '^https?://' and length(external_url)<=4000))
);
create table if not exists public.visu_image_edits (
 item_id text not null check(length(item_id) between 1 and 250), image_key text not null check(length(image_key) between 1 and 5000),
 metadata jsonb not null default '{}'::jsonb check(jsonb_typeof(metadata)='object'),
 status text check(status in ('approved','rejected','pending')),
 updated_by uuid not null references auth.users(id), updated_at timestamptz not null default now(),
 primary key(item_id,image_key)
);
create table if not exists public.visu_comments (
 id uuid primary key default gen_random_uuid(), item_id text not null check(length(item_id) between 1 and 250),
 author_id uuid not null references auth.users(id), author_name text not null,
 body text not null check(length(trim(body)) between 1 and 2000), removed boolean not null default false,
 created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index if not exists visu_comments_item_created on public.visu_comments(item_id,created_at);
alter table public.visu_shared_images enable row level security;
alter table public.visu_image_edits enable row level security;
alter table public.visu_comments enable row level security;
revoke all on public.visu_shared_images,public.visu_image_edits,public.visu_comments from public,anon,authenticated;
grant select on public.visu_shared_images,public.visu_image_edits,public.visu_comments to authenticated;
drop policy if exists "Members read shared images" on public.visu_shared_images;
create policy "Members read shared images" on public.visu_shared_images for select to authenticated using(public.visu_allowed('member'));
drop policy if exists "Members read image edits" on public.visu_image_edits;
create policy "Members read image edits" on public.visu_image_edits for select to authenticated using(public.visu_allowed('member'));
drop policy if exists "Members read comments" on public.visu_comments;
create policy "Members read comments" on public.visu_comments for select to authenticated using(public.visu_allowed('member') and (not removed or author_id=auth.uid() or public.visu_allowed('admin')));

create or replace function public.visu_set_image_status(p_item text,p_key text,p_status text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
begin
 if not public.visu_allowed('review') then raise exception 'No permission to review images'; end if;
 if p_status not in ('approved','rejected','pending') then raise exception 'Invalid status'; end if;
 insert into public.visu_image_edits(item_id,image_key,status,updated_by) values(p_item,p_key,p_status,auth.uid())
 on conflict(item_id,image_key) do update set status=excluded.status,updated_by=auth.uid(),updated_at=now();
end; $$;
create or replace function public.visu_edit_image_metadata(p_item text,p_key text,p_metadata jsonb)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare field text; value jsonb;
begin
 if not public.visu_allowed('edit') then raise exception 'No permission to edit images'; end if;
 if jsonb_typeof(p_metadata) is distinct from 'object' then raise exception 'Invalid metadata'; end if;
 for field,value in select * from jsonb_each(p_metadata) loop
  if field not in ('description','author','license','page','reference') or jsonb_typeof(value)<>'string' or length(value#>>'{}')>4000 then raise exception 'Invalid metadata field'; end if;
  if field='page' and (value#>>'{}')<>'' and (value#>>'{}')!~'^https?://' then raise exception 'Invalid source URL'; end if;
 end loop;
 insert into public.visu_image_edits(item_id,image_key,metadata,updated_by) values(p_item,p_key,p_metadata,auth.uid())
 on conflict(item_id,image_key) do update set metadata=visu_image_edits.metadata||excluded.metadata,updated_by=auth.uid(),updated_at=now();
end; $$;
create or replace function public.visu_add_image(p_item text,p_image jsonb)
returns uuid language plpgsql security definer set search_path=public,pg_temp as $$
declare new_id uuid; object_name text:=nullif(p_image->>'object_path',''); image_url text:=nullif(p_image->>'external_url','');
begin
 if not public.visu_allowed('add') then raise exception 'No permission to add images'; end if;
 if coalesce(p_image->>'source_url','')<>'' and (p_image->>'source_url')!~'^https?://' then raise exception 'Invalid source URL'; end if;
 if object_name is not null and (split_part(object_name,'/',1)<>auth.uid()::text or not exists(select 1 from storage.objects where bucket_id='visu-user-images' and name=object_name)) then raise exception 'Upload your own image first'; end if;
 insert into public.visu_shared_images(item_id,object_path,external_url,reference,source_url,author,license,description,created_by)
 values(p_item,object_name,image_url,left(p_image->>'reference',1000),left(coalesce(p_image->>'source_url',''),4000),left(coalesce(p_image->>'author',''),1000),left(coalesce(p_image->>'license',''),1000),left(coalesce(p_image->>'description',''),4000),auth.uid()) returning id into new_id;
 return new_id;
end; $$;
create or replace function public.visu_write_comment(p_item text,p_body text,p_id uuid default null,p_removed boolean default false)
returns uuid language plpgsql security definer set search_path=public,pg_temp as $$
declare result uuid; own_name text;
begin
 if not public.visu_allowed('comment') then raise exception 'No permission to comment'; end if;
 if p_id is null then
  select display_name into own_name from public.visu_members where user_id=auth.uid();
  insert into public.visu_comments(item_id,author_id,author_name,body) values(p_item,auth.uid(),left(own_name,80),trim(p_body)) returning id into result;
 else
  update public.visu_comments set body=case when p_removed then body else trim(p_body) end,removed=p_removed,updated_at=now()
  where id=p_id and item_id=p_item and (author_id=auth.uid() or (public.visu_allowed('admin') and p_removed)) returning id into result;
  if result is null then raise exception 'Comment not found or not owned'; end if;
 end if;
 return result;
end; $$;
create or replace function public.visu_list_members()
returns table(user_id uuid,email text,display_name text,enabled boolean,is_admin boolean,can_add_images boolean,can_edit_images boolean,can_review_images boolean,can_comment boolean)
language plpgsql security definer set search_path=public,pg_temp as $$
begin
 if not public.visu_allowed('admin') then raise exception 'Administrator required'; end if;
 return query select m.user_id,u.email::text,m.display_name,m.enabled,m.is_admin,m.can_add_images,m.can_edit_images,m.can_review_images,m.can_comment from public.visu_members m join auth.users u on u.id=m.user_id order by u.email;
end; $$;
create or replace function public.visu_set_member(p_email text,p_name text,p_enabled boolean,p_add boolean,p_edit boolean,p_review boolean,p_comment boolean)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare target uuid;
begin
 if not public.visu_allowed('admin') then raise exception 'Administrator required'; end if;
 select id into target from auth.users where lower(email)=lower(trim(p_email));
 if target is null then raise exception 'Primero crea esta cuenta en Authentication > Users de Supabase'; end if;
 if exists(select 1 from public.visu_members where visu_members.user_id=target and is_admin) then raise exception 'Los permisos del administrador solo se cambian desde SQL Editor'; end if;
 if length(trim(p_name)) not between 1 and 80 then raise exception 'Indica un nombre de 1 a 80 caracteres'; end if;
 insert into public.visu_members(user_id,display_name,enabled,can_add_images,can_edit_images,can_review_images,can_comment)
 values(target,trim(p_name),p_enabled,p_add,p_edit,p_review,p_comment)
 on conflict(user_id) do update set display_name=excluded.display_name,enabled=excluded.enabled,can_add_images=excluded.can_add_images,can_edit_images=excluded.can_edit_images,can_review_images=excluded.can_review_images,can_comment=excluded.can_comment;
end; $$;

insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values('visu-user-images','visu-user-images',false,15728640,array['image/jpeg','image/png','image/webp'])
on conflict(id) do update set public=false,file_size_limit=excluded.file_size_limit,allowed_mime_types=excluded.allowed_mime_types;
drop policy if exists "Visu members read private additions" on storage.objects;
create policy "Visu members read private additions" on storage.objects for select to authenticated
using(bucket_id='visu-user-images' and public.visu_allowed('member'));
drop policy if exists "Visu contributors upload their own additions" on storage.objects;
create policy "Visu contributors upload their own additions" on storage.objects for insert to authenticated
with check(bucket_id='visu-user-images' and public.visu_allowed('add') and (storage.foldername(name))[1]=auth.uid()::text);

revoke all on function public.visu_set_image_status(text,text,text),public.visu_edit_image_metadata(text,text,jsonb),public.visu_add_image(text,jsonb),public.visu_write_comment(text,text,uuid,boolean),public.visu_list_members(),public.visu_set_member(text,text,boolean,boolean,boolean,boolean,boolean) from public,anon;
grant execute on function public.visu_set_image_status(text,text,text),public.visu_edit_image_metadata(text,text,jsonb),public.visu_add_image(text,jsonb),public.visu_write_comment(text,text,uuid,boolean),public.visu_list_members(),public.visu_set_member(text,text,boolean,boolean,boolean,boolean,boolean) to authenticated;
-- Bootstrap the existing owner explicitly in SQL Editor; no new member is auto-authorized.

-- Bind each UI mutation to the account that initiated it, even during sign-out.
create or replace function public.visu_dispatch(p_actor uuid,p_action text,p_payload jsonb)
returns jsonb language plpgsql security invoker set search_path=public,pg_temp as $$
declare result uuid;
begin
 if auth.uid() is null or p_actor is distinct from auth.uid() then raise exception 'Account changed; operation cancelled'; end if;
 case p_action
 when 'visu_set_image_status' then perform public.visu_set_image_status(p_payload->>'p_item',p_payload->>'p_key',p_payload->>'p_status');
 when 'visu_edit_image_metadata' then perform public.visu_edit_image_metadata(p_payload->>'p_item',p_payload->>'p_key',p_payload->'p_metadata');
 when 'visu_add_image' then result=public.visu_add_image(p_payload->>'p_item',p_payload->'p_image');
 when 'visu_write_comment' then result=public.visu_write_comment(p_payload->>'p_item',p_payload->>'p_body',(p_payload->>'p_id')::uuid,coalesce((p_payload->>'p_removed')::boolean,false));
 when 'visu_set_member' then perform public.visu_set_member(p_payload->>'p_email',p_payload->>'p_name',(p_payload->>'p_enabled')::boolean,(p_payload->>'p_add')::boolean,(p_payload->>'p_edit')::boolean,(p_payload->>'p_review')::boolean,(p_payload->>'p_comment')::boolean);
 else raise exception 'Unknown operation';
 end case;
 return coalesce(to_jsonb(result),'null'::jsonb);
end; $$;
revoke all on function public.visu_dispatch(uuid,text,jsonb) from public,anon;
grant execute on function public.visu_dispatch(uuid,text,jsonb) to authenticated;
