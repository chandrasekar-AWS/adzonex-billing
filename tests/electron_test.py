import sys, time, os, json
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)) if (i and not c) else ''),flush=True)
srv=Server(); errs=[]
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp('http://127.0.0.1:9333'); ctx=b.contexts[0]; pg=ctx.pages[0]
    ctx.route(SB+'/**',srv.handle)
    ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css'))
    ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e))); pg.on('console',lambda m:errs.append('CONSOLE '+m.text) if m.type=='error' else None)
    pg.reload(); pg.wait_for_selector('#zxl',timeout=15000)
    check('Electron: app loads from file:// (strict CSP did not break it)',pg.url.startswith('file://') and pg.evaluate("typeof S=='object'&&!!window.supabase&&!!window.ZX_LOGO"),pg.url)
    check('Electron: secure context, localStorage works',pg.evaluate("isSecureContext&&(()=>{try{localStorage.setItem('t','1');localStorage.removeItem('t');return true}catch(e){return false}})()"))
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]')
    pg.wait_for_selector('#zxl',state='detached',timeout=10000)
    end=time.time()+8
    while time.time()<end and not pg.evaluate("/Synced/.test(document.querySelector('#sync').textContent)"): pg.wait_for_timeout(150)
    check('Electron: sign in works and sync shows Synced',pg.evaluate("/Synced/.test(document.querySelector('#sync').textContent)"),pg.inner_text('#sync'))
    pg.fill('[data-k=cust]','Desktop Customer'); pg.fill('[data-k=phone]','9000000001')
    c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','2500')
    pg.click('[data-k=gst]'); pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(1500)
    check('Electron: invoice saved and uploaded to Supabase',any(r['customer']=='Desktop Customer' for r in srv.docs.values()))
    pg.click('#app > .sw tr.row'); pg.wait_for_selector('#pa'); pg.fill('#pa','1000'); pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill'); pg.wait_for_timeout(500)
    r=pg.evaluate("""(async()=>{const d=S.docs.find(x=>x.id==location.hash.slice(4));const P=await pdfMake(d);const u=P.output('arraybuffer');return {n:u.byteLength,head:new TextDecoder().decode(new Uint8Array(u).slice(0,5)),pages:P.getNumberOfPages(),no:no(d)}})()""")
    check('Electron: PDF is created inside the desktop app (valid A4 PDF)',r['head']=='%PDF-' and r['pages']==1 and r['n']>50000 and r['no'].startswith('INV'),r)
    pg.screenshot(path='/home/claude/test/el_shot.png')
    check('Electron: no JS errors / CSP violations',not [x for x in errs if x.startswith('PAGEERR') or 'Content Security' in x or 'Refused' in x],errs[:4])
    b.close()
print(sum(R),'/',len(R)); sys.exit(0 if all(R) else 1)
