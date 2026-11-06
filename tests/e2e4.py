import sys, time, json, re
sys.path.insert(0,'/home/claude/test')
exec(open('/home/claude/test/e2e.py').read().split("with sync_playwright() as p:")[0])
R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)) if (i and not c) else ''),flush=True)
def poll(pg,js,t=15000):
    end=time.time()+t/1000
    while time.time()<end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(120)
    return False
def txt(pg): return pg.inner_text('#sync')
def seed(srv,n=5):
    for i in range(n):
        d={'id':'old%d'%i,'u':1000+i,'estNo':'202610-25%d'%(101+i),'billNo':'','cust':'Old %d'%i,'date':'2026-10-25','items':[{'n':'Logo Design','q':'1','p':'100','u':'','s':'','h':''}],'dm':[],'pay':[],'log':[],'terms':'t','gst':False,'rate':18}
        srv.docs[d['id']]={'user_id':UID,'id':d['id'],'updated':d['u'],'data':d,'est_no':d['estNo'],'bill_no':None,'customer':d['cust'],'status':'estimate'}
def newdoc(pg,name):
    pg.evaluate("location.hash='#/'"); pg.wait_for_selector('[data-k=cust]'); pg.fill('[data-k=cust]',name)
    c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','700'); pg.click('[data-a=save]'); pg.wait_for_selector('.toast')
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    # ===== A) database still the OLDER PRIVATE layout (what a not-yet-upgraded Supabase looks like) =====
    srv=Server(); srv.legacy=True; seed(srv); ctx=new_ctx(b,srv); pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    msgs=[]; pg.on('dialog',lambda d:(msgs.append(d.message),d.accept()))
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); poll(pg,"/Synced|problem|help/i.test(document.querySelector('#sync').textContent)")
    poll(pg,"/Synced/.test(document.querySelector('#sync').textContent)",8000)
    check('older database: app still syncs (shows "Synced (not shared)")',txt(pg)=='Synced (not shared)',txt(pg))
    check('older database: earlier invoices are loaded and numbering continues (106)',pg.evaluate("no(newDoc())")=='EST202610-26106' or pg.evaluate("mkNo(today())").endswith('106'),pg.evaluate("mkNo(today())"))
    newdoc(pg,'Legacy Customer'); pg.wait_for_timeout(2500)
    check('older database: new invoice is saved to the cloud',any(r['customer']=='Legacy Customer' for r in srv.docs.values()),txt(pg))
    check('older database: settings saved in the old layout (no id column)',srv.settings is not None and 'id' not in srv.settings)
    pg.click('#sync'); pg.wait_for_timeout(300)
    check('click on status explains the problem and the fix',msgs and 'older private version' in msgs[-1] and 'supabase.sql' in msgs[-1],msgs[-1:] )
    pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-a=test]')
    check('Settings shows the "not shared" notice',('not shared' in pg.inner_text('#app')))
    pg.click('[data-a=sec]'); poll(pg,"document.querySelector('#secout').textContent.includes('team')||document.querySelector('#secout').textContent.includes('private')",8000)
    check('security check tells you to upgrade the database',('older private version' in pg.inner_text('#secout')),pg.inner_text('#secout'))
    srv.legacy=False   # <- the owner runs supabase.sql
    pg.click('[data-a=test]'); poll(pg,"document.querySelector('#sync').textContent=='Synced'",10000)
    check('after supabase.sql is run, Sync now switches to shared mode',txt(pg)=='Synced' and 'not shared' not in pg.inner_text('#app'),txt(pg))
    newdoc(pg,'Shared Customer'); pg.wait_for_timeout(2500)
    check('shared mode saves normally again',any(r['customer']=='Shared Customer' for r in srv.docs.values()))
    ctx.close()
    # ===== B) login that is NOT in the team =====
    srv=Server(); seed(srv); ctx=new_ctx(b,srv); pg=ctx.new_page(); msgs=[]; pg.on('dialog',lambda d:(msgs.append(d.message),d.accept()))
    pg.goto(URL); pg.wait_for_selector('#zxl'); pg.fill('#zxl input[name=email]','outsider@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached')
    poll(pg,"/team/i.test(document.querySelector('#sync').textContent)",8000)
    check('not in team: status says so right away (no silent empty app)',('team' in txt(pg).lower()),txt(pg))
    pg.click('#sync'); pg.wait_for_timeout(300)
    check('not in team: help shows the exact SQL with THIS login\'s email',msgs and "email = 'outsider@adzonex.in'" in msgs[-1] and 'public.team' in msgs[-1],msgs[-1:])
    srv.team.add(USERS['outsider@adzonex.in']); pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-a=test]'); pg.click('[data-a=test]'); poll(pg,"document.querySelector('#sync').textContent=='Synced'",10000)
    check('after being added to the team, Sync now works and loads the bills',txt(pg)=='Synced' and pg.evaluate("S.docs.length")==5,(txt(pg),pg.evaluate("S.docs.length")))
    ctx.close()
    # ===== C) tables missing =====
    srv=Server(); srv.notables=True; ctx=new_ctx(b,srv); pg=ctx.new_page(); msgs=[]; pg.on('dialog',lambda d:(msgs.append(d.message),d.accept()))
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); poll(pg,"/not set up/i.test(document.querySelector('#sync').textContent)",8000)
    check('tables missing: status says "Database not set up"',('not set up' in txt(pg)),txt(pg))
    pg.click('#sync'); pg.wait_for_timeout(300); check('tables missing: help points to supabase.sql',msgs and 'supabase.sql' in msgs[-1])
    srv.notables=False; pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-a=test]'); pg.click('[data-a=test]'); poll(pg,"document.querySelector('#sync').textContent=='Synced'",10000)
    check('tables missing: works once the SQL has been run',txt(pg)=='Synced',txt(pg))
    ctx.close()
    # ===== D) session expires while the app is open =====
    srv=Server(); ctx=new_ctx(b,srv); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); poll(pg,"document.querySelector('#sync').textContent=='Synced'",8000)
    r0=srv.refreshes; srv.expire_once=True; newdoc(pg,'After Expiry'); pg.wait_for_timeout(3500)
    check('expired login token is renewed automatically and the save still goes through',any(r['customer']=='After Expiry' for r in srv.docs.values()) and srv.refreshes>r0,(srv.refreshes,r0))
    ctx.close()
    # ===== E) offline =====
    srv=Server(); ctx=new_ctx(b,srv); pg=ctx.new_page(); msgs=[]; pg.on('dialog',lambda d:(msgs.append(d.message),d.accept())); pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); poll(pg,"document.querySelector('#sync').textContent=='Synced'",8000)
    srv.offline=True; newdoc(pg,'Offline Doc'); poll(pg,"/Offline|problem/.test(document.querySelector('#sync').textContent)",25000)
    check('offline: saved locally and status is "Offline, will retry"',pg.evaluate("S.docs.some(d=>d.cust=='Offline Doc')") and 'ffline' in txt(pg),txt(pg))
    pg.click('#sync'); pg.wait_for_timeout(300); check('offline: help says the work is safe on this device',msgs and 'saved on this device' in msgs[-1],msgs[-1:])
    srv.offline=False; pg.evaluate("dispatchEvent(new Event('online'))"); poll(pg,"document.querySelector('#sync').textContent=='Synced'",25000); pg.wait_for_timeout(600)
    check('offline: uploads by itself when the connection returns',any(r['customer']=='Offline Doc' for r in srv.docs.values()))
    check('no JS errors',not errs,errs[:3])
    b.close()
print(sum(R),'/',len(R)); sys.exit(0 if all(R) else 1)
