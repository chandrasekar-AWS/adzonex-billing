-- Ad ZoneX Billing: Supabase schema (shared team workspace).
-- Run in Supabase > SQL Editor. Safe to run again. Works for a new project AND upgrades the older "private per login" version
-- without losing bills.
--
-- Everyone in the `team` table shares ALL bills and settings. A login that is not in `team` sees nothing.
--
-- Security notes (version 2):
--  * Re-running this script NEVER re-adds people to the team. Logins are added to the team automatically only the very
--    first time (when the team table is empty). Anyone you removed stays removed.
--  * The app never deletes bills (it only marks them "deleted"), so the database does not allow DELETE or TRUNCATE
--    from the app either. A stolen login can therefore change bills but cannot wipe them all in one go.
--  * Rows are checked: bill id format, JSON object, size limit, and "saved by" must be the person who is logged in.

-- 1. Team ---------------------------------------------------------------------
create table if not exists public.team (
  user_id uuid primary key references auth.users(id) on delete cascade,
  email   text
);
alter table public.team add column if not exists role text not null default 'admin';   -- 'admin' = everything, 'biller' = can only make bills
alter table public.team drop constraint if exists team_role_ok;
alter table public.team add constraint team_role_ok check (role in ('admin','biller'));
alter table public.team enable row level security;           -- no policies: nobody can read/change it through the API
revoke all on public.team from anon, authenticated;

create or replace function public.is_team_member() returns boolean
language sql stable security definer set search_path = ''
as $$ select exists (select 1 from public.team where user_id = (select auth.uid())) $$;
revoke all on function public.is_team_member() from public, anon;
grant execute on function public.is_team_member() to authenticated;

create or replace function public.my_role() returns text
language sql stable security definer set search_path = ''
as $$ select role from public.team where user_id = (select auth.uid()) $$;
revoke all on function public.my_role() from public, anon;
grant execute on function public.my_role() to authenticated;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = ''
as $$ select exists (select 1 from public.team where user_id = (select auth.uid()) and role = 'admin') $$;
revoke all on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated;

-- 2. Bills (one row per estimate / bill) ---------------------------------------
create table if not exists public.docs (
  id       text primary key,
  user_id  uuid default auth.uid() references auth.users(id) on delete set null,   -- who saved it last
  updated  bigint not null default 0,
  data     jsonb  not null,                                  -- the whole estimate / bill
  est_no   text, bill_no text, customer text,
  status   text                                              -- estimate | bill | deleted
);

-- upgrade from the older private layout (primary key was user_id + id)
do $$ begin
  if (select count(*) from information_schema.key_column_usage
        where table_schema='public' and table_name='docs' and constraint_name='docs_pkey') = 2 then
    delete from public.docs a using public.docs b
      where a.id = b.id and (a.updated, a.user_id::text) < (b.updated, b.user_id::text);   -- same id twice: keep the newest
    alter table public.docs drop constraint docs_pkey;
    alter table public.docs add primary key (id);
    alter table public.docs alter column user_id drop not null;
    alter table public.docs drop constraint if exists docs_user_id_fkey;
    alter table public.docs add constraint docs_user_id_fkey foreign key (user_id) references auth.users(id) on delete set null;
  end if;
end $$;

-- 3. Business settings (exactly one shared row) -------------------------------
create table if not exists public.app_settings (
  id      text primary key default 'main',
  user_id uuid default auth.uid() references auth.users(id) on delete set null,
  updated bigint not null default 0,
  data    jsonb  not null
);

do $$ begin
  if not exists (select 1 from information_schema.columns
                  where table_schema='public' and table_name='app_settings' and column_name='id') then
    delete from public.app_settings a using public.app_settings b
      where (a.updated, a.user_id::text) < (b.updated, b.user_id::text);                   -- keep only the newest settings row
    alter table public.app_settings drop constraint app_settings_pkey;
    alter table public.app_settings add column id text not null default 'main';
    alter table public.app_settings add primary key (id);
    alter table public.app_settings alter column user_id drop not null;
    alter table public.app_settings drop constraint if exists app_settings_user_id_fkey;
    alter table public.app_settings add constraint app_settings_user_id_fkey foreign key (user_id) references auth.users(id) on delete set null;
  end if;
