import sys, time, json
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
srv=Server(); srv.ttl=40; errs=[]
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp('http://127.0.0.1:9333'); ctx=b.contexts[0]; pg=ctx.pages[0]
    ctx.route(SB+'/**',srv.handle); ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css')); ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    pg.on('console',lambda m:errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.reload(); pg.wait_for_selector('#zxl',timeout=15000)
    print('navigator.locks usable on file://:', pg.evaluate("(async()=>{try{await navigator.locks.request('t',()=>1);return 'yes'}catch(e){return 'NO: '+e.name+' '+e.message}})()"))
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached',timeout=10000)
    pg.wait_for_timeout(3000); print('after login:',pg.inner_text('#sync'))
    t0=time.time()
    while time.time()-t0<90 and srv.refreshes<1: pg.wait_for_timeout(1000)
    print('token refreshes seen by server:',srv.refreshes,'after',round(time.time()-t0),'s')
    pg.fill('[data-k=cust]','Refresh Customer'); c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','900'); pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(2500)
    print('status after save:',pg.inner_text('#sync'),'| saved on server:',any(r['customer']=='Refresh Customer' for r in srv.docs.values()))
    print('console:',errs[:5]); b.close()
