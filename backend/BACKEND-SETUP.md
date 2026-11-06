# Ad ZoneX Billing: Backend (Supabase)

Already connected in the app (app/app.js, top): Project URL https://krfjrasoihxhxnjskrhi.supabase.co and the publishable key.
The publishable key is safe in the browser. NEVER put the secret key or service_role key in the app, in GitHub, or in a chat.

## How sharing works
Everyone listed in the `team` table shares ALL bills and ONE set of business settings. A login that is not in the team sees nothing and cannot save anything.
New logins are NOT added to the team automatically, so a stranger can never join by accident.

## Part 1: Database, logins and team (required)
1. Supabase dashboard > SQL Editor > New query. Paste all of `supabase.sql`, click Run ("Success. No rows returned").
   Safe to run again (it never re-adds anyone to the team, so removed people stay removed). The last line it prints is the list of team members: check it every time. If you used an older version, it upgrades it and keeps your bills (if two logins had the same bill number, the newest copy is kept).
2. Authentication > Users > Add user > Create new user: email + a long password (14+ characters), tick "Auto Confirm User". Do this for yourself and for each person who needs access.
3. Authentication > Sign In / Providers > Email: turn OFF "Allow new users to sign up".
4. Authentication > URL Configuration: Site URL = https://chandrasekar-aws.github.io/adzonex-billing/
5. Open the app > Settings > "Run security check". Every line should show a tick.
6. Adding someone later: create the login (step 2), then run this in SQL Editor with their email:
       insert into public.team (user_id, email) select id, email from auth.users where email = 'friend@example.com' on conflict do nothing;
   Removing someone: delete them from Authentication > Users (their bills stay), or run: delete from public.team where email = 'friend@example.com';

## Part 2: Email for bills (optional)
Skip if you do not email bills. Only the logins you list can send; no secret is stored in the app.
1. Create a Google Sheet > Extensions > Apps Script. Paste all of `Code.gs`.
2. At the top, put your login emails in ALLOWED_EMAILS. Save.
3. Deploy > New deployment > Web app. Execute as: Me. Who has access: Anyone. Deploy, then allow the permissions (it needs to send mail and contact Supabase to check the login).
4. Copy the Web app URL. In the app: Settings > Email > paste the URL > Save settings. (Email settings are per device.)
Updating Code.gs later (for example after this update): paste the new Code.gs, then Deploy > Manage deployments > pencil icon > Version: New version > Deploy. The web app URL stays the same.
The app now attaches its own high-quality PDF to the email (same file as Download PDF).

## Part 3: Security checklist
- Sign-ups off (Part 1, step 3).
- Use strong unique passwords. Optional: Authentication > Multi-Factor.
- Sign out on shared computers (Settings > Sign out removes the local copy).
- Download a backup now and then (Settings > Backup).
- If a secret key is ever shown to anyone: Project Settings > API Keys > create a new secret key and delete the old one.
- Both tables are locked to team members only (tested, see the tests folder).
- The app never deletes bills (it only marks them deleted), so the database does not allow DELETE or TRUNCATE from any login. To permanently remove bills yourself, use the SQL editor (it runs with full rights).
- Email script: paste only the address of YOUR script. The app sends your login token to that address.
- Extra safety in Supabase: keep sign-ups turned OFF, use a long unique password, and keep a monthly Backup (Settings > Backup).

## Good to know
- If two people edit the same bill at the same moment, the later save wins.
- If two people create a new bill at exactly the same time before syncing, they could get the same number. Keep the app open online and this is very rare.

## Old tables
If you ran my very first SQL (settings, items, invoices, invoice_items) they are unused. Remove with:
    drop table if exists invoice_items, invoices, items, settings;

## Roles: full admin and "bill maker only" (new)
1. Open Supabase > SQL Editor, paste everything from `supabase.sql` and click **Run** (safe to run again; your bills are kept).
2. Create the second person's login (Authentication > Users) and add them to the team (Part 1, step 6). Everyone in the team starts as **admin**.
3. Make that person a bill maker only:
   `update public.team set role = 'biller' where email = 'friend@example.com';`
   To give full access back: `update public.team set role = 'admin' where email = 'friend@example.com';`
4. The person signs out and in again. A **bill maker** sees only the Billing page. They can make estimates and invoices, record the advance, print, download PDF and send on WhatsApp for the bills they made. They cannot open History, Calendar, Expenses or Settings, delete a bill, remove a payment, or open bills made by others.
5. The database enforces this too: a bill maker cannot change business settings (bank details, expenses, calendar) or edit another person's bill, even from a hacked page.

Limit to know: a bill maker's phone still downloads the shared settings record (it holds the expense and calendar lists) because the app needs your business name, services and terms from it. The screens are hidden and nothing can be changed, but a technical person could read it through the API. If expenses must be fully secret from that person, tell me and I will move expenses into a separate admin-only table.