end $$;

drop index if exists public.docs_user_updated;
create index if not exists docs_updated on public.docs (updated desc);

-- 4. Security: only team members can read or write ------------------------------
alter table public.docs         enable row level security;
alter table public.app_settings enable row level security;
revoke all on public.docs, public.app_settings from anon;
-- RLS does not cover TRUNCATE / REFERENCES / TRIGGER, and DELETE is not needed by the app: take them away from logins.
revoke truncate, references, trigger, delete on public.docs, public.app_settings from authenticated;

-- data checks (NOT VALID = applies to every new/changed row, does not fail on old rows)
alter table public.docs drop constraint if exists docs_sane;
alter table public.docs add constraint docs_sane check (
  id ~ '^[A-Za-z0-9_-]{1,64}$' and jsonb_typeof(data) = 'object' and pg_column_size(data) <= 4000000
  and (status is null or status in ('estimate','bill','deleted'))) not valid;
alter table public.app_settings drop constraint if exists settings_sane;
alter table public.app_settings add constraint settings_sane check (
  id = 'main' and jsonb_typeof(data) = 'object' and pg_column_size(data) <= 4000000) not valid;

drop policy if exists "own docs" on public.docs;
drop policy if exists "team docs" on public.docs;
drop policy if exists "team docs read" on public.docs;
drop policy if exists "team docs insert" on public.docs;
drop policy if exists "team docs update" on public.docs;
create policy "team docs read"   on public.docs for select to authenticated using (public.is_team_member());
create policy "team docs insert" on public.docs for insert to authenticated
  with check (public.is_team_member() and user_id = (select auth.uid()));
-- a 'biller' can only change bills that they saved themselves; an 'admin' can change every bill
create policy "team docs update" on public.docs for update to authenticated
  using (public.is_team_member() and (public.is_admin() or user_id = (select auth.uid())))
  with check (public.is_team_member() and user_id = (select auth.uid()));

drop policy if exists "own settings" on public.app_settings;
drop policy if exists "team settings" on public.app_settings;
drop policy if exists "team settings read" on public.app_settings;
drop policy if exists "team settings insert" on public.app_settings;
drop policy if exists "team settings update" on public.app_settings;
create policy "team settings read"   on public.app_settings for select to authenticated using (public.is_team_member());
-- business settings (bank details, expenses, calendar, services...) can only be changed by an 'admin'
create policy "team settings insert" on public.app_settings for insert to authenticated
  with check (public.is_admin() and user_id = (select auth.uid()));
create policy "team settings update" on public.app_settings for update to authenticated
  using (public.is_admin()) with check (public.is_admin() and user_id = (select auth.uid()));

-- 5. First install only: put the logins that exist right now into the team --------
-- This runs ONLY while the team table is empty (first install, or upgrade from the older private version).
-- Later runs never add anybody, so removing a person from the team is permanent.
-- New logins you add later are NOT added automatically (so a stranger can never join by accident). To add one:
--   insert into public.team (user_id, email) select id, email from auth.users where email = 'friend@example.com' on conflict do nothing;
do $$ begin
  if not exists (select 1 from public.team) then
    insert into public.team (user_id, email) select id, email from auth.users on conflict do nothing;
    raise notice 'Team was empty: added every existing login. Check the list below and remove anyone who should not be there.';
  end if;
end $$;

-- Make a login "bill maker only" (can create bills, cannot open History, Calendar, Expenses or Settings):
--   update public.team set role = 'biller' where email = 'friend@example.com';
-- Make it a full admin again:
--   update public.team set role = 'admin' where email = 'friend@example.com';

-- Review this list after every run. These are the only people who can see or change bills:
select email as "TEAM MEMBERS (should be only people you trust)", role from public.team order by email;
