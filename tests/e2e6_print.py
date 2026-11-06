"""Printing + logo tests: native direct print (Android plugin), fallbacks, web print, real print-media render."""
import sys, time, re, json, subprocess, base64
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
URL='http://localhost:8123/index.html'; R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)[:300]) if (i and not c) else ''),flush=True)
def wait(pg,js,t=15000):
    end=time.time()+t/1000
    while time.time()<end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(120)
    return False
def ctx_for(b,srv,init=None):
    ctx=b.new_context(accept_downloads=True,service_workers='block',viewport={'width':1280,'height':900}); ctx.route(SB+'/**',srv.handle)
    ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css')); ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    if init: ctx.add_init_script(init)
    return ctx
def login(pg):
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached')
    wait(pg,"/Synced/.test(document.querySelector('#sync').textContent)")
def mkbill(pg):
    pg.fill('[data-k=cust]','Print Customer'); pg.fill('[data-k=phone]','9000000002')
    c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','1500')
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.click('#app > .sw tr.row'); pg.wait_for_selector('#pa'); pg.fill('#pa','500'); pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill')
def native_init(print_mode):
    # print_mode: 'ok' | 'reject' | 'absent' | 'notimpl'
    plug={'ok':"{printPdf:async o=>{(window.__pr=window.__pr||[]).push(o)}}",
          'reject':"{printPdf:async o=>{(window.__pr=window.__pr||[]).push(o);throw new Error('print service unavailable')}}",
          'notimpl':"{printPdf:async o=>{const e=new Error('\"ZXPrint\" plugin is not implemented on ios');e.code='UNIMPLEMENTED';throw e}}"}.get(print_mode)
    reg=("registerPlugin:n=>("+plug+"),") if plug else ""
    return ("window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',"+reg+
            "Plugins:{Filesystem:{writeFile:async o=>{(window.__fw=window.__fw||[]).push(o);return {uri:'file:///cache/'+o.path}}},Share:{share:async o=>{(window.__sh=window.__sh||[]).push(o)}}}};")

