"""Audit suite: probes for logic bugs, security weaknesses and robustness problems found during code review,
plus a randomized 'click everything' monkey test. Every check is PASS when the app behaves correctly.
Run: serve app on :8123, then  python3 e2e5_audit.py   (uses mock.py as the Supabase server)"""
import sys, json, time, re, random
sys.path.insert(0, '/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8123/index.html'
R = []
def check(name, cond, info=''):
    R.append((name, bool(cond), info))
    print(('PASS ' if cond else 'FAIL ') + name + (('  -> ' + str(info)[:300]) if (info and not cond) else ''), flush=True)

def new_ctx(b, srv, **kw):
    kw.setdefault('viewport', {'width': 1280, 'height': 900})
    ctx = b.new_context(accept_downloads=True, service_workers='block', **kw)
    ctx.route(SB + '/**', srv.handle)
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, body='', content_type='text/css'))
    ctx.route('https://fonts.gstatic.com/**', lambda r: r.abort())
    return ctx

def poll(pg, js, t=6000):
    end = time.time() + t / 1000
    while time.time() < end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(100)
    raise Exception('poll timeout: ' + js)
def wait_sync(pg, t=6000): poll(pg, "!!document.querySelector('#sync')&&/Synced/.test(document.querySelector('#sync').textContent)", t)

def fresh(b, srv=None, **kw):
    srv = srv or Server()
    ctx = new_ctx(b, srv, **kw)
    pg = ctx.new_page()
    errs, dialogs = [], []
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    def on_dialog(d):
        dialogs.append((d.type, d.message)); d.accept()
    pg.on('dialog', on_dialog)
    pg.add_init_script("window.print=()=>{window.__printed=(window.__printed||0)+1}")
    pg.goto(URL); pg.wait_for_selector('#zxl')
    pg.fill('#zxl input[name=email]', 'owner@adzonex.in'); pg.fill('#zxl input[name=password]', 'Correct-Horse-9'); pg.click('#zxl button[type=submit]')
    pg.wait_for_selector('#zxl', state='detached'); wait_sync(pg)
    return ctx, pg, srv, errs, dialogs

def add_row(pg, n='Normal Flex', s='8 x 4', q='2', p='12', i=0):
    pg.fill(f'[data-g=items][data-i="{i}"][data-k=n]', n); pg.keyboard.press('Escape')
    pg.fill(f'[data-g=items][data-i="{i}"][data-k=s]', s); pg.fill(f'[data-g=items][data-i="{i}"][data-k=q]', q); pg.fill(f'[data-g=items][data-i="{i}"][data-k=p]', p)

def make_estimate(pg, cust='Probe Co', **kw):
    pg.evaluate("location.hash='#/'"); pg.wait_for_selector('[data-k=cust]')
    pg.fill('[data-k=cust]', cust); add_row(pg, **kw)
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast')

