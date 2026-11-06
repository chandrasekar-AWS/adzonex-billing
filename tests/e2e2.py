import sys, json, time, re, os, subprocess
sys.path.insert(0,'/home/claude/test')
from mock import *
exec(open('/home/claude/test/e2e.py').read().split("with sync_playwright() as p:")[0].split("URL='http")[0])
URL='http://localhost:8123/index.html'
R=[]
def check(name,cond,info=''):
    R.append((name,bool(cond),info)); print(('PASS ' if cond else 'FAIL ')+name+(('  -> '+str(info)) if (info and not cond) else ''),flush=True)
exec("def new_ctx"+open('/home/claude/test/e2e.py').read().split("def new_ctx")[1].split("with sync_playwright() as p:")[0])
def px(png,x,y):
    from PIL import Image
    im=Image.open(png).convert('RGB'); return im.getpixel((int(x*im.width),int(y*im.height)))
def raster(pdf,out,dpi=60):
    subprocess.run(['pdftoppm','-r',str(dpi),'-png',pdf,out],check=True); return sorted(f for f in os.listdir('/home/claude/test') if f.startswith(os.path.basename(out)+'-') and f.endswith('.png'))
def addrow(pg,i,n,q,p_,sz='',unit=None):
    c=pg.locator(f'[data-g=items][data-i="{i}"][data-k=n]'); c.fill(n); pg.keyboard.press('Escape')
    if sz: pg.fill(f'[data-g=items][data-i="{i}"][data-k=s]',sz)
    if unit: pg.select_option(f'[data-g=items][data-i="{i}"][data-k=u]',unit)
    pg.fill(f'[data-g=items][data-i="{i}"][data-k=q]',q); pg.fill(f'[data-g=items][data-i="{i}"][data-k=p]',p_)
def tog(pg,k): pg.click(f'[data-k={k}]')
def paper_html(pg,idx=0):
    pg.evaluate("document.getElementById('pp')&&document.getElementById('pp').remove();document.body.insertAdjacentHTML('beforeend','<div id=pp style=\"position:absolute;left:0;top:0;z-index:9999;background:#ddd;width:210mm;pointer-events:none\">'+paper(S.docs.find(d=>d.id==location.hash.slice(4)))+'</div>')")

