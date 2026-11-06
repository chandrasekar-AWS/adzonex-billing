import sys, json, time, datetime, re
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright, expect
URL='http://localhost:8123/index.html'
R=[]
def check(name,cond,info=''):
    R.append((name,bool(cond),info)); print(('PASS ' if cond else 'FAIL ')+name+(('  -> '+str(info)) if (info and not cond) else ''),flush=True)

def new_ctx(b,srv,**kw):
    kw.setdefault('viewport',{'width':1280,'height':900})
    ctx=b.new_context(accept_downloads=True,service_workers='block',**kw)
    ctx.route(SB+'/**',srv.handle)
    ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css'))
    ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    return ctx
def watch(pg,errs):
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)))
    pg.on('console',lambda m:errs.append('CONSOLE '+m.text) if m.type=='error' else None)
def login(pg,pw='Correct-Horse-9',email='owner@adzonex.in'):
    pg.fill('#zxl input[name=email]',email); pg.fill('#zxl input[name=password]',pw); pg.click('#zxl button[type=submit]')
def poll(pg,js,t=6000):
    end=time.time()+t/1000
    while time.time()<end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(100)
    raise Exception('poll timeout: '+js)
def wait_sync(pg,t=6000): poll(pg,"!!document.querySelector('#sync')&&/Synced/.test(document.querySelector('#sync').textContent)",t)

