# Security & bug audit: what changed

Result: all 178 browser checks + 6 desktop checks + 29 database attack tests + 28 email-script tests pass.

## Backend
- supabase.sql: re-running no longer re-adds removed people to the team; DELETE/TRUNCATE blocked for logins; bill id/JSON/size/status checks; "saved by" cannot be faked.
- Code.gs: rejects anonymous / wrong-type tokens, malformed addresses, header injection; no internal error text leaked; failed sends do not use the daily allowance.

## App
- Backup restore: no longer replaces the email-script address, keeps bills that exist only on this device, survives malformed files, size-limited.
- All bills and settings from the cloud or a backup are sanitised before use (one bad record can no longer crash every device or inject markup).
- App refuses to display inside another website (clickjacking); CSP adds frame-src 'none'.
- Email-script address must be a real Apps Script address; email addresses validated; auto-email no longer pops alerts.
- Money: negative values ignored, every line rounded to 2 decimals so lines add up to the sub total, Sqm label fixed, overpayment asks for confirmation on the Billing page, cleared date falls back to today.
- Deleted bills can no longer be opened through their old link; unique bill ids; focus-sync de-duplicated; WhatsApp numbers with leading 0; image/backup file checks.
- Service worker now caches the PDF libraries (PDF works offline).

## Desktop / build
- Electron 43.7.9 -> 43.8.3 (fixes the high-severity advisory); npm audit: 0 vulnerabilities.
- Second copy of the app can no longer open a window; DevTools off (set ZX_DEBUG=1 to enable); navigation limited to the app page.
- GitHub Actions pinned to exact commits; Dependabot added; Android WebView debugging explicitly off.

## Not changed (you should know)
- Real security lives in Supabase RLS; the in-app login screen is only a front door. Bills are stored unencrypted in this device's browser storage (anyone using your unlocked device can read them).
- GitHub Pages cannot send X-Frame-Options; the in-app frame check covers it.
- Two people creating a bill at the same moment can still get the same bill number (documented limitation).
- I could not reach your live Supabase project; verify with the in-app Settings > Security check after you run the new SQL.
