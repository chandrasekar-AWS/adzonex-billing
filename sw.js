const C='axb-v18',A=['./','index.html','style.css','app.js','logo.js','libs/supabase.js','libs/html2canvas.min.js','libs/jspdf.umd.min.js','icon-180.png','manifest.webmanifest','icon-192.png','icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=C&&x!='zx-note').map(x=>caches.delete(x)))).then(()=>clients.claim())));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!='GET'||new URL(r.url).origin!=location.origin)return;e.respondWith(fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(r,y))}return x}).catch(()=>caches.match(r).then(m=>m||caches.match('index.html'))))});
self.addEventListener('notificationclick',e=>{e.notification.close();e.waitUntil(clients.matchAll({type:'window'}).then(l=>l.length?l[0].focus():clients.openWindow('./#/c')))});
// Background check (installed Chrome/Edge apps): the page saves the list of people to collect from in the 'zx-note' cache, the browser wakes this worker now and then.
async function dueCheck(){try{const c=await caches.open('zx-note'),r=await c.match('due.json');if(!r)return;const j=await r.json(),n=new Date(),p=v=>String(v).padStart(2,'0'),t=n.getFullYear()+'-'+p(n.getMonth()+1)+'-'+p(n.getDate()),hm=p(n.getHours())+':'+p(n.getMinutes());
const td=(j.list||[]).filter(x=>x.d===t);if(!td.length||hm<(j.rt||'09:00')||j.last===t)return;j.last=t;await c.put('due.json',new Response(JSON.stringify(j)));
await self.registration.showNotification('Collect money today ('+td.length+')',{body:td.map(x=>x.n+' - \u20b9'+(+x.a).toLocaleString('en-IN')+(x.ph?' ('+x.ph+')':'')).join('\n'),icon:'icon-192.png',tag:'zx-pay-'+t})}catch(e){}}
self.addEventListener('periodicsync',e=>{if(e.tag=='zx-due')e.waitUntil(dueCheck())});
