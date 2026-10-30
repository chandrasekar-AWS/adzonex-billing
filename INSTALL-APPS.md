# Ad ZoneX Billing: install as an app

One codebase, the same app everywhere. Your bills sync through Supabase, so every device shows the same data.

| Device | What you get | Where from |
|---|---|---|
| Android phone / tablet | `AdZoneX-Billing-android.apk` | GitHub > Actions (or Releases) |
| Windows 10 / 11 | `AdZoneX-Billing-x.y.z-win-x64.exe` (installer) | GitHub > Actions (or Releases) |
| Mac (Apple chip and Intel) | `AdZoneX-Billing-x.y.z-mac-arm64.dmg` / `...-mac-x64.dmg` | GitHub > Actions (or Releases) |
| Linux | `...-linux-x86_64.AppImage` or `...-linux-amd64.deb` | GitHub > Actions (or Releases) |
| iPhone / iPad | Add the website to the Home Screen (below) | no download |

## A. Build the installers (about 15 minutes, free)
1. **Once only (Android key):** open `android-signing/SECRETS-TO-ADD.txt` (in your download, not in this repo) and add the 4 secrets in
   GitHub: your repo > **Settings > Secrets and variables > Actions > New repository secret**.
   This gives the APK a permanent signature, so a new version installs over the old one without uninstalling.
   (Skip it and you still get an APK, but you must uninstall the old app before installing a new build.)
2. Open your repo > **Actions** > **Build apps** > **Run workflow**.
3. When all jobs are green, open the run and download from **Artifacts**:
   `android-apk`, `desktop-windows-latest`, `desktop-macos-latest`, `desktop-ubuntu-latest`, `ios-xcode-project`.
   (Each is a zip. Unzip it to get the installer.)

**Publish a release with download links** (optional): in a terminal inside the repo folder run
`git tag v1.0.1` then `git push origin v1.0.1`. The same build runs and all installers appear on the repo's **Releases** page.

**Update the apps after you change the website:** run the workflow again (or push a new tag). Install the new file over the old one.
The website itself (GitHub Pages) updates by itself as soon as you push, so the phone web app and browsers are always current.

## B. Install on each device
**Android:** copy the `.apk` to the phone and tap it. If asked, allow "Install unknown apps" for your file manager or browser.
Open **Ad ZoneX Billing**, sign in. **Print** and **Print history** open Android's own print dialog, so you can pick any printer your phone can reach (Wi-Fi, USB or Bluetooth printers with their Android print service installed) or choose Save as PDF. **PDF** and **Backup** open the share sheet (WhatsApp, Save to Files...). On iPhone, Print opens the share sheet: choose Print there (AirPrint). On Windows, Mac and in a browser, Print opens the normal system print window.

**Windows:** double-click the `.exe`.
You will see "**Windows protected your PC**" (SmartScreen, "Unknown publisher"). This is **not** a virus warning. Windows shows it for every
installer whose publisher has not bought a code-signing certificate, which costs money every year. Click **More info > Run anyway**.
It appears only once, for the installer. The installed app opens with no warning.
Ways to avoid the message (all free):
1. **Unblock the file before running it.** Right-click the downloaded `.zip` (before unzipping) or the `.exe` > **Properties** > tick **Unblock** > OK.
   Or in PowerShell: `Unblock-File "E:\path\to\AdZoneX-Billing-1.0.0-win-x64.exe"`
2. **Install from the browser instead (no installer at all):** open https://chandrasekar-aws.github.io/adzonex-billing/ in **Edge** or **Chrome**,
   click the install icon in the address bar (or menu > Apps > Install this site as an app). You get a Start-menu app that updates itself.
3. **Remove the message for good:** it needs a paid code-signing certificate (about 150 to 300 USD a year from a certificate company) or
   publishing in the Microsoft Store. Microsoft's own cheaper signing service is not open to individuals in India. Even with a certificate,
   a brand-new publisher can still see the message for the first weeks until Windows learns to trust it.

**Mac:** open the `.dmg`, drag the app to Applications. The first time, **right-click the app > Open > Open**.
If macOS says the app "is damaged", open Terminal and run: `xattr -cr "/Applications/Ad ZoneX Billing.app"` and open it again.
Choose `arm64` for Apple chips (M1/M2/M3/M4) and `x64` for older Intel Macs.

**Linux:** AppImage: `chmod +x AdZoneX-Billing-*.AppImage` then double-click or run it (needs `libfuse2` on Ubuntu 22.04+: `sudo apt install libfuse2`).
Debian/Ubuntu package: `sudo apt install ./AdZoneX-Billing-*.deb`.

**iPhone / iPad (no App Store needed):** open https://chandrasekar-aws.github.io/adzonex-billing/ in **Safari** > tap **Share** >
**Add to Home Screen** > **Add**. It opens full screen like an app, works offline, and PDF opens the iPhone share sheet.
(A real App Store app needs an Apple Developer account, 99 USD a year. If you get one, use the `ios-xcode-project` download:
unzip it on a Mac, open `ios/App/App.xcworkspace` in Xcode, choose your team under Signing, press Run.
With a free Apple ID you can also run it on your own iPhone, renewed every 7 days.)

## C. Good to know
- First sign-in needs internet. After that the apps open and work offline; new bills upload when you are back online.
- Sign out removes the local copy from that device. Bills stay safe in Supabase.
- Desktop and Android apps contain a copy of the website at the time of the build. Use the same website version and installers together
  after a big update (run the workflow again).
- The Android build, Windows installer, Mac app and iPhone project are made by GitHub's servers, not on your computer.

## D. If the sync status is red
Click the red status text (left side, under the logo; on a phone tap it). A window explains exactly what is wrong and how to fix it:
- **"Synced (not shared)"**: your Supabase database is still the older private version. Everything works, but bills are not shared between logins.
  Fix: Supabase > SQL Editor > paste everything from `backend/supabase.sql` > Run. Your bills are kept. Then press Settings > Sync now.
- **"Login not in team"**: the window shows the one line of SQL to run for this login.
- **"Database not set up"**: run `backend/supabase.sql` once.
- **"Offline"**: no internet. Nothing is lost. Bills upload by themselves when the connection is back.
- **"Please sign in again"**: Settings > Sign out, then sign in.
