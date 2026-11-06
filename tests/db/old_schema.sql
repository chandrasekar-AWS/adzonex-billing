create table public.docs (
  user_id uuid not null references auth.users(id) on delete cascade,
  id text not null, updated bigint not null default 0, data jsonb not null,
  est_no text, bill_no text, customer text, status text,
  primary key (user_id, id));
create index docs_user_updated on public.docs (user_id, updated desc);
create table public.app_settings (
  user_id uuid primary key references auth.users(id) on delete cascade,
  updated bigint not null default 0, data jsonb not null);
alter table public.docs enable row level security; alter table public.app_settings enable row level security;
create policy "own docs" on public.docs for all to authenticated using (user_id=(select auth.uid())) with check (user_id=(select auth.uid()));
create policy "own settings" on public.app_settings for all to authenticated using (user_id=(select auth.uid())) with check (user_id=(select auth.uid()));
-- data: same bill id saved by two logins (newest must win), plus unique ones
insert into public.docs(user_id,id,updated,data) values
 ('11111111-1111-1111-1111-111111111111','b1',100,'{"v":"owner-old"}'),
 ('22222222-2222-2222-2222-222222222222','b1',200,'{"v":"friend-NEW"}'),
 ('11111111-1111-1111-1111-111111111111','b2',50,'{"v":"only-owner"}'),
 ('22222222-2222-2222-2222-222222222222','b3',60,'{"v":"only-friend"}');
insert into public.app_settings values ('11111111-1111-1111-1111-111111111111',10,'{"name":"old-owner"}'),('22222222-2222-2222-2222-222222222222',20,'{"name":"NEWEST-friend"}');
