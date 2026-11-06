"""Print preview (bill / history / expenses), month-wise history, editable expense titles, and the bug fixes of this update.
Run: serve the app folder on http://localhost:8123, then `python3 e2e9_preview.py` (needs mock.py on the path, see README)."""
import sys, time, re, json, subprocess
sys.path.insert(0, '/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
URL = 'http://localhost:8123/index.html'; R = []
def check(n, c, i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + ((' -> ' + str(i)[:400]) if (i and not c) else ''), flush=True)
def wait(pg, js, t=15000):
    end = time.time() + t / 1000
    while time.time() < end:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(120)
    return False
def ctx_for(b, srv, init=None):
    ctx = b.new_context(accept_downloads=True, service_workers='block', viewport={'width': 1280, 'height': 900}); ctx.route(SB + '/**', srv.handle)
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, body='', content_type='text/css')); ctx.route('https://fonts.gstatic.com/**', lambda r: r.abort())
    if init: ctx.add_init_script(init)
    return ctx
def login(pg):
    pg.fill('#zxl input[name=email]', 'owner@adzonex.in'); pg.fill('#zxl input[name=password]', 'Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl', state='detached')
    wait(pg, "/Synced/.test(document.querySelector('#sync').textContent)")
SEED = """()=>{const mk=(c,dt,p,pay)=>{const d=newDoc();d.cust=c;d.phone='9000000001';d.date=dt;d.items=[{n:'Logo Design',h:'998391',s:'',q:'1',u:'Nos',p:String(p)}];d.pay=pay?[{d:dt,a:pay,m:'Cash'}]:[];commit(d);fix(d);touch(d);return d.id};
 mk('Aug Customer','2026-08-12',1000,1000);mk('Sep Customer','2026-09-10',2000,500);mk('Sep Two','2026-09-21',3000,0);mk('Oct Customer','2026-10-05',4000,4000);mk('Oct Two','2026-10-25',500,100);}"""
PRINT_STUB = "window.print=()=>{window.__printed=(window.__printed||0)+1;window.__during=document.body.classList.contains('pj')&&!!document.querySelector('.pw .zp');window.__html=(document.querySelector('.pw')||{}).innerHTML||''}"
def native_init():
    return ("window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',registerPlugin:n=>({printPdf:async o=>{(window.__pr=window.__pr||[]).push(o)}}),"
            "Plugins:{Filesystem:{writeFile:async o=>({uri:'file:///c/'+o.path})},Share:{share:async o=>{(window.__sh=window.__sh||[]).push(o)}}}};")

