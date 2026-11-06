End-to-end test (Python + Playwright) with a simulated Supabase server (mock.py). 124 checks (e2e.py 67, e2e2.py 57): login, billing maths, PDF, payments, History,
Settings, two-device and two-person team sync, outsider blocked, offline, script-injection attempts, sign-out, India time zone, mobile layout.
Run: serve the app folder on http://localhost:8123, then `python3 e2e.py`.
Database rules were tested separately on real PostgreSQL (owner / other user / not logged in).

e2e2.py covers the invoice redesign: HSN slider, CGST/SGST/IGST, titles, layout, signature per bill, PDF and print output (rendered and checked), History tabs/counts/search, colours.

e2e3.py: phone paths (Android/iOS native share and save, browser share sheet) with emulated Capacitor. electron_test.py: runs inside the real packaged Linux desktop app (Electron) under a virtual screen.
e2e4.py: every cloud-sync situation (older private database, login not in team, tables missing, expired login, offline). electron_legacy.py / electron_refresh.py: the desktop app against an older database and across token renewal.
Totals at release: e2e 67 + e2e2 57 + e2e3 12 + e2e4 20 + electron 6 + electron_legacy 4 = 166 checks.


## Security audit tests (added)
- `e2e5_audit.py` - 22 checks: money maths, payments, backup-restore abuse, malformed cloud data, framing/clickjacking, CSP, focus-sync chatter, and a randomized click-everything monkey test.
- `db/` - PostgreSQL attack tests for `backend/supabase.sql` (`setup_env.sql` simulates Supabase, `attack.sql` runs as anonymous / outsider / team member, `old_schema.sql` tests upgrade). Run with a local PostgreSQL 16.
- `gs/gs_test.js` - `node gs/gs_test.js ../backend/Code.gs` attacks the email script inside a fake Apps Script sandbox (28 checks).

## Print and logo tests (added)
- `e2e6_print.py` - 21 checks: Android direct print + fallbacks, desktop/browser print, print-media render (1 page A4), logo tagline spacing.
- `logo/fix_logo.py` - the script used to repair the R/O overlap in the logo tagline (kept for reference).
- Android plugin logic was compile-checked against stand-in Android classes; a real phone is the final test.
