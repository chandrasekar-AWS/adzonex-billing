import json, time, base64, re, urllib.parse
SB='https://krfjrasoihxhxnjskrhi.supabase.co'
KEY='sb_publishable_E9aUji5CGt6_MPWWzfMJbw_tw8NXJ1s'
UID='11111111-1111-1111-1111-111111111111'
def b64(o): return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip('=')
def jwt(ttl=3600): return b64({'alg':'HS256','typ':'JWT'})+'.'+b64({'sub':UID,'role':'authenticated','exp':int(time.time())+ttl,'email':'owner@adzonex.in'})+'.sig'
USERS={'owner@adzonex.in':'11111111-1111-1111-1111-111111111111','friend@adzonex.in':'22222222-2222-2222-2222-222222222222','outsider@adzonex.in':'33333333-3333-3333-3333-333333333333'}
USER={'id':UID,'aud':'authenticated','role':'authenticated','email':'owner@adzonex.in','email_confirmed_at':'2026-01-01T00:00:00Z','app_metadata':{},'user_metadata':{},'created_at':'2026-01-01T00:00:00Z'}
CORS={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'GET,POST,PATCH,DELETE,OPTIONS','access-control-expose-headers':'*'}
class Server:
    def __init__(s): s.docs={}; s.settings=None; s.log=[]; s.token=None; s.disable_signup=True; s.fail=False; s.password='Correct-Horse-9'; s.tokens={}; s.ttl=3600; s.refreshes=0; s.legacy=False; s.notables=False; s.expire_once=False; s.offline=False; s.team={USERS['owner@adzonex.in'],USERS['friend@adzonex.in']}
    def session(s,email='owner@adzonex.in'):
        t=jwt(s.ttl)+str(len(s.tokens)); s.tokens[t]=email; s.token=t; return {'access_token':t,'token_type':'bearer','expires_in':s.ttl,'expires_at':int(time.time())+s.ttl,'refresh_token':'r-'+str(time.time()),'user':{**USER,'id':USERS[email],'email':email}}
    def who(s,req):
        a=req.headers.get('authorization','');return s.tokens.get(a[7:]) if a.startswith('Bearer ') else None
    def authed(s,req):
        a=req.headers.get('authorization','');return a.startswith('Bearer ') and a[7:] in s.tokens
    def handle(s,route):
        req=route.request; u=urllib.parse.urlparse(req.url); q=urllib.parse.parse_qs(u.query); path=u.path
        h=dict(CORS)
        if s.offline: return route.abort('internetdisconnected')
        if req.method=='OPTIONS': return route.fulfill(status=204,headers=h)
        s.log.append((req.method,path,u.query,dict(req.headers)))
        def js(o,st=200,extra=None):
            hh={**h,'content-type':'application/json'};hh.update(extra or {})
            return route.fulfill(status=st,headers=hh,body=json.dumps(o))
        if s.fail and path.startswith('/rest/'): return js({'message':'boom','code':'XX000'},500)
        if path=='/auth/v1/token':
            gt=q.get('grant_type',[''])[0]
            if gt=='password':
                b=json.loads(req.post_data or '{}')
                if b.get('password')!=s.password or b.get('email') not in USERS: return js({'code':400,'error_code':'invalid_credentials','msg':'Invalid login credentials'},400)
                return js(s.session(b['email']))
            s.refreshes+=1
            return js(s.session())
        if path=='/auth/v1/user': return js({**USER,'email':s.who(req),'id':USERS[s.who(req)]}) if s.authed(req) else js({'msg':'bad jwt'},401)
        if path=='/auth/v1/logout':
            a=req.headers.get('authorization','')[7:]; s.tokens.pop(a,None); return route.fulfill(status=204,headers=h)
        if path=='/auth/v1/settings': return js({'disable_signup':s.disable_signup,'external':{'email':True}})
        if path=='/rest/v1/rpc/is_team_member' and s.legacy: return js({'code':'PGRST202','message':'Could not find the function public.is_team_member without parameters in the schema cache'},404)
        if path=='/rest/v1/rpc/is_team_member':
            return js(bool(s.authed(req) and USERS[s.who(req)] in s.team)) if s.authed(req) else js({'message':'permission denied'},401)
        if path=='/rest/v1/rpc/my_role':
            if not s.authed(req): return js({'message':'permission denied'},401)
            return js(getattr(s,'roles',{}).get(s.who(req),'admin'))
        m=re.match(r'/rest/v1/(docs|app_settings)$',path)
        if not m: return js({'message':'not found'},404)
        if s.notables: return js({'code':'PGRST205','message':"Could not find the table 'public."+m.group(1)+"' in the schema cache"},404)
        if s.expire_once and s.authed(req): s.expire_once=False; return js({'code':'PGRST301','message':'JWT expired'},401)
        t=m.group(1); ok=s.authed(req) and (s.legacy or USERS[s.who(req)] in s.team); me=USERS[s.who(req)] if s.authed(req) else None
        if req.method=='GET':
            if not ok: return js([])
            sel=q.get('select',['*'])[0]
            if t=='docs':
                rows=list(s.docs.values())
                if 'id' in q and q['id'][0].startswith('in.('):
                    ids=[x.strip('"') for x in q['id'][0][4:-1].split(',')]; rows=[r for r in rows if r['id'] in ids]
                rows.sort(key=lambda r:r['id'])
                off=int(q.get('offset',['0'])[0]); lim=int(q.get('limit',['1000'])[0]); rows=rows[off:off+lim]
            else: rows=[s.settings] if s.settings else []
            return js([{k:r[k] for k in (r.keys() if sel=='*' else sel.split(','))} for r in rows])
        if req.method=='POST':
            if not ok: return js({'code':'42501','message':'new row violates row-level security policy'},403)
            body=json.loads(req.post_data); body=body if isinstance(body,list) else [body]
            oc=q.get('on_conflict',[''])[0]
            if s.legacy:
                if t=='docs' and oc=='id': return js({'code':'42P10','message':'there is no unique or exclusion constraint matching the ON CONFLICT specification'},400)
                if t=='app_settings' and any('id' in r for r in body): return js({'code':'PGRST204','message':"Could not find the 'id' column of 'app_settings' in the schema cache"},400)
            for r in body:
                role=getattr(s,'roles',{}).get(s.who(req),'admin')
                if role=='biller' and t=='app_settings': return js({'code':'42501','message':'new row violates row-level security policy'},403)
                if role=='biller' and t=='docs' and r['id'] in s.docs and s.docs[r['id']].get('user_id')!=me: return js({'code':'42501','message':'new row violates row-level security policy'},403)
                assert r['user_id']==me, 'user_id spoof'
                if t=='docs': s.docs[r['id']]=r
                else:
                    assert r.get('id','main')=='main'; s.settings=r
            return route.fulfill(status=201,headers=h,body='')
        return js({'message':'unsupported'},405)
