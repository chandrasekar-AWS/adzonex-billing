const { app, BrowserWindow, Menu, shell, session } = require('electron');
const path = require('path');

app.setAppUserModelId('in.adzonex.billing');
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) { app.quit(); process.exit(0); }   // a second copy must never open its own window
const APP_URL = require('url').pathToFileURL(path.join(__dirname, '..', 'index.html')).href;

let win = null;
function create() {
  win = new BrowserWindow({
    width: 1280, height: 860, minWidth: 380, minHeight: 560, show: false, autoHideMenuBar: true,
    backgroundColor: '#000000', title: 'Ad ZoneX Billing', icon: path.join(__dirname, '..', 'icon-512.png'),
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true, webSecurity: true, spellcheck: true, devTools: !!process.env.ZX_DEBUG, allowRunningInsecureContent: false }
  });
  win.once('ready-to-show', () => win.show());
  win.loadFile(path.join(__dirname, '..', 'index.html'));
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

app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });
app.whenReady().then(() => {
  // the app needs no camera, microphone, location or notifications
  session.defaultSession.setPermissionRequestHandler((wc, permission, cb) => cb(false));
  session.defaultSession.setPermissionCheckHandler(() => false);
  session.defaultSession.on('will-download', (e, item) => item.setSaveDialogOptions({ defaultPath: path.join(app.getPath('downloads'), item.getFilename()) }));
  Menu.setApplicationMenu(menu());
  create();
  app.on('activate', () => { if (!BrowserWindow.getAllWindows().length) create(); });
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
