\set ON_ERROR_STOP off
\pset format unaligned
\pset tuples_only on
-- seed as superuser, outsider is NOT in team (added later, like a stranger who got a login)
delete from public.team where email='outsider@adzonex.in';
insert into public.docs(id,user_id,updated,data,status) values ('seed1','11111111-1111-1111-1111-111111111111',1,'{"cust":"Secret Co"}','bill') on conflict do nothing;
insert into public.app_settings(id,updated,data) values ('main',1,'{"name":"Biz"}') on conflict do nothing;

create or replace procedure t(name text, ok boolean) language plpgsql as $$ begin raise notice '% : %', case when ok then 'PASS' else 'FAIL' end, name; end $$;
grant execute on procedure t(text,boolean) to anon, authenticated;

-- ===== ANON (not logged in)
set role anon;
do $$ declare n int; begin
  begin select count(*) into n from public.docs; call t('anon cannot read docs (got error or 0)', n=0); exception when others then call t('anon cannot read docs (permission denied)', true); end;
  begin insert into public.docs(id,updated,data) values('evil',1,'{}'); call t('anon cannot insert docs', false); exception when others then call t('anon cannot insert docs', true); end;
  begin select count(*) into n from public.team; call t('anon cannot read team', false); exception when others then call t('anon cannot read team', true); end;
  begin perform public.is_team_member(); call t('anon cannot call is_team_member', false); exception when others then call t('anon cannot call is_team_member', true); end;
  begin select count(*) into n from public.app_settings; call t('anon cannot read settings', n=0); exception when others then call t('anon cannot read settings', true); end;
end $$;
reset role;

-- ===== OUTSIDER (valid login, NOT in team)
set role authenticated; set request.jwt.claim.sub='33333333-3333-3333-3333-333333333333';
do $$ declare n int; begin
  select count(*) into n from public.docs; call t('outsider sees 0 docs', n=0);
  select count(*) into n from public.app_settings; call t('outsider sees 0 settings', n=0);
  begin insert into public.docs(id,updated,data) values('evil',1,'{}'); call t('outsider cannot insert doc', false); exception when others then call t('outsider cannot insert doc', true); end;
  begin update public.docs set data='{"hacked":1}' where id='seed1'; get diagnostics n = row_count; call t('outsider cannot update doc', n=0); exception when others then call t('outsider cannot update doc', true); end;
  begin delete from public.docs where id='seed1'; get diagnostics n = row_count; call t('outsider cannot delete doc', n=0); exception when others then call t('outsider cannot delete doc', true); end;
  begin insert into public.team(user_id,email) values('33333333-3333-3333-3333-333333333333','outsider@adzonex.in'); call t('outsider cannot add self to team', false); exception when others then call t('outsider cannot add self to team', true); end;
  begin update public.app_settings set data='{"hacked":1}'; get diagnostics n = row_count; call t('outsider cannot change settings', n=0); exception when others then call t('outsider cannot change settings', true); end;
  call t('outsider is_team_member() = false', public.is_team_member()=false);
end $$;
reset role;

-- ===== TEAM MEMBER (friend)
set role authenticated; set request.jwt.claim.sub='22222222-2222-2222-2222-222222222222';
do $$ declare n int; begin
  select count(*) into n from public.docs; call t('team member sees docs', n=1);
  begin insert into public.docs(id,updated,data,status) values('f1',2,'{"cust":"X"}','estimate'); call t('team member can create doc', true); exception when others then call t('team member can create doc', false); end;
  begin update public.docs set updated=3 where id='f1'; get diagnostics n=row_count; call t('team member can update doc', n=1); exception when others then call t('team member can update doc', false); end;
  begin insert into public.docs(id,user_id,updated,data) values('f1','22222222-2222-2222-2222-222222222222',5,'{"cust":"Y"}') on conflict (id) do update set user_id=excluded.user_id, updated=excluded.updated, data=excluded.data; call t('upsert (app push path) works', true); exception when others then call t('upsert (app push path) works', false); end;
  begin insert into public.app_settings(id,user_id,updated,data) values('main','22222222-2222-2222-2222-222222222222',9,'{"name":"B2"}') on conflict (id) do update set user_id=excluded.user_id,updated=excluded.updated,data=excluded.data; call t('team can upsert settings', true); exception when others then call t('team can upsert settings', false); end;
  begin insert into public.team(user_id,email) values('33333333-3333-3333-3333-333333333333','x'); call t('team member cannot edit team table', false); exception when others then call t('team member cannot edit team table', true); end;
  begin select count(*) into n from public.team; call t('team member cannot read team table', false); exception when others then call t('team member cannot read team table', true); end;
  begin truncate public.docs; call t('team member cannot TRUNCATE docs', false); exception when others then call t('team member cannot TRUNCATE docs', true); end;
end $$;
reset role;
insert into public.docs(id,user_id,updated,data,status) values ('seed2','11111111-1111-1111-1111-111111111111',1,'{"cust":"Keep me"}','bill') on conflict do nothing;
set role authenticated; set request.jwt.claim.sub='22222222-2222-2222-2222-222222222222';
do $$ declare n int; begin
  begin delete from public.docs where id='seed2'; get diagnostics n=row_count; call t('team session cannot DELETE a bill (0 rows)', n=0); exception when others then call t('team session cannot DELETE a bill (permission denied)', true); end;
end $$;
reset role;
select 'seed2 still present: '||count(*) from public.docs where id='seed2';
set role authenticated; set request.jwt.claim.sub='22222222-2222-2222-2222-222222222222';
do $$ declare n int; begin
  begin insert into public.docs(id,user_id,updated,data) values('spoof',  '11111111-1111-1111-1111-111111111111',1,'{}'); call t('cannot save a bill as another person (user_id spoof)', false); exception when others then call t('cannot save a bill as another person (user_id spoof)', true); end;
  begin insert into public.docs(id,updated,data) values('has space',1,'{}'); call t('bad bill id rejected', false); exception when others then call t('bad bill id rejected', true); end;
  begin insert into public.docs(id,updated,data) values('arr',1,'[1,2]'); call t('non-object json rejected', false); exception when others then call t('non-object json rejected', true); end;
  begin insert into public.docs(id,updated,data,status) values('st',1,'{}','hacked'); call t('unknown status rejected', false); exception when others then call t('unknown status rejected', true); end;
  begin insert into public.app_settings(id,updated,data) values('second',1,'{}'); call t('second settings row rejected', false); exception when others then call t('second settings row rejected', true); end;
  begin insert into public.docs(id,updated,data) values('big',1,jsonb_build_object('x',repeat('a',5000000))); call t('5 MB bill rejected', false); exception when others then call t('5 MB bill rejected', true); end;
end $$;
-- the old "mass delete" probe, now meaningful
do $$ declare n int; begin
  begin delete from public.docs; get diagnostics n=row_count; call t('team session cannot mass-DELETE all bills', n=0); exception when others then call t('team session cannot mass-DELETE all bills', true); end;
end $$;
reset role;
select 'docs remaining after tests: '||count(*) from public.docs;