with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- A) native app WITH the direct-print plugin ----------
    srv=Server(); errs=[]; ctx=ctx_for(b,srv,native_init('ok')); pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    dl=[]; pg.on('dialog',lambda d:(dl.append(d.message),d.accept()))
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); mkbill(pg)
    pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); ok=wait(pg,"window.__pr&&window.__pr.length>=1")
    pr=pg.evaluate("window.__pr||[]"); sh=pg.evaluate("window.__sh||[]")
    check('native: Print sends the bill PDF straight to the phone print dialog',ok and pr[0]['data'].startswith('JVBERi') and pr[0]['name'].startswith('Invoice INV') and not pr[0]['name'].endswith('.pdf'),pr[:1] and {k:str(v)[:30] for k,v in pr[0].items()})
    check('native: Print does NOT open the share sheet any more',len(sh)==0,sh)
    pg.keyboard.press('Escape'); pg.click('[data-a=pdf]'); check('native: "Download PDF" still shares/saves the file (not printed)',wait(pg,"window.__sh&&window.__sh.length==1") and len(pg.evaluate("window.__pr"))==1)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); n0=len(pg.evaluate("window.__pr"))
    pb=pg.query_selector('[data-p]'); 
    if pb: pb.click(); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]')
    check('native: History row Print goes to the print dialog',pb is not None and wait(pg,f"window.__pr.length>{n0}") and pg.evaluate("window.__pr[window.__pr.length-1].data.slice(0,5)")=='JVBER')
    pg.keyboard.press('Escape'); n1=len(pg.evaluate("window.__pr")); pg.click('[data-a=ph]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); ok=wait(pg,f"window.__pr.length>{n1}",25000); last=pg.evaluate("window.__pr[window.__pr.length-1]")
    check('native: "Print history" report goes to the print dialog',ok and last['name'].startswith('Invoice history') and last['data'].startswith('JVBERi'),last['name'] if ok else None)
    check('native: no error alerts / JS errors while printing',not dl and not errs,(dl,errs)); pg.close(); ctx.close()

    # ---------- B) plugin fails or is missing -> falls back to the share sheet (which has Print on it) ----------
    for mode,label in (('reject','print service error'),('notimpl','plugin not implemented (iPhone / old build)'),('absent','no plugin at all')):
        srv=Server(); errs=[]; ctx=ctx_for(b,srv,native_init(mode)); pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); dl=[]; pg.on('dialog',lambda d:(dl.append(d.message),d.accept()))
        pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); mkbill(pg); pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); 
        ok=wait(pg,"window.__sh&&window.__sh.length>=1"); fw=pg.evaluate("window.__fw||[]")
        check(f'native fallback ({label}): Print opens the share sheet with the PDF',ok and fw and fw[0]['data'].startswith('JVBERi'),fw[:1])
        check(f'native fallback ({label}): no error popup or crash',not dl and not errs,(dl,errs)); pg.close(); ctx.close()

    # ---------- C) desktop / browser print ----------
    srv=Server(); errs=[]; ctx=ctx_for(b,srv,"window.print=()=>{window.__printed=(window.__printed||0)+1;window.__during=!!document.querySelector('.pw')&&document.body.classList.contains('pj')}"); pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); mkbill(pg)
    pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); pg.wait_for_timeout(400)
    check('browser/desktop: Print opens the system print dialog with the invoice laid out for printing',pg.evaluate("window.__printed")==1 and pg.evaluate("window.__during"),pg.evaluate("[window.__printed,window.__during]"))
    check('browser/desktop: page returns to normal after printing',pg.evaluate("!document.querySelector('.pw')&&!document.body.classList.contains('pj')"))
    # real print-media render (what the printer receives)
    pg.evaluate("""()=>{const d=S.docs.find(x=>!x.del);const w=document.createElement('div');w.className='pw';w.innerHTML=paper(d);document.body.append(w);document.body.classList.add('pj')}""")
    pg.wait_for_timeout(600)
    pdfb=pg.pdf(prefer_css_page_size=True,print_background=True); open('/tmp/print_out.pdf','wb').write(pdfb)
    info=subprocess.run(['pdfinfo','/tmp/print_out.pdf'],capture_output=True,text=True).stdout
    pages=int(re.search(r'Pages:\s+(\d+)',info).group(1)); size=re.search(r'Page size:\s+(.*)',info).group(1)
    check('print output: invoice fits on 1 page, A4',pages==1 and 'A4' in size,(pages,size))
    txt=subprocess.run(['pdftotext','/tmp/print_out.pdf','-'],capture_output=True,text=True).stdout
    check('print output: contains the bill, none of the app screen (menus, buttons)',('Print Customer' in txt) and ('Logo Design' in txt) and not re.search(r'Print history|Record payment|Sign out|Save',txt),txt[:200])
    subprocess.run(['pdftoppm','-png','-r','110','/tmp/print_out.pdf','/tmp/print_page'])
    check('no JS errors',not errs,errs); pg.close(); ctx.close()

    # ---------- D) logo ----------
    srv=Server(); ctx=ctx_for(b,srv); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_selector('#zxl')
    r=pg.evaluate("""async()=>{const out={};for(const k of ['ZX_LOGO','ZX_LOGO_D']){const im=new Image();im.src=window[k];await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const x=c.getContext('2d');x.drawImage(im,0,0);
      const W=im.width,H=im.height,d=x.getImageData(0,Math.round(H*.84),W,Math.round(H*.12)).data,h=Math.round(H*.12);
      // columns (within the tagline band) that contain green ink
      const cols=[];for(let xx=0;xx<W;xx++){let on=0;for(let yy=0;yy<h;yy++){const i=(yy*W+xx)*4;if(d[i+3]>60&&d[i+1]>d[i]+25&&d[i+1]>d[i+2]+60){on=1;break}}cols.push(on)}
      const runs=[];let s=-1;cols.forEach((v,i)=>{if(v&&s<0)s=i;if(!v&&s>=0){runs.push([s,i]);s=-1}});out[k]={w:W,h:H,runs:runs}}return out}""")
    for k,v in r.items():
        runs=v['runs']; gaps=[runs[i+1][0]-runs[i][1] for i in range(len(runs)-1)]
        last4=runs[-4:]; gl=[last4[i+1][0]-last4[i][1] for i in range(3)]
        check(f'logo {k}: tagline GROW has 4 separate letters with clear gaps (R and O no longer overlap)',len(runs)>=17 and min(gl)>=8,(len(runs),gl))
        check(f'logo {k}: whole tagline fits inside the image',runs[-1][1]<v['w']-4,(runs[-1],v['w']))
    pg.close(); ctx.close(); b.close()
ok=sum(R); print(f'\n{ok}/{len(R)} passed')