with sync_playwright() as p:
    b = p.chromium.launch()
    srv = Server(); errs = []; dl = []
    ctx = ctx_for(b, srv, PRINT_STUB); pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: (dl.append(d.message), d.accept()))
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg)
    pg.evaluate(SEED); pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')

    # ------------------------------------------------------------ month wise on the History screen
    opts = pg.evaluate("[...document.querySelectorAll('#qm option')].map(o=>o.value)")
    check('History: month drop-down lists every month that has bills (newest first)', opts == ['', '2026-10', '2026-09', '2026-08'], opts)
    check('History: shows all 5 bills at first', pg.locator('#app > .sw tr.row').count() == 5)
    pg.select_option('#qm', '2026-09'); pg.wait_for_timeout(150)
    rows = pg.locator('#app > .sw tr.row').count(); txt = pg.inner_text('#app')
    check('History: choosing September shows only the 2 September bills', rows == 2 and 'Sep Customer' in txt and 'Oct Customer' not in txt, (rows,))
    check('History: top cards follow the month (Received = Rs 500)', '₹ 500.00' in pg.inner_text('.stats .hero') and 'September 2026' in pg.inner_text('.stats .hero'), pg.inner_text('.stats .hero'))
    pg.select_option('#qm', ''); pg.fill('#qd', '2026-10-05'); pg.dispatch_event('#qd', 'change'); pg.wait_for_timeout(150)
    check('History: picking an exact date clears the month and shows that day', pg.locator('#app > .sw tr.row').count() == 1 and pg.input_value('#qm') == '', pg.locator('#app > .sw tr.row').count())
    pg.fill('#qd', ''); pg.dispatch_event('#qd', 'change'); pg.wait_for_timeout(150)

    # ------------------------------------------------------------ print preview of the history
    pg.click('[data-a=ph]'); pg.wait_for_selector('.pvw .zp')
    check('Print history opens a PREVIEW (no print dialog yet)', pg.evaluate("window.__printed||0") == 0 and pg.locator('.pvw').count() == 1)
    pt = pg.inner_text('.pvw .zp')
    check('Preview shows the report: title, all 5 bills, totals', 'INVOICE HISTORY' in pt.upper() and all(x in pt for x in ['Aug Customer', 'Sep Two', 'Oct Two']) and '₹ 10,500.00' in pt, pt[:300])
    check('Preview has the month-wise summary (Aug, Sep, Oct rows with totals)', 'MONTH-WISE SUMMARY' in pt.upper() and 'August 2026' in pt and 'September 2026' in pt and 'October 2026' in pt and '₹ 5,000.00' in pt, pt[-700:])
    check('Preview has Print, Save PDF, Close buttons and a month picker', all(pg.locator(s).count() == 1 for s in ['[data-pv=print]', '[data-pv=pdf]', '[data-pv=x]', '.pvw [data-pm]']))
    check('Preview month picker offers: All months + each month', pg.evaluate("[...document.querySelectorAll('.pvw [data-pm] option')].map(o=>o.value)") == ['', '2026-10', '2026-09', '2026-08'])
    pg.select_option('.pvw [data-pm]', '2026-10'); pg.wait_for_timeout(200)
    pt = pg.inner_text('.pvw .zp')
    check('Preview: switching to October shows only October bills, no month summary', 'Oct Customer' in pt and 'Sep Customer' not in pt and 'MONTH-WISE SUMMARY' not in pt.upper() and 'October 2026' in pt, pt[:300])
    # print from the preview
    pg.click('[data-pv=print]'); pg.wait_for_timeout(500)
    check('Preview > Print opens the system print window with the report laid out', pg.evaluate("window.__printed") == 1 and pg.evaluate("window.__during"), pg.evaluate("[window.__printed,window.__during]"))
    check('page returns to normal after the print window closes', pg.evaluate("!document.querySelector('.pw')&&!document.body.classList.contains('pj')"))
    # what a printer really receives: with the preview still open
    pg.evaluate("""()=>{const w=document.createElement('div');w.className='pw';w.innerHTML=histPaper(histSel().L);document.body.append(w);document.body.classList.add('pj')}""")
    pg.wait_for_timeout(500); pdfb = pg.pdf(prefer_css_page_size=True, print_background=True); open('/tmp/hist_print.pdf', 'wb').write(pdfb)
    info = subprocess.run(['pdfinfo', '/tmp/hist_print.pdf'], capture_output=True, text=True).stdout; txt = subprocess.run(['pdftotext', '-layout', '/tmp/hist_print.pdf', '-'], capture_output=True, text=True).stdout
    check('print output: report on 1 A4 page, contains the bills, NOT the preview toolbar or app menu', int(re.search(r'Pages:\s+(\d+)', info).group(1)) == 1 and 'Oct Customer' in txt and 'Save PDF' not in txt and 'Calendar' not in txt and 'Settings' not in txt, txt[:300])
    pg.evaluate("document.body.classList.remove('pj');document.querySelectorAll('.pw').forEach(e=>e.remove())")
    # Save PDF
    with pg.expect_download() as di: pg.click('[data-pv=pdf]')
    dn = di.value; check('Preview > Save PDF downloads a PDF named after the month', dn.suggested_filename == 'Invoice-history-2026-10.pdf', dn.suggested_filename)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    check('Escape closes the preview and History now follows the chosen month (October)', pg.locator('.pvw').count() == 0 and pg.input_value('#qm') == '2026-10' and pg.locator('#app > .sw tr.row').count() == 2, (pg.input_value('#qm'),))
    check('History screen is usable again after the preview (not locked)', pg.evaluate("!document.querySelector('.shell').inert"))
    pg.select_option('#qm', '')

    # ------------------------------------------------------------ print preview of one bill (and estimates can be printed now)
    pg.click('#app > .sw tr.row [data-p] >> nth=0'); pg.wait_for_selector('.pvw .zp')
    check('History row Print icon opens a preview of that bill', pg.locator('.pvw [data-pm]').count() == 0 and re.search(r'(INVOICE|ESTIMATE)', pg.inner_text('.pvw .zp').upper()) is not None)
    pg.click('[data-pv=x]'); pg.wait_for_timeout(100)
    check('estimate rows have a Print icon too', pg.locator('#app > .sw tr.row [data-p]').count() == 5, pg.locator('#app > .sw tr.row [data-p]').count())
    pg.click('#app > .sw tr.row >> nth=0'); pg.wait_for_selector('#pa'); pg.click('[data-a=print]'); pg.wait_for_selector('.pvw .zp')
    check('Billing page Print opens the preview with the invoice number in it', 'INV' in pg.inner_text('.pvw .zp') or 'EST' in pg.inner_text('.pvw .zp'))
    n0 = pg.evaluate("window.__printed||0"); pg.click('[data-pv=print]'); pg.wait_for_timeout(400)
    check('Billing page: Print > system print window, bill laid out', pg.evaluate("window.__printed") == n0 + 1 and pg.evaluate("window.__during"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    check('Ctrl+P on a bill opens the same preview', (pg.keyboard.press('Control+p'), pg.wait_for_selector('.pvw .zp', timeout=3000))[1] is not None)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    check('printing is logged in the bill history (list refreshes when the preview closes)', 'Printed' in pg.inner_text('#app'), '')

    # ------------------------------------------------------------ expenses: pick month + editable titles
    pg.evaluate("location.hash='#/x'"); pg.wait_for_selector('#xa')
    def addx(d, c, n, a):
        pg.fill('#xd', d); pg.fill('#xc', c); pg.fill('#xn', n); pg.fill('#xa', str(a)); pg.click('[data-xa=add]'); pg.wait_for_timeout(150)
    pg.click('[data-xt=all]'); pg.wait_for_timeout(100)
    addx('2026-09-03', 'Fuel', 'van petrol', 500); addx('2026-09-18', 'fuel', 'bike petrol', 300); addx('2026-10-07', 'Material', 'vinyl roll', 4000); addx('2026-10-20', 'Fuel', 'petrol', 250)
    check('typing "fuel" reuses the existing title "Fuel" (no duplicate with a small f)', pg.evaluate("xAll().filter(x=>x.c.toLowerCase()=='fuel').every(x=>x.c=='Fuel')") and pg.evaluate("xAll().filter(x=>x.c=='Fuel').length") == 3)
    pg.click('[data-xt=mon]'); pg.wait_for_selector('#xmo')
    check('Pick month tab: month list contains the months that have expenses', {'2026-09', '2026-10'} <= set(pg.evaluate("[...document.querySelectorAll('#xmo option')].map(o=>o.value)")))
    pg.select_option('#xmo', '2026-09'); pg.wait_for_timeout(150)
    txt = pg.inner_text('#app')
    check('Pick month: September shows only September expenses with total Rs 800', 'van petrol' in txt and 'vinyl roll' not in txt and '₹ 800.00' in txt, txt[:500])
    # titles
    pg.click('#xtl summary'); pg.wait_for_timeout(100)
    check('Edit expense titles panel lists every title with how many expenses use it', pg.locator('[data-xcr]').count() >= 10 and pg.locator('[data-xcr="Fuel"]').count() == 1 and '3 used' in pg.inner_text('#xtl'), pg.inner_text('#xtl')[:300])
    check('"Other" is locked (cannot be renamed or deleted)', pg.locator('[data-xcr="Other"][readonly]').count() == 1 and pg.locator('[data-xcd="Other"]').count() == 0)
    pg.fill('[data-xcr="Fuel"]', 'Petrol & Diesel'); pg.press('[data-xcr="Fuel"]', 'Enter'); pg.wait_for_timeout(300)
    check('Renaming a title renames it on every past expense (3 of them)', pg.evaluate("xAll().filter(x=>x.c=='Petrol & Diesel').length") == 3 and pg.evaluate("xAll().filter(x=>x.c=='Fuel').length") == 0)
    check('panel stays open after renaming and shows the new name', pg.evaluate("document.querySelector('#xtl').open") and pg.locator('[data-xcr="Petrol & Diesel"]').count() == 1)
    check('the Category box suggestions use the new title', 'Petrol &amp; Diesel' in pg.evaluate("document.querySelector('#xcl').innerHTML") and 'value="Fuel"' not in pg.evaluate("document.querySelector('#xcl').innerHTML"))
    pg.fill('#xcn', 'Packing'); pg.press('#xcn', 'Enter'); pg.wait_for_timeout(250)
    check('Add title: "Packing" is added (Enter key works)', pg.locator('[data-xcr="Packing"]').count() == 1)
    pg.fill('#xcn', 'packing'); pg.click('[data-xca]'); pg.wait_for_timeout(150)
    check('Adding the same title again (any capitals) is refused', any('already exists' in m for m in dl) and pg.locator('[data-xcr]').filter(has_text='').count() >= 1)
    pg.fill('[data-xcr="Packing"]', 'material'); pg.press('[data-xcr="Packing"]', 'Enter'); pg.wait_for_timeout(250)
    check('Renaming into an existing title asks to merge (and is cancellable)', any('already exists' in m for m in dl[-2:]) )
    pg.click('[data-xcd="Material"]'); pg.wait_for_timeout(250)
    check('Delete a title moves its expenses to "Other"', pg.evaluate("xAll().filter(x=>x.n=='vinyl roll')[0].c") == 'Other' and pg.locator('[data-xcr="Material"]').count() == 0)
    check('Titles are in the settings that sync to the cloud', pg.evaluate("SH.includes('xcat')") and pg.evaluate("S.set.xcat.includes('Petrol & Diesel')"))
    wait(pg, "!S.pset&&pend.size==0&&/Synced/.test(document.querySelector('#sync').textContent)", 20000)
    saved = (srv.settings or {}).get('data', {}).get('v', {}).get('xcat', [])
    check('...and reached the cloud', 'Petrol & Diesel' in saved and 'Material' not in saved, saved)
    # a second device sees the new titles
    ctx2 = ctx_for(b, srv, PRINT_STUB); p2 = ctx2.new_page(); p2.on('pageerror', lambda e: errs.append(str(e))); p2.goto(URL); p2.wait_for_selector('#zxl'); login(p2); p2.wait_for_timeout(500)
    check('second device: gets the renamed titles and the renamed expenses', p2.evaluate("S.set.xcat&&S.set.xcat.includes('Petrol & Diesel')") and p2.evaluate("xAll().filter(x=>x.c=='Petrol & Diesel').length") == 3, p2.evaluate("[S.set.xcat,xAll().map(x=>x.c)]"))
    p2.close(); ctx2.close()
    # expense preview
    pg.click('[data-xe=prn]'); pg.wait_for_selector('.pvw .zp')
    pt = pg.inner_text('.pvw .zp')
    check('Expenses > Print opens a preview with the report for the month on screen (Sep)', 'EXPENSE REPORT' in pt.upper() and 'van petrol' in pt and 'vinyl roll' not in pt and 'Petrol & Diesel' in pt, pt[:300])
    pg.select_option('.pvw [data-pm]', ''); pg.wait_for_timeout(200); pt = pg.inner_text('.pvw .zp')
    check('Expense preview: All months shows both months and a month-wise summary', 'vinyl roll' in pt and 'MONTH-WISE SUMMARY' in pt.upper() and 'September 2026' in pt and 'October 2026' in pt and '₹ 5,050.00' in pt, pt[-500:])
    n0 = pg.evaluate("window.__printed||0"); pg.click('[data-pv=print]'); pg.wait_for_timeout(400)
    check('Expense preview > Print opens the system print window', pg.evaluate("window.__printed") == n0 + 1 and pg.evaluate("window.__during"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    check('closing the expense preview returns to the screen set in the preview (All)', pg.locator('[data-xt=all].on').count() == 1, '')

    # ------------------------------------------------------------ bug fixes
    # double click on "Add" in History must record the payment only once
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')
    did = pg.evaluate("S.docs.find(d=>!d.del&&d.cust=='Sep Two').id"); before = pg.evaluate("S.docs.find(d=>d.id=='%s').pay.length" % did)
    pg.fill('input[data-amt="%s"]' % did, '100'); pg.dblclick('[data-add="%s"]' % did); pg.wait_for_timeout(400)
    check('History > Add payment: a double click records ONE payment, not two', pg.evaluate("S.docs.find(d=>d.id=='%s').pay.length" % did) == before + 1, pg.evaluate("S.docs.find(d=>d.id=='%s').pay" % did))
    # backup restore keeps expenses added after the backup
    bk = pg.evaluate("JSON.stringify({...S,set:{...S.set,key:''}})")
    pg.evaluate("location.hash='#/x'"); pg.wait_for_selector('#xa'); pg.click('[data-xt=all]'); addx('2026-10-28', 'Rent', 'added after backup', 999)
    open('/tmp/bk.json', 'w').write(bk); pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('#im', state='attached')
    pg.set_input_files('#im', '/tmp/bk.json'); pg.wait_for_timeout(700)
    check('Restore backup: expenses added after the backup are NOT lost', pg.evaluate("xAll().some(x=>x.n=='added after backup')"), pg.evaluate("xAll().length"))
    check('no unexpected popups / JS errors during the whole run', not errs and not [m for m in dl if 'wrong' in m.lower() or 'could not' in m.lower()], (errs, dl))
    pg.close(); ctx.close()

    # ------------------------------------------------------------ phone app: Print inside the preview goes to the Android print dialog
    srv = Server(); errs = []; ctx = ctx_for(b, srv, native_init()); pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: d.accept())
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); pg.evaluate(SEED); pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')
    pg.click('[data-a=ph]'); pg.wait_for_selector('.pvw .zp')
    check('phone app: preview first, nothing sent to the printer yet', pg.evaluate("(window.__pr||[]).length") == 0)
    pg.click('[data-pv=print]'); ok = wait(pg, "window.__pr&&window.__pr.length>=1", 25000); last = pg.evaluate("window.__pr&&window.__pr[window.__pr.length-1]")
    check('phone app: Print in the preview sends the PDF to the phone print dialog', ok and last['data'].startswith('JVBERi') and last['name'].startswith('Invoice history'), last and last['name'])
    pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(300)
    bx = pg.evaluate("(()=>{const p=document.querySelector('#pvp').getBoundingClientRect();return [p.width,innerWidth]})()")
    check('phone screen: the page is scaled down to fit the width (no sideways scrolling)', bx[0] <= bx[1] - 12, bx)
    check('phone app: no JS errors', not errs, errs)
    b.close()
print('\n%d/%d passed' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
