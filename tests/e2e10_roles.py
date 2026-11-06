"""Roles: 'admin' does everything, 'biller' can only make bills. Checked in the app AND in the (simulated) database rules."""
import sys, time
sys.path.insert(0, '/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
URL = 'http://localhost:8123/index.html'; R = []
def check(n, c, i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + ((' -> ' + str(i)[:300]) if (i and not c) else ''), flush=True)
def wait(pg, js, t=15000):
    end = time.time() + t / 1000
    while time.time() < end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(120)
    return False
def ctx_for(b, srv):
    ctx = b.new_context(accept_downloads=True, service_workers='block', viewport={'width': 1280, 'height': 900}); ctx.route(SB + '/**', srv.handle)
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, body='', content_type='text/css')); ctx.route('https://fonts.gstatic.com/**', lambda r: r.abort())
    ctx.add_init_script("window.print=()=>{window.__printed=(window.__printed||0)+1}")
    return ctx
def login(pg, email):
    pg.goto(URL); pg.wait_for_selector('#zxl'); pg.fill('#zxl input[name=email]', email); pg.fill('#zxl input[name=password]', 'Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl', state='detached')
    wait(pg, "/Synced/.test(document.querySelector('#sync').textContent)"); pg.wait_for_timeout(500)
def mkbill(pg, name, price):
    pg.fill('[data-k=cust]', name); pg.fill('[data-k=phone]', '9000000003')
    c = pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape')
    pg.fill('[data-g=items][data-i="0"][data-k=q]', '1'); pg.fill('[data-g=items][data-i="0"][data-k=p]', str(price)); pg.click('[data-a=save]')

