-- Synthetic database-only fixtures. No invitations/emails; all changes roll back.
begin;
insert into auth.users(id,aud,role,email,created_at,updated_at)
select ('00000000-0000-4000-8000-0000000000d'||n)::uuid,'authenticated','authenticated','visu-role-'||n||'@example.invalid',now(),now() from generate_series(1,6) n;
insert into public.visu_members(user_id,display_name,is_admin,can_add_images,can_edit_images,can_review_images,can_comment)
select ('00000000-0000-4000-8000-0000000000d'||n)::uuid,'Test '||n,n=1,n=3,n=4,n=5,n<>5 from generate_series(1,5) n;
insert into public.visu_shared_images(id,item_id,external_url,reference,created_by) values
 ('00000000-0000-4000-8000-00000000aa01','__role_test','https://example.invalid/specimen.jpg','Test fixture','00000000-0000-4000-8000-0000000000d1');
set local role authenticated;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d2","role":"authenticated"}',true);
do $$ declare blocked boolean; cid uuid; begin
 if not public.visu_allowed('member') or public.visu_allowed('add') or public.visu_allowed('edit') or public.visu_allowed('review') or public.visu_allowed('admin') then raise exception 'FAIL reader capabilities'; end if;
 if not exists(select 1 from public.visu_shared_images where item_id='__role_test') then raise exception 'FAIL shared read'; end if;
 blocked=false;begin perform public.visu_set_image_status('__role_test','base','approved');exception when raise_exception then if sqlerrm='No permission to review images' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL reader review';end if;
 blocked=false;begin perform public.visu_edit_image_metadata('__role_test','base','{"description":"x"}');exception when raise_exception then if sqlerrm='No permission to edit images' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL reader edit';end if;
 blocked=false;begin perform public.visu_add_image('__role_test','{"external_url":"https://example.invalid/x.jpg","reference":"x"}');exception when raise_exception then if sqlerrm='No permission to add images' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL reader add';end if;
 blocked=false;begin perform public.visu_set_member('visu-role-2@example.invalid','Escalation',true,true,true,true,true);exception when raise_exception then if sqlerrm='Administrator required' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL self escalation';end if;
 blocked=false;begin perform * from public.visu_list_members();exception when raise_exception then if sqlerrm='Administrator required' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL member emails exposed';end if;
 blocked=false;begin update public.visu_members set is_admin=true where user_id=auth.uid();exception when insufficient_privilege then blocked=true;end;if not blocked then raise exception 'FAIL direct membership update';end if;
 cid=public.visu_write_comment('__role_test','Reader comment');
 perform public.visu_write_comment('__role_test','Reader edited',cid);
 if (select body from public.visu_comments where id=cid)<>'Reader edited' then raise exception 'FAIL own comment edit';end if;
 blocked=false;begin insert into public.visu_comments(item_id,author_id,author_name,body) values('__role_test',auth.uid(),'Spoof','x');exception when insufficient_privilege then blocked=true;end;if not blocked then raise exception 'FAIL direct comment spoof';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d3","role":"authenticated"}',true);
do $$ declare blocked boolean; image_id uuid; begin
 image_id=public.visu_add_image('__role_test','{"external_url":"https://example.invalid/new.jpg","reference":"Named source","status":"approved"}');
 if exists(select 1 from public.visu_image_edits where item_id='__role_test' and image_key='__role_test::shared:'||image_id::text and status='approved') then raise exception 'FAIL uploader self approval';end if;
 blocked=false;begin perform public.visu_set_image_status('__role_test','base','approved');exception when raise_exception then if sqlerrm='No permission to review images' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL uploader review';end if;
 blocked=false;begin insert into storage.objects(bucket_id,name) values('visu-user-images','00000000-0000-4000-8000-0000000000d2/hijack.jpg');exception when insufficient_privilege then blocked=true;end;if not blocked then raise exception 'FAIL foreign upload prefix';end if;
 insert into storage.objects(bucket_id,name) values('visu-user-images',auth.uid()::text||'/fixture.jpg');
 perform public.visu_add_image('__role_test',jsonb_build_object('object_path',auth.uid()::text||'/fixture.jpg','reference','Own uploaded image'));
 blocked=false;begin perform public.visu_write_comment('__role_test','Overwrite',(select id from public.visu_comments where author_id='00000000-0000-4000-8000-0000000000d2' limit 1));exception when raise_exception then if sqlerrm='Comment not found or not owned' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL foreign comment edit';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d4","role":"authenticated"}',true);
