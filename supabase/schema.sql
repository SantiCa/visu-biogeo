-- Supabase > SQL Editor. Idempotent; keeps existing progress.
-- Membership is granted only by the project owner in SQL Editor.
-- Sharing the public project key does not grant membership or access to any rows.
create table if not exists public.visu_members (
 user_id uuid primary key references auth.users(id) on delete cascade,
 enabled boolean not null default true,
 created_at timestamptz not null default now()
);
alter table public.visu_members enable row level security;
revoke all on table public.visu_members from public,anon,authenticated;
grant select on table public.visu_members to authenticated;
drop policy if exists "Users see only their own membership" on public.visu_members;
create policy "Users see only their own membership" on public.visu_members
 for select to authenticated using ((select auth.uid())=user_id);

create table if not exists public.study_states (
 user_id uuid not null references auth.users(id) on delete cascade,
 item_id text not null, state jsonb not null,
 updated_at timestamptz not null default now(),
 primary key(user_id,item_id)
);
alter table public.study_states enable row level security;
revoke all on table public.study_states from public,anon,authenticated;
drop policy if exists "Users read their own study state" on public.study_states;
drop policy if exists "Users insert their own study state" on public.study_states;
drop policy if exists "Users update their own study state" on public.study_states;
create policy "Users read their own study state" on public.study_states for select to authenticated
 using ((select auth.uid())=user_id and exists(select 1 from public.visu_members m where m.user_id=(select auth.uid()) and m.enabled));
create policy "Users insert their own study state" on public.study_states for insert to authenticated
 with check ((select auth.uid())=user_id and exists(select 1 from public.visu_members m where m.user_id=(select auth.uid()) and m.enabled));
create policy "Users update their own study state" on public.study_states for update to authenticated
 using ((select auth.uid())=user_id and exists(select 1 from public.visu_members m where m.user_id=(select auth.uid()) and m.enabled))
 with check ((select auth.uid())=user_id and exists(select 1 from public.visu_members m where m.user_id=(select auth.uid()) and m.enabled));
grant select,insert,update on public.study_states to authenticated;

-- Per-entry last-write-wins for priorities and image decisions.
create or replace function public.visu_merge_map(old_map jsonb,new_map jsonb)
returns jsonb language sql immutable set search_path=public as $$
 select coalesce(jsonb_object_agg(key,value),'{}'::jsonb) from (
  select distinct on(key) key,value from (
   select key,value,0 as tie from jsonb_each(coalesce(old_map,'{}'::jsonb))
   union all
   select key,value,1 as tie from jsonb_each(coalesce(new_map,'{}'::jsonb))
  ) entries order by key,coalesce((value->>'updatedAt')::numeric,0) desc,tie asc
 ) latest;
$$;
-- SECURITY INVOKER: row policies remain in effect; never use service_role in browser.
create or replace function public.merge_study_states(incoming jsonb)
returns void language plpgsql security invoker set search_path=public as $$
declare entry jsonb;
begin
 if auth.uid() is null then raise exception 'Authentication required'; end if;
 if not exists(select 1 from public.visu_members where user_id=auth.uid() and enabled) then raise exception 'Account not authorized for Visu'; end if;
 if jsonb_typeof(incoming) is distinct from 'array' then raise exception 'Expected array'; end if;
 if jsonb_array_length(incoming)>100 then raise exception 'Maximum batch size is 100'; end if;
 for entry in select * from jsonb_array_elements(incoming) loop
  if (entry->>'user_id')::uuid is distinct from auth.uid() then raise exception 'Wrong user'; end if;
  if jsonb_typeof(entry->'state') is distinct from 'object' or length(entry->>'item_id') not between 1 and 250 then raise exception 'Invalid state'; end if;
  insert into public.study_states(user_id,item_id,state)
  values(auth.uid(),entry->>'item_id',entry->'state')
  on conflict(user_id,item_id) do update set
   state=case when excluded.item_id='__preferences_v3' then
    jsonb_build_object(
     'overrides',public.visu_merge_map(study_states.state->'overrides',excluded.state->'overrides'),
     'decisions',public.visu_merge_map(study_states.state->'decisions',excluded.state->'decisions'),
     'preferences',public.visu_merge_map(study_states.state->'preferences',excluded.state->'preferences'))
   when coalesce((excluded.state->>'lastReviewed')::numeric,0)>coalesce((study_states.state->>'lastReviewed')::numeric,0) then excluded.state
   else study_states.state end,
   updated_at=now();
 end loop;
end;
$$;
revoke all on function public.merge_study_states(jsonb) from public;
grant execute on function public.merge_study_states(jsonb) to authenticated;
revoke all on function public.visu_merge_map(jsonb,jsonb) from public,anon;
grant execute on function public.visu_merge_map(jsonb,jsonb) to authenticated;

-- After inviting the app account in Authentication > Users, grant that UUID:
-- insert into public.visu_members(user_id) values ('AUTH-USER-UUID')
-- on conflict(user_id) do update set enabled=true;
-- Disable public signups in Authentication > Sign In / Providers.
