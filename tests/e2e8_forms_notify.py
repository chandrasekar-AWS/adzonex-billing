"""Forms clear after Save on every page + notifications (phone alarms, browser, service worker).
Run: serve app/ on http://localhost:8123, then  python3 e2e8_forms_notify.py"""
from playwright.sync_api import sync_playwright
import datetime, json
D=datetime.date.today(); T=D.isoformat(); F=(D+datetime.timedelta(days=3)).isoformat(); F2=(D+datetime.timedelta(days=5)).isoformat()
res=[]
def ok(c,m):
    res.append(bool(c)); print(('PASS ' if c else 'FAIL ')+m)
URL='http://localhost:8123/index.html'
def boot(ctx,init=None):
    pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('dialog',lambda d:d.accept())
    if init: pg.add_init_script(init)
    pg.route('**/*supabase.co/**',lambda r:r.abort()); pg.route('**/fonts.g*/**',lambda r:r.abort())
    pg.goto(URL); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const o=document.querySelector('#zxl');if(o)o.remove();const s=document.querySelector('.shell');if(s)s.inert=false}")
    return pg,errs
MOCK="""
window.__ln={calls:[],pending:[],perm:localStorage.getItem('mockperm')||'prompt',exact:'granted'};
window.Capacitor={isNativePlatform:()=>true,Plugins:{LocalNotifications:{
 checkPermissions:async()=>({display:__ln.perm}),
 requestPermissions:async()=>{__ln.perm='granted';localStorage.setItem('mockperm','granted');return{display:'granted'}},
 createChannel:async c=>{__ln.calls.push(['channel',c])},
 getPending:async()=>({notifications:__ln.pending.map(n=>({id:n.id}))}),
 cancel:async o=>{__ln.pending=__ln.pending.filter(p=>!o.notifications.some(n=>n.id==p.id))},
 schedule:async o=>{__ln.pending.push(...o.notifications);__ln.calls.push(['schedule',o.notifications.length])},
 addListener:async(e,f)=>{__ln.l=__ln.l||{};__ln.l[e]=f;return{remove(){}}},
 checkExactNotificationSetting:async()=>({exact_alarm:__ln.exact}),changeExactNotificationSetting:async()=>{__ln.exactAsked=1}}}};
"""
with sync_playwright() as p:
    b=p.chromium.launch(channel='chromium')
    # ================= 1. FORMS CLEAR AFTER SAVE =================
    ctx=b.new_context(viewport={'width':1300,'height':900},timezone_id='Asia/Kolkata'); pg,errs=boot(ctx)
    pg.goto(URL+'#/x'); pg.wait_for_timeout(300)
    pg.fill('#xc','Fuel'); pg.fill('#xn','Petrol for van'); pg.fill('#xa','500'); pg.select_option('#xm','UPI')
    pg.click('[data-xa=add]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#xc')=='' and pg.input_value('#xn')=='' and pg.input_value('#xa')=='','Expenses: category, description, amount cleared after Add')
    ok(pg.input_value('#xm')=='UPI' and pg.input_value('#xd')==T,'Expenses: date and paid-by kept for the next entry')
    ok(pg.evaluate("()=>S.set.exp.filter(x=>!x.del).length")==1,'Expenses: entry saved')
    ok(pg.evaluate("()=>document.activeElement&&document.activeElement.id")=='xn','Expenses: cursor back in description box')
    pg.click('[data-xed]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#xn')=='Petrol for van' and pg.input_value('#xa')=='500' and pg.input_value('#xc')=='Fuel','Expenses: Edit loads the saved entry into the form')
    pg.fill('#xa','650'); pg.click('[data-xa=add]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#xa')=='' and pg.input_value('#xn')=='','Expenses: form cleared after Update')
    ok(pg.evaluate("()=>S.set.exp.filter(x=>!x.del).map(x=>x.a)")==[650],'Expenses: update changed the amount, no duplicate')
    pg.click('[data-xed]'); pg.wait_for_timeout(200); pg.click('[data-xa=cancel]'); pg.wait_for_timeout(200)
    ok(pg.input_value('#xn')=='' and pg.input_value('#xa')=='','Expenses: Cancel clears the form')
    pg.fill('#xn','half typed'); pg.click('[data-xt=month]'); pg.wait_for_timeout(200)
    ok(pg.input_value('#xn')=='half typed','Expenses: switching tab keeps text you were typing')
    pg.click('[data-xdel]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#xn')=='half typed' and pg.evaluate("()=>S.set.exp.filter(x=>!x.del).length")==0,'Expenses: delete keeps typed text, removes entry')
    pg.fill('#xn','enter key test'); pg.fill('#xa','40'); pg.press('#xa','Enter'); pg.wait_for_timeout(250)
    ok(pg.input_value('#xn')=='' and pg.input_value('#xa')=='','Expenses: Enter key saves and clears')
    # calendar
    pg.goto(URL+'#/c'); pg.wait_for_timeout(300)
    pg.fill('#cn','Ravi'); pg.fill('#cp','9876543210'); pg.fill('#ca','300'); pg.fill('#cno','advance')
    pg.click('[data-ca=save]'); pg.wait_for_timeout(250)
    ok(all(pg.input_value(i)=='' for i in ['#cn','#cp','#ca','#cno']),'Calendar: all boxes cleared after Add')
    ok(pg.evaluate("()=>S.set.cal.filter(x=>!x.del).length")==1,'Calendar: entry saved')
    pg.click('[data-ced]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#cn')=='Ravi' and pg.input_value('#ca')=='300','Calendar: Edit loads entry')
    pg.fill('#ca','350'); pg.click('[data-ca=save]'); pg.wait_for_timeout(250)
    ok(pg.input_value('#cn')=='' and pg.input_value('#ca')=='','Calendar: cleared after Update')
    # billing
    pg.goto(URL+'#/'); pg.wait_for_timeout(300)
    pg.fill('input[data-k=cust]','Sam'); pg.fill('input[data-k=phone]','9000000000'); pg.fill('textarea[data-k=rem]','note')
    pg.fill('input[data-g=items][data-i="0"][data-k=n]','Normal Flex'); pg.fill('input[data-g=items][data-i="0"][data-k=q]','2'); pg.fill('input[data-g=items][data-i="0"][data-k=p]','100')
    pg.click('button[data-a=save]'); pg.wait_for_timeout(350)
    ok(pg.url.endswith('#/h'),'Billing: Save goes to History')
    pg.click('[data-nav][href="#/"]'); pg.wait_for_timeout(250)
    ok(pg.input_value('input[data-k=cust]')=='' and pg.input_value('input[data-k=phone]')=='' and pg.input_value('textarea[data-k=rem]')=='' and pg.input_value('input[data-g=items][data-i="0"][data-k=n]')=='','Billing: new bill page is empty after Save')
    pg.goto(URL+'#/h'); pg.wait_for_timeout(250); pg.click('tr.row'); pg.wait_for_timeout(250)
    pg.fill('#pa','50'); pg.click('button[data-a=pay]'); pg.wait_for_timeout(450)
    ok(pg.input_value('#pa')=='','Bill: payment amount box cleared after Record payment')
    pg.goto(URL+'#/h'); pg.wait_for_timeout(250)
    pg.fill('input[data-amt]','10'); pg.click('[data-add]'); pg.wait_for_timeout(450)
    ok(pg.input_value('input[data-amt]')=='','History: quick-pay box cleared after Add')
    ok(errs==[],'no JavaScript errors on any page '+str(errs)); ctx.close()

    # ================= 2. PHONE APP: alarms scheduled by the phone =================
    ctx=b.new_context(viewport={'width':420,'height':900},timezone_id='Asia/Kolkata'); pg,errs=boot(ctx,MOCK)
    seed="""([T,F,F2])=>{S.set.cal=[{id:'a1',d:F,n:'Ravi',ph:'9876543210',t:'custom',a:500,doc:'',note:'',ok:0,u:Date.now()},{id:'a2',d:F,n:'Sam',ph:'',t:'custom',a:250,doc:'',note:'',ok:0,u:Date.now()},{id:'a3',d:F2,n:'Meena',ph:'',t:'custom',a:900,doc:'',note:'',ok:0,u:Date.now()},{id:'a4',d:F2,n:'Done',ph:'',t:'custom',a:100,doc:'',note:'',ok:1,u:Date.now()}];save()}"""
    pg.evaluate(seed,[T,F,F2])
    pg.goto(URL+'#/c'); pg.wait_for_timeout(500)
    ok('Notifications are not turned on yet' in pg.inner_text('#nts'),'Phone: status says not turned on yet')
    pg.click('[data-nt]'); pg.wait_for_timeout(1800)
    st=pg.evaluate("()=>({perm:__ln.perm,pend:__ln.pending,calls:__ln.calls.map(c=>c[0]+(c[1]!==undefined&&typeof c[1]!='object'?':'+c[1]:''))})")
    ok(st['perm']=='granted','Phone: permission asked')
    ok('channel' in [c.split(':')[0] for c in st['calls']],'Phone: notification channel created')
    days=sorted(n['schedule']['at'][:10] if isinstance(n['schedule']['at'],str) else '' for n in st['pend'] if n['id']!=1)
    ok(len([n for n in st['pend'] if n['id']!=1])==2,'Phone: one alarm per day with money due (2 days), received entry ignored: '+str(len(st['pend'])))
    pend=sorted([n for n in st['pend'] if n['id']!=1],key=lambda n:n['id'])
    ok(pend[0]['id']==int(F.replace('-','')) and 'Ravi' in pend[0]['body'] and 'Sam' in pend[0]['body'] and pend[0]['title']=='Collect money today (2)','Phone: day-1 alarm lists both people, id = date')
    ok('Done' not in pend[1]['body'] and 'Meena' in pend[1]['body'],'Phone: received person not in reminder')
    at=pg.evaluate("()=>__ln.pending.filter(n=>n.id!=1).map(n=>[n.schedule.at.getFullYear(),n.schedule.at.getMonth()+1,n.schedule.at.getDate(),n.schedule.at.getHours(),n.schedule.at.getMinutes()])")
    ok(at[0][3:]==[9,0],'Phone: alarm time is the reminder time (09:00)')
    ok(all(n.get('smallIcon')=='ic_stat_zx' and n.get('channelId')=='pay' for n in pend),'Phone: alarms use bell icon and channel')
    # change reminder time -> rescheduled
    pg.fill('#rt','18:30'); pg.dispatch_event('#rt','change'); pg.wait_for_timeout(1900)
    at=pg.evaluate("()=>__ln.pending.filter(n=>n.id!=1).map(n=>[n.schedule.at.getHours(),n.schedule.at.getMinutes()])")
    ok(at==[[18,30],[18,30]],'Phone: changing reminder time reschedules '+str(at))
    # mark received -> alarm removed
    pg.evaluate("()=>{const x=S.set.cal.find(y=>y.id=='a3');x.ok=1;x.u=Date.now();sch()}"); pg.wait_for_timeout(1900)
    ids=sorted(pg.evaluate("()=>__ln.pending.filter(n=>n.id!=1).map(n=>n.id)"))
    ok(ids==[int(F.replace('-',''))],'Phone: when everyone for a day is Received that alarm is cancelled')
    # app restarts -> schedule again from stored data
    pg.reload(); pg.wait_for_timeout(3500)
    ok(pg.evaluate("()=>__ln.calls.filter(c=>c[0]=='schedule').length")>=1,'Phone: after app restart the alarms are scheduled again')
    pg.evaluate("()=>{__ln.exact='denied';localStorage.removeItem('zx-exact')}"); pg.goto(URL+'#/c'); pg.wait_for_timeout(300); pg.evaluate("()=>{const o=document.querySelector('#zxl');if(o)o.remove();const s=document.querySelector('.shell');if(s)s.inert=false}"); pg.click('[data-nt]'); pg.wait_for_timeout(1500)
    ok(pg.evaluate("()=>__ln.exactAsked===1"),'Phone: when exact alarms are not allowed, the app sends you to the setting once')
    # tap on notification opens Calendar
    pg.goto(URL+'#/h'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>__ln.l.localNotificationActionPerformed({})"); pg.wait_for_timeout(300)
    ok(pg.url.endswith('#/c'),'Phone: tapping the notification opens the Calendar')
    # in-app timer must not duplicate the phone alarm
    pg.evaluate("()=>{S.set.cal.push({id:'t1',d:today(),n:'TodayGuy',ph:'',t:'custom',a:5,doc:'',note:'',ok:0,u:Date.now()});S.set.rt='00:00';S.set.rn='';__ln.calls.length=0;remCheck()}"); pg.wait_for_timeout(300)
    ok(pg.evaluate("()=>__ln.calls.filter(c=>c[0]=='schedule').length")==0,'Phone: in-app timer stays quiet (phone alarm does the job)')
    ok(errs==[],'Phone: no JavaScript errors '+str(errs)); ctx.close()

    # ================= 3. BROWSER / INSTALLED WEB APP =================
    ctx=b.new_context(viewport={'width':1300,'height':900},timezone_id='Asia/Kolkata'); ctx.grant_permissions(['notifications'],origin='http://localhost:8123'); pg,errs=boot(ctx)
    pg.wait_for_timeout(800)
    reg=pg.evaluate("async()=>!!(await navigator.serviceWorker.getRegistration())"); ok(reg,'Web: service worker registered')
    pg.evaluate("()=>{S.set.cal=[{id:'w1',d:today(),n:'Webguy',ph:'9111111111',t:'custom',a:1234,doc:'',note:'',ok:0,u:Date.now()}];S.set.rt='00:00';S.set.rn='';save();remCheck()}"); pg.wait_for_timeout(1200)
    shown=pg.evaluate("async()=>(await (await navigator.serviceWorker.ready).getNotifications()).map(n=>[n.title,n.body,n.tag])")
    ok(len(shown)==1 and shown[0][0]=='Collect money today (1)' and 'Webguy' in shown[0][1] and '1,234' in shown[0][1],'Web: reminder notification shown through the service worker '+str(shown))
    ok(pg.evaluate("()=>S.set.rn===today()"),'Web: fires once per day')
    # list handed to the service worker for background checks
    due=pg.evaluate("async()=>{const r=await (await caches.open('zx-note')).match('due.json');return r?await r.json():null}")
    ok(due and due['rt']=='00:00' and len(due['list'])==1 and due['last']==T,'Web: due list + last-notified stored for the background check '+str(due))
    # background check inside the service worker (what Chrome runs when the page is closed)
    pg.evaluate("async()=>{const r=await navigator.serviceWorker.ready;(await r.getNotifications()).forEach(n=>n.close());const c=await caches.open('zx-note');await c.put('due.json',new Response(JSON.stringify({rt:'00:00',last:'',list:[{d:today(),n:'BG Guy',a:777,ph:''}]})))}")
    cdp=ctx.new_cdp_session(pg); regs=[]
    cdp.on('ServiceWorker.workerRegistrationUpdated',lambda e:regs.extend(e.get('registrations',[])))
    cdp.send('ServiceWorker.enable'); pg.wait_for_timeout(600)
    rid=regs[-1]['registrationId'] if regs else None
    if rid:
        cdp.send('ServiceWorker.dispatchPeriodicSyncEvent',{'origin':'http://localhost:8123','registrationId':rid,'tag':'zx-due'}); pg.wait_for_timeout(1500)
        shown=pg.evaluate("async()=>(await (await navigator.serviceWorker.ready).getNotifications()).map(n=>[n.title,n.body])")
        ok(len(shown)==1 and 'BG Guy' in shown[0][1] and '777' in shown[0][1],'Web: background (periodic sync) check shows the notification with the page not involved '+str(shown))
        pg.evaluate("async()=>{(await (await navigator.serviceWorker.ready).getNotifications()).forEach(n=>n.close())}")
        cdp.send('ServiceWorker.dispatchPeriodicSyncEvent',{'origin':'http://localhost:8123','registrationId':rid,'tag':'zx-due'}); pg.wait_for_timeout(1000)
        ok(pg.evaluate("async()=>(await (await navigator.serviceWorker.ready).getNotifications()).length")==0,'Web: background check does not repeat the same day')
    else: print('SKIP background-sync dispatch (no registration id from CDP)')
    # cache survives service-worker update (activate keeps zx-note)
    ok('zx-note' in pg.evaluate("async()=>await caches.keys()"),'Web: reminder cache is kept by service worker clean-up')
    ok(errs==[],'Web: no JavaScript errors '+str(errs)); ctx.close()
    b.close()
print('\n%d/%d checks passed'%(sum(res),len(res)))
raise SystemExit(0 if all(res) else 1)
