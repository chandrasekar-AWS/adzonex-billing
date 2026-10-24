const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');
function create() {
  const w = new BrowserWindow({ width: 1280, height: 860, backgroundColor: '#000000', title: 'Ad ZoneX Billing',
    icon: path.join(__dirname, '..', 'icon-512.png'), webPreferences: { contextIsolation: true } });
  if (process.platform !== 'darwin') Menu.setApplicationMenu(null);
  w.loadFile(path.join(__dirname, '..', 'index.html'));
  w.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
}
app.whenReady().then(() => { create(); app.on('activate', () => { if (!BrowserWindow.getAllWindows().length) create(); }); });
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