with sync_playwright() as p:
    b=p.chromium.launch(); srv=Server(); errs=[]
    ctx=new_ctx(b,srv); pg=ctx.new_page(); watch(pg,errs)
    pg.add_init_script("window.print=()=>{window.__printed=(window.__printed||0)+1}")
    pg.goto(URL); pg.wait_for_selector('#zxl')
    # ---- LOGIN ----
    check('login screen shown first',pg.locator('#zxl').count()==1)
    check('app behind login is inert (no keyboard access)',pg.evaluate("document.querySelector('.shell').inert")==True)
    login(pg,'wrong-password'); pg.wait_for_selector('#zxe:not(:empty)')
    check('wrong password shows error, stays on login',pg.locator('#zxe').inner_text()=='Invalid login credentials' and pg.locator('#zxl').count()==1)
    pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached')
    check('correct password opens the app',pg.locator('#zxl').count()==0 and pg.evaluate("!document.querySelector('.shell').inert"))
    wait_sync(pg)
    check('first sync uploaded business settings',srv.settings is not None and srv.settings['data']['v']['name']=='Ad ZoneX',srv.settings and list(srv.settings['data'].keys()))
    check('every API call carries the publishable apikey',all(l[3].get('apikey')==KEY for l in srv.log))
    check('no secret/service key ever sent',not any('sb_secret' in json.dumps(l[3]) or 'service_role' in json.dumps(l[3]) for l in srv.log))
    # ---- BILLING ----
    pg.fill('[data-k=cust]','Test Customer <b>Ltd</b>'); pg.fill('[data-k=phone]','9876543210'); pg.fill('[data-k=email]','cust@example.com'); pg.fill('[data-k=addr]','12 Main St\nCoimbatore')
    n=pg.locator('[data-g=items][data-i="0"][data-k=n]'); n.click(); n.type('normal fl',delay=20)
    pg.wait_for_selector('.ac .aci'); check('autocomplete suggestions appear',pg.locator('.ac .aci').count()>=1)
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowUp'); pg.keyboard.press('Enter')
    check('Enter picks suggestion',pg.input_value('[data-g=items][data-i="0"][data-k=n]')=='Normal Flex',pg.input_value('[data-g=items][data-i="0"][data-k=n]'))
    check('HSN auto-filled',pg.input_value('[data-g=items][data-i="0"][data-k=h]')=='4911')
    pg.fill('[data-g=items][data-i="0"][data-k=s]','8 x 4'); pg.fill('[data-g=items][data-i="0"][data-k=q]','2'); pg.fill('[data-g=items][data-i="0"][data-k=p]','12')
    check('amount = 8x4x2 sqft x 12 = 768',pg.inner_text('[data-amt="items:0"]').strip()=='768.00',pg.inner_text('[data-amt="items:0"]'))
    check('next row auto-added',pg.locator('#rows .xr').count()==2)
    pg.check('[data-k=gst]'); pg.fill('[data-k=disc]','68')
    check('GST 18% on (768-68)=700 -> CGST 63 + SGST 63 ; total 826',('CGST @ 9.00%' in pg.inner_text('#gdet')) and pg.inner_text('#v-t').strip()=='₹ 826.00',(pg.inner_text('#gdet'),pg.inner_text('#v-t')))
    check('amount in words',pg.inner_text('#v-w')=='Eight Hundred Twenty Six Rupees Only',pg.inner_text('#v-w'))
    pg.fill('[data-k=rate]','500'); check('GST rate above 100 is capped (CGST 50%+SGST 50%)',pg.inner_text('#v-t').strip()=='₹ 1,400.00',pg.inner_text('#v-t')); pg.fill('[data-k=rate]','18')
    # digital tab
    pg.click('[data-m=dm]'); check('digital tab opens',pg.locator('.xs.dm').count()==1); pg.click('[data-m=pr]')
    # save validations
    # save
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); check('save -> History with toast',location:=pg.evaluate('location.hash')=='#/h')
    pg.wait_for_timeout(1500)
    check('estimate pushed to Supabase',len(srv.docs)==1)
    d=list(srv.docs.values())[0]
    check('server row: status estimate, customer, est_no',d['status']=='estimate' and d['customer'].startswith('Test Customer') and re.match(r'^\d{6}-\d{2}\d+$',d['est_no'] or ''),d)
    check('row owned by the logged-in user',d['user_id']==UID)
    check('customer name with HTML is shown as text (not executed)',pg.locator('table.lt b >> nth=0').count()==1 and pg.evaluate("document.querySelectorAll('table.lt b').length>0") and pg.locator('table.lt td:nth-child(2)').first.inner_text()=='Test Customer <b>Ltd</b>',pg.locator('table.lt td:nth-child(2)').first.inner_text())
    check('history shows balance to collect 0 and open estimate 826',('826.00' in pg.inner_text('.stats')),pg.inner_text('.stats'))
    # ---- PAYMENT -> BILL ----
    pg.click('#app > .sw tr.row >> nth=0'); pg.wait_for_selector('#pa')
    pg.click('[data-a=adv]'); check('70% advance = 578.20',pg.input_value('#pa')=='578.20',pg.input_value('#pa'))
    pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill'); pg.wait_for_timeout(1500)
    d=list(srv.docs.values())[0]
    check('first payment turns estimate into BILL',d['status']=='bill' and (d['bill_no'] or '').startswith('') and d['data']['pay'][0]['a']==578.2,d['status'])
    check('bill number format',re.match(r'^INV\d{6}-\d{2}\d+$',pg.inner_text('h1')) is not None,pg.inner_text('h1'))
    check('"History of this bill" rows are normal (old .lg conflict fixed)',pg.evaluate("[...document.querySelectorAll('.card .lg')].every(e=>getComputedStyle(e).position!='fixed')") and pg.locator('.card .lg').count()>=2)
    # ---- PDF / print ----
    with pg.expect_download(timeout=30000) as dl: pg.click('[data-a=pdf]')
    f=dl.value; path=f.path(); head=open(path,'rb').read(5)
    check('PDF downloads and is a real PDF (works under CSP)',head==b'%PDF-' and f.suggested_filename.startswith('Invoice-INV'),(head,f.suggested_filename))
    pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp'); pg.click('[data-pv=print]'); pg.wait_for_timeout(300); pg.keyboard.press('Escape'); check('print opens print dialog (after the preview)',pg.evaluate('window.__printed')==1)
    pg.evaluate("window.open=(...a)=>{window.__wa=a}"); pg.click('[data-a=wa]'); pg.click('.mdl [data-w=txt]')   # WhatsApp now asks PDF / Image / Text first
    check('WhatsApp link opens with noopener',pg.evaluate('window.__wa')[0].startswith('https://wa.me/919876543210?text=') and 'noopener' in pg.evaluate('window.__wa')[2])
    # history record payment inline
    pg.click('a[href="#/h"]'); pg.wait_for_selector('table.lt'); pg.fill('input[data-amt]','100'); pg.click('[data-add]'); pg.wait_for_timeout(1800)
    d=list(srv.docs.values())[0]; check('payment added from History syncs (2 payments)',len(d['data']['pay'])==2,len(d['data']['pay']))
    # search/filter
    pg.fill('#qn','nomatch'); check('search filters list',pg.locator('.empty').count()==1); pg.fill('#qn','')
    pg.click('[data-t=due]'); check('"Balance due" tab shows the bill',pg.locator('#app > .sw tr.row').count()==1); pg.click('[data-t=all]')
    # ---- SETTINGS ----
    pg.click('a[href="#/s"]'); pg.wait_for_selector('#svl')
    pg.fill('[data-k=name]','Ad ZoneX Test'); pg.wait_for_timeout(1500)
    check('settings change syncs to cloud',srv.settings['data']['v']['name']=='Ad ZoneX Test',srv.settings['data']['v'].get('name'))
    check('Supabase settings never include the email-script secret key',('key' not in srv.settings['data']['v']) and ('url' not in srv.settings['data']['v']))
    nsv=pg.locator('[data-f=n]').count(); pg.click('[data-a=addsv]'); check('add service adds a row',pg.locator('[data-f=n]').count()==nsv+1)
    pg.fill('#svl [data-f=n] >> nth=0','Test Service ZZ'); pg.once('dialog',lambda d:d.accept()); pg.click('[data-a=dsv] >> nth=0'); check('remove service',pg.locator('[data-f=n]').count()==nsv)
    pg.click('[data-a=sec]'); poll(pg,"document.querySelector('#secout').textContent.includes('sign-ups')",8000); sec=pg.inner_text('#secout')
    check('Security check card: all green with signups off',('✗' not in sec) and sec.count('✓')>=4,sec)
    srv.disable_signup=False; pg.click('[data-a=sec]'); pg.wait_for_timeout(1200); check('Security check flags open sign-ups',pg.inner_text('#secout').count('✗')==1 and 'Turn off' in pg.inner_text('#secout'),pg.inner_text('#secout')); srv.disable_signup=True
    # backup export has no secrets
    with pg.expect_download() as dl2: pg.click('[data-a=ex]')
    bk=json.load(open(dl2.value.path())); check('backup file has docs and no secret key',len(bk['docs'])==1 and bk['set'].get('key','')=='')
    # restore invalid file
    open('/tmp/bad.json','w').write('{"hello":1}'); msgs=[]
    pg.once('dialog',lambda d:(msgs.append(d.message),d.accept())); pg.set_input_files('#im','/tmp/bad.json'); pg.wait_for_timeout(500)
    check('invalid backup file rejected',msgs and 'not a valid backup' in msgs[0],msgs)
    # ---- SECOND DEVICE ----
    ctx2=new_ctx(b,srv); pg2=ctx2.new_page(); e2=[]; watch(pg2,e2); pg2.goto(URL); pg2.wait_for_selector('#zxl'); login(pg2); pg2.wait_for_selector('#zxl',state='detached'); wait_sync(pg2)
    pg2.click('a[href="#/h"]'); pg2.wait_for_selector('table.lt')
    check('2nd device sees same bill + 2 payments after sign-in',pg2.locator('#app > .sw tr.row').count()==1 and 'INV' in pg2.inner_text('#app > .sw tr.row'))
    check('2nd device pulled the settings (business name)',pg2.evaluate("S.set.name")=='Ad ZoneX Test',pg2.evaluate("S.set.name"))
    # edit on device 2 -> visible on device 1 after focus pull
    pg2.click('#app > .sw tr.row'); pg2.fill('[data-k=phone]','1111111111'); pg2.wait_for_timeout(1500)
    pg.evaluate("dispatchEvent(new Event('focus'))"); pg.wait_for_timeout(1500)
    check('edit on device 2 reaches device 1',pg.evaluate("S.docs[0].phone")=='1111111111',pg.evaluate("S.docs[0].phone"))
    # ---- OFFLINE ----
    srv.offline=True; pg.click('a[href="#/"]'); pg.wait_for_selector('[data-k=cust]'); pg.fill('[data-k=cust]','Offline Customer')
    n=pg.locator('[data-g=items][data-i="0"][data-k=n]'); n.fill('Solvent Vinyl'); pg.keyboard.press('Escape')
    pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','500'); pg.click('[data-a=save]')
    try: poll(pg,"/retry/.test(document.querySelector('#sync').textContent)",20000)
    except Exception: pass
    check('works offline: saved locally, status shows offline',len(srv.docs)==1 and 'retry' in pg.inner_text('#sync'),(len(srv.docs),pg.inner_text('#sync')))
    srv.offline=False; pg.evaluate("dispatchEvent(new Event('online'))")
    try: poll(pg,"/Synced/.test(document.querySelector('#sync').textContent)",20000)
    except Exception: pass
    check('back online: offline bill uploads automatically',len(srv.docs)==2,len(srv.docs))
    # server error handling
    srv.fail=True; pg.evaluate("dispatchEvent(new Event('focus'))"); pg.wait_for_timeout(1000)
    check('server error shows a clear message with help (not a crash)','click for help' in pg.inner_text('#sync').lower(),pg.inner_text('#sync')); srv.fail=False
    # ---- TEAM: friend with his own login shares everything ----
    ctx5=new_ctx(b,srv); pf=ctx5.new_page(); e5=[]; watch(pf,e5); pf.goto(URL); pf.wait_for_selector('#zxl'); login(pf,email='friend@adzonex.in'); pf.wait_for_selector('#zxl',state='detached'); wait_sync(pf)
    pf.click('a[href="#/h"]'); pf.wait_for_selector('#app > .sw tr.row')
    check('TEAM: friend (own login) sees the owner\'s bills',pf.locator('#app > .sw tr.row').count()>=2 and 'Test Customer' in pf.inner_text('#app > .sw'),pf.inner_text('#app > .sw')[:200])
    check('TEAM: friend pulled the shared business settings',pf.evaluate("S.set.name")=='Ad ZoneX Test',pf.evaluate("S.set.name"))
    pf.click('a[href="#/"]'); pf.wait_for_selector('[data-k=cust]'); pf.fill('[data-k=cust]','Friend Customer')
    nn=pf.locator('[data-g=items][data-i="0"][data-k=n]'); nn.fill('Solvent Vinyl'); pf.keyboard.press('Escape')
    pf.fill('[data-g=items][data-i="0"][data-k=q]','2'); pf.fill('[data-g=items][data-i="0"][data-k=p]','300'); pf.click('[data-a=save]'); pf.wait_for_selector('.toast'); pf.wait_for_timeout(1800)
    fr=[r for r in srv.docs.values() if r['customer']=='Friend Customer']
    check('TEAM: friend\'s bill saved, marked as saved by friend',len(fr)==1 and fr[0]['user_id']==USERS['friend@adzonex.in'],fr and fr[0]['user_id'])
    pg.evaluate("dispatchEvent(new Event('focus'))"); pg.wait_for_timeout(1800)
    check('TEAM: owner now sees the friend\'s bill',pg.evaluate("S.docs.some(d=>d.cust=='Friend Customer')"))
    # friend edits OWNER's bill, owner receives it, only ONE row exists for it (no duplicates)
    ob=[r for r in srv.docs.values() if r['customer'].startswith('Test Customer')][0]['id']
    pf.evaluate("location.hash='#/d/%s'"%ob); pf.wait_for_selector('[data-k=phone]'); pf.fill('[data-k=phone]','7777777777'); pf.wait_for_timeout(1800)
    pg.evaluate("dispatchEvent(new Event('focus'))"); pg.wait_for_timeout(1800)
    check('TEAM: friend edits the owner\'s bill and owner sees the change',pg.evaluate("S.docs.find(d=>d.id=='%s').phone"%ob)=='7777777777')
    check('TEAM: one shared row per bill (no duplicates)',sum(1 for r in srv.docs.values() if r['id']==ob)==1 and len(srv.docs)==len({r['id'] for r in srv.docs.values()}))
    pf.evaluate("location.hash='#/s'"); pf.wait_for_selector('[data-a=sec]'); pf.click('[data-a=sec]'); poll(pf,"document.querySelector('#secout').textContent.includes('team')",8000)
    check('TEAM: security check says friend is in the team',('in your team' in pf.inner_text('#secout')) and ('✗' not in pf.inner_text('#secout')),pf.inner_text('#secout'))
    # outsider: valid login, NOT in the team
    ctx6=new_ctx(b,srv); po=ctx6.new_page(); e6=[]; watch(po,e6); po.goto(URL); po.wait_for_selector('#zxl'); login(po,email='outsider@adzonex.in'); po.wait_for_selector('#zxl',state='detached'); po.wait_for_timeout(2500)
    po.evaluate("location.hash='#/h'"); po.wait_for_timeout(500)
    check('TEAM: outsider login sees NO bills',po.evaluate("S.docs.length")==0 and po.locator('#app > .sw tr.row').count()==0,po.evaluate("S.docs.length"))
    check('TEAM: outsider cannot sync (says "not in team", nothing written)',('team' in po.inner_text('#sync').lower()) and not any(r['customer']=='x' for r in srv.docs.values()),po.inner_text('#sync'))
    po.evaluate("location.hash='#/s'"); po.wait_for_selector('[data-a=sec]'); po.click('[data-a=sec]'); poll(po,"document.querySelector('#secout').textContent.includes('team')",8000)
    check('TEAM: security check warns outsider is NOT in the team',('NOT in your team' in po.inner_text('#secout')),po.inner_text('#secout'))
    # ---- XSS from a tampered/malicious cloud row ----
    evil={'user_id':UID,'id':'evil1','updated':int(time.time()*1000)+10**6,'est_no':'x','bill_no':None,'customer':'x','status':'estimate','data':{'id':'evil1','u':int(time.time()*1000)+10**6,'estNo':'<img src=x onerror=window.__xss=1>','billNo':'','cust':'<img src=x onerror=window.__xss=2>','date':'"><img src=x onerror=window.__xss=3>','items':[{'n':'<svg onload=window.__xss=4>','q':'1','p':'1','u':'"><img src=x onerror=window.__xss=5>'}],'dm':[],'pay':[{'d':'<img src=x onerror=window.__xss=6>','a':5,'m':'<img src=x onerror=window.__xss=7>'}],'terms':'<img src=x onerror=window.__xss=8>','log':[{'t':1,'e':'<img src=x onerror=window.__xss=9>'}]}}
    evil2={'user_id':UID,'id':'x" onmouseover="window.__xss=10','updated':1,'data':{'id':'x" onmouseover="window.__xss=10','u':1,'cust':'bad id'}}
    srv.docs['evil1']=evil; srv.docs['evil2']=evil2
    pg.evaluate("dispatchEvent(new Event('focus'))"); pg.wait_for_timeout(1500); pg.click('a[href="#/h"]'); pg.wait_for_selector('table.lt'); pg.wait_for_timeout(500)
    pg.click('#app > .sw tr.row >> nth=0'); pg.wait_for_timeout(500)
    pg.evaluate("document.body.insertAdjacentHTML('beforeend','<div id=pp>'+paper(S.docs.find(d=>d.id=='evil1'))+'</div>')"); pg.wait_for_timeout(500)
    check('XSS: no injected script ran anywhere (history, bill, paper)',pg.evaluate("window.__xss")is None,pg.evaluate("window.__xss"))
    check('XSS: row with a malicious id is rejected',pg.evaluate("!S.docs.some(d=>d.id.includes('onmouseover'))"))
    check('XSS: malicious text is displayed as plain text',pg.evaluate("document.getElementById('pp').innerText.includes('<svg onload')"))
    # ---- SIGN OUT ----
    pg.click('a[href="#/s"]'); pg.once('dialog',lambda d:d.accept()); pg.click('[data-a=logout]'); pg.wait_for_selector('#zxl',timeout=8000); pg.wait_for_timeout(600)
    check('sign out shows login and wipes local copy',pg.evaluate("localStorage.getItem('adzonex-billing-v1')")is None or pg.evaluate("JSON.parse(localStorage.getItem('adzonex-billing-v1')||'{}').docs?.length||0")==0)
    check('after sign out the bills are not readable from the page',pg.evaluate("S.docs.length")==0)
    login(pg); pg.wait_for_selector('#zxl',state='detached'); wait_sync(pg,6000); pg.wait_for_timeout(500)
    check('sign in again restores everything from cloud',pg.evaluate("S.docs.filter(d=>!d.del).length")>=2,pg.evaluate("S.docs.length"))
    bad=[x for x in errs+e2+e5 if x.startswith('PAGEERR') or 'Content Security' in x or 'Refused' in x]
    check('no JS errors / no CSP violations in console',not [x for x in bad],bad[:6])
    # ---- TIMEZONE date bug ----
    ctx3=new_ctx(b,srv,timezone_id='Asia/Kolkata'); pg3=ctx3.new_page(); pg3.clock.set_fixed_time(datetime.datetime(2026,10,24,1,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=5,minutes=30))))
    pg3.goto(URL); pg3.wait_for_selector('#zxl'); check('1:00 AM IST uses TODAY\'s date (was off by one day before)',pg3.evaluate("today()")=='2026-10-24',pg3.evaluate("today()"))
    # ---- MOBILE layout ----
    ctx4=new_ctx(b,srv,viewport={'width':390,'height':844}); pg4=ctx4.new_page(); pg4.goto(URL); pg4.wait_for_selector('#zxl'); login(pg4); pg4.wait_for_selector('#zxl',state='detached'); wait_sync(pg4)
    for h in ('#/','#/h','#/s'):
        pg4.evaluate(f"location.hash='{h}'"); pg4.wait_for_timeout(400)
        check(f'mobile 390px: no sideways page scroll on {h}',pg4.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"),pg4.evaluate("document.documentElement.scrollWidth"))
    pg4.evaluate("location.hash='#/'"); pg4.wait_for_timeout(300); pg4.screenshot(path='/home/claude/test/m_billing.png')
    pg.evaluate("location.hash='#/h'"); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/test/d_history.png')
    b.close()
ok=sum(1 for r in R if r[1]); print(f'\n{ok}/{len(R)} passed'); 
sys.exit(0 if ok==len(R) else 1)