with sync_playwright() as p:
    b = p.chromium.launch()

    # ---------- CALCULATION PROBES ----------
    ctx, pg, srv, errs, dialogs = fresh(b)
    pg.fill('[data-k=cust]', 'Calc Co')
    add_row(pg, 'Service A', '', '1', '-500')
    tot = pg.inner_text('#v-t'); sub0 = pg.inner_text('#v-s'); dsc0 = pg.inner_text('#v-d')
    check('a negative price cannot produce a negative sub total / discount / total', not re.search(r'-\s*[\d]', (tot + sub0).replace('₹', '')) and not re.search(r'₹\s*-', dsc0), (sub0, dsc0, tot))
    pg.fill('[data-g=items][data-i="0"][data-k=p]', '0.333'); pg.fill('[data-g=items][data-i="0"][data-k=q]', '1')
    pg.wait_for_timeout(100)
    # three rows of 0.333 each
    for i in (1, 2):
        pg.wait_for_selector(f'[data-g=items][data-i="{i}"][data-k=n]', state='attached') if pg.locator(f'[data-g=items][data-i="{i}"][data-k=n]').count() else None
        add_row(pg, f'Service {i}', '', '1', '0.333', i=i)
    shown = [pg.inner_text(f'[data-amt="items:{i}"]').strip() for i in range(3)]
    sub = pg.inner_text('#v-s').replace('₹', '').strip()
    check('sub total equals the sum of the printed line amounts (3 x 0.333)',
          abs(sum(float(x.replace(',', '')) for x in shown) - float(sub.replace(',', ''))) < 0.001, (shown, sub))
    r = pg.evaluate("""()=>{const d=newDoc();d.items=[{n:'Banner',h:'',s:'2 x 3',q:'1',u:'Sqm',p:'10'}];d.gst=false;d.pay=[{d:'2026-01-01',a:5,m:'Cash'}];return paper(d)}""")
    check('area for a Sqm item is not labelled "sqft"', 'sqft' not in r.lower(), re.findall(r'\(\d[^)]*\)', r)[:2])
    check('two new bills made in the same millisecond get different ids', pg.evaluate("(()=>{const a=newDoc(),b=newDoc();return a.id!==b.id})()"))
    pg.close(); ctx.close()

    # ---------- PAYMENT / MAIL FLOW PROBES ----------
    ctx, pg, srv, errs, dialogs = fresh(b)
    make_estimate(pg, 'Pay Probe', q='1', s='', p='1000', n='Service A')
    pg.evaluate("S.set.url='https://script.google.com/macros/s/AKfycbTEST/exec';S.set.auto=true;S.set.copy=''")
    pg.click('tr.row >> nth=0'); pg.wait_for_selector('#pa')
    dialogs.clear()
    pg.fill('#pa', '5000'); pg.click('[data-a=pay]'); pg.wait_for_timeout(800)
    kinds = [k for k, m in dialogs]
    check('recording a payment bigger than the total asks for confirmation (Billing page)', 'confirm' in kinds, dialogs)
    dialogs.clear()
    pg.evaluate("S.docs[0].pay=[];fix(S.docs[0]);route()"); pg.wait_for_selector('#pa'); dialogs.clear()
    pg.fill('#pa', '100'); pg.click('[data-a=pay]'); pg.wait_for_timeout(1200)
    check('auto-email with nobody to send to does not pop up an alert after every payment', not any(k == 'alert' for k, m in dialogs), dialogs)
    # date cleared
    pg.evaluate("location.hash='#/'"); pg.wait_for_selector('[data-k=cust]')
    pg.fill('[data-k=cust]', 'No Date'); add_row(pg, q='1', s='', p='50'); pg.fill('[data-k=date]', '')
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast')
    check('saving with the date field cleared falls back to a real date', pg.evaluate("/^\\d{4}-\\d{2}-\\d{2}$/.test(S.docs[0].date)"), pg.evaluate("S.docs[0].date"))
    # deleted bill must not be reachable by URL
    did = pg.evaluate("S.docs[0].id"); pg.evaluate("S.docs[0].del=1;touch(S.docs[0])")
    pg.evaluate(f"location.hash='#/d/{did}'"); pg.wait_for_timeout(300)
    check('a deleted bill cannot be opened/edited through its old link', pg.evaluate("!document.querySelector('[data-a=rm]')"))
    check('no JS errors in payment/mail flows', not errs, errs)
    pg.close(); ctx.close()

    # ---------- BACKUP RESTORE ABUSE ----------
    ctx, pg, srv, errs, dialogs = fresh(b)
    make_estimate(pg, 'Local Only Co', q='1', s='', p='10', n='X')
    pg.evaluate("S.set.url='https://script.google.com/macros/s/MINE/exec'")
    pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('#im', state='attached')
    bad = {'docs': [{'id': 'r1', 'u': 5, 'cust': 'From Backup', 'items': [None, 5, {'n': 'ok', 'q': '1', 'p': '9'}], 'dm': 'x', 'pay': [None]}],
           'set': {'name': 'Backup Biz', 'url': 'https://script.google.com/macros/s/ATTACKER/exec', 'colors': None, 'services': [None, 3], 'ne': '"><img id=pwn src=x>'}}
    pg.set_input_files('#im', files=[{'name': 'b.json', 'mimeType': 'application/json', 'buffer': json.dumps(bad).encode()}])
    pg.wait_for_timeout(1200)
    check('restoring a backup does NOT silently replace the email-script URL (your login token is sent there)',
          pg.evaluate("(S.set.url||'').indexOf('ATTACKER')<0"), pg.evaluate("S.set.url"))
    check('restoring a backup keeps bills that exist only on this device', pg.evaluate("S.docs.some(d=>d.cust=='Local Only Co')"))
    for h in ('#/', '#/h', '#/s'):
        pg.evaluate(f"location.hash='{h}'"); pg.wait_for_timeout(250)
    check('app still works after restoring a malformed backup (no crash on any page)', not errs, errs)
    check('markup in a numeric setting cannot inject elements', pg.evaluate("!document.getElementById('pwn')"))
    pg.close(); ctx.close()

    # ---------- MALICIOUS / MALFORMED CLOUD DATA ----------
    srv = Server()
    srv.docs['bad1'] = {'id': 'bad1', 'user_id': UID, 'updated': 9, 'data': {'id': 'bad1', 'u': 9, 'cust': 'Mal', 'items': [None, 5, 'x'], 'dm': 'q', 'pay': [None, {'a': 'x'}], 'date': '2026-01-01'}, 'status': 'estimate'}
    srv.settings = {'id': 'main', 'user_id': UID, 'updated': 99999999999999, 'data': {'u': 99999999999999, 'v': {'name': 'Mal Biz', 'ne': '"><img id=pwn src=x>', 'colors': None, 'services': [None, {'n': 5}], 'bw': 'yes'}}}
    ctx, pg, srv, errs, dialogs = fresh(b, srv)
    pg.wait_for_timeout(800)
    for h in ('#/h', '#/s', '#/', '#/d/bad1'):
        pg.evaluate(f"location.hash='{h}'"); pg.wait_for_timeout(300)
    check('malformed bills/settings from the cloud do not crash the app', not errs, errs)
    check('markup in cloud settings cannot inject elements', pg.evaluate("!document.getElementById('pwn')"))
    pg.close(); ctx.close()

    # ---------- SYNC CHATTER ----------
    ctx, pg, srv, errs, dialogs = fresh(b)
    n0 = len([l for l in srv.log if l[1] == '/rest/v1/docs' and l[0] == 'GET'])
    for _ in range(6): pg.evaluate("window.dispatchEvent(new Event('focus'))")
    pg.wait_for_timeout(1500)
    n1 = len([l for l in srv.log if l[1] == '/rest/v1/docs' and l[0] == 'GET'])
    check('switching windows 6 times does not trigger 6 full downloads of every bill', (n1 - n0) <= 2, n1 - n0)
    pg.close(); ctx.close()

    # ---------- CLICKJACKING / EMBEDDING ----------
    ctx = new_ctx(b, Server()); pg = ctx.new_page()
    ctx.route('http://localhost:8123/_frame.html', lambda r: r.fulfill(status=200, content_type='text/html', body='<iframe id=f src="/index.html" width=900 height=700></iframe>'))
    pg.goto('http://localhost:8123/_frame.html'); pg.wait_for_timeout(2500)
    fr = [f for f in pg.frames if f.url.endswith('/index.html')]
    loaded = bool(fr)
    ui_shown = bool(fr) and fr[0].evaluate("!!document.querySelector('#zxl') || !!document.querySelector('.shell:not([hidden])')")
    framed_login_usable = bool(fr) and fr[0].evaluate("!!document.querySelector('#zxl input[type=password]')")
    check('(test sanity) the framed page really loaded', loaded)
    check("app refuses to show its login form / UI inside someone else's frame (clickjacking)", loaded and not framed_login_usable, 'login form rendered inside iframe')
    pg.close(); ctx.close()

    # ---------- CSP EFFECTIVENESS ----------
    ctx, pg, srv, errs, dialogs = fresh(b)
    pol = pg.evaluate("document.querySelector('meta[http-equiv=Content-Security-Policy]').content")
    ss = re.search(r"script-src ([^;]*)", pol).group(1)
    r = pg.evaluate("""async()=>{const o={};
      try{await fetch('https://evil.example/x',{mode:'no-cors'});o.fetch='allowed'}catch(e){o.fetch='blocked'}
      const s=document.createElement('script');s.textContent='window.__x=1';document.body.append(s);o.inline=window.__x?'allowed':'blocked';
      const i=document.createElement('img');i.src='https://evil.example/p.png';document.body.append(i);await new Promise(r=>setTimeout(r,300));o.img=i.complete&&i.naturalWidth>0?'allowed':'blocked';
      return o}""")
    check("CSP: script-src is 'self' only (no unsafe-inline / unsafe-eval)", ss.strip() == "'self'", ss)
    check('CSP blocks inline script, calls and images to other sites', r == {'fetch': 'blocked', 'inline': 'blocked', 'img': 'blocked'}, r)
    pg.close(); ctx.close()

    # ---------- MONKEY TEST ----------
    random.seed(7)
    ctx, pg, srv, errs, dialogs = fresh(b)
    make_estimate(pg, 'Monkey Co', q='2', s='8 x 4', p='10')
    junk = ['', '0', '-1', '1e3', '99999999999', 'abc', '<img src=x onerror=alert(1)>', '"\'><svg/onload=1>', '0.001', ' ', 'x' * 300, '8 x', 'x x x', '3 * 4', '１２']
    acts = 0; stuck = 0
    for rnd in range(70):
        pg.evaluate(f"location.hash='{random.choice(['#/', '#/h', '#/s', '#/', '#/s'])}'"); pg.wait_for_timeout(40)
        els = pg.query_selector_all('#app button:not([disabled]), #app input:not([type=file]):not([readonly]), #app select, #app textarea, #app .row')
        if not els: stuck += 1; continue
        for el in random.sample(els, min(3, len(els))):
            try:
                if not el.is_visible(): continue
                tag = el.evaluate('e=>e.tagName+(e.type?":"+e.type:"")+"|"+(e.dataset.a||"")')
                if '|logout' in tag: continue          # signing out would end the session; covered by other suites
                if '|rs' in tag or '|rm' in tag or '|clr' in tag or '|dsv' in tag: pass   # destructive ones are fine - dialogs auto-accept
                if tag.startswith('INPUT:checkbox'): el.click(timeout=800)
                elif tag.startswith('INPUT:color'): el.evaluate("(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}", random.choice(['#ff0000', '#ffffff', '#000000']))
                elif tag.startswith('INPUT:date'): el.fill(random.choice(['2026-02-30', '2025-12-31', '']), timeout=800)
                elif tag.startswith('INPUT') or tag.startswith('TEXTAREA'): el.fill(random.choice(junk), timeout=800)
                elif tag.startswith('SELECT'):
                    opts = el.evaluate("e=>[...e.options].map(o=>o.value||o.text)"); el.select_option(random.choice(opts), timeout=800)
                else: el.click(timeout=800)
                acts += 1
            except Exception as ex:
                pass
        pg.wait_for_timeout(20)
    check('monkey test: ~%d random clicks / inputs across Billing, History, Settings -> no JS errors' % acts, not errs, errs[:5])
    check('monkey test: app still responds afterwards', pg.evaluate("document.querySelector('#app').children.length>0"))
    pg.close(); ctx.close()
    b.close()

ok = sum(1 for _, c, _ in R if c)
print(f'\n{ok}/{len(R)} passed')
