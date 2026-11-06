# What's new (latest)

## Print panel inside the app, always upright, and bill-maker logins
- **Windows / Mac / Linux app:** Print > preview > **Print** now opens our own print panel (choose printer, copies, colour). This replaces the Windows window that said "This app doesn't support print preview". The job is always **A4 portrait**, so the invoice can no longer come out turned sideways on a landscape page. "Windows print window" is still there as a back-up button. Rebuild the apps (Actions > Build apps) to get it.
- **Roles:** a login can be an **admin** (everything) or a **bill maker** (only makes bills). See backend/BACKEND-SETUP.md, "Roles". Run `backend/supabase.sql` once more in Supabase to switch it on. The sidebar now shows who is signed in and a Sign out button.
- Tests: tests/e2e10_roles.py (24 checks), tests/electron_print.py (11 checks, real Electron).

## Earlier update
## Print preview, month-wise reports, editable expense titles
- **Print preview.** Print no longer jumps straight to the system print window (the Windows window says "This app doesn't support print preview"). Every Print button (bill, History row, Print history, Expenses) now opens a full-screen preview of the document first, with **Print**, **Save PDF** and **Close**. Estimates can be printed too. Ctrl+P (or File > Print preview in the desktop app) opens the preview of the page you are on.
- **Month-wise History.** New Month drop-down next to the search boxes. The cards, the list and the printed report follow the month. The preview has its own month picker and a **Month-wise summary** table (entries, billed, received, balance per month) when more than one month is shown.
- **Expenses:** new **Pick month** tab, a month picker in the preview, and a month-wise summary in the report.
- **Edit expense titles** (Expenses page, panel under the Add box): rename a title (all past expenses are renamed too), add a title, delete a title (its expenses move to "Other"). Titles sync with your other devices. Typing "fuel" now reuses "Fuel" instead of creating a duplicate.

## Bugs and loopholes fixed
- Double-clicking **Add** for a payment in History recorded the payment twice. Fixed (it also no longer waits for the network first).
- **Restore backup** deleted calendar entries and expenses made after the backup was taken. They are now merged and kept.
- Printing on a phone/tablet browser could print a blank page because the print layer was removed too early. It now waits for the print window to close, and a stale print layer can no longer double the next print.
- Ctrl+P on the app screen used to print a blank page. It now opens the preview.
- An expense saved with a date outside the dates on screen looked like it vanished. A message now says where it went.
- The bill's own History list now shows "Printed" right after printing.
- Test: tests/e2e9_preview.py (49 checks). Older tests updated for the preview step. All 8 suites pass.

## Earlier update
## This update
- Settings > Services are now split under four titles: Design, Print, Signage, Digital. Each title has its own "+ Add ... service" button, so a new service lands right under its title. A drop-down on every service moves it to another title. (Default split: Signage = frame, backlit and foam items; Print = the other flex/vinyl/UV items.)
- New Calendar page: click a date, note who pays that day (Full, Half, Balance or any amount, optionally linked to a bill), Call and WhatsApp buttons, mark Received (can also add the payment to the bill). A "Collect money today" box shows on every page on the day, and a notification can be turned on at a time you choose.
- New Expenses page: add daily expenses, filter by Today / This month / All / Pick dates, and export or print as PDF, Image, Text or Print.
- Remark box on every bill; it prints on the bill (above the terms).
- The new-bill page no longer has the Upload signature box (it is still on saved bills, and a signed bill still prints its signature).
- WhatsApp icon now asks PDF / Image / Text, then opens the customer's WhatsApp chat.
- Calendar and Expenses sync through the same cloud settings record (no database change needed).
- Test: tests/e2e7_new_features.py (37 checks).

## Logo
- Fixed the tagline: in "DESIGN . BRAND . GROW" the R and O of GROW were fused together. All logo files were repaired
  (white-text, dark-text, original, and the copy built into the app), so the app, PDFs, prints and emails all show it correctly.

## Printing on your own printer
- Android app: Print, History > Print and "Print history" now open Android's print dialog directly (choose a printer, or Save as PDF).
  This is a small native plugin (app/native/android/ZXPrintPlugin.java) that the GitHub build installs automatically.
  If it cannot open (for example on iPhone), the app falls back to the share sheet, which also has a Print action.
- Windows / Mac / browser: Print opens the normal system print window (unchanged, tested: one A4 page, bill only).
- Tests: tests/e2e6_print.py (21 checks).

## Fixes: forms, and notifications when the app is closed

- **Expenses page**: after Add the typed text stayed in the boxes (Edit and Cancel were affected too). Fixed. Boxes now clear after Add, Update, Cancel and Enter; text you are typing is kept when you switch tabs or delete a row.
- **Android / iPhone app**: payment reminders are now scheduled as phone alarms (one per day with money due, next 60 days), so they appear even when the app is closed. Changing the reminder time, marking someone Received or syncing re-schedules them. Tapping one opens the Calendar. **Rebuild the apps** (Actions > Build apps) to get this.
- **Windows / Mac / Linux app**: closing the window now hides the app to the tray so reminders keep arriving. Notification permission is no longer blocked. The installed app starts with the computer on first run; switch it off in the tray menu. Quit from the tray icon.
- **Browser / installed web app**: reminders show while open; installed Chrome/Edge also check in the background. Phones cannot guarantee this with the app fully closed, so use the Android app for that.
- Old tests updated for the WhatsApp PDF/Image/Text chooser; new tests in tests/e2e8_forms_notify.py (43 checks).

## Client name suggestions
- Typing a client name in a new bill or estimate now suggests saved clients (from past bills, estimates and calendar entries). Press Tab to fill the name, phone, email, address, GSTIN and place of supply. Keep typing to use a new or different name.
