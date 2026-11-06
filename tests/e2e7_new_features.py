from playwright.sync_api import sync_playwright
import json,datetime
T=datetime.date.today().isoformat()
errs=[];res=[]
def ok(c,m):
    res.append((bool(c),m));print(('PASS ' if c else 'FAIL ')+m)
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1300,'height':900},accept_downloads=True,permissions=['clipboard-read','clipboard-write'])
    pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'supabase' not in m.text.lower() and 'Failed to load resource' not in m.text else None)
    pg.route('**/*supabase.co/**',lambda r:r.abort())
    ctx.route('**/wa.me/**',lambda r:r.fulfill(status=200,body='ok'))   # no internet needed for the test
    pg.route('**/fonts.g*/**',lambda r:r.abort())
    pg.goto('http://localhost:8123/index.html');pg.wait_for_timeout(800)
    pg.evaluate("()=>{const o=document.querySelector('#zxl');if(o)o.remove();document.querySelector('.shell').inert=false}")
    nav=pg.eval_on_selector_all('nav a span','e=>e.map(x=>x.textContent)');ok(nav==['Billing','History','Calendar','Expenses','Settings'],'nav '+str(nav))
    # billing page: no signature card on new bill
    ok(pg.locator('text=Upload signature').count()==0,'no upload signature on new bill')
    ok(pg.locator('textarea[data-k=rem]').count()==1,'remark box present')
    # fill bill
    pg.fill('input[data-k=cust]','Ravi');pg.fill('input[data-k=phone]','9876543210')
    pg.fill('input[data-g=items][data-i="0"][data-k=n]','Normal Flex');pg.wait_for_timeout(200);pg.keyboard.press('Enter')
    pg.fill('input[data-g=items][data-i="0"][data-k=s]','8 x 8');pg.fill('input[data-g=items][data-i="0"][data-k=q]','1');pg.fill('input[data-g=items][data-i="0"][data-k=p]','100')
    pg.fill('textarea[data-k=rem]','Deliver before Friday')
    pg.click('button[data-a=save]');pg.wait_for_timeout(500)
    ok(pg.url.endswith('#/h'),'saved -> history')
    d=pg.evaluate("()=>JSON.parse(localStorage.getItem('adzonex-billing-v1')).docs[0]");ok(d['rem']=='Deliver before Friday','remark stored')
    # open bill, signature card visible on saved, record payment
    pg.click('tr.row');pg.wait_for_timeout(300)
    ok(pg.locator('text=Upload signature').count()==1,'signature card on saved bill')
    pg.fill('#pa','2000');pg.click('button[data-a=pay]');pg.wait_for_timeout(500)
    ok(pg.locator('button[data-a=wa]').count()==1,'wa icon after payment')
    html=pg.evaluate("()=>paper(S.docs[0])");ok('Deliver before Friday' in html and 'Remark' in html,'remark in printed paper')
    # whatsapp modal
    pg.click('button[data-a=wa]');pg.wait_for_timeout(200)
    ok(pg.locator('.mdl [data-w=pdf]').count()==1 and pg.locator('.mdl [data-w=img]').count()==1 and pg.locator('.mdl [data-w=txt]').count()==1,'wa modal has pdf/image/text')
    with ctx.expect_page() as np_:
        pg.click('[data-w=txt]')
    w=np_.value;ok('wa.me/919876543210?text=' in w.url or 'wa.me' in w.url,'text opens wa.me chat: '+w.url[:60]);w.close()
    pg.click('button[data-a=wa]');pg.wait_for_timeout(200)
    with pg.expect_download(timeout=60000) as dl:
        pg.click('[data-w=pdf]')
    f=dl.value;ok(f.suggested_filename.endswith('.pdf'),'pdf downloaded '+f.suggested_filename)
    pg.wait_for_selector('#wgo:not([hidden])',timeout=30000);ok(pg.get_attribute('#wgo','href')=='https://wa.me/919876543210','open-chat link shown')
    pg.click('[data-w=x]')
    pg.click('button[data-a=wa]');pg.wait_for_timeout(200)
    with pg.expect_download(timeout=60000) as dl:
        pg.click('[data-w=img]')
    f=dl.value;ok(f.suggested_filename.endswith('.png'),'image downloaded '+f.suggested_filename)
    pg.wait_for_selector('#wgo:not([hidden])',timeout=30000);pg.click('[data-w=x]')
    # settings groups
    pg.goto('http://localhost:8123/index.html#/s');pg.wait_for_timeout(500)
    hs=pg.eval_on_selector_all('.sgh h3','e=>e.map(x=>x.textContent.trim())');print(hs)
    ok([h.split(' ')[0] for h in hs]==['Design','Print','Signage','Digital'],'4 titles in order')
    pg.click('.sgh button[data-g=Signage]');pg.wait_for_timeout(200)
    ok(pg.evaluate("()=>S.set.services[0].g")=='Signage','new service under Signage')
    pg.fill('[data-i="0"][data-f=n]','Neon Board');pg.wait_for_timeout(100)
    pos=pg.evaluate("()=>{const h=[...document.querySelectorAll('.sgh')].find(x=>x.textContent.includes('Signage'));const n=h.nextElementSibling.querySelector('[data-f=n]');return n.value}");ok(pos=='Neon Board','new service displayed right under Signage title')
    cnt=pg.evaluate("()=>Object.fromEntries(['Design','Print','Signage','Digital'].map(g=>[g,S.set.services.filter(v=>v.g==g).length]))");print(cnt)
    ok(all(v>0 for v in cnt.values()),'all groups populated')
    # billing autocomplete picks new service? digital in dm
    # calendar
    pg.goto('http://localhost:8123/index.html#/c');pg.wait_for_timeout(500)
    pg.click(f'[data-cd="{T}"]')
    pg.fill('#cn','Ravi');pg.wait_for_timeout(200)
    ok(pg.input_value('#cp')=='9876543210','phone autofilled from bill')
    ok(pg.input_value('#cb')!='','bill auto-linked')
    ok(pg.input_value('#ca')!='','amount auto-filled '+pg.input_value('#ca'))
    pg.select_option('#ct','half');ok(pg.input_value('#ca')!='','half amount '+pg.input_value('#ca'))
    pg.select_option('#ct','custom');pg.fill('#ca','1234')
    pg.click('[data-ca=save]');pg.wait_for_timeout(300)
    ok(pg.locator('.ent').count()==1,'entry added')
    pg.fill('#cn','Kumar');pg.fill('#cp','9000000001');pg.select_option('#ct','custom');pg.fill('#ca','500');pg.click('[data-ca=save]');pg.wait_for_timeout(300)
    ok(pg.locator('.ent').count()==2,'second entry')
    pg.goto('http://localhost:8123/index.html#/h');pg.wait_for_timeout(500)
    ok(pg.locator('.rb').count()==1 and 'Collect money today (2)' in pg.inner_text('.rb'),'banner on history: '+pg.inner_text('.rb')[:50].replace('\n',' '))
    ok(pg.locator('.rb a[href^="tel:"]').count()==2,'call links')
    # received with payment on bill
    pg.once('dialog',lambda d:d.accept())
    pg.locator('.rb [data-bok]').first.click();pg.wait_for_timeout(800)
    docs=pg.evaluate("()=>S.docs[0].pay.length");print('pays',docs)
    pg.goto('http://localhost:8123/index.html#/c');pg.wait_for_timeout(400)
    ok(pg.locator('.ent.dn').count()>=1,'marked received')
    # notifications ui
    ok(pg.locator('#rt').count()==1,'reminder time box')
    # expenses
    pg.goto('http://localhost:8123/index.html#/x');pg.wait_for_timeout(500)
    pg.fill('#xc','Fuel');pg.fill('#xn','Petrol');pg.fill('#xa','500');pg.click('[data-xa=add]');pg.wait_for_timeout(300)
    pg.fill('#xn','Tea');pg.fill('#xc','Food & Tea');pg.fill('#xa','80.5');pg.press('#xa','Enter');pg.wait_for_timeout(300)
    ok(pg.locator('table.lt tr').count()==3,'2 expenses listed (+header)')
    ok('580.50' in pg.inner_text('.stats'),'total 580.50')
    for k,ext in [('pdf','.pdf'),('img','.png'),('txt','.txt')]:
        with pg.expect_download(timeout=60000) as dl:
            pg.click(f'[data-xe={k}]')
        fn=dl.value.suggested_filename;ok(fn.endswith(ext),'expense export '+fn)
        if k=='txt':
            path=dl.value.path();t=open(path,encoding='utf-8').read();print(t);ok('580.50' in t,'txt has total')
    pg.screenshot(path='/home/claude/x.png')
    # sync merge semantic check
    r=pg.evaluate("()=>{const a=[{id:'a',u:1},{id:'b',u:5}],b=[{id:'a',u:2},{id:'c',u:1}];return mergeL(a,b).map(x=>x.id+x.u).sort().join()}");ok(r=='a2,b5,c1','mergeL '+r)
    # old backup / okSet
    r=pg.evaluate("()=>{const o=okSet({cal:[{id:'z',d:'2026-01-01',n:'x',a:5,t:'full'}],exp:[{id:'y',d:'bad'}],services:[{n:'a',k:'pr',c:'Design'}]});return [o.cal.length,o.exp.length,o.services[0].g].join()}");ok(r=='1,0,Design','okSet sanitises '+r)
    # print expense paper in print media (1 page check)
    # mobile layout
    m=ctx.new_page();m.set_viewport_size({'width':390,'height':800});m.route('**/*supabase.co/**',lambda r:r.abort());m.goto('http://localhost:8123/index.html#/c');m.wait_for_timeout(500)
    m.evaluate("()=>{const o=document.querySelector('#zxl');if(o)o.remove();document.querySelector('.shell').inert=false}")
    ok(m.evaluate("()=>document.documentElement.scrollWidth<=innerWidth+1"),'calendar no horizontal scroll on mobile')
    m.goto('http://localhost:8123/index.html#/x');m.wait_for_timeout(300);ok(m.evaluate("()=>document.documentElement.scrollWidth<=innerWidth+1"),'expenses no horizontal scroll on mobile')
    m.screenshot(path='/home/claude/m.png')
    b.close()
print('ERRORS',errs[:8]);print(sum(1 for r in res if r[0]),'/',len(res))
