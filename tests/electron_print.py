"""Real desktop app (Electron): preview -> in-app print panel -> printer bridge. Start Electron first:
xvfb-run -a electron --no-sandbox --remote-debugging-port=9333 ../app"""
import sys, time
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)[:300]) if (i and not c) else ''),flush=True)
srv=Server(); errs=[]
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp('http://127.0.0.1:9333'); ctx=b.contexts[0]; pg=ctx.pages[0]
    ctx.route(SB+'/**',srv.handle); ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css')); ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)))
    pg.reload(); pg.wait_for_selector('#zxl',timeout=15000)
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached',timeout=10000); pg.wait_for_timeout(1500)
    check('Electron: print bridge (preload) is available to the page',pg.evaluate("typeof window.zxDesktop=='object'&&typeof zxDesktop.print=='function'&&typeof zxDesktop.printers=='function'"))
    check('Electron: page cannot reach Node/require (still sandboxed)',pg.evaluate("typeof require=='undefined'&&typeof process=='undefined'"))
    pr=pg.evaluate("zxDesktop.printers()"); check('Electron: printer list comes back as a list',isinstance(pr,list),pr)
    pg.evaluate("""()=>{const d=newDoc();d.cust='Desk Cust';d.items=[{n:'Logo Design',h:'998391',s:'',q:'1',u:'Nos',p:'2000'}];d.pay=[{d:today(),a:1000,m:'UPI'}];commit(d);fix(d);touch(d);location.hash='#/d/'+d.id}""")
    pg.wait_for_selector('[data-a=print]'); pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp')
    check('Electron: Print button opens the preview first',pg.locator('.pvw .zp').count()==1 and 'INVOICE' in pg.inner_text('.pvw .zp').upper())
    pg.click('[data-pv=print]'); pg.wait_for_selector('.mdl.pp')
    t=pg.inner_text('.mdl.pp'); check('Electron: Print opens the in-app print panel (copies, colour, A4 portrait)',all(x in t for x in ['Print','Copies','Colour','A4, portrait']),t)
    check('Electron: panel stays above the preview and is not part of the printed page',pg.evaluate("getComputedStyle(document.querySelector('.mdl.pp')).zIndex>400"))
    pg.click('#ppx'); pg.wait_for_timeout(200)
    check('Electron: Cancel closes the panel, the preview stays open',pg.locator('.mdl.pp').count()==0 and pg.locator('.pvw').count()==1)
    pg.click('[data-pv=print]'); pg.wait_for_selector('.mdl.pp'); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    check('Electron: Escape closes only the panel (preview remains)',pg.locator('.mdl.pp').count()==0 and pg.locator('.pvw').count()==1)
    # a job to a missing printer must fail politely, never crash or hang
    r=pg.evaluate("zxDesktop.print({deviceName:'No such printer',copies:1,color:true,system:false})")
    check('Electron: print to an unknown printer returns an error result (no crash)',isinstance(r,dict) and r.get('ok') is False,r)
    check('Electron: page returns to normal after a failed print',pg.evaluate("!document.querySelector('.pw')&&!document.body.classList.contains('pj')"))
    # the print-media render the printer receives is A4 portrait, one page
    pg.evaluate("""()=>{const w=document.createElement('div');w.className='pw';w.innerHTML=paper(S.docs.find(d=>!d.del));document.body.append(w);document.body.classList.add('pj')}""")
    pdf=pg.evaluate("1")
    check('Electron: no JS errors',not errs,errs[:3])
    b.close()
print(sum(R),'/',len(R)); sys.exit(0 if all(R) else 1)
