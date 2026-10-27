-- Run as the project owner. All synthetic users/data are rolled back.
begin;
insert into auth.users(id,aud,role,email,created_at,updated_at) values
 ('00000000-0000-4000-8000-0000000000a1','authenticated','authenticated','visu-test-a@example.invalid',now(),now()),
 ('00000000-0000-4000-8000-0000000000b2','authenticated','authenticated','visu-test-b@example.invalid',now(),now()),
 ('00000000-0000-4000-8000-0000000000c3','authenticated','authenticated','visu-test-c@example.invalid',now(),now());
insert into public.visu_members(user_id) values
 ('00000000-0000-4000-8000-0000000000a1'),('00000000-0000-4000-8000-0000000000b2');
insert into public.study_states(user_id,item_id,state) values
 ('00000000-0000-4000-8000-0000000000a1','test-private-a','{"total":1,"lastReviewed":10}'),
 ('00000000-0000-4000-8000-0000000000b2','test-private-b','{"total":7,"lastReviewed":20}');
set local role authenticated;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000a1","role":"authenticated"}',true);
do $$ declare n integer; blocked boolean; begin
 select count(*) into n from public.study_states;
 if n<>1 then raise exception 'FAIL: user A can see another user'; end if;
 select count(*) into n from public.visu_members;
 if n<>1 then raise exception 'FAIL: membership leaks'; end if;
 blocked=false;
 begin insert into public.study_states(user_id,item_id,state) values('00000000-0000-4000-8000-0000000000b2','cross-user','{}');
 exception when insufficient_privilege then blocked=true; end;
 if not blocked then raise exception 'FAIL: cross-user insert'; end if;
 update public.study_states set state='{}' where user_id='00000000-0000-4000-8000-0000000000b2';
 get diagnostics n=row_count;
 if n<>0 then raise exception 'FAIL: cross-user update'; end if;
 blocked=false;
 begin perform public.merge_study_states('[{"user_id":"00000000-0000-4000-8000-0000000000b2","item_id":"rpc-cross-user","state":{}}]');
 exception when raise_exception then if sqlerrm='Wrong user' then blocked=true; else raise; end if; end;
 if not blocked then raise exception 'FAIL: cross-user RPC'; end if;
 blocked=false;
 begin update public.visu_members set enabled=false where user_id=auth.uid();
 exception when insufficient_privilege then blocked=true; end;
 if not blocked then raise exception 'FAIL: client can edit membership'; end if;
 perform public.merge_study_states('[{"user_id":"00000000-0000-4000-8000-0000000000a1","item_id":"test-private-a","state":{"total":2,"lastReviewed":30}}]');
 if (select (state->>'total')::integer from public.study_states where item_id='test-private-a')<>2 then raise exception 'FAIL: owner cannot merge'; end if;
 perform public.merge_study_states('[{"user_id":"00000000-0000-4000-8000-0000000000a1","item_id":"test-private-a","state":{"total":1,"lastReviewed":10}}]');
 if (select (state->>'total')::integer from public.study_states where item_id='test-private-a')<>2 then raise exception 'FAIL: old device overwrites new progress'; end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000c3","role":"authenticated"}',true);
do $$ declare n integer; blocked boolean; begin
 select count(*) into n from public.study_states;
 if n<>0 then raise exception 'FAIL: unapproved account can read'; end if;
 blocked=false;
 begin perform public.merge_study_states('[{"user_id":"00000000-0000-4000-8000-0000000000c3","item_id":"not-a-member","state":{}}]');
 exception when raise_exception then if sqlerrm='Account not authorized for Visu' then blocked=true; else raise; end if; end;
 if not blocked then raise exception 'FAIL: unapproved account can upload'; end if;
end $$;
reset role;
set local role anon;
select set_config('request.jwt.claims','{}',true);
do $$ declare blocked boolean; begin
 blocked=false;
 begin perform 1 from public.study_states; exception when insufficient_privilege then blocked=true; end;
 if not blocked then raise exception 'FAIL: anonymous access'; end if;
end $$;
reset role;
rollback;
select 'PASS: 11 isolation and merge checks; synthetic data rolled back' as verification;