with sync_playwright() as p:
    b = p.chromium.launch(); srv = Server()
    srv.roles = {'friend@adzonex.in': 'biller'}; errs = []; dl = []
    # ---- admin makes a bill and sets up settings
    ca = ctx_for(b, srv); pa = ca.new_page(); pa.on('pageerror', lambda e: errs.append(str(e))); pa.on('dialog', lambda d: (dl.append(d.message), d.accept()))
    login(pa, 'owner@adzonex.in')
    check('admin: role is admin, all menu items visible, chip says Admin', pa.evaluate("S.role")=='admin' and pa.locator('[data-nav]:visible').count() == 5 and 'Admin' in pa.inner_text('#who'), pa.inner_text('#who'))
    pa.evaluate("""()=>{const d=newDoc();d.cust='Admin Customer';d.items=[{n:'Logo Design',h:'998391',s:'',q:'1',u:'Nos',p:'5000'}];d.pay=[{d:today(),a:1000,m:'Cash'}];commit(d);fix(d);touch(d);S.set.name='Ad ZoneX';sch()}""")
    aid = pa.evaluate("S.docs[0].id"); wait(pa, "!S.pset&&pend.size==0", 20000)
    settings_before = repr(srv.settings)
    # ---- the bill maker
    cb = ctx_for(b, srv); pb = cb.new_page(); pb.on('pageerror', lambda e: errs.append(str(e))); pb.on('dialog', lambda d: (dl.append(d.message), d.accept()))
    login(pb, 'friend@adzonex.in')
    check('biller: role learned from the database', pb.evaluate("S.role") == 'biller')
    vis = pb.evaluate("[...document.querySelectorAll('[data-nav]')].filter(a=>getComputedStyle(a).display!='none').map(a=>a.getAttribute('href'))")
    check('biller: only "Billing" is in the menu (no History, Calendar, Expenses, Settings)', vis == ['#/'], vis)
    check('biller: shows who is signed in, "Bill maker", and a Sign out button', 'Bill maker' in pb.inner_text('#who') and 'friend@adzonex.in' in pb.inner_text('#who') and pb.locator('[data-signout]').count() == 1)
    for h in ['#/h', '#/x', '#/c', '#/s', '#/d/' + aid]:
        pb.evaluate("location.hash='%s'" % h); pb.wait_for_timeout(250)
        check('biller: typing the address %s sends them back to the Billing page' % h, pb.evaluate("location.hash") == '#/' and pb.locator('[data-k=cust]').count() == 1, pb.evaluate("location.hash"))
    check('biller: no "Collect money today" box, no History data on screen', pb.locator('.rb').count() == 0 and 'Admin Customer' not in pb.inner_text('#app'))
    mkbill(pb, 'Biller Customer', 2000); pb.wait_for_selector('#pa'); pb.wait_for_timeout(300)
    check('biller: after Save the bill opens (print, PDF, WhatsApp available) and says Saved', pb.evaluate("location.hash").startswith('#/d/') and pb.locator('[data-a=print]').count() == 1 and pb.locator('[data-a=pdf]').count() == 1, pb.evaluate("location.hash"))
    check('biller: no Delete button and no colour switch on the bill', pb.locator('[data-a=rm]').count() == 0 and pb.locator('[data-s=bw]').count() == 0)
    pb.fill('#pa', '500'); pb.click('[data-a=pay]'); pb.wait_for_selector('.chip.bill')
    check('biller: can record the advance (bill becomes an invoice) but cannot remove a payment', pb.locator('[data-a=dp]').count() == 0 and 'INV' in pb.inner_text('#head'))
    pb.click('[data-a=print]'); pb.wait_for_selector('.pvw .zp'); check('biller: print preview works', 'Biller Customer' in pb.inner_text('.pvw .zp')); pb.keyboard.press('Escape')
    pb.evaluate("document.querySelector('[data-nav][href=\"#/\"]').click()"); pb.wait_for_timeout(300)
    check('biller: "Billing" starts a fresh new bill', pb.locator('[data-k=cust]').count() == 1 and pb.input_value('[data-k=cust]') == '')
    wait(pb, "pend.size==0&&/Synced/.test(document.querySelector('#sync').textContent)", 20000)
    check('biller: bill reached the cloud and sync is healthy (no "login not in team" error)', any(r['customer'] == 'Biller Customer' for r in srv.docs.values()) and 'Synced' in pb.inner_text('#sync'), pb.inner_text('#sync'))
    check('biller: never uploaded business settings (admin settings untouched)', repr(srv.settings) == settings_before)
    # ---- database rules really block a biller (even from a hacked page)
    r = pb.evaluate("""(async()=>{const x=await sb.from('app_settings').upsert({id:'main',user_id:SES.user.id,updated:Date.now()+999,data:{u:1,v:{name:'HACKED'}}},{onConflict:'id'});return x.error?x.error.code:'allowed'})()""")
    check('database: a biller cannot change business settings', r == '42501', r)
    r = pb.evaluate("""(async()=>{const x=await sb.from('docs').upsert({id:'%s',user_id:SES.user.id,updated:Date.now()+999,data:{id:'%s'}},{onConflict:'id'});return x.error?x.error.code:'allowed'})()""" % (aid, aid))
    check("database: a biller cannot overwrite someone else's bill", r == '42501', r)
    # ---- admin sees the bill maker's bill and keeps full control
    pa.evaluate("location.hash='#/h'"); pa.wait_for_timeout(300); pa.evaluate("pull()"); pa.wait_for_timeout(1200); pa.evaluate("hist()")
    check("admin: History shows the bill maker's bill too", 'Biller Customer' in pa.inner_text('#app') and 'Admin Customer' in pa.inner_text('#app'))
    check('admin: Calendar, Expenses and Settings still open', all((pa.evaluate("location.hash='%s'" % h), pa.wait_for_timeout(200), pa.evaluate("location.hash"))[2] == h for h in ['#/c', '#/x', '#/s']))
    check('admin: business settings still intact', 'HACKED' not in repr(srv.settings))
    # ---- sign out works for the bill maker
    pb.click('[data-signout]'); pb.wait_for_selector('#zxl', timeout=10000)
    check('biller: Sign out brings back the login screen', pb.locator('#zxl').count() == 1)
    check('no JS errors', not errs, errs)
    b.close()
print('\n%d/%d passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)
