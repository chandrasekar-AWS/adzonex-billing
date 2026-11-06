import sys, time, os, json, re
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
exec("def new_ctx"+open('/home/claude/test/e2e.py').read().split("def new_ctx")[1].split("with sync_playwright() as p:")[0])
URL='http://localhost:8123/index.html'; R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)) if (i and not c) else ''),flush=True)
def login(pg):
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached')
def mkbill(pg):
    pg.fill('[data-k=cust]','Phone Customer'); pg.fill('[data-k=phone]','9000000002')
    c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','1500')
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.click('#app > .sw tr.row'); pg.wait_for_selector('#pa'); pg.fill('#pa','500'); pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill')
def wait(pg,js,t=15000):
    end=time.time()+t/1000
    while time.time()<end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(120)
    return False
with sync_playwright() as p:
    b=p.chromium.launch(); srv=Server(); errs=[]
    # ---------- A) Android / iOS NATIVE app (Capacitor) ----------
    ctx=new_ctx(b,srv); pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("""window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',Plugins:{Filesystem:{writeFile:async o=>{(window.__fw=window.__fw||[]).push(o);return {uri:'file:///cache/'+o.path}}},Share:{share:async o=>{(window.__sh=window.__sh||[]).push(o)}}}};""")
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); wait(pg,"/Synced/.test(document.querySelector('#sync').textContent)")
    check('native app: service worker is NOT registered inside the app',pg.evaluate("navigator.serviceWorker.getRegistrations().then(r=>r.length)")==0)
    mkbill(pg)
    pg.click('[data-a=pdf]'); ok=wait(pg,"window.__sh&&window.__sh.length>=1")
    fw=pg.evaluate("window.__fw||[]"); sh=pg.evaluate("window.__sh||[]")
    check('native: Download PDF writes a real PDF to the phone and opens the share sheet',ok and fw[0]['path'].startswith('Invoice-INV') and fw[0]['path'].endswith('.pdf') and fw[0]['data'].startswith('JVBERi') and sh[0]['url'].startswith('file:///cache/Invoice-'),(fw[:1] and fw[0]['path'],sh))
    pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); ok=wait(pg,"window.__sh&&window.__sh.length>=2")
    check('native: Print button produces a shareable/printable PDF (WebView cannot print pages)',ok and len(pg.evaluate("window.__sh"))==2)
    pg.keyboard.press('Escape'); pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-a=ex]'); pg.click('[data-a=ex]'); ok=wait(pg,"window.__fw&&window.__fw.length>=3")
    fw=pg.evaluate("window.__fw"); import base64
    bk=json.loads(base64.b64decode(fw[2]['data'])) if ok else {}
    check('native: Backup is saved to a file and shared (download links do not work in apps)',ok and fw[2]['path'].startswith('adzonex-backup-') and len(bk.get('docs',[]))>=1 and bk['set'].get('key','')=='',fw[2]['path'] if ok else None)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); pg.click('[data-a=ph]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); ok=wait(pg,"window.__fw&&window.__fw.length>=4",25000)
    pg.keyboard.press('Escape')
    fw=pg.evaluate("window.__fw")
    check('native: Print history creates a PDF report and shares it',ok and fw[3]['path'].startswith('Invoice-history-') and fw[3]['data'].startswith('JVBERi'),fw[3]['path'] if ok else None)
    pg.evaluate("window.__opened=null;window.open=(...a)=>{window.__opened=a}"); pg.evaluate("location.hash='#/h'"); pg.click('#app > .sw tr.row'); pg.wait_for_selector('[data-a=wa]'); pg.click('[data-a=wa]'); pg.click('.mdl [data-w=txt]')   # chooser: Text
    check('native: WhatsApp button opens the wa.me link',str(pg.evaluate("window.__opened and window.__opened[0]") if False else pg.evaluate("(window.__opened||[''])[0]")).startswith('https://wa.me/919000000002'))
    check('native app: no JS errors',not errs,errs[:3])
    ctx.close()
    # ---------- B) iPhone / Android BROWSER or installed web app: share sheet ----------
    ctx=new_ctx(b,srv,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    pg=ctx.new_page(); pg.add_init_script("""navigator.canShare=d=>!!(d&&d.files&&d.files.length);navigator.share=async d=>{if(window.__deny){const e=new Error('x');e.name='NotAllowedError';throw e}if(window.__cancel){const e=new Error('x');e.name='AbortError';throw e}window.__shared=d}""")
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); wait(pg,"/Synced/.test(document.querySelector('#sync').textContent)"); mkbill(pg)
    pg.click('[data-a=pdf]'); ok=wait(pg,"!!window.__shared")
    sh=pg.evaluate("window.__shared&&{n:window.__shared.files[0].name,t:window.__shared.files[0].type,s:window.__shared.files[0].size}")
    check('iPhone/Android browser: PDF opens the phone share sheet (WhatsApp, Files, Print...)',ok and sh['t']=='application/pdf' and sh['n'].startswith('Invoice-INV') and sh['s']>50000,sh)
    pg.evaluate("window.__shared=null;window.__deny=true")
    with pg.expect_download(timeout=30000) as dl: pg.click('[data-a=pdf]')
    check('if the share sheet is refused, the PDF is simply downloaded instead',dl.value.suggested_filename.startswith('Invoice-INV'))
    pg.evaluate("window.__deny=false;window.__cancel=true;window.__downloaded=0"); pg.once('download',lambda d:pg.evaluate("window.__downloaded=1")); pg.click('[data-a=pdf]'); pg.wait_for_timeout(6000)
    check('cancelling the share sheet does not also start a download',pg.evaluate("window.__downloaded")==0)
    ctx.close()
    # ---------- C) Desktop browser: still plain download ----------
    ctx=new_ctx(b,srv); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); wait(pg,"/Synced/.test(document.querySelector('#sync').textContent)"); mkbill(pg)
    with pg.expect_download(timeout=30000) as dl: pg.click('[data-a=pdf]')
    check('desktop browser: PDF downloads normally',dl.value.suggested_filename.startswith('Invoice-INV'))
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')
    check('History print preview exists on desktop too',pg.evaluate("typeof histPv=='function'"))
    b.close()
print(sum(R),'/',len(R)); sys.exit(0 if all(R) else 1)