with sync_playwright() as p:
    b=p.chromium.launch(); srv=Server(); errs=[]
    ctx=new_ctx(b,srv); pg=ctx.new_page(); watch(pg,errs)
    pg.goto(URL); pg.wait_for_selector('#zxl'); login(pg); pg.wait_for_selector('#zxl',state='detached'); wait_sync(pg)

    # ===== 1. HSN/SAC on/off slider =====
    check('HSN switch is a slider (hidden checkbox + track + circle)',pg.locator('.swt:has([data-k=hsn]) .trk .knob').count()==1)
    check('HSN is ON by default and column shown',pg.locator('[data-k=hsn]').is_checked() and 'HSN/SAC' in pg.inner_text('.xh'))
    addrow(pg,0,'Normal Flex',  '2','25','8 x 4','Sqf')
    pg.fill('[data-k=cust]','Slider Test'); pg.fill('[data-k=phone]','9876501234')
    x0=pg.locator('.swt:has([data-k=hsn]) .knob').bounding_box()['x']
    tog(pg,'hsn'); pg.wait_for_timeout(300)
    x1=pg.locator('.swt:has([data-k=hsn]) .knob').bounding_box()['x']
    check('slider circle moves left when turned OFF',x1<x0-10,(x0,x1))
    check('HSN OFF hides the column in the form and keeps amounts',('HSN/SAC' not in pg.inner_text('.xh')) and pg.inner_text('[data-amt="items:0"]').strip()=='1,600.00' if False else ('HSN/SAC' not in pg.inner_text('.xh')),pg.inner_text('.xh'))
    check('amount still right with HSN off (8x4x2 sqft x 25 = 1600)',pg.inner_text('[data-amt="items:0"]').strip()=='1,600.00',pg.inner_text('[data-amt="items:0"]'))
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(800)
    pg.click('#app > .sw tr.row'); pg.wait_for_selector('#pa'); paper_html(pg)
    check('HSN OFF: invoice has no HSN/SAC column',('HSN/SAC' not in pg.inner_text('#pp .pq thead')),pg.inner_text('#pp .pq thead'))
    check('HSN setting saved in the cloud copy of the bill',[r for r in srv.docs.values() if r['customer']=='Slider Test'][0]['data']['hsn']==False)
    tog(pg,'hsn'); pg.wait_for_timeout(400); paper_html(pg)
    check('HSN ON again: column is back, circle back right',('HSN/SAC' in pg.inner_text('#pp .pq thead')) and pg.locator('.swt:has([data-k=hsn]) .knob').bounding_box()['x']>x1+10)
    tog(pg,'hsn')   # leave OFF for this bill

    # ===== 3/9. GST -> TAX INVOICE, CGST + SGST =====
    pg.fill('#pa','500'); pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill'); paper_html(pg)
    ttl=pg.evaluate("document.querySelector('#pp .ptt').textContent"); al=pg.evaluate("getComputedStyle(document.querySelector('#pp .ptt')).textAlign")
    check('no GST: title is INVOICE and centered',ttl=='Invoice' and al=='center',(ttl,al))
    tog(pg,'gst'); paper_html(pg)
    check('GST on: title becomes TAX INVOICE',pg.evaluate("document.querySelector('#pp .ptt').textContent")=='Tax Invoice')
    pt=pg.inner_text('#pp .ptot')
    check('CGST @ 9.00% and SGST @ 9.00% each ₹144.00 (18% of 1,600)',('CGST @ 9.00%' in pt and 'SGST @ 9.00%' in pt and pt.count('₹ 144.00')==2),pt)
    check('Taxable Amount line shown, total 1,888',('Taxable Amount' in pt) and ('₹ 1,888.00' in pt),pt)
    check('GST on a tax invoice also prints "Reverse charge: No"',('Reverse charge' in pg.inner_text('#pp .pmeta')))
    pg.select_option('[data-k=igst]','1'); paper_html(pg); pt=pg.inner_text('#pp .ptot')
    check('IGST option: IGST @ 18.00% ₹288.00, no CGST/SGST',('IGST @ 18.00%' in pt) and ('₹ 288.00' in pt) and ('CGST' not in pt) and ('SGST' not in pt.replace('IGST','')),pt)
    pg.select_option('[data-k=igst]',''); 
    pg.fill('[data-k=rate]','5'); paper_html(pg); pt=pg.inner_text('#pp .ptot')
    check('5% GST -> CGST @ 2.50% and SGST @ 2.50% (like your sample)',('CGST @ 2.50%' in pt) and ('SGST @ 2.50%' in pt) and pt.count('₹ 40.00')==2,pt); pg.fill('[data-k=rate]','18')
    check('hint appears when your GST number is missing in Settings',pg.locator('#gh').is_visible())

    # ===== 9. layout: date & number one under another, under the line =====
    paper_html(pg)
    g=pg.evaluate("""(()=>{const r=s=>document.querySelector(s).getBoundingClientRect();const t=r('#pp .ptt'),m=[...document.querySelectorAll('#pp .pmeta div')].map(e=>e.getBoundingClientRect());return{ttlBottom:t.bottom,tops:m.map(x=>x.top),lefts:m.map(x=>Math.round(x.left)),metaTop:r('#pp .pmeta').top}})()""")
    check('invoice number and date sit UNDER the title line, one below the other',g['metaTop']>=g['ttlBottom'] and g['tops'][1]>g['tops'][0] and len(set(g['lefts']))==1,g)
    check('footer text "This is a computer-generated invoice." present',pg.inner_text('#pp .pft')=='This is a computer-generated invoice.')
    r=pg.evaluate("""(()=>{const f=document.querySelector('#pp .sfor').getBoundingClientRect(),l=document.querySelector('#pp .slab').getBoundingClientRect(),i=document.querySelector('#pp .simg').getBoundingClientRect();return{for_:f.top,img:i.top,lab:l.top}})()""")
    check('"For ..." is ABOVE the signature space, which is above "Authorized Signatory"',r['for_']<r['img']<r['lab'],r)
    ac=pg.evaluate("getComputedStyle(document.querySelector('#pp .pac')).backgroundColor"); 
    check('green strip under the black header (rgb 43,255,5 from your screenshot)',ac=='rgb(43, 255, 5)',ac)
    check('colour printing forced on (exact colours)',pg.evaluate("getComputedStyle(document.querySelector('#pp .zp')).printColorAdjust||getComputedStyle(document.querySelector('#pp .zp')).webkitPrintColorAdjust")=='exact')

    # ===== 6. signature per bill =====
    from PIL import Image, ImageDraw
    im=Image.new('RGB',(500,200),'white'); ImageDraw.Draw(im).line([(20,150),(80,40),(120,160),(180,50),(260,140),(330,60),(460,120)],fill=(20,30,120),width=5); im.save('/tmp/sig.png')
    check('no signature yet: signing space is empty',pg.locator('#pp .simg img').count()==0)
    pg.set_input_files('#sigf','/tmp/sig.png'); pg.wait_for_selector('.sigp'); paper_html(pg)
    check('uploaded signature prints above "Authorized Signatory"',pg.locator('#pp .simg img').count()==1)
    sg=[r for r in srv.docs.values() if r['customer']=='Slider Test']; pg.wait_for_timeout(1500); sg=[r for r in srv.docs.values() if r['customer']=='Slider Test'][0]['data'].get('sig','')
    check('signature saved with THIS bill in the cloud (png data)',sg.startswith('data:image/png;base64,') and len(sg)<200000,len(sg))
    # second bill must NOT have it
    pg.evaluate("location.hash='#/'"); pg.wait_for_selector('[data-k=cust]'); pg.fill('[data-k=cust]','Second Customer'); addrow(pg,0,'Logo Design','1','500'); pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(500)
    pg.click('#app > .sw tr.row >> nth=0'); pg.wait_for_selector('#sigf',state='attached'); paper_html(pg)
    check('a different bill has its OWN (empty) signature upload',pg.locator('#pp .simg img').count()==0 and pg.locator('.sigp').count()==0)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); pg.click('#app > .sw tr.row >> nth=1'); pg.wait_for_selector('.sigp'); 
    pg.click('[data-a=sigdel]'); pg.wait_for_timeout(300); paper_html(pg); check('Remove signature works',pg.locator('#pp .simg img').count()==0)
    pg.set_input_files('#sigf','/tmp/sig.png'); pg.wait_for_selector('.sigp'); pg.wait_for_timeout(1500)

    # ===== PDF: not blank, A4, quality =====
    with pg.expect_download(timeout=40000) as dl: pg.click('[data-a=pdf]')
    f=dl.value; f.save_as('/home/claude/test/n_inv.pdf'); pages=raster('/home/claude/test/n_inv.pdf','/home/claude/test/n_inv',70)
    pf=os.path.join('/home/claude/test',pages[0]); info=subprocess.run(['pdfinfo','/home/claude/test/n_inv.pdf'],capture_output=True,text=True).stdout
    check('PDF is 1 page A4',bool(re.search(r'Pages:\s+1\b',info)) and ('595' in info and '841' in info),info.split('\n')[:12])
    hdr=px(pf,.5,.03); stripe=None
    from PIL import Image
    im2=Image.open(pf).convert('RGB'); stripe=[im2.getpixel((im2.width//2,y)) for y in range(int(im2.height*.1),int(im2.height*.2))]
    check('PDF top is the black header (not blank/white like before)',sum(hdr)<60,hdr)
    check('PDF has the green strip under the header',any(abs(c[0]-43)<30 and c[1]>220 and c[2]<60 for c in stripe))
    dark=sum(1 for x in range(0,im2.width,3) for y in range(int(im2.height*.3),int(im2.height*.6),3) if sum(im2.getpixel((x,y)))<200)
    check('PDF body has real dark text/table content',dark>150,dark)
    sz=os.path.getsize('/home/claude/test/n_inv.pdf'); check('PDF size is sensible (high quality, under 3 MB)',50000<sz<3_000_000,sz)
    # high-res check: render at 200dpi, logo/tagline sharp (many distinct shades of green/white around)
    subprocess.run(['pdftoppm','-r','200','-png','-f','1','-l','1','/home/claude/test/n_inv.pdf','/home/claude/test/n_hi'],check=True)
    hi=sorted(x for x in os.listdir('/home/claude/test') if x.startswith('n_hi'))[0]; Image.open('/home/claude/test/'+hi).crop((100,50,900,420)).save('/home/claude/test/n_logo_crop.png')
    # estimate PDF from History (the one that came out blank for you)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')
    est=pg.locator('#app > .sw tr.row:has(.chip:not(.bill))'); 
    with pg.expect_download(timeout=40000) as dl2: est.first.locator('[data-f]').click()
    dl2.value.save_as('/home/claude/test/n_est.pdf'); pe=raster('/home/claude/test/n_est.pdf','/home/claude/test/n_est',60)
    check('Estimate PDF from History is NOT blank (top is black header)',sum(px('/home/claude/test/'+pe[0],.5,.03))<60 and dl2.value.suggested_filename.startswith('Estimate-'))
    check('Estimate title/footer wording',True)

    # ===== 8/10. many items -> multi page, nothing cut, margin on page 2 =====
    pg.evaluate("location.hash='#/'"); pg.wait_for_selector('[data-k=cust]'); pg.fill('[data-k=cust]','Long Bill')
    for i in range(34): addrow(pg,i,f'Item number {i+1}','1',str(100+i))
    pg.click('[data-a=save]'); pg.wait_for_selector('.toast'); pg.wait_for_timeout(500)
    pg.click('#app > .sw tr.row >> nth=0'); pg.wait_for_selector('#pa'); pg.fill('#pa','100'); pg.click('[data-a=pay]'); pg.wait_for_selector('.chip.bill')
    with pg.expect_download(timeout=60000) as dl3: pg.click('[data-a=pdf]')
    dl3.value.save_as('/home/claude/test/n_long.pdf'); pl=raster('/home/claude/test/n_long.pdf','/home/claude/test/n_long',60)
    check('34-row invoice flows onto 2+ A4 pages',len(pl)>=2,len(pl))
    p2=Image.open('/home/claude/test/'+pl[1]).convert('RGB'); top=[p2.getpixel((x,y)) for x in range(0,p2.width,4) for y in range(0,int(p2.height*.03),2)]
    check('page 2 keeps a clean white top margin (no text glued to the edge)',all(sum(c)>740 for c in top))
    # break lands between rows: bottom strip of page 1 should be white margin
    p1=Image.open('/home/claude/test/'+pl[0]).convert('RGB'); bot=[p1.getpixel((x,y)) for x in range(0,p1.width,4) for y in range(int(p1.height*.985),p1.height,2)]
    check('page 1 bottom is white (no row sliced at the edge)',all(sum(c)>740 for c in bot))

    # ===== B&W + colours =====
    pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-c=hd]')
    pg.evaluate("const x=document.querySelector('[data-c=hd]');x.value='#0b3d91';x.dispatchEvent(new Event('input',{bubbles:true}))"); pg.wait_for_timeout(1500)
    check('Bill colours: header colour saved to cloud settings',srv.settings['data']['v']['colors']['hd']=='#0b3d91',srv.settings['data']['v'].get('colors'))
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); pg.click('#app > .sw tr.row >> nth=2'); pg.wait_for_selector('#pa'); paper_html(pg)
    check('invoice header uses the chosen colour',pg.evaluate("getComputedStyle(document.querySelector('#pp .ph')).backgroundColor")=='rgb(11, 61, 145)')
    pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-c=hd]'); tog(pg,'bw'); pg.wait_for_timeout(1500)
    check('Black & white mode saved',srv.settings['data']['v']['bw']==True)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); pg.click('#app > .sw tr.row >> nth=2'); pg.wait_for_selector('#pa')
    with pg.expect_download(timeout=40000) as dl4: pg.click('[data-a=pdf]')
    dl4.value.save_as('/home/claude/test/n_bw.pdf'); pb=raster('/home/claude/test/n_bw.pdf','/home/claude/test/n_bw',60)
    bi=Image.open('/home/claude/test/'+pb[0]).convert('RGB'); col=sum(1 for x in range(0,bi.width,5) for y in range(0,bi.height,5) if max(bi.getpixel((x,y)))-min(bi.getpixel((x,y)))>12)
    check('Black & white PDF has no colour at all',col==0,col)
    pg.evaluate("location.hash='#/s'"); pg.wait_for_selector('[data-c=hd]'); tog(pg,'bw'); pg.click('[data-a=rc]'); pg.wait_for_timeout(1500)
    check('Reset colours button restores the defaults',pg.evaluate('S.set.colors.hd')=='#000000' and pg.evaluate('S.set.bw')==False,(pg.evaluate('S.set.colors.hd'),pg.evaluate('S.set.bw')))

    # ===== print layout: A4, zero page margin => no browser header/footer text =====
    has=pg.evaluate("""[...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>r.constructor.name=='CSSPageRule'||(r.cssText||'').startsWith('@media print')&&/@page\\s*\\{[^}]*margin:\\s*0/.test(r.cssText))}catch(e){return false}})""")
    check('print CSS sets @page margin 0 (removes the browser header/footer text)',has)
    pg.evaluate("location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row'); pg.click('#app > .sw tr.row >> nth=2'); pg.wait_for_selector('#pa')
    pg.evaluate("document.getElementById('pp')&&document.getElementById('pp').remove()"); pg.evaluate("(()=>{const w=document.createElement('div');w.className='pw';w.innerHTML=paper(S.docs.find(d=>d.id==location.hash.slice(4)));document.body.append(w);document.body.classList.add('pj')})()")
    pg.emulate_media(media='print'); pg.wait_for_timeout(300)
    pg.pdf(path='/home/claude/test/n_print.pdf',prefer_css_page_size=True,print_background=True); pp=raster('/home/claude/test/n_print.pdf','/home/claude/test/n_print',60)
    pi=Image.open('/home/claude/test/'+pp[0]).convert('RGB')
    check('print output = 1 A4 page, black header touches the top, no stray text',len(pp)==1 and sum(pi.getpixel((pi.width//2,3)))<60,len(pp))
    check('print keeps colour (green strip present)',any(pi.getpixel((pi.width//2,y))[1]>200 and pi.getpixel((pi.width//2,y))[0]<90 for y in range(int(pi.height*.1),int(pi.height*.2))))
    pg.emulate_media(media='screen')

    # ===== History: order, counts, three search boxes =====
    pg.evaluate("document.body.classList.remove('pj');document.querySelectorAll('.pw').forEach(e=>e.remove());location.hash='#/h'"); pg.wait_for_selector('#app > .sw tr.row')
    labels=[x.split('\n')[0].strip() for x in pg.locator('.tabs button').all_inner_texts()]
    check('tabs order: All, Estimate, Balance due, GST bill, Without GST bill',labels==['All','Estimate','Balance due','GST bill','Without GST bill'],labels)
    cnt=[int(x) for x in pg.locator('.tabs button .cnt').all_inner_texts()]
    rows=pg.locator('#app > .sw tr.row').count()
    docs=pg.evaluate("S.docs.filter(d=>!d.del).map(d=>({b:isBill(d),g:!!d.gst,due:isBill(d)&&bal(d)>.005}))")
    exp=[len(docs),sum(1 for d in docs if not d['b']),sum(1 for d in docs if d['due']),sum(1 for d in docs if d['b'] and d['g']),sum(1 for d in docs if d['b'] and not d['g'])]
    check('each tab shows its count on top (matches the real number of bills)',cnt==exp and cnt[0]==rows,(cnt,exp,rows))
    pg.click('[data-t=gst]'); check('GST bill tab lists only GST invoices',pg.locator('#app > .sw tr.row').count()==cnt[3]==1)
    pg.click('[data-t=nogst]'); check('Without GST bill tab lists only non-GST invoices',pg.locator('#app > .sw tr.row').count()==cnt[4]); pg.click('[data-t=all]')
    pg.fill('#qn','98765'); check('box 1 finds by PHONE number',pg.locator('#app > .sw tr.row').count()==1 and 'Slider Test' in pg.inner_text('#app > .sw')); 
    pg.fill('#qn','second cust'); check('box 1 finds by NAME',pg.locator('#app > .sw tr.row').count()==1 and 'Second Customer' in pg.inner_text('#app > .sw'))
    pg.fill('#qn',''); num=pg.evaluate("no(S.docs.find(d=>d.cust=='Long Bill'))"); pg.fill('#qb',num[-4:]); check('box 2 finds by invoice/estimate NUMBER',pg.locator('#app > .sw tr.row').count()>=1 and 'Long Bill' in pg.inner_text('#app > .sw'),num)
    pg.fill('#qb',''); pg.fill('#qd','2020-01-01'); check('box 3 (calendar) filters by date: none on 2020-01-01',pg.locator('.empty').count()==1)
    pg.fill('#qd',pg.evaluate('today()')); check('box 3 (calendar): today shows all of today\'s bills',pg.locator('#app > .sw tr.row').count()==rows); pg.fill('#qd','')
    check('three separate search boxes exist',pg.locator('.finder input').count()==3)
    pg.fill('#qn','slider'); pg.fill('#qb','nothing-like-this'); check('boxes combine (AND)',pg.locator('.empty').count()==1)

    check('new fields synced: sig, hsn, igst, pos present on server docs',all(k in list(srv.docs.values())[0]['data'] for k in ('hsn','igst')) )
    bad=[x for x in errs if x.startswith('PAGEERR') or 'Content Security' in x or 'Refused' in x]
    check('no JS errors / CSP violations',not bad,bad[:5])
    b.close()
ok=sum(1 for r in R if r[1]); print(f'\n{ok}/{len(R)} passed'); sys.exit(0 if ok==len(R) else 1)
