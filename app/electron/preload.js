// Tiny, safe bridge: the page can only ask for the printer list and send a print job. Nothing else of Node/Electron is exposed.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('zxDesktop', {
  printers: () => ipcRenderer.invoke('zx:printers'),
  print: o => ipcRenderer.invoke('zx:print', { deviceName: String((o && o.deviceName) || ''), copies: +(o && o.copies) || 1, color: !(o && o.color === false), system: !!(o && o.system) })
});
