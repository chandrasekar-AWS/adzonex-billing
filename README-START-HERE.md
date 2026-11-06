# Ad ZoneX Billing: complete package

app/      The website. Upload everything inside this folder to your GitHub repo (replace old files).
backend/  supabase.sql (run once; also upgrades an older install), BACKEND-SETUP.md (steps, team sharing, security), Code.gs (optional email script).
logo/     Your logo (transparent PNG, original) and app icon.
tests/    The automated tests used to check the app (optional, you can ignore).
android-signing/  PRIVATE. The permanent key for your Android app + the 4 GitHub secrets to add. Never upload this folder anywhere. Back it up.
INSTALL-APPS.md   How to get and install the Android, Windows, Mac, Linux and iPhone apps.

## Steps
1. Backend: backend/BACKEND-SETUP.md, Part 1 (run supabase.sql, create a login for each person, turn off sign-ups).
2. Upload the contents of app/ to GitHub (repo root, so index.html is at the top). Keep the hidden .github and .nojekyll files.
3. Wait about a minute, open https://chandrasekar-aws.github.io/adzonex-billing/ and hard-refresh (Ctrl+Shift+R).
4. Sign in. Bills already saved in this browser upload to Supabase automatically.
5. Settings > Run security check. All lines should be ticked.

## Newest changes
See WHATS-NEW.md: service titles in Settings, Calendar, Expenses, bill Remark, WhatsApp PDF/Image/Text chooser.

## What changed in the earlier version
- HSN/SAC on/off slider on every bill. GST on/off slider. Optional IGST for customers in another state.
- Title is INVOICE, or TAX INVOICE when GST is on. Tax is shown as Taxable Amount, CGST and SGST (or IGST).
- New bill layout: centred title, number and date under the line, green strip under the header, signature space, computer-generated line at the bottom.
- Signature image upload on every bill (not shared between bills).
- History: tabs All, Estimate, Balance due, GST bill, Without GST bill, each with a count. Three search boxes: name or phone, number, date.
- Sharper PDF (3x), page margin 0 for printing so the browser prints no header or footer text.
- Settings > Bill colours: header, strip, table heading, total bars, plus a black and white switch.
- No database change is needed for this version (supabase.sql is unchanged).

## Native apps (Android APK, Windows, Mac, Linux, iPhone)
1. Put the contents of app/ on GitHub as before (it now also contains the app builder: .github/workflows/build-apps.yml, native/, package-lock.json).
2. Add the 4 Android secrets from android-signing/SECRETS-TO-ADD.txt (GitHub repo > Settings > Secrets and variables > Actions).
3. GitHub repo > Actions > Build apps > Run workflow. After about 15 minutes download the installers from the run's Artifacts.
Full instructions per device: INSTALL-APPS.md.