do $$ declare blocked boolean; begin
 perform public.visu_edit_image_metadata('__role_test','base','{"description":"Verified metadata"}');
 if (select metadata->>'description' from public.visu_image_edits where item_id='__role_test' and image_key='base')<>'Verified metadata' then raise exception 'FAIL editor write';end if;
 blocked=false;begin perform public.visu_edit_image_metadata('__role_test','base','{"status":"approved"}');exception when raise_exception then if sqlerrm='Invalid metadata field' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL metadata bypass';end if;
 blocked=false;begin perform public.visu_set_image_status('__role_test','base','approved');exception when raise_exception then if sqlerrm='No permission to review images' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL editor review';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d5","role":"authenticated"}',true);
do $$ declare blocked boolean; begin
 perform public.visu_set_image_status('__role_test','base','approved');
 if (select status from public.visu_image_edits where item_id='__role_test' and image_key='base')<>'approved' then raise exception 'FAIL reviewer write';end if;
 if (select metadata->>'description' from public.visu_image_edits where item_id='__role_test' and image_key='base')<>'Verified metadata' then raise exception 'FAIL review overwrites metadata';end if;
 blocked=false;begin perform public.visu_write_comment('__role_test','Unauthorized comment');exception when raise_exception then if sqlerrm='No permission to comment' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL comment permission';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d6","role":"authenticated"}',true);
do $$ begin
 if public.visu_allowed('member') or exists(select 1 from public.visu_shared_images) or exists(select 1 from public.visu_image_edits) or exists(select 1 from public.visu_comments) then raise exception 'FAIL nonmember access';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d1","role":"authenticated"}',true);
do $$ declare cid uuid; begin
 if not exists(select 1 from public.visu_list_members() where email='visu-role-2@example.invalid') then raise exception 'FAIL admin list';end if;
 perform public.visu_set_member('visu-role-2@example.invalid','Reader disabled',false,false,false,false,false);
 select id into cid from public.visu_comments where item_id='__role_test' and author_id='00000000-0000-4000-8000-0000000000d2' limit 1;
 perform public.visu_write_comment('__role_test','',cid,true);
 if not (select removed from public.visu_comments where id=cid) then raise exception 'FAIL admin comment moderation';end if;
end $$;
select set_config('request.jwt.claims','{"sub":"00000000-0000-4000-8000-0000000000d2","role":"authenticated"}',true);
do $$ begin if public.visu_allowed('member') or exists(select 1 from public.visu_shared_images) then raise exception 'FAIL revoked access';end if;end $$;
do $$ declare blocked boolean; begin
 blocked=false;begin perform public.visu_dispatch('00000000-0000-4000-8000-0000000000d1','visu_write_comment','{"p_item":"__role_test","p_body":"Wrong account"}');exception when raise_exception then if sqlerrm='Account changed; operation cancelled' then blocked=true;else raise;end if;end;if not blocked then raise exception 'FAIL changed-account dispatcher';end if;
end $$;
reset role;
set local role anon;
do $$ declare blocked boolean; begin
 blocked=false;begin perform 1 from public.visu_comments;exception when insufficient_privilege then blocked=true;end;if not blocked then raise exception 'FAIL anonymous comments';end if;
 blocked=false;begin perform public.visu_set_image_status('__role_test','base','approved');exception when insufficient_privilege then blocked=true;end;if not blocked then raise exception 'FAIL anonymous RPC';end if;
end $$;
reset role;
rollback;
select 'PASS: role separation, storage prefixes, comments, moderation and revocation; synthetic data rolled back' as verification;
