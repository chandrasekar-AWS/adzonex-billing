const { app, BrowserWindow, Menu, shell, session, Tray, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');

app.setAppUserModelId('in.adzonex.billing');
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) { app.quit(); process.exit(0); }   // a second copy must never open its own window
const APP_URL = require('url').pathToFileURL(path.join(__dirname, '..', 'index.html')).href;

let win = null, tray = null, quitting = false;
const startHidden = process.argv.includes('--hidden');
function create() {
  win = new BrowserWindow({
    width: 1280, height: 860, minWidth: 380, minHeight: 560, show: false, autoHideMenuBar: true,
    backgroundColor: '#000000', title: 'Ad ZoneX Billing', icon: path.join(__dirname, '..', 'icon-512.png'),
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true, webSecurity: true, backgroundThrottling: false, spellcheck: true, devTools: !!process.env.ZX_DEBUG, allowRunningInsecureContent: false }
  });
  win.once('ready-to-show', () => { if (!startHidden || !tray) win.show(); });
  win.loadFile(path.join(__dirname, '..', 'index.html'));
  win.on('close', e => { if (!quitting && tray) { e.preventDefault(); win.hide(); } });   // keep running in the tray so payment reminders still arrive
  win.on('closed', () => { win = null; });
  // links to other sites open in the normal browser, never inside the app
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https:\/\//.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (url.split('#')[0] !== APP_URL) { e.preventDefault(); if (/^https:\/\//.test(url)) shell.openExternal(url); } });
  win.webContents.on('will-attach-webview', e => e.preventDefault());
}

function menu() {
  const mac = process.platform === 'darwin';
  return Menu.buildFromTemplate([
    ...(mac ? [{ role: 'appMenu' }] : []),
    { label: 'File', submenu: [mac ? { role: 'close' } : { role: 'quit' }] },
    { role: 'editMenu' },
    { label: 'View', submenu: [{ role: 'reload' }, { role: 'togglefullscreen' }, { type: 'separator' }, { role: 'resetZoom' }, { role: 'zoomIn' }, { role: 'zoomOut' }] },
    { role: 'windowMenu' }
  ]);
}

function showWin() { if (!win) { create(); return; } if (win.isMinimized()) win.restore(); win.show(); win.focus(); }
function trayMenu() {
  const on = app.getLoginItemSettings().openAtLogin;
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: 'Open Ad ZoneX Billing', click: showWin },
    { label: 'Start when I sign in to this computer', type: 'checkbox', checked: on, click: i => { app.setLoginItemSettings({ openAtLogin: i.checked, args: ['--hidden'] }); trayMenu(); } },
    { type: 'separator' },
    { label: 'Quit (stops payment reminders)', click: () => { quitting = true; app.quit(); } }
  ]));
}
function makeTray() {
  try {
    const sz = process.platform === 'darwin' ? 18 : 20;
    tray = new Tray(nativeImage.createFromPath(path.join(__dirname, '..', 'icon-192.png')).resize({ width: sz, height: sz }));
    tray.setToolTip('Ad ZoneX Billing');
    tray.on('click', showWin);
    trayMenu();
  } catch (e) { console.warn('Tray not available:', e && e.message); tray = null; }
}
// first run of the installed app: start with the computer (hidden) so reminders work without opening it. Can be switched off from the tray menu.
function firstRunAutostart() {
  try {
    const mark = path.join(app.getPath('userData'), 'autostart-set');
    if (app.isPackaged && !fs.existsSync(mark)) { app.setLoginItemSettings({ openAtLogin: true, args: ['--hidden'] }); fs.writeFileSync(mark, '1'); }
  } catch (e) {}
}
app.on('before-quit', () => { quitting = true; });
app.on('second-instance', showWin);
app.whenReady().then(() => {
  // the app needs no camera, microphone or location. It does show payment-reminder notifications.
  session.defaultSession.setPermissionRequestHandler((wc, permission, cb) => cb(permission === 'notifications'));
  session.defaultSession.setPermissionCheckHandler((wc, permission) => permission === 'notifications');
  session.defaultSession.on('will-download', (e, item) => item.setSaveDialogOptions({ defaultPath: path.join(app.getPath('downloads'), item.getFilename()) }));
  Menu.setApplicationMenu(menu());
  makeTray();
  firstRunAutostart();
  create();
  app.on('activate', showWin);
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
