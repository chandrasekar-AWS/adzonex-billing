import sys, time, json
sys.path.insert(0,'/home/claude/test')
from mock import *
from playwright.sync_api import sync_playwright
exec(open('/home/claude/test/e2e4.py').read().split("with sync_playwright() as p:")[0].split("R=[]")[1].split("def poll")[0]) if False else None
R=[]
def check(n,c,i=''):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n+((' -> '+str(i)) if (i and not c) else ''),flush=True)
srv=Server(); srv.legacy=True
for i in range(5):
    d={'id':'old%d'%i,'u':1000+i,'estNo':'202610-25%d'%(101+i),'billNo':'','cust':'Old %d'%i,'date':'2026-10-25','items':[{'n':'Logo Design','q':'1','p':'100','u':'','s':'','h':''}],'dm':[],'pay':[],'log':[],'terms':'t','gst':False,'rate':18}
    srv.docs[d['id']]={'user_id':UID,'id':d['id'],'updated':d['u'],'data':d,'est_no':d['estNo'],'bill_no':None,'customer':d['cust'],'status':'estimate'}
msgs=[]
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp('http://127.0.0.1:9333'); ctx=b.contexts[0]; pg=ctx.pages[0]
    ctx.route(SB+'/**',srv.handle); ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body='',content_type='text/css')); ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    pg.on('dialog',lambda d:(msgs.append(d.message),d.accept()))
    pg.reload(); pg.wait_for_selector('#zxl',timeout=15000)
    pg.fill('#zxl input[name=email]','owner@adzonex.in'); pg.fill('#zxl input[name=password]','Correct-Horse-9'); pg.click('#zxl button[type=submit]'); pg.wait_for_selector('#zxl',state='detached',timeout=10000); pg.wait_for_timeout(4000)
    check('Desktop app + older database: shows "Synced (not shared)" instead of an error',pg.inner_text('#sync')=='Synced (not shared)',pg.inner_text('#sync'))
    check('Desktop app: your earlier invoices are loaded (next number 106)',pg.evaluate("mkNo(today())").endswith('106'),pg.evaluate("mkNo(today())"))
    pg.fill('[data-k=cust]','Windows Customer'); c=pg.locator('[data-g=items][data-i="0"][data-k=n]'); c.fill('Logo Design'); pg.keyboard.press('Escape'); pg.fill('[data-g=items][data-i="0"][data-k=q]','1'); pg.fill('[data-g=items][data-i="0"][data-k=p]','800'); pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(3000)
    check('Desktop app: new invoice reaches the cloud',any(r['customer']=='Windows Customer' for r in srv.docs.values()))
    pg.click('#sync'); pg.wait_for_timeout(400)
    check('Desktop app: clicking the status explains what to do',msgs and 'supabase.sql' in msgs[-1],msgs[-1:])
    b.close()
print(sum(R),'/',len(R)); sys.exit(0 if all(R) else 1)
