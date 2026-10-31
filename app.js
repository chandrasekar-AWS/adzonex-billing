const FRAMED=window.top!==window.self;if(FRAMED)document.documentElement.setAttribute('data-framed','1');
const $=s=>document.querySelector(s),K='adzonex-billing-v1',app=$('#app');
const SV=[{"n":"Normal Flex","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/normal-flex.svg","h":"","p":0},{"n":"Black Flex","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/black-flex.svg","h":"","p":0},{"n":"Star Flex","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/star-flex.svg","h":"","p":0},{"n":"Normal Flex with 1\" MS frame","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/normal-flex-with-1-ms-frame.svg","h":"","p":0},{"n":"Black Flex with 1\" MS frame","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/black-flex-with-1-ms-frame.svg","h":"","p":0},{"n":"Star Flex with 1\" MS frame","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/star-flex-with-1-ms-frame.svg","h":"","p":0},{"n":"Star Backlit","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/star-backlit.svg","h":"","p":0},{"n":"Star Backlit with 1\" MS frame","c":"Flex Printing","k":"pr","u":"Sqf","i":"images/star-backlit-with-1-ms-frame.svg","h":"","p":0},{"n":"Solvent Vinyl","c":"Solvent Vinyl","k":"pr","u":"Sqf","i":"images/solvent-vinyl.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl","c":"Solvent Vinyl","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl.svg","h":"","p":0},{"n":"Solvent Vinyl with Lamination","c":"Solvent Vinyl","k":"pr","u":"Sqf","i":"images/solvent-vinyl-with-lamination.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl with Lamination","c":"Solvent Vinyl","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl-with-lamination.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl","c":"Eco Solvent Vinyl","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl.svg","h":"","p":0},{"n":"Eco Solvent Vinyl with Lamination","c":"Eco Solvent Vinyl","k":"pr","u":"Sqf","i":"images/eco-solvent-vinyl-with-lamination.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl with Lamination","c":"Eco Solvent Vinyl","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl-with-lamination.svg","h":"","p":0},{"n":"Solvent Vinyl with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/solvent-vinyl-with-3mm-foam.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl-with-3mm-foam.svg","h":"","p":0},{"n":"Solvent Vinyl with Lamination with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/solvent-vinyl-with-lamination-with-3mm-foam.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl with Lamination with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl-with-lamination-with-3mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl-with-3mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Vinyl with Lamination with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-vinyl-with-lamination-with-3mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl with Lamination with 3mm Foam","c":"Vinyl with 3mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl-with-lamination-with-3mm-foam.svg","h":"","p":0},{"n":"Solvent Vinyl with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/solvent-vinyl-with-5mm-foam.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl-with-5mm-foam.svg","h":"","p":0},{"n":"Solvent Vinyl with Lamination with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/solvent-vinyl-with-lamination-with-5mm-foam.svg","h":"","p":0},{"n":"Solvent Grey Back Vinyl with Lamination with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/solvent-grey-back-vinyl-with-lamination-with-5mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl-with-5mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Vinyl with Lamination with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-vinyl-with-lamination-with-5mm-foam.svg","h":"","p":0},{"n":"Eco Solvent Grey Back Vinyl with Lamination with 5mm Foam","c":"Vinyl with 5mm Foam","k":"pr","u":"Sqf","i":"images/eco-solvent-grey-back-vinyl-with-lamination-with-5mm-foam.svg","h":"","p":0},{"n":"Solvent One-way Vision","c":"One-way Vision & Clear Vinyl","k":"pr","u":"Sqf","i":"images/solvent-one-way-vision.svg","h":"","p":0},{"n":"Eco Solvent One-way Vision","c":"One-way Vision & Clear Vinyl","k":"pr","u":"Sqf","i":"images/eco-solvent-one-way-vision.svg","h":"","p":0},{"n":"Solvent Clear Vinyl","c":"One-way Vision & Clear Vinyl","k":"pr","u":"Sqf","i":"images/solvent-clear-vinyl.svg","h":"","p":0},{"n":"Eco Solvent Clear Vinyl","c":"One-way Vision & Clear Vinyl","k":"pr","u":"Sqf","i":"images/eco-solvent-clear-vinyl.svg","h":"","p":0},{"n":"UV Backlit","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-backlit.svg","h":"","p":0},{"n":"UV Flex","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-flex.svg","h":"","p":0},{"n":"UV Flex with 1\" MS frame","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-flex-with-1-ms-frame.svg","h":"","p":0},{"n":"UV Backlit with 1\" MS frame","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-backlit-with-1-ms-frame.svg","h":"","p":0},{"n":"UV Vinyl","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-vinyl.svg","h":"","p":0},{"n":"UV Clear","c":"UV Printing","k":"pr","u":"Sqf","i":"images/uv-clear.svg","h":"","p":0},{"n":"Acrylic Direct UV Print","c":"UV Printing","k":"pr","u":"Sqf","i":"images/acrylic-direct-uv-print.svg","h":"","p":0},{"n":"Foam Direct UV Print","c":"UV Printing","k":"pr","u":"Sqf","i":"images/foam-direct-uv-print.svg","h":"","p":0},{"n":"Logo Design","c":"Design","k":"pr","u":"Nos","i":"images/logo-design.svg","h":"","p":0},{"n":"Poster & Flex Design","c":"Design","k":"pr","u":"Nos","i":"images/poster-flex-design.svg","h":"","p":0},{"n":"Graphic Design","c":"Design","k":"pr","u":"Nos","i":"images/graphic-design.svg","h":"","p":0},{"n":"Social Media Management","c":"Digital Marketing","k":"dm","u":"Month","i":"images/social-media-management.svg","h":"","p":0},{"n":"Ads Management (Meta / Google)","c":"Digital Marketing","k":"dm","u":"Month","i":"images/ads-management-meta-google.svg","h":"","p":0},{"n":"SEO","c":"Digital Marketing","k":"dm","u":"Month","i":"images/seo.svg","h":"","p":0},{"n":"Content & Reels","c":"Digital Marketing","k":"dm","u":"Month","i":"images/content-reels.svg","h":"","p":0},{"n":"Website Design","c":"Digital Marketing","k":"dm","u":"Month","i":"images/website-design.svg","h":"","p":0},{"n":"AWS Cloud Services","c":"Digital Marketing","k":"dm","u":"Month","i":"images/aws-cloud-services.svg","h":"","p":0}];
const GR=['Design','Print','Signage','Digital'],grOf=v=>v.k=='dm'?'Digital':v.c=='Design'?'Design':/frame|backlit|foam/i.test(v.n||'')?'Signage':'Print';SV.forEach(x=>x.g=grOf(x));
const DC={hd:'#000000',ac:'#2bff05',th:'#111111',tt:'#111111'};
const D0={ne:101,nb:0,nv:0,name:'Ad ZoneX',addr:'#132/2, 2nd Street, Gm Nagar,\nUkkadam\nCoimbatore - 641001',gst:'',phone:'9342307860',email:'enqury@adzonex.in',bank:'',acc:'',ifsc:'',holder:'',payto:'ADZONEDESIGN',logo:'',url:'',key:'',copy:'',auto:true,bw:false,colors:{...DC},su:0,services:SV,cal:[],exp:[],terms:'70% Advance to initiate the job process\nThe balance amount to be settled after the installations\nGST 18% extra\nTransport charge extra\nScaffolding charge extra'};
let S={set:{},docs:[]};try{S=JSON.parse(localStorage.getItem(K))||S}catch{}S.set={...D0,...S.set};S.set.key='';S.set.colors={...DC,...(S.set.colors&&typeof S.set.colors=='object'?S.set.colors:{})};S.docs=S.docs||[];

function tdy(){const t=new Date();return t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0')}
const sx=(v,m=2000)=>typeof v=='string'?v.slice(0,m):(typeof v=='number'&&isFinite(v)?String(v):''),ob=a=>(Array.isArray(a)?a:[]).filter(x=>x&&typeof x=='object'&&!Array.isArray(x)).slice(0,500),ob2=(a,m=20000)=>(Array.isArray(a)?a:[]).filter(x=>x&&typeof x=='object'&&!Array.isArray(x)).slice(0,m),dOk=v=>/^\d{4}-\d{2}-\d{2}$/.test(v||'');
const okImg=u=>typeof u=='string'&&(/^images\/[\w.-]+\.svg$/.test(u)||(u.length<400000&&/^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+\/=]+$/.test(u)))?u:'images/logo-design.svg';
const okSv=x=>{const o={n:sx(x.n,120),c:sx(x.c,60)||'Other',k:x.k=='dm'?'dm':'pr',u:sx(x.u,12),h:sx(x.h,12),p:isFinite(+x.p)&&+x.p>0?+x.p:0,i:okImg(x.i)};o.g=GR.includes(x.g)?x.g:grOf(o);o.k=o.g=='Digital'?'dm':'pr';return o};
const TXT=['name','addr','gst','phone','email','bank','acc','ifsc','holder','payto','terms','copy'];
function okSet(v){const o={};if(!v||typeof v!='object'||Array.isArray(v))return o;
TXT.forEach(k=>{if(k in v)o[k]=sx(v[k],k=='terms'||k=='addr'?2000:200)});
['ne','nb'].forEach(k=>{if(k in v){const n=Math.floor(+v[k]);o[k]=isFinite(n)&&n>=0&&n<1e9?n:0}});
['auto','bw'].forEach(k=>{if(k in v)o[k]=v[k]===true});
if('svv' in v)o.svv=+v.svv||0;
if(v.colors&&typeof v.colors=='object')o.colors=Object.fromEntries(Object.keys(DC).map(k=>[k,hx(v.colors[k],DC[k])]));
if(Array.isArray(v.services))o.services=ob(v.services).map(okSv);
if(Array.isArray(v.cal))o.cal=ob2(v.cal).map(okCal).filter(Boolean);
if(Array.isArray(v.exp))o.exp=ob2(v.exp).map(okExp).filter(Boolean);
return o}
const okDoc=r=>{if(!r||typeof r!='object'||typeof r.id!='string'||!/^[\w-]{1,64}$/.test(r.id))return null;
const o={id:r.id,u:+r.u||0};['estNo','billNo','cust','phone','email','addr','cgst','pos','disc'].forEach(k=>o[k]=sx(r[k],k=='addr'?600:200));o.terms=sx(r.terms,3000);o.rem=sx(r.rem,1000);
o.date=dOk(r.date)?r.date:tdy();o.hsn=r.hsn!==false;o.igst=!!r.igst;o.gst=!!r.gst;o.rate=r.rate===''||r.rate==null||!isFinite(+r.rate)?18:+r.rate;
o.pfx=r.pfx==='INV'?'INV':r.pfx?'BIL':undefined;if(r.del)o.del=1;if(r.bl)o.bl=1;
o.sig=typeof r.sig=='string'&&r.sig.length<900000&&/^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+\/=]+$/.test(r.sig)?r.sig:'';
o.items=ob(r.items).map(i=>({n:sx(i.n,300),h:sx(i.h,20),s:sx(i.s,40),q:sx(i.q,20),u:sx(i.u,12),p:sx(i.p,20)}));
o.dm=ob(r.dm).map(i=>({n:sx(i.n,300),d:sx(i.d,500),m:sx(i.m,20),p:sx(i.p,20)}));
o.pay=ob(r.pay).map(x=>({d:dOk(x.d)?x.d:tdy(),a:isFinite(+x.a)&&+x.a>0&&+x.a<1e10?+x.a:0,m:sx(x.m,30)})).filter(x=>x.a>0);
o.log=ob(r.log).map(x=>({t:+x.t||0,e:sx(x.e,200)})).slice(-200);return o};
function okCal(r){if(!r||typeof r!='object'||typeof r.id!='string'||!/^[\w-]{1,64}$/.test(r.id)||!dOk(r.d))return null;const a=+r.a;return{id:r.id,d:r.d,n:sx(r.n,120),ph:sx(r.ph,30),t:['full','half','bal','custom'].includes(r.t)?r.t:'custom',a:isFinite(a)&&a>=0&&a<1e10?a:0,doc:/^[\w-]{1,64}$/.test(r.doc||'')?r.doc:'',note:sx(r.note,300),ok:r.ok?1:0,u:+r.u||0,...(r.del?{del:1}:{})}}
function okExp(r){if(!r||typeof r!='object'||typeof r.id!='string'||!/^[\w-]{1,64}$/.test(r.id)||!dOk(r.d))return null;const a=+r.a;return{id:r.id,d:r.d,c:sx(r.c,40),n:sx(r.n,200),a:isFinite(a)&&a>=0&&a<1e10?a:0,m:sx(r.m,20),u:+r.u||0,...(r.del?{del:1}:{})}}
const mergeL=(a,b)=>{const m=new Map();[...(a||[]),...(b||[])].forEach(x=>{const o=m.get(x.id);if(!o||x.u>o.u)m.set(x.id,x)});return[...m.values()]};
S.docs=S.docs.map(okDoc).filter(Boolean);S.set.cal=ob2(S.set.cal).map(okCal).filter(Boolean);S.set.exp=ob2(S.set.exp).map(okExp).filter(Boolean);

const save=()=>{try{localStorage.setItem(K,JSON.stringify(S))}catch{alert('Could not save. Browser storage is full or blocked.')}};
const SB_URL='https://krfjrasoihxhxnjskrhi.supabase.co',SB_KEY='sb_publishable_E9aUji5CGt6_MPWWzfMJbw_tw8NXJ1s';
const sb=!FRAMED&&window.supabase?supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:false}}):null;
let SES=null;
const cloud=()=>!!(sb&&SES),mailOk=()=>!!(cloud()&&okUrl(S.set.url));
const okUrl=u=>/^https:\/\/script\.google\.com\/(?:a\/macros\/[\w.-]+\/|a\/[\w.-]+\/macros\/|macros\/)s\/[\w-]+\/exec$/.test(u||''),EMRE=/^[^\s@,;<>"()\[\]\\]+@[^\s@,;<>"()\[\]\\]+\.[^\s@,;<>"()\[\]\\]+$/;
function st(t,c,m){SYNCINFO=m||'';const b=$('#sync');if(b){b.textContent=t;b.className='sync '+(c||'');b.title=m||'';if(m){b.setAttribute('role','button');b.tabIndex=0}else{b.removeAttribute('role');b.removeAttribute('tabindex')}}}
document.addEventListener('click',e=>{if(SYNCINFO&&e.target.closest&&e.target.closest('#sync'))alert(SYNCINFO)});document.addEventListener('keydown',e=>{if(SYNCINFO&&e.key==='Enter'&&e.target.id==='sync')alert(SYNCINFO)});
const mk=r=>{const x=new Error(r.error.message||'Unknown error');x.code=r.error.code;x.status=r.status;return x},ck=r=>{if(r.error)throw mk(r);return r.data};
let LEGACY=false,SCHEMA=null,MEMBER=null,SYNCINFO='';
const oldSchema=x=>!!x&&(x.code==='42P10'||x.code==='PGRST204'||/ON CONFLICT/i.test(x.message||'')),authErr=x=>!!x&&(x.status===401||/\bJWT\b|jwt expired/i.test(x.message||''));
const TEAMSQL=em=>"insert into public.team (user_id, email) select id, email from auth.users where email = '"+String(em).replace(/'/g,"''")+"' on conflict do nothing;";
function explain(x){const m=String((x&&x.message)||x||''),c=x&&x.code,em=(SES&&SES.user&&SES.user.email)||'your-login@example.com';
if(!navigator.onLine||/Failed to fetch|NetworkError|Load failed|network request failed|ERR_/i.test(m))return['Offline','There is no internet connection right now. Everything you do is saved on this device and uploads by itself when the connection is back.'];
if(c==='PGRST205'||c==='42P01'||/Could not find the table|does not exist/i.test(m))return['Database not set up','The Supabase tables are missing.\n\nOpen Supabase > SQL Editor > New query, paste everything from backend/supabase.sql, click Run, then press Sync now.'];
if(c==='42501'||/row-level security|permission denied/i.test(m))return['Login not in team','This login ('+em+') is not in your team yet, so Supabase refuses to save.\n\nOpen Supabase > SQL Editor and run:\n\n'+TEAMSQL(em)+'\n\nThen press Sync now.'];
if(c==='PGRST202'||c==='42883'||/Could not find the function/i.test(m))return['Database needs upgrade','Your Supabase database is the older private version.\n\nOpen Supabase > SQL Editor, paste everything from backend/supabase.sql and click Run. Your bills are kept.'];
if(authErr(x))return['Please sign in again','Your login session has expired.\n\nGo to Settings > Sign out, then sign in again.'];
if(x&&x.status>=500)return['Server busy','Supabase is not answering right now. The app will try again in a few seconds.'];
return['Sync problem','Details: '+m+(c?' ('+c+')':'')]}
const syncFail=(x,retry)=>{const[sh,lg]=explain(x);st(sh=='Offline'?(retry?'Offline, will retry':'Offline'):sh+' - click for help','bad',lg)};
async function mailApi(p){if(!okUrl(S.set.url))throw new Error('The email script address in Settings is not a valid Google Apps Script web app address.');const ss=(await sb.auth.getSession()).data.session;if(!ss)throw new Error('Not signed in');const r=await fetch(S.set.url,{method:'POST',headers:{'Content-Type':'text/plain'},body:JSON.stringify({jwt:ss.access_token,a:'mail',...p}),signal:AbortSignal.timeout(30000)});const j=await r.json();if(j.err)throw new Error(j.err);return j}
async function api(a,p={}){try{return await api0(a,p)}catch(x){if(authErr(x)&&sb){const r=await sb.auth.refreshSession();if(r.data&&r.data.session){SES=r.data.session;return await api0(a,p)}}throw x}}
async function upDocs(rows){if(!LEGACY){const r=await sb.from('docs').upsert(rows,{onConflict:'id'});if(!r.error)return;if(!oldSchema(r.error))throw mk(r);LEGACY=true}ck(await sb.from('docs').upsert(rows,{onConflict:'user_id,id'}))}
async function upSet(o){if(!LEGACY){const r=await sb.from('app_settings').upsert({id:'main',...o},{onConflict:'id'});if(!r.error)return;if(!oldSchema(r.error))throw mk(r);LEGACY=true}ck(await sb.from('app_settings').upsert(o,{onConflict:'user_id'}))}
async function api0(a,p={}){if(!cloud())throw new Error('Not signed in');
if(a=='ping'){ck(await sb.from('app_settings').select('updated').limit(1));return{ok:1}}
if(a=='pull'){const o=[];for(let f=0;;f+=1000){const d=ck(await sb.from('docs').select('data').order('id').range(f,f+999));o.push(...d.map(r=>r.data));if(d.length<1000)break}
const s=ck(await sb.from('app_settings').select('data').maybeSingle());return{docs:o,set:s?s.data:null}}
if(a=='push'){const m=new Map();for(let f=0;f<p.docs.length;f+=100){ck(await sb.from('docs').select('id,updated').in('id',p.docs.slice(f,f+100).map(d=>d.id))).forEach(r=>m.set(r.id,+r.updated))}
const rows=p.docs.filter(d=>!(m.has(d.id)&&m.get(d.id)>=d.u)).map(d=>({user_id:SES.user.id,id:d.id,updated:d.u,data:d,est_no:d.estNo||null,bill_no:d.billNo||null,customer:d.cust||null,status:d.del?'deleted':(d.pay&&d.pay.length?'bill':'estimate')}));
for(let f=0;f<rows.length;f+=50)await upDocs(rows.slice(f,f+50));return{ok:1}}
if(a=='pushset'){const r=ck(await sb.from('app_settings').select('updated').maybeSingle());if(!r||+r.updated<p.set.u)await upSet({user_id:SES.user.id,updated:p.set.u,data:p.set});return{ok:1}}
throw new Error('Unknown action')}
const pend=new Set();let tm;
function touch(d){if(!S.docs.includes(d))return;d.u=Date.now();save();pend.add(d.id);clearTimeout(tm);tm=setTimeout(push,800)}
function commit(d){if(!S.docs.includes(d)){d.estNo=d.estNo||mkNo(d.date);lg(d,'Estimate '+d.estNo+' saved');S.docs.unshift(d)}touch(d)}
const SH=['name','addr','gst','phone','email','bank','acc','ifsc','holder','payto','terms','copy','auto','services','svv','logo','ne','nb','bw','colors','cal','exp'];
const sch=()=>{S.set.su=Date.now();S.pset=1;save();clearTimeout(tm);tm=setTimeout(push,800);schedNote()};
async function push(){if(!cloud())return;const ids=[...pend];try{st('Saving…');pend.clear();if(ids.length)await api('push',{docs:S.docs.filter(d=>ids.includes(d.id))});if(S.pset){await api('pushset',{set:{u:S.set.su,v:Object.fromEntries(SH.map(k=>[k,S.set[k]]))}});S.pset=0;save()}LEGACY?st('Synced (not shared)','ok','Your Supabase database is still the older private version, so bills are NOT shared between logins.\n\nTo share them: Supabase > SQL Editor > paste everything from backend/supabase.sql > Run. Your bills are kept.'):st('Synced','ok')}catch(x){console.warn('push',x);ids.forEach(i=>pend.add(i));syncFail(x,true);clearTimeout(tm);tm=setTimeout(push,15000)}}
let PULLING=null,LASTPULL=0;function pull(){if(PULLING)return PULLING;return PULLING=pull0().finally(()=>{PULLING=null;LASTPULL=Date.now()})}
async function pull0(){if(!cloud())return;try{st('Syncing…');if(SCHEMA===null){const t=await sb.rpc('is_team_member');if(t.error){if(authErr(mk(t))){const e=mk(t);throw e}if(t.error.code==='PGRST202'||t.error.code==='42883'||/Could not find the function/i.test(t.error.message||'')){SCHEMA='old';LEGACY=true}}else{SCHEMA='new';MEMBER=t.data===true}}
if(SCHEMA==='new'&&MEMBER===false){const[sh,lg]=explain({code:'42501',message:'row-level security'});st(sh+' - click for help','bad',lg);return}
const j=await api('pull'),rd=j.docs.map(okDoc).filter(Boolean);
rd.forEach(r=>{const l=S.docs.find(d=>d.id==r.id);if(!l)S.docs.push(r);else if(r.u>l.u)Object.assign(l,r)});
const rm=new Map(rd.map(r=>[r.id,r.u]));S.docs.forEach(d=>{if(!rm.has(d.id)||d.u>rm.get(d.id))pend.add(d.id)});
let np=0;const rc=j.set&&j.set.v&&typeof j.set.v=='object'?okSet(j.set.v):null;
if(rc)['cal','exp'].forEach(k=>{const rr=k in rc?rc[k]:[],m=mergeL(S.set[k],rr);if(m.length!=rr.length||m.some(x=>{const r=rr.find(y=>y.id==x.id);return!r||r.u<x.u}))np=1;S.set[k]=m});
if(rc&&+j.set.u>(S.set.su||0)){SH.forEach(k=>{if(k in rc&&k!='cal'&&k!='exp')S.set[k]=rc[k]});if(!Array.isArray(S.set.services)||!S.set.services.length)S.set.services=SV.map(x=>({...x}));S.set.su=+j.set.u}else if(!j.set)S.pset=1;
if(np){S.set.su=Date.now();S.pset=1}
S.docs.sort((a,b)=>b.u-a.u);save();schedNote();await push()}catch(x){console.warn('sync',x);syncFail(x,false)}}
async function mail(d,auto){if(!mailOk()){if(!auto)alert('Email is not set up. Sign in, then add the email script URL in Settings > Email.');return}const ta=[d.email,S.set.copy].map(x=>String(x||'').trim()).filter(Boolean),bad=ta.filter(x=>!EMRE.test(x));if(!ta.length){if(!auto)alert('Add the customer email, or your own email in Settings.');return}if(bad.length){if(!auto)alert('This email address does not look right: '+bad[0]);else st('Email not sent: check the address','bad');return}const to=ta.join(',');
try{st('Sending email…');let pdfB='';try{pdfB=(await pdfMake(d)).output('datauristring').split(',')[1]}catch(x){console.warn('pdf for mail',x)}await mailApi({to,subject:(isBill(d)?'Invoice ':'Estimate ')+no(d)+' - '+S.set.name,file:no(d).replace(/[\/\\]/g,'-'),html:paper(d),pdf:pdfB});lg(d,'Emailed to '+to);touch(d);st('Email sent','ok');if(!auto)alert('Email sent to '+to)}catch(x){st('Email failed','bad');alert('Email failed: '+x.message)}}
const NQ=/^\d{6}-\d{2}(\d+)$/,OQ=/^\d{4}-\d{2}-\d{2}-(\d+)$/,seqOf=c=>{const m=NQ.exec(c||'')||OQ.exec(c||'');return m?+m[1]:0},nextSeq=()=>Math.max(+S.set.ne||101,S.docs.reduce((a,d)=>Math.max(a,seqOf(d.estNo)),0)+1),mkNo=dt=>{const p=(dt||today()).split('-');return p[0]+p[1]+'-'+p[2]+nextSeq()};
if(S.set.nv!=3){S.set.ne=101;S.set.nv=3}
S.docs.forEach(d=>{if(!d.u){d.u=1;pend.add(d.id)}const m=/^(\d{4})-(\d{2})-(\d{2})-(\d+)$/.exec(d.estNo||'');if(m){d.estNo=m[1]+m[2]+'-'+m[3]+m[4];d.u=Date.now();pend.add(d.id)}});
if(!Array.isArray(S.set.services)||!S.set.services.length||S.set.svv!=2){const fresh=!(S.set.su>0);S.set.services=SV.map(x=>({...x}));S.set.svv=2;if(!fresh){S.set.su=Date.now();S.pset=1}}
S.set.services=S.set.services.filter(v=>v&&typeof v=='object');if(!S.set.services.length)S.set.services=SV.map(x=>({...x}));
S.set.services.forEach(v=>{v.c=v.c||'Other';v.k=v.k||'pr';v.i=v.i||'images/logo-design.svg';v.h=v.h||hsnFor(v.n)});
S.set.services.forEach(v=>{v.g=GR.includes(v.g)?v.g:grOf(v);v.k=v.g=='Digital'?'dm':'pr'});
function lg(d,t){(d.log=d.log||[]).push({t:Date.now(),e:t})}
function pj(h){const w=document.createElement('div');w.className='pw';w.innerHTML=h;document.body.append(w);document.body.classList.add('pj');try{print()}finally{w.remove();document.body.classList.remove('pj')}}
const isNat=()=>{const C=window.Capacitor;return !!(C&&C.isNativePlatform&&C.isNativePlatform())};
const bl=()=>({n:'',h:'',s:'',q:'',u:'',p:''}),bd=()=>({n:'',d:'',m:'',p:''});
const newDoc=()=>({id:Date.now().toString(36)+Math.random().toString(36).slice(2,7),estNo:'',billNo:'',disc:'',date:today(),cust:'',phone:'',email:'',addr:'',cgst:'',pos:'',sig:'',hsn:true,igst:false,gst:false,rate:18,rem:'',terms:S.set.terms,items:[bl()],dm:[bd()],pay:[],log:[]});
async function renderPdf(html,title){const L=u=>new Promise((r,j)=>{const x=document.createElement('script');x.src=u;x.onload=r;x.onerror=j;document.head.append(x)});if(!window.html2canvas)await L('libs/html2canvas.min.js');if(!window.jspdf)await L('libs/jspdf.umd.min.js');
try{await document.fonts.ready}catch{}
const w=document.createElement('div');w.className='pdfx';w.innerHTML=html;document.body.append(w);
try{const el=w.firstElementChild;await Promise.all([...el.querySelectorAll('img')].map(i=>i.decode?i.decode().catch(()=>{}):0));
const cv=await html2canvas(el,{scale:3,backgroundColor:'#ffffff',useCORS:true,logging:false}),R=el.getBoundingClientRect(),Wd=R.width,Ht=R.height,K=cv.width/Wd,Ph=Wd*297/210,M=44,y0=R.top;
const cand=[...el.querySelectorAll('tr,.pbot,.prm,.pf,.psg,.pft,h4')].map(x=>x.getBoundingClientRect().top-y0).filter(v=>v>0);
const tb=el.querySelector('.pq'),thd=tb&&tb.querySelector('thead'),tbB=tb?tb.getBoundingClientRect().bottom-y0:0,thT=thd?thd.getBoundingClientRect().top-y0:0,thB=thd?thd.getBoundingClientRect().bottom-y0:0,thH=thB-thT,hdr=(f,yy)=>(!f&&thd&&yy>thB&&yy<tbB-2)?thH:0;
const sl=[];let y=0,first=true;const cap=()=>first?Ph-M:Ph-2*M;
if(Ht>Ph+2)while(Ht-y>cap()-hdr(first,y)+1){const hh=hdr(first,y),lim=y+cap()-hh;let br=cand.filter(c=>c>y+(cap()-hh)*.45&&c<=lim+.5).pop();if(br==null)br=lim;sl.push([y,br,hh]);y=br;first=false}
sl.push([y,Ht,hdr(first,y)]);
const P=new jspdf.jsPDF({unit:'mm',format:'a4',orientation:'p',compress:true}),mm=210/Wd,gray=!!S.set.bw;
P.setProperties({title:title,author:S.set.name||''});
sl.forEach(([a,b2,hh],n)=>{if(n)P.addPage();const hp=Math.round(hh*K),bp=Math.max(1,Math.round((b2-a)*K)),c=document.createElement('canvas');c.width=cv.width;c.height=hp+bp;const x=c.getContext('2d',{willReadFrequently:gray});x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);if(hh)x.drawImage(cv,0,Math.round(thT*K),cv.width,hp,0,0,c.width,hp);x.drawImage(cv,0,Math.round(a*K),cv.width,bp,0,hp,c.width,bp);
if(gray){const id=x.getImageData(0,0,c.width,c.height),p=id.data;for(let i=0;i<p.length;i+=4){const l=.299*p[i]+.587*p[i+1]+.114*p[i+2];p[i]=p[i+1]=p[i+2]=l}x.putImageData(id,0,0)}
P.addImage(c.toDataURL('image/png'),'PNG',0,n?M*mm:0,210,(hh+b2-a)*mm,undefined,'FAST')});
return P}finally{w.remove()}}
const pdfMake=d=>renderPdf(paper(d),(isBill(d)?'Invoice ':'Estimate ')+no(d));
const mobileUA=()=>/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
const b64=blob=>new Promise((r,j)=>{const f=new FileReader();f.onload=()=>r(String(f.result).split(',')[1]);f.onerror=j;f.readAsDataURL(blob)});
// Android app: the native 'ZXPrint' plugin sends the PDF straight to the phone's print dialog (printers on Wi-Fi / USB / Bluetooth).
// Where it does not exist (iPhone, older build) we fall back to the share sheet, which also has a Print action.
const zxPrint=()=>{try{const C=window.Capacitor;return C&&C.registerPlugin?C.registerPlugin('ZXPrint'):(C&&C.Plugins&&C.Plugins.ZXPrint)||null}catch{return null}};
async function saveFile(name,blob,mime,title,prn){const C=window.Capacitor;
if(isNat()&&prn){const Z=zxPrint();if(Z&&Z.printPdf){try{await Z.printPdf({data:await b64(blob),name:(title||name).replace(/\.pdf$/i,'')});return}catch(x){console.warn('Direct print not available, using share sheet',x)}}}
if(isNat()&&C.Plugins.Filesystem&&C.Plugins.Share){const data=await b64(blob);const f=await C.Plugins.Filesystem.writeFile({path:name,data,directory:'CACHE'});await C.Plugins.Share.share({title:title||name,url:f.uri,dialogTitle:title||name});return}
if(mobileUA()&&navigator.canShare){try{const f=new File([blob],name,{type:mime});if(navigator.canShare({files:[f]})){await navigator.share({files:[f],title:title||name});return}}catch(x){if(x&&x.name==='AbortError')return}}
const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),4000)}
async function pdf(d,prn){const P=await pdfMake(d),fn=(isBill(d)?'Invoice-':'Estimate-')+(no(d)||'draft').replace(/[\/\\]/g,'-')+'.pdf';await saveFile(fn,P.output('blob'),'application/pdf',fn,prn)}
async function histPdf(prn){const el=document.querySelector('.rep');if(!el)return;const P=await renderPdf('<div class="rep" style="display:block;width:210mm">'+el.innerHTML+'</div>','Invoice history');await saveFile('Invoice-history-'+today()+'.pdf',P.output('blob'),'application/pdf','Invoice history',prn)}
const e=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const n2=x=>(+x||0).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
const pad=n=>String(n).padStart(4,'0'),today=()=>{const t=new Date();return t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0')};
const dm=d=>d?e(String(d).split('-').reverse().join('-')):'';
const nn=x=>{x=+x;return isFinite(x)&&x>0?x:0};
const ar=i=>{const m=/^\s*([\d.]+)\s*[x×*]\s*([\d.]+)\s*$/i.exec(i.s||'');return m&&/^sq/i.test(i.u||'')?nn(m[1])*nn(m[2])*nn(i.q):0},amt=i=>r2((ar(i)||nn(i.q))*nn(i.p)),dma=i=>r2(nn(i.m)*nn(i.p)),sub=d=>r2(d.items.reduce((a,i)=>a+amt(i),0)+(d.dm||[]).reduce((a,i)=>a+dma(i),0)),dsc=d=>Math.min(Math.max(+d.disc||0,0),sub(d)),r2=x=>Math.round((+x+1e-9)*100)/100,rt=d=>Math.min(Math.max(+d.rate||0,0),100),txb=d=>r2(sub(d)-dsc(d)),cg=d=>d.gst&&!d.igst?r2(txb(d)*rt(d)/200):0,sg2=d=>cg(d),ig=d=>d.gst&&d.igst?r2(txb(d)*rt(d)/100):0,gst=d=>cg(d)+sg2(d)+ig(d),tot=d=>r2(txb(d)+gst(d)),pd=d=>r2(d.pay.reduce((a,p)=>a+nn(p.a),0));
const isBill=d=>pd(d)>0,no=d=>{const c=isBill(d)&&d.billNo?d.billNo:d.estNo;return NQ.test(c||'')?(isBill(d)?(d.pfx||'BIL'):'EST')+c:c},bal=d=>Math.max(0,tot(d)-pd(d));
function words(v){const a='One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen'.split(' '),b=',,Twenty,Thirty,Forty,Fifty,Sixty,Seventy,Eighty,Ninety'.split(',');
const w=n=>n<20?a[n-1]||'':b[n/10|0]+(n%10?' '+a[n%10-1]:''),h=n=>(n>99?a[(n/100|0)-1]+' Hundred'+(n%100?' ':''):'')+w(n%100);
let r=Math.floor(v+1e-9),p=Math.round((v-r)*100),o=[];[[1e7,'Crore'],[1e5,'Lakh'],[1e3,'Thousand']].forEach(([m,l])=>{if(r>=m){o.push(h(r/m|0)+' '+l);r%=m}});if(r)o.push(h(r));
return (o.join(' ')||'Zero')+' Rupees'+(p?' and '+w(p)+' Paise':'')+' Only'}
function fix(d){if(isBill(d)&&!d.bl){d.bl=1;d.pfx='INV';lg(d,'Converted to invoice '+no(d))}}
const stat=d=>!isBill(d)?['Estimate','']:bal(d)<=0.005?['Invoice - Paid','bill']:['Invoice - Balance due','bill'];
const UN=['Sqf','Nos','Sqm','Rft','Set'];
const IC={print:'<path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2"/><rect x="6" y="14" width="12" height="7"/>',pdf:'<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',mail:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',wa:'<path d="M3 21l1.6-4.7A8.5 8.5 0 1 1 8 19.5z"/><path d="M9 9c0 3.2 2.8 6 6 6l1-1.6-2-1-1 .8c-.9-.4-1.7-1.2-2.1-2.1l.8-1-1-2z"/>'};
const ib=(a,t,icon,x='',attr='data-a')=>`<button class="ib ${x}" ${attr}="${e(a)}" title="${t}" aria-label="${t}"><svg viewBox="0 0 24 24" aria-hidden="true">${IC[icon]}</svg></button>`;
function hsnFor(n){n=(n||'').toLowerCase().trim();if(!n)return'';if(/website|web design|web develop/.test(n))return'998314';if(/aws|cloud|hosting/.test(n))return'998315';if(/seo|marketing|ads|advert|social|reel|content|campaign/.test(n))return'998361';if(/design|logo|graphic|poster/.test(n))return'998391';return'4911'}
const PCSS=`.zp{--hd:#000;--ac:#2bff05;--th:#111;--tt:#111;--hf:#fff;--thf:#fff;--ttf:#fff;--ink:#14181d;--mut:#5b6470;--ln:#cfd4da;position:relative;display:flex;flex-direction:column;width:210mm;min-height:297mm;margin:0 auto;background:#fff;color:var(--ink);font:12.5px/1.5 Inter,"Segoe UI",Arial,Helvetica,sans-serif;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;text-align:left}
.zp *{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.zp.bw{filter:grayscale(1)}
.zp .ph{display:flex;justify-content:space-between;align-items:center;gap:20px;background:var(--hd);color:var(--hf);padding:7mm 14mm}
.zp .plogo{height:17mm;width:auto;display:block}
.zp .pco{text-align:right;font-size:11.5px;line-height:1.55}
.zp .pco b{display:block;font-size:16px;margin-bottom:2px}
.zp .pl{white-space:pre-line}
.zp .pac{height:1.4mm;background:var(--ac)}
.zp .pbody{flex:1;display:flex;flex-direction:column;padding:6mm 14mm 0}
.zp .ptt{margin:0 0 3.5mm;padding:0 0 2.5mm;text-align:center;font:700 21px/1.2 Inter,"Segoe UI",Arial,sans-serif;letter-spacing:.22em;text-transform:uppercase;border-bottom:2px solid var(--ink)}
.zp .pinfo{display:flex;justify-content:space-between;align-items:flex-start;gap:12mm}
.zp .pbt{flex:1;min-width:0}
.zp .pbt small{display:block;color:var(--mut);font-size:9.5px;letter-spacing:.16em;margin-bottom:1px}
.zp .pbt b{display:block;font-size:15px;line-height:1.3}
.zp .pmeta{width:66mm;flex:none}
.zp .pmeta div{display:flex;justify-content:space-between;gap:10px;padding:1.5px 0}
.zp .pmeta span{color:var(--mut)}
.zp .pq{width:100%;border-collapse:collapse;margin-top:5.5mm;border:1px solid var(--ln)}
.zp .pq th{background:var(--th);color:var(--thf);padding:7px 8px;font-size:11.5px;font-weight:600;text-align:left;border:1px solid var(--th)}
.zp .pq td{padding:7px 8px;border:1px solid var(--ln);vertical-align:top}
.zp .pq small{color:var(--mut)}
.zp .pq .r{text-align:right}.zp .pq .nw{white-space:nowrap}
.zp thead{display:table-header-group}.zp tr{break-inside:avoid;page-break-inside:avoid}
.zp h4{margin:5mm 0 0;font:700 12px Inter,"Segoe UI",Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase}
.zp h4+.pq{margin-top:2mm}
.zp .pbot{display:flex;justify-content:space-between;align-items:flex-start;gap:10mm;margin-top:5.5mm;break-inside:avoid}
.zp .pw2{flex:1;min-width:0}.zp .pw2 b{display:block}.zp .pw2 p{margin:3px 0 0}
.zp .ptot{width:80mm;flex:none}
.zp .ptot>div{display:flex;justify-content:space-between;gap:10px;padding:4px 8px}
.zp .ptot .sep{border-top:1px solid var(--ln);margin-top:2px;padding-top:6px}
.zp .ptot .gr{background:var(--tt);color:var(--ttf);font-weight:700}
.zp .pf{display:flex;justify-content:space-between;gap:10mm;margin-top:6mm;padding-top:3mm;border-top:1px solid var(--ln);break-inside:avoid}
.zp .pf b{display:block;margin-bottom:2px}.zp .pf ol{margin:2px 0 0;padding-left:16px}.zp .pbk{width:66mm;flex:none}
.zp .psg{display:flex;justify-content:flex-end;margin-top:auto;padding-top:8mm;break-inside:avoid}
.zp .sgb{width:66mm;text-align:center}
.zp .sfor{font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.zp .simg{height:20mm;display:flex;align-items:flex-end;justify-content:center;margin:1mm 0}
.zp .simg img{max-height:20mm;max-width:100%;object-fit:contain;display:block}
.zp .slab{border-top:1px solid var(--ink);padding-top:3px;color:#333}
.zp .prm{margin-top:4mm;padding:2.5mm 3mm;border:1px solid var(--ln);border-left:3px solid var(--ac);break-inside:avoid}.zp .prm b{display:block;margin-bottom:1px}
.zp .pft{margin-top:6mm;padding:3mm 14mm 6mm;text-align:center;font-size:10.5px;color:var(--mut);border-top:1px solid var(--ln);margin-left:14mm;margin-right:14mm;padding-left:0;padding-right:0}`;
const hx=(v,df)=>/^#[0-9a-f]{6}$/i.test(v||'')?v:df,lumOf=h=>{const n=parseInt(h.slice(1),16);return(.299*(n>>16&255)+.587*(n>>8&255)+.114*(n&255))/255},fgOf=h=>lumOf(h)>.6?'#111111':'#ffffff';
function paper(d){const s=S.set,b=isBill(d),t=tot(d),I=d.items.filter(i=>i.n||amt(i)),M=(d.dm||[]).filter(i=>i.n||dma(i)),dc=dsc(d),ti=b&&!!d.gst,W=b?'Invoice':'Estimate',H=d.hsn!==false,
C=s.colors||DC,hd=hx(C.hd,DC.hd),ac=hx(C.ac,DC.ac),th=hx(C.th,DC.th),tt=hx(C.tt,DC.tt),logo=(lumOf(hd)>.6?window.ZX_LOGO_D:window.ZX_LOGO)||'',
sg=/^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+\/=]+$/.test(d.sig||'')?d.sig:'';
const tr=[`<div>Sub Total<span>₹ ${n2(sub(d))}</span></div>`];
if(dc)tr.push(`<div>Discount<span>- ₹ ${n2(dc)}</span></div>`);
if(d.gst){tr.push(`<div class="sep">Taxable Amount<span>₹ ${n2(txb(d))}</span></div>`);
if(d.igst)tr.push(`<div>IGST @ ${n2(rt(d))}%<span>₹ ${n2(ig(d))}</span></div>`);
else tr.push(`<div>CGST @ ${n2(rt(d)/2)}%<span>₹ ${n2(cg(d))}</span></div><div>SGST @ ${n2(rt(d)/2)}%<span>₹ ${n2(sg2(d))}</span></div>`)}
tr.push(`<div class="gr">Total<span>₹ ${n2(t)}</span></div>`);
if(b){d.pay.forEach(x=>tr.push(`<div>Received ${dm(x.d)}${x.m?' ('+e(x.m)+')':''}<span>₹ ${n2(x.a)}</span></div>`));tr.push(`<div class="gr">Balance due<span>₹ ${n2(bal(d))}</span></div>`)}
return `<div class="zp${s.bw?' bw':''}" id="paper" style="--hd:${hd};--ac:${ac};--th:${th};--tt:${tt};--hf:${fgOf(hd)};--thf:${fgOf(th)};--ttf:${fgOf(tt)}"><style>${PCSS}</style>
<div class="ph"><img class="plogo" src="${logo}" alt="${e(s.name)}"><div class="pco"><b>${e(s.name)}</b><div class="pl">${e(s.addr)}</div>${s.gst?'GSTIN : '+e(s.gst)+'<br>':''}Phone : ${e(s.phone)}<br>${e(s.email)}</div></div><div class="pac"></div>
<div class="pbody"><h3 class="ptt">${b?(d.gst?'Tax Invoice':'Invoice'):'Estimate'}</h3>
<div class="pinfo"><div class="pbt"><small>BILLED TO</small><b>${e(d.cust)||'-'}</b><div class="pl">${e(d.addr)}${d.phone?'\nPh: '+e(d.phone):''}${d.cgst?'\nGSTIN: '+e(d.cgst):''}</div></div>
<div class="pmeta"><div><span>${W} No.</span><b>${e(no(d))}</b></div><div><span>Date</span><b>${dm(d.date)}</b></div>${ti&&d.pos?`<div><span>Place of supply</span><b>${e(d.pos)}</b></div>`:''}${ti?'<div><span>Reverse charge</span><b>No</b></div>':''}</div></div>
${I.length?`<table class="pq"><thead><tr><th>#<th>Service${H?'<th>HSN/SAC':''}<th>Size<th class="r">Qty<th>Unit<th class="r">Price<th class="r">Amount</tr></thead><tbody>${I.map((i,k)=>`<tr><td>${k+1}<td>${e(i.n)}${H?`<td>${e(i.h)}`:''}<td>${e(i.s)}<td class="r">${e(i.q)}${ar(i)?' <small>('+(+ar(i).toFixed(2))+(/^sqm/i.test(i.u||'')?' sqm':' sqft')+')</small>':''}<td>${e(i.u)}<td class="r nw">₹ ${n2(i.p)}<td class="r nw">₹ ${n2(amt(i))}</tr>`).join('')}</tbody></table>`:''}
${M.length?`<h4>Digital Marketing</h4><table class="pq"><thead><tr><th>#<th>Service<th>Details<th class="r">Months<th class="r">Monthly fee<th class="r">Amount</tr></thead><tbody>${M.map((i,k)=>`<tr><td>${k+1}<td>${e(i.n)}<td>${e(i.d)}<td class="r">${e(i.m)}<td class="r nw">₹ ${n2(i.p)}<td class="r nw">₹ ${n2(dma(i))}</tr>`).join('')}</tbody></table>`:''}
<div class="pbot"><div class="pw2"><b>${W} amount in words</b><p>${words(t)}</p></div><div class="ptot">${tr.join('')}</div></div>
${d.rem?`<div class="prm"><b>Remark</b><div class="pl">${e(d.rem)}</div></div>`:''}
<div class="pf"><div><b>Terms and Conditions</b><ol class="pl">${(d.terms||'').split('\n').filter(Boolean).map(x=>`<li>${e(x)}</li>`).join('')}</ol></div><div class="pbk"><b>Pay to</b>${e(s.holder||s.payto)}<br>Bank : ${e(s.bank)}<br>A/c No. : ${e(s.acc)}<br>IFSC : ${e(s.ifsc)}</div></div>
<div class="psg"><div class="sgb"><div class="sfor">For ${e(s.payto)}</div><div class="simg">${sg?`<img src="${sg}" alt="Signature">`:''}</div><div class="slab">Authorized Signatory</div></div></div></div>
<div class="pft">This is a computer-generated ${b?'invoice':'estimate'}.</div></div>`}
const mt=(s,q)=>{const n=s.n.toLowerCase();return n.startsWith(q)?0:n.split(/[^a-z0-9]+/).some(w=>w.startsWith(q))?1:n.includes(q)?2:(s.c||'').toLowerCase().includes(q)?3:9};
const ac={el:null,items:[],sel:0,t:null,cb:null};
function acHide(){if(ac.el){ac.el.remove();ac.el=null}ac.items=[]}
function acShow(t,g,cb){acHide();const q=t.value.toLowerCase().trim();if(!q)return;
ac.items=S.set.services.filter(s=>(s.k=='dm')==(g=='dm')&&mt(s,q)<9).sort((a,b)=>mt(a,q)-mt(b,q)).slice(0,8);if(!ac.items.length)return;
ac.sel=0;ac.t=t;ac.cb=cb;const r=t.getBoundingClientRect(),w=Math.max(r.width,290),el=document.createElement('div');el.className='ac';
el.style.width=w+'px';
el.innerHTML=ac.items.map((s,x)=>`<div class="aci${x?'':' on'}" data-x="${x}"><img src="${e(s.i)}" alt=""><span>${e(s.n)}<small>${e(s.c)}</small></span>${+s.p?`<b>₹ ${n2(s.p)}</b>`:''}</div>`).join('');
el.onmousedown=ev=>{ev.preventDefault();const it=ev.target.closest('.aci');if(it)acPick(+it.dataset.x)};document.body.append(el);ac.el=el;acPos()}
function acPos(){if(!ac.el||!ac.t)return;const r=ac.t.getBoundingClientRect(),el=ac.el,w=el.offsetWidth,h=el.offsetHeight,vh=window.visualViewport?visualViewport.height:innerHeight;if(r.bottom<0||r.top>vh){acHide();return}let top=r.bottom+2;if(top+h>vh-8&&r.top-h-2>8)top=r.top-h-2;el.style.left=Math.max(8,Math.min(r.left,innerWidth-w-8))+'px';el.style.top=top+'px'}
function acPick(x){const s=ac.items[x],t=ac.t,cb=ac.cb;acHide();if(s)cb(t,s)}
function acKey(ev){if(!ac.el)return false;const n=ac.items.length,k=ev.key;
if(k=='ArrowDown'||k=='ArrowUp'){ev.preventDefault();ac.sel=(ac.sel+(k=='ArrowDown'?1:n-1))%n;[...ac.el.children].forEach((c,i)=>c.classList.toggle('on',i==ac.sel));return true}
if(k=='Enter'){ev.preventDefault();acPick(ac.sel);return true}if(k=='Escape'){acHide();return true}return false}
let md='pr';
const LB={n:'Service',h:'HSN/SAC',s:'Size',q:'Quantity',u:'Unit',p:'Price',d:'Details',m:'Months'};
let draft=null,flash='';
function sigLoad(f,d,cb){if(!/^image\//.test(f.type)||f.size>10e6){alert('Choose an image file (up to 10 MB).');return}
const u=URL.createObjectURL(f),im=new Image();im.onload=()=>{const m=Math.min(1,560/im.width,220/im.height),w=Math.max(1,Math.round(im.width*m)),h=Math.max(1,Math.round(im.height*m)),c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(im,0,0,w,h);
try{const id=x.getImageData(0,0,w,h),p=id.data;if(p[3]>=250){for(let i=0;i<p.length;i+=4){const l=.299*p[i]+.587*p[i+1]+.114*p[i+2];if(l>225)p[i+3]=0;else p[i+3]=Math.min(255,(225-l)*3)}x.putImageData(id,0,0)}}catch{}
d.sig=c.toDataURL('image/png');URL.revokeObjectURL(u);cb()};im.onerror=()=>{URL.revokeObjectURL(u);alert('Could not read that image.')};im.src=u}
function bill(d0){const d=d0||(draft=draft||newDoc()),V=S.set.services,sv=()=>S.docs.includes(d),hs=()=>d.hsn!==false,TT=()=>isBill(d)?'Invoice':'Estimate';
d.items=d.items&&d.items.length?d.items:[bl()];d.dm=d.dm&&d.dm.length?d.dm:[bd()];
const gk=()=>md=='dm'?'dm':'items',blank=g=>g=='dm'?bd():bl(),done=(g,r)=>!!String(r.n||'').trim()&&(g=='dm'?+r.m>0:+r.q>0)&&+r.p>0;
['items','dm'].forEach(g=>{if(done(g,d[g][d[g].length-1]))d[g].push(blank(g))});
const at=v=>v?n2(v):'',F=(k,l,t,c,ph)=>`<div class="${c||''}"><label>${l}<input type="${t||'text'}" data-k="${k}" value="${e(d[k])}" ${ph?`placeholder="${e(ph)}"`:''}></label></div>`;
const SWT=(k,l,on,x='')=>`<label class="swt${x}"><input type="checkbox" role="switch" data-k="${k}" ${on?'checked':''}><span class="trk"><span class="knob"></span></span><span class="swl">${l}</span></label>`;
const I=(g,k,f,v,x='',t='')=>`<input ${t?'type="number" min="0" step="any" inputmode="decimal"':'type="text"'} data-g="${g}" data-i="${k}" data-k="${f}" value="${e(v)}" aria-label="${LB[f]}" ${x}>`;
const SU=(k,v)=>`<select data-g="items" data-i="${k}" data-k="u" aria-label="Unit"><option value="">Unit</option>${(UN.includes(v)||!v?UN:[...UN,v]).map(u=>`<option${u==v?' selected':''}>${e(u)}</option>`).join('')}</select>`;
const prow=(r,k)=>`<div class="xr"><div class="xc n">${k+1}</div><div class="xc">${I('items',k,'n',r.n,'class="svn" autocomplete="off" placeholder="Type a service"')}</div>${hs()?`<div class="xc">${I('items',k,'h',r.h)}</div>`:''}<div class="xc">${I('items',k,'s',r.s,'placeholder="8 x 8"')}</div><div class="xc">${I('items',k,'q',r.q,'','n')}</div><div class="xc">${SU(k,r.u)}</div><div class="xc">${I('items',k,'p',r.p,'','n')}</div><div class="xc amt" data-amt="items:${k}">${at(amt(r))}</div><div class="xc"><button class="x" data-a="del" data-g="items" data-i="${k}" aria-label="Remove row">✕</button></div></div>`;
const drow=(r,k)=>`<div class="xr"><div class="xc n">${k+1}</div><div class="xc">${I('dm',k,'n',r.n,'class="svn" autocomplete="off" placeholder="Type a service"')}</div><div class="xc">${I('dm',k,'d',r.d,'placeholder="e.g. 12 posts + 4 reels / month"')}</div><div class="xc">${I('dm',k,'m',r.m,'','n')}</div><div class="xc">${I('dm',k,'p',r.p,'','n')}</div><div class="xc amt" data-amt="dm:${k}">${at(dma(r))}</div><div class="xc"><button class="x" data-a="del" data-g="dm" data-i="${k}" aria-label="Remove row">✕</button></div></div>`;
const rowH=(g,k)=>g=='dm'?drow(d.dm[k],k):prow(d.items[k],k),rowsH=g=>d[g].map((r,k)=>rowH(g,k)).join('');
const trow=()=>md=='dm'?`<div class="xc"></div><div class="xc b">Total</div><div class="xc"></div><div class="xc"></div><div class="xc"></div><div class="xc b amt">${n2(d.dm.reduce((a,r)=>a+dma(r),0))}</div><div class="xc"></div>`:`<div class="xc"></div><div class="xc b">Total</div>${hs()?'<div class="xc"></div>':''}<div class="xc"></div><div class="xc b">${d.items.reduce((a,r)=>a+(+r.q||0),0)||''}</div><div class="xc"></div><div class="xc"></div><div class="xc b amt">${n2(d.items.reduce((a,r)=>a+amt(r),0))}</div><div class="xc"></div>`;
const H=()=>md=='dm'?['#','Service','Details','Months','Monthly fee','Amount','']:['#','Service',...(hs()?['HSN/SAC']:[]),'Size','Quantity','Unit','Price','Amount',''];
const sheet=()=>`<div class="xs ${md}${md=='pr'&&!hs()?' nh':''}"><div class="xr xh">${H().map(h=>`<div class="xc">${h}</div>`).join('')}</div><div id="rows">${rowsH(gk())}</div><div class="xr xt" id="trow">${trow()}</div></div>`;
const head=()=>{const[st,c]=stat(d);return `<div><h1>${sv()?e(no(d)):'New estimate'}</h1><span class="chip ${c}">${st}</span> <small>${isBill(d)?'Paid ₹ '+n2(pd(d))+' of ₹ '+n2(tot(d)):sv()?'No payment yet':'Not saved yet'}</small></div>`};
const bAct=isBill(d)?ib('print','Print','print')+ib('pdf','Download PDF','pdf')+ib('mail','Email copy','mail')+ib('wa','Send on WhatsApp','wa'):sv()?ib('pdf','Download estimate PDF','pdf'):'';
const acts=(sv()?`<label class="swt sm"><input type="checkbox" role="switch" data-s="bw" ${S.set.bw?'checked':''}><span class="trk"><span class="knob"></span></span><span class="swl">Black &amp; white</span></label>`:'')+bAct;
const pays=()=>d.pay.map((x,k)=>`<div class="pay"><div>${dm(x.d)}</div><div>₹ ${n2(x.a)}</div><div>${e(x.m)}</div><button class="ghost" data-a="dp" data-i="${k}" aria-label="Remove payment">✕</button></div>`).join('');
const gdet=()=>d.gst?`<div>Taxable Amount<span>₹ ${n2(txb(d))}</span></div>`+(d.igst?`<div>IGST @ ${n2(rt(d))}%<span>₹ ${n2(ig(d))}</span></div>`:`<div>CGST @ ${n2(rt(d)/2)}%<span>₹ ${n2(cg(d))}</span></div><div>SGST @ ${n2(rt(d)/2)}%<span>₹ ${n2(sg2(d))}</span></div>`):'';
const sigH=()=>`<div class="sigb">${d.sig?`<img src="${e(d.sig)}" alt="Signature" class="sigp">`:'<span class="hint">No signature added. The printed invoice keeps an empty space for signing by hand.</span>'}<label class="btn ghost up">${d.sig?'Change signature':'Upload signature'}<input type="file" accept="image/*" id="sigf" hidden></label>${d.sig?'<button class="ghost" data-a="sigdel">Remove</button>':''}</div>`;
app.innerHTML=`${RB()}<div class="state" id="head">${head()}<div class="act">${acts}</div></div>
<div class="card"><h2>Client details</h2><div class="cg">${F('cust','Client name','text','s2')}${F('phone','Phone','tel')}${F('email','Email (gets a copy)','email')}<div class="s2"><label>Address<textarea data-k="addr" style="min-height:44px">${e(d.addr)}</textarea></label></div>${F('cgst','Client GSTIN (optional)')}${F('date','Date','date')}<div><label>${TT()} no. (automatic)<input id="nobox" value="${e(no(d)||'EST'+mkNo(d.date))}" readonly></label></div>${F('pos','Place of supply (optional)')}</div></div>
<div class="card"><h2>Services</h2><div class="svh"><div class="seg" id="seg"><button data-m="pr" class="${md=='pr'?'on':''}">Design / Print / Signage</button><button data-m="dm" class="${md=='dm'?'on':''}">Digital services</button></div><span id="hsnsw" ${md=='dm'?'hidden':''}>${SWT('hsn','HSN/SAC',hs())}</span></div><div class="sw" id="sw">${sheet()}</div><p class="hint">Type a service and pick it from the suggestions. Fill the row and the next row appears. HSN/SAC, Amount and Total fill in automatically.</p>
<div class="sum"><div class="words"><b id="wl">${TT()} Amount In Words</b><p id="v-w">${words(tot(d))}</p></div><div class="tt"><div>Sub Total<span id="v-s">₹ ${n2(sub(d))}</span></div><div><label class="gl">Discount ₹ <input type="number" step="any" inputmode="decimal" data-k="disc" class="rate dsc" min="0" value="${e(d.disc)}" aria-label="Discount amount"></label><span id="v-d">- ₹ ${n2(dsc(d))}</span></div><div class="gx">${SWT('gst','GST',d.gst)}<span class="gin"><input type="number" step="any" data-k="rate" class="rate" min="0" max="100" value="${e(d.rate)}" aria-label="GST percent"> %</span><select data-k="igst" class="gty" aria-label="Tax type"><option value="">CGST + SGST</option><option value="1" ${d.igst?'selected':''}>IGST (other state)</option></select></div><div class="gdet" id="gdet">${gdet()}</div><div class="gr">Total<span id="v-t">₹ ${n2(tot(d))}</span></div></div></div><p class="hint" id="gh" ${d.gst&&!S.set.gst?'':'hidden'}>Add your GST number in Settings so it prints on the tax invoice.</p></div>
${sv()?`<div class="card"><h2>Payments</h2><p style="margin:0;color:var(--mut)">The first payment, including an advance, turns this estimate into an invoice.</p><div id="pays">${pays()}</div>
<div class="pay"><label>Date<input type="date" id="pd" value="${today()}"></label><label>Amount (₹)<input type="number" min="0" step="any" id="pa" inputmode="decimal"></label><label>Mode<select id="pm"><option>Cash<option>UPI<option>Bank transfer<option>Cheque</select></label><button data-a="pay">Record payment</button></div><button class="ghost" data-a="adv" style="margin-top:10px">Fill 70% advance</button></div>`:''}
<div class="card"><h2>Remark</h2><textarea data-k="rem" style="min-height:70px" placeholder="Anything to note on this bill. It prints on the bill.">${e(d.rem)}</textarea></div>
<div class="card"><h2>Terms</h2><textarea data-k="terms">${e(d.terms)}</textarea></div>
${sv()?`<div class="card"><h2>Signature</h2><p style="margin:0 0 10px;color:var(--mut)">Upload a photo or scan of the signature for this ${TT().toLowerCase()} only. It prints above "Authorized Signatory". Every ${TT().toLowerCase()} has its own signature.</p><div id="sigbox">${sigH()}</div></div>`:''}
${(d.log||[]).length?`<div class="card"><h2>History of this ${TT().toLowerCase()}</h2>${d.log.slice().reverse().map(x=>`<div class="lg"><b>${new Date(x.t).toLocaleString('en-IN',{dateStyle:'medium',timeStyle:'short'})}</b><span>${e(x.e)}</span></div>`).join('')}</div>`:''}
<div class="act" style="margin-bottom:20px">${sv()?'<button class="danger" data-a="rm">Delete</button>':'<button class="ghost" data-a="clr">Clear</button>'}<button data-a="save">Save</button></div>`;
const upd=()=>{fix(d);touch(d);$('#v-w').textContent=words(tot(d));$('#v-s').textContent='₹ '+n2(sub(d));$('#v-d').textContent='- ₹ '+n2(dsc(d));$('#gdet').innerHTML=gdet();$('#gh').hidden=!(d.gst&&!S.set.gst);$('#v-t').textContent='₹ '+n2(tot(d));$('#trow').innerHTML=trow();$('#wl').textContent=TT()+' Amount In Words';$('#head').firstElementChild.outerHTML=head()};
const rowUpd=(g,i)=>{const r=d[g][i],o=document.querySelector(`[data-amt="${g}:${i}"]`);if(o)o.textContent=at(g=='dm'?dma(r):amt(r));if(i==d[g].length-1&&done(g,r)){d[g].push(blank(g));$('#rows').insertAdjacentHTML('beforeend',rowH(g,i+1))}};
const cellOf=(g,i,f)=>document.querySelector(`[data-g="${g}"][data-i="${i}"][data-k="${f}"]`);
const pick=(t,s)=>{const g=t.dataset.g,i=+t.dataset.i,r=d[g][i],set=(f,v)=>{r[f]=v;const x=cellOf(g,i,f);if(x)x.value=v};set('n',s.n);if(g!='dm'){set('h',s.h||hsnFor(s.n));r._ah=false;set('u',s.u||'')}if(+s.p)set('p',s.p);rowUpd(g,i);upd();const x=cellOf(g,i,g=='dm'?'d':'s');x&&x.focus()};
app.oninput=ev=>{const t=ev.target,k=t.dataset.k,g=t.dataset.g;if(t.dataset.s)return;if(!k)return;if(g){const i=+t.dataset.i,r=d[g][i];r[k]=t.value;if(k=='h')r._ah=false;if(k=='n'){acShow(t,g,pick);if(g!='dm'&&(!r.h||r._ah)){r.h=hsnFor(t.value);r._ah=true;const x=cellOf(g,i,'h');if(x)x.value=r.h}}rowUpd(g,i)}else{if(k=='igst')d.igst=t.value=='1';else d[k]=t.type=='checkbox'?t.checked:t.value;if(k=='date'&&!sv())$('#nobox').value='EST'+mkNo(d.date);if(k=='hsn')$('#sw').innerHTML=sheet()}upd()};
app.onchange=ev=>{const t=ev.target;if(t.dataset.s=='bw'){S.set.bw=t.checked;sch();return}if(t.id=='sigf'&&t.files&&t.files[0]){sigLoad(t.files[0],d,()=>{$('#sigbox').innerHTML=sigH();fix(d);touch(d)});t.value=''}};
app.onfocusout=ev=>{if(ev.target.classList&&ev.target.classList.contains('svn'))setTimeout(acHide,200)};
app.onkeydown=ev=>{const t=ev.target;if(t.classList.contains('svn')&&acKey(ev))return;if(ev.key!='Enter'||!t.dataset.g)return;ev.preventDefault();const g=t.dataset.g,i=+t.dataset.i,ins=[...t.closest('.xr').querySelectorAll('input,select')],x=ins.indexOf(t);
if(x<ins.length-1){ins[x+1].focus();return}if(i==d[g].length-1){if(!String(d[g][i].n||'').trim())return;d[g].push(blank(g));$('#rows').insertAdjacentHTML('beforeend',rowH(g,i+1))}
const nx=cellOf(g,i+1,'n');nx&&nx.focus()};
app.onclick=ev=>{const b=ev.target.closest('[data-a],[data-m]');if(!b)return;if(b.dataset.m){md=b.dataset.m;acHide();$('#sw').innerHTML=sheet();$('#hsnsw').hidden=md=='dm';$('#seg').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x.dataset.m==md));return}
const a=b.dataset.a,i=+b.dataset.i,g=b.dataset.g;
if(a=='save'){if(!String(d.cust||'').trim()){alert('Enter the client name first.');return}if(!['items','dm'].some(x=>d[x].some(r=>String(r.n||'').trim()))){alert('Add at least one service first.');return}if(!dOk(d.date))d.date=today();const nw=!sv();commit(d);if(nw)draft=null;flash=nw?'Estimate '+no(d)+' saved. Open it here to record the payment.':'Saved '+no(d);location.hash='#/h';return}
if(a=='clr'){if(confirm('Clear everything on this page?')){draft=null;route()}return}
if(a=='print'){lg(d,'Printed');touch(d);isNat()?pdf(d,true).catch(x=>{console.warn(x);alert('Could not print.')}):pj(paper(d));return}
if(a=='pdf'){b.disabled=true;lg(d,'PDF downloaded');touch(d);pdf(d).catch(x=>{console.warn(x);alert('Could not create the PDF. Please try again.')}).finally(()=>b.disabled=false);return}
if(a=='wa'){waShare(d);return}
if(a=='mail'){mail(d);return}
if(a=='rm'){if(confirm('Delete '+no(d)+'? This cannot be undone.')){d.del=1;touch(d);location.hash='#/h'}return}
if(a=='del'){d[g].splice(i,1);if(!d[g].length||done(g,d[g][d[g].length-1]))d[g].push(blank(g));$('#rows').innerHTML=rowsH(g);upd();return}
if(a=='sigdel'){d.sig='';touch(d);$('#sigbox').innerHTML=sigH();return}
if(a=='adv'){$('#pa').value=(tot(d)*.7).toFixed(2);return}
if(a=='dp'){if(confirm('Remove this payment?')){d.pay.splice(i,1);lg(d,'Payment removed');fix(d);touch(d);bill(d)}return}
if(a=='pay'){const v=+$('#pa').value;if(!(v>0)||!isFinite(v)||v>=1e10){alert('Enter a payment amount.');return}if(v>bal(d)+.005&&!confirm('That is more than the balance of ₹ '+n2(bal(d))+'. Record it anyway?'))return;d.pay.push({d:dOk($('#pd').value)?$('#pd').value:today(),a:v,m:$('#pm').value});lg(d,'Payment ₹'+n2(v)+' received ('+$('#pm').value+')');(async()=>{touch(d);fix(d);touch(d);bill(d);if(S.set.auto&&mailOk())mail(d,1)})()}}}
let tab='all',q='',qb='',qd='';
const PM=['Cash','UPI','Bank','Cheque'],paidOk=d=>isBill(d)&&bal(d)<=0.005;
const tr=(d,x)=>`<tr class="row" tabindex="0" data-o="${e(d.id)}"><td><b>${e(no(d))}</b><td>${e(d.cust)||'-'}<td>${dm(d.date)}<td class="r">₹ ${n2(tot(d))}<td class="r">₹ ${n2(pd(d))}<td class="nw">${paidOk(d)?'<span class="tick">✓</span> <b>Paid</b>':`<span class="chip ${stat(d)[1]}">${stat(d)[0]}</span>`}<td class="r bl${paidOk(d)?'':' due'}">₹ ${n2(bal(d))}${x?`<td><div class="pc">${paidOk(d)?'<small>Fully paid</small>':`<input type="number" step="any" inputmode="decimal" placeholder="Amount" data-amt="${e(d.id)}" aria-label="Amount received"><select data-mode="${e(d.id)}" aria-label="Payment mode">${PM.map(m=>`<option>${m}`).join('')}</select><button class="sm" data-add="${e(d.id)}">Add</button>`}</div><td class="nw">${isBill(d)?ib(d.id,'Print','print','sm','data-p')+' ':''}${ib(d.id,'Download PDF','pdf','sm','data-f')}`:''}</tr>`;
async function addPay(id){const d=S.docs.find(x=>x.id==id&&!x.del);if(!d)return;const v=+document.querySelector(`input[data-amt="${id}"]`).value,m=document.querySelector(`select[data-mode="${id}"]`).value;
if(!(v>0)||!isFinite(v)||v>=1e10){alert('Type the amount received first.');return}
if(v>bal(d)+.005&&!confirm('That is more than the balance of ₹ '+n2(bal(d))+'. Record it anyway?'))return;
d.pay.push({d:today(),a:v,m});lg(d,'Payment ₹'+n2(v)+' received ('+m+', from History)');touch(d);if(!d.billNo)await pull();fix(d);touch(d);hist();if(S.set.auto&&mailOk())mail(d,1)}
function hist(){const A=S.docs.filter(d=>!d.del).sort((a,b)=>b.u-a.u),RC=A.reduce((a,d)=>a+pd(d),0),OB=A.filter(isBill).reduce((a,d)=>a+bal(d),0),ES=A.filter(d=>!isBill(d)).reduce((a,d)=>a+tot(d),0);
const ql=q.trim().toLowerCase(),dq=q.replace(/\D/g,''),numq=!!dq&&/^[\d\s+()-]+$/.test(q.trim()),bq=qb.trim().toLowerCase();
const mf=d=>(!ql||String(d.cust||'').toLowerCase().includes(ql)||(numq&&(d.phone||'').replace(/\D/g,'').includes(dq)))&&(!bq||no(d).toLowerCase().includes(bq))&&(!qd||d.date===qd);
const B=A.filter(mf),isDue=d=>isBill(d)&&bal(d)>.005,TB={all:()=>true,est:d=>!isBill(d),due:isDue,gst:d=>isBill(d)&&!!d.gst,nogst:d=>isBill(d)&&!d.gst},CT={};Object.keys(TB).forEach(k=>CT[k]=B.filter(TB[k]).length);
const L=B.filter(TB[tab]||TB.all),T=L.reduce((a,d)=>a+tot(d),0),P=L.reduce((a,d)=>a+pd(d),0);
const tbl=x=>`<div class="sw"><table class="lt"><tr><th>Number<th>Customer<th>Date<th class="r">Total<th class="r">Paid<th>Status<th class="r">Balance${x?'<th>Receive money<th>':''}</tr>${L.map(d=>tr(d,x)).join('')}</table></div>`;
const sum=`<div class="tt"><div>Billed<span>₹ ${n2(T)}</span></div><div>Paid<span>₹ ${n2(P)}</span></div><div class="gr">Balance<span>₹ ${n2(T-P)}</span></div></div>`;
const fl=flash;flash='';const TABS=[['all','All'],['est','Estimate'],['due','Balance due'],['gst','GST bill'],['nogst','Without GST bill']];
app.innerHTML=RB()+(fl?`<div class="toast">${e(fl)}</div>`:'')+`<div class="state"><h1>History</h1><button data-a="ph">Print history</button></div><div class="stats"><div class="hero"><small>Received</small><b>₹ ${n2(RC)}</b></div><div><small>Balance to collect</small><b>₹ ${n2(OB)}</b></div><div><small>Open estimates</small><b>₹ ${n2(ES)}</b></div></div>
<div class="bar tabs">${TABS.map(t=>`<button class="${tab==t[0]?'on':''}" data-t="${t[0]}">${t[1]}<i class="cnt" aria-label="${CT[t[0]]} items">${CT[t[0]]}</i></button>`).join('')}</div>
<div class="bar finder"><input id="qn" class="f1" value="${e(q)}" placeholder="Search by customer name or phone" aria-label="Customer name or phone"><input id="qb" class="f2" value="${e(qb)}" placeholder="Invoice or estimate number" aria-label="Invoice or estimate number"><input id="qd" class="f3" type="date" value="${e(qd)}" aria-label="Date"></div>`+
(L.length?tbl(1)+sum:`<div class="empty">${A.length?'Nothing matches your search.':'No bills yet. Open Billing to create your first one.'}</div>`)+`<div class="rep"><b>${e(S.set.name)}</b><h3>Invoice history${qd?' - '+dm(qd):''}</h3>${L.length?tbl(0)+sum:''}</div>`;
app.onclick=ev=>{const T=ev.target,ad=T.closest('[data-add]'),p=T.closest('[data-p]'),f=T.closest('[data-f]');if(ad){addPay(ad.dataset.add);return}if(T.closest('input,select'))return;
if(p){const d=S.docs.find(x=>x.id==p.dataset.p);if(d)isNat()?pdf(d,true).catch(x=>{console.warn(x);alert('Could not print.')}):pj(paper(d));return}if(f){const fd=S.docs.find(x=>x.id==f.dataset.f);if(!fd)return;f.disabled=true;pdf(fd).catch(x=>{console.warn(x);alert('Could not create the PDF.')}).finally(()=>f.disabled=false);return}if(T.closest('[data-a=ph]')){if(isNat()){histPdf(true).catch(x=>{console.warn(x);alert('Could not print.')})}else print();return}const t=T.closest('[data-t]'),o=T.closest('[data-o]');if(t){tab=t.dataset.t;hist()}else if(o)location.hash='#/d/'+o.dataset.o};
app.onkeydown=ev=>{const t=ev.target;if(ev.key!='Enter')return;if(t.dataset.amt){addPay(t.dataset.amt);return}if(t.dataset.o)location.hash='#/d/'+t.dataset.o};app.oninput=null;app.onchange=null;app.onfocusout=null;
const keep=(id,v)=>{const el=$('#'+id),p=el.selectionStart;v(el.value);hist();const n=$('#'+id);n.focus();try{n.setSelectionRange(p,p)}catch{}};
$('#qn').oninput=()=>keep('qn',v=>q=v);$('#qb').oninput=()=>keep('qb',v=>qb=v);$('#qd').onchange=ev=>{qd=ev.target.value;hist()}}
function sets(){const s=S.set,L=s.services;let sq='';
const F=(k,l,w='')=>`<div class="${w}"><label>${l}<input data-k="${k}" value="${e(s[k])}"></label></div>`;
const row=([v,k])=>`<div class="svr"><img class="th" src="${e(v.i||'images/logo-design.svg')}" alt=""><input data-i="${k}" data-f="n" value="${e(v.n)}" placeholder="Service name" aria-label="Service name"><input data-i="${k}" data-f="c" value="${e(v.c)}" placeholder="Heading" aria-label="Heading"><select data-i="${k}" data-f="g" aria-label="Title">${GR.map(g=>`<option${v.g==g?' selected':''}>${g}`).join('')}</select><input data-i="${k}" data-f="h" value="${e(v.h)}" placeholder="HSN/SAC" aria-label="HSN/SAC"><input data-i="${k}" data-f="u" value="${e(v.u)}" placeholder="Unit" aria-label="Unit"><input type="number" min="0" step="any" inputmode="decimal" data-i="${k}" data-f="p" value="${e(v.p)}" placeholder="Price" aria-label="Price"><label class="btn ghost up">Photo<input type="file" accept="image/*" data-img="${k}" hidden></label><button class="ghost" data-a="dsv" data-i="${k}" aria-label="Remove service">✕</button></div>`;
const svl=()=>{const R=L.map((v,k)=>[v,k]).filter(([v])=>(v.n+' '+v.c).toLowerCase().includes(sq.toLowerCase()));return GR.map(g=>{const r=R.filter(([v])=>v.g==g);if(sq&&!r.length)return'';return `<div class="sgh"><h3>${g} <small>(${r.length})</small></h3><button class="ghost sm" data-a="addsv" data-g="${g}">+ Add ${g.toLowerCase()} service</button></div>${r.length?r.map(row).join(''):`<div class="empty">No ${g.toLowerCase()} services yet.</div>`}`}).join('')||'<div class="empty">No service matches.</div>'};
app.innerHTML=`${RB()}<div class="state"><h1>Settings</h1></div>
<div class="card"><h2>Services you offer</h2><p style="color:var(--mut);margin-top:0">Add, edit or remove services here. They appear as suggestions when you type in Billing. Services are split under four titles: Design, Print, Signage and Digital. Use the + button under a title to add a service there, or move a service to another title with its drop-down.</p><div class="act" style="margin-bottom:10px"><button class="ghost" data-a="rs">Restore default list</button></div><input id="sq" class="search" type="search" placeholder="Search your services" aria-label="Search services"><div id="svl">${svl()}</div></div>
<div class="card"><h2>Business details</h2><div class="g2">${F('name','Business name')}${F('gst','GST No')}${F('phone','Phone')}${F('email','Email')}<div class="w"><label>Address<textarea data-k="addr">${e(s.addr)}</textarea></label></div></div></div>
<div class="card"><h2>Bank and payee</h2><div class="g2">${F('payto','Pay to / For')}${F('holder','Account holder name')}${F('bank','Bank name')}${F('acc','Account number')}${F('ifsc','IFSC code')}</div></div>
<div class="card"><h2>Numbering</h2><p style="color:var(--mut);margin-top:0">Estimates and invoices share one automatic number made of the date and an order number, like EST202610-23101. When an estimate becomes an invoice, the same number turns into INV202610-23101. Invoices made before this update keep their BIL number.</p><label>Start numbering from<input type="number" data-k="ne" value="${e(s.ne)}"></label></div>
<div class="card"><h2>Default terms</h2><textarea data-k="terms">${e(s.terms)}</textarea><p style="color:var(--mut)">Applies to new bills only.</p></div>
<div class="card"><h2>Bill colours</h2><p style="color:var(--mut);margin-top:0">Choose the colours used on printed and PDF invoices. They print exactly as shown here. Turn on black &amp; white to print every bill in greys.</p><div class="cpk">${[['hd','Header band'],['ac','Accent strip'],['th','Table heading'],['tt','Total bars']].map(([k,l])=>`<label>${l}<input type="color" data-c="${k}" value="${e(hx(s.colors[k],DC[k]))}"></label>`).join('')}</div>
<div class="cprev" id="cprev" style="--hd:${e(hx(s.colors.hd,DC.hd))};--ac:${e(hx(s.colors.ac,DC.ac))};--th:${e(hx(s.colors.th,DC.th))};--tt:${e(hx(s.colors.tt,DC.tt))};--hf:${fgOf(hx(s.colors.hd,DC.hd))};--thf:${fgOf(hx(s.colors.th,DC.th))};--ttf:${fgOf(hx(s.colors.tt,DC.tt))}"><div class="cph"><img src="${(lumOf(hx(s.colors.hd,DC.hd))>.6?window.ZX_LOGO_D:window.ZX_LOGO)||''}" alt=""></div><div class="cpa"></div><div class="cpt"><span>Service</span><span>Qty</span><span>Amount</span></div><div class="cpg"><span>Total</span><span>₹ 0.00</span></div></div>
<div class="act" style="margin-top:12px"><label class="swt"><input type="checkbox" role="switch" data-k="bw" ${s.bw?'checked':''}><span class="trk"><span class="knob"></span></span><span class="swl">Black &amp; white</span></label><button class="ghost" data-a="rc">Reset colours</button></div></div>
<div class="card"><h2>Cloud sync</h2><p style="color:var(--mut);margin-top:0">${cloud()?'Signed in as <b>'+e(SES.user.email)+'</b>. Everyone in your team shares one bill history and one set of settings.':'Not signed in.'}</p>${LEGACY?'<p style="color:#ffb020">Your Supabase database is still the older private version, so bills are <b>not shared</b> between logins. In Supabase open SQL Editor, paste everything from <b>backend/supabase.sql</b> and click Run (your bills are kept), then press Sync now.</p>':''}<div class="act"><button data-a="test">Sync now</button><button class="ghost" data-a="logout">Sign out</button></div></div>
<div class="card"><h2>Security check</h2><p style="color:var(--mut);margin-top:0">Checks that your data is private and that nobody else can create an account.</p><button class="ghost" data-a="sec">Run security check</button><div id="secout" style="margin-top:10px"></div></div>
<div class="card"><h2>Email (optional)</h2><p style="color:var(--mut);margin-top:0">To email bills, connect the Google email script (see backend/BACKEND-SETUP.md, part 2). Leave empty if you do not need email. Paste only the address of your own script: your login token is sent to it.</p><p class="hint" id="urlw" ${!s.url||okUrl(s.url)?'hidden':''} style="color:#ffb020">This does not look like a Google Apps Script web app address (https://script.google.com/macros/s/.../exec). Email stays off until it does.</p><div class="g2">${F('url','Email script URL (https://script.google.com/...)','w')}${F('copy','Your email (gets a copy of every bill)','w')}</div><p><label><input type="checkbox" data-k="auto" ${s.auto?'checked':''} style="width:auto"> Email the bill automatically when a payment is recorded</label></p></div>
<div class="card"><h2>Backup</h2><p style="color:var(--mut)">Data is stored in this browser and in your Supabase cloud. Download a backup regularly.</p><div class="act"><button data-a="ex">Download backup</button><label class="btn ghost" style="margin:0">Restore backup<input type="file" id="im" accept=".json" hidden></label></div></div>
<div class="act" style="margin-bottom:20px"><button data-a="savesets">Save settings</button></div>`;
app.oninput=ev=>{const t=ev.target;if(t.dataset.c){const c=t.dataset.c,v=t.value,pv=$('#cprev');S.set.colors[c]=v;if(pv){pv.style.setProperty('--'+c,v);if(c=='hd'){pv.style.setProperty('--hf',fgOf(v));const im=pv.querySelector('img');if(im)im.src=(lumOf(v)>.6?window.ZX_LOGO_D:window.ZX_LOGO)||''}if(c=='th')pv.style.setProperty('--thf',fgOf(v));if(c=='tt')pv.style.setProperty('--ttf',fgOf(v))}sch();return}if(t.id=='sq'){sq=t.value;$('#svl').innerHTML=svl();return}if(t.dataset.i!==undefined){const v=L[t.dataset.i],f=t.dataset.f;if(f=='g'){v.g=GR.includes(t.value)?t.value:'Print';v.k=v.g=='Digital'?'dm':'pr';sch();$('#svl').innerHTML=svl();return}v[f]=t.value;if(f=='h')v._ah=false;if(f=='n'&&(!v.h||v._ah)){v.h=hsnFor(t.value);v._ah=true;const hx=t.parentNode.querySelector('[data-f=h]');if(hx)hx.value=v.h}sch();return}const k=t.dataset.k;if(k){S.set[k]=t.type=='checkbox'?t.checked:['ne','nb'].includes(k)?+t.value:t.value;if(k=='url'){S.set.url=String(S.set.url||'').trim();const w=$('#urlw');if(w)w.hidden=!S.set.url||okUrl(S.set.url)}SH.includes(k)?sch():save()}};
app.onchange=ev=>{const t=ev.target,fl=t.files&&t.files[0];if(!fl)return;if(t.dataset.img!==undefined&&!/^image\//.test(fl.type)){alert('Choose an image file.');t.value='';return}if(t.id=='im'&&fl.size>50e6){alert('That file is too large to be a backup.');t.value='';return}const rd=new FileReader();
if(t.dataset.img!==undefined)rd.onload=()=>{const im=new Image();im.onload=()=>{const k=Math.min(1,360/im.width),c=document.createElement('canvas');c.width=im.width*k;c.height=im.height*k;c.getContext('2d').drawImage(im,0,0,c.width,c.height);L[t.dataset.img].i=c.toDataURL('image/jpeg',.6);sch();$('#svl').innerHTML=svl()};im.onerror=()=>alert('Could not read that image.');im.src=rd.result},rd.readAsDataURL(fl);
else if(t.id=='lg')rd.onload=()=>{const im=new Image();im.onload=()=>{const k=Math.min(1,240/im.width),c=document.createElement('canvas');c.width=im.width*k;c.height=im.height*k;c.getContext('2d').drawImage(im,0,0,c.width,c.height);S.set.logo=c.toDataURL('image/png');sch();sets()};im.src=rd.result},rd.readAsDataURL(fl);
else if(t.id=='im')fl.text().then(x=>{try{const j=JSON.parse(x);if(!Array.isArray(j.docs)||!j.set||typeof j.set!='object')throw 0;if(confirm('Restore this backup? Bills in it replace matching bills on this device and in the cloud. Bills that exist only on this device are kept. The email script address stays as it is on this device.')){const docs=j.docs.slice(0,50000).map(okDoc).filter(Boolean),kp=S.docs.filter(l=>!docs.some(b=>b.id===l.id));S={set:{...D0,...S.set,...okSet(j.set),key:''},docs:[...docs,...kp]};if(!Array.isArray(S.set.services)||!S.set.services.length)S.set.services=SV.map(x=>({...x}));docs.forEach(d=>{d.u=Date.now();pend.add(d.id)});S.set.su=Date.now();S.pset=1;save();push();location.hash='#/h';route()}}catch{alert('This is not a valid backup file.')}})};
app.onclick=ev=>{const b=ev.target.closest('[data-a]');if(!b)return;const a=b.dataset.a;
if(a=='savesets'){save();S.pset=1;push();toast('Settings saved');return}
if(a=='test'){SCHEMA=null;LEGACY=false;api('ping').then(()=>{S.pset=1;return pull()}).then(()=>{toast('Synced');if(location.hash=='#/s')sets()}).catch(x=>alert(explain(x)[1]))}
if(a=='logout')signOut();
if(a=='sec')secCheck();
if(a=='nl'){S.set.logo='';sch();sets()}
if(a=='rc'){S.set.colors={...DC};sch();sets()}
if(a=='ex'){saveFile('adzonex-backup-'+today()+'.json',new Blob([JSON.stringify({...S,set:{...S.set,key:''}})],{type:'application/json'}),'application/json','Ad ZoneX backup').catch(x=>alert('Could not save the backup: '+x.message))}
if(a=='addsv'){const g=GR.includes(b.dataset.g)?b.dataset.g:'Print';L.unshift({n:'',c:g=='Digital'?'Digital Marketing':g,g,k:g=='Digital'?'dm':'pr',h:'',u:g=='Digital'?'Month':g=='Design'?'Nos':'Sqf',p:0,i:'images/logo-design.svg'});sq='';$('#sq').value='';sch();$('#svl').innerHTML=svl();const f=document.querySelector('#svl [data-i="0"][data-f="n"]');f&&f.focus()}
if(a=='rs'&&confirm('Replace your service list with the default list? Your edits to services will be lost.')){S.set.services=SV.map(x=>({...x}));sch();sets()}
if(a=='dsv'&&confirm('Remove this service?')){L.splice(b.dataset.i,1);sch();$('#svl').innerHTML=svl()}}}
async function signOut(){if(!sb||!confirm('Sign out of this device? Your bills stay safe in the cloud. This device\'s local copy will be removed.'))return;
if(cloud()){st('Saving…');try{await push()}catch{}}
if((pend.size||S.pset)&&!confirm('Some changes have not reached the cloud yet. Sign out anyway and lose them?'))return;
try{localStorage.removeItem(K)}catch{}try{await sb.auth.signOut()}catch{}location.reload()}
async function secCheck(){const o=$('#secout');if(!o)return;o.textContent='Checking…';const L=[],add=(g,t)=>L.push((g?'OK: ':'FIX: ')+t);
try{add(location.protocol=='https:'||location.hostname=='localhost'||location.protocol=='file:','This page is served over '+location.protocol.replace(':','')+(location.protocol=='http:'&&location.hostname!='localhost'?' (should be https)':''));
const an=supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false,storageKey:'zx-sec-check'}});
for(const t of['docs','app_settings']){const r=await an.from(t).select('*').limit(1);const open=!r.error&&r.data&&r.data.length>0;add(!open,'Without logging in, "'+t+'" is '+(open?'READABLE by anyone. Run supabase.sql again.':'private'))}
const a=await fetch(SB_URL+'/auth/v1/settings',{headers:{apikey:SB_KEY}}).then(x=>x.json());
add(!!a.disable_signup,'New user sign-ups are '+(a.disable_signup?'turned off':'ON. Turn off in Supabase > Authentication > Sign In / Providers'));
add(cloud(),'Signed in: '+(cloud()?SES.user.email:'no'));if(cloud()){const tm=await sb.rpc('is_team_member');if(tm.error)add(false,'Database is the older private version. Run backend/supabase.sql in Supabase to share bills with your team');else add(tm.data===true,tm.data===true?'This login is in your team (shares all bills)':'This login is NOT in your team, so it cannot see or save bills. Add it in Supabase (see BACKEND-SETUP.md, Part 1, step 6)')}}catch(x){add(false,'Check failed: '+x.message)}
o.textContent='';L.forEach(x=>{const r=document.createElement('div'),g=x.startsWith('OK');r.style.color=g?'var(--ink)':'#ff6b6b';r.textContent=(g?'✓ ':'✗ ')+x.replace(/^(OK|FIX): /,'');o.append(r)})}
function toast(m){const t=document.createElement('div');t.className='toast fx';t.textContent=m;document.body.append(t);setTimeout(()=>t.remove(),2600)}
/* ===== helpers shared by Calendar, Expenses and WhatsApp ===== */
const waNum=p=>{const x=String(p||'').replace(/\D/g,'').replace(/^0+/,'').replace(/^(\d{10})$/,'91$1');return x.length>=8&&x.length<=15?x:''},telH=p=>String(p||'').replace(/[^\d+]/g,''),uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,7),dr=d=>String(d||'').split('-').reverse().join('-');
const MN=['January','February','March','April','May','June','July','August','September','October','November','December'],CTL={full:'Full',half:'Half',bal:'Balance',custom:'Amount'};
const loadJs=u=>new Promise((r,j)=>{const x=document.createElement('script');x.src=u;x.onload=r;x.onerror=j;document.head.append(x)});
async function renderImg(html){if(!window.html2canvas)await loadJs('libs/html2canvas.min.js');try{await document.fonts.ready}catch{}
const w=document.createElement('div');w.className='pdfx';w.innerHTML=html;document.body.append(w);
try{const el=w.firstElementChild;await Promise.all([...el.querySelectorAll('img')].map(i=>i.decode?i.decode().catch(()=>{}):0));
const cv=await html2canvas(el,{scale:2,backgroundColor:'#ffffff',useCORS:true,logging:false});
if(S.set.bw){const x=cv.getContext('2d',{willReadFrequently:true}),id=x.getImageData(0,0,cv.width,cv.height),p=id.data;for(let i=0;i<p.length;i+=4){const l=.299*p[i]+.587*p[i+1]+.114*p[i+2];p[i]=p[i+1]=p[i+2]=l}x.putImageData(id,0,0)}
return await new Promise((r,j)=>cv.toBlob(b=>b?r(b):j(new Error('image failed')),'image/png'))}finally{w.remove()}}

/* ===== WhatsApp: choose PDF / Image / Text, then open the customer's chat ===== */
function waShare(d){const ph=waNum(d.phone);if(!ph){alert('Add a valid customer phone number first.');return}
const T=isBill(d)?'Invoice':'Estimate',base=T+'-'+(no(d)||'draft').replace(/[\/\\]/g,'-'),chat='https://wa.me/'+ph,
txt=S.set.name+'\n'+T+' '+(no(d)||'')+'\nTotal ₹'+n2(tot(d))+(isBill(d)?'\nPaid ₹'+n2(pd(d))+'\nBalance ₹'+n2(bal(d)):'')+(d.rem?'\nRemark: '+d.rem:'');
const o=document.createElement('div');o.className='mdl';
o.innerHTML=`<div class="mdc" role="dialog" aria-modal="true" aria-label="Send on WhatsApp"><h2>Send on WhatsApp</h2><p class="hint" style="margin-top:0">To <b>+${e(ph)}</b>${d.cust?' ('+e(d.cust)+')':''}. What do you want to send?</p><div class="wopt"><button data-w="pdf">PDF</button><button data-w="img">Image</button><button data-w="txt">Text</button></div><p class="hint" id="wst" role="status"></p><div class="act"><a class="btn" id="wgo" hidden target="_blank" rel="noopener noreferrer" href="${chat}">Open WhatsApp chat</a><button class="ghost" data-w="x">Close</button></div></div>`;
document.body.append(o);
const esc=ev=>{if(ev.key=='Escape')close()},close=()=>{o.remove();document.removeEventListener('keydown',esc)};document.addEventListener('keydown',esc);
o.addEventListener('click',async ev=>{if(ev.target===o){close();return}const b=ev.target.closest('[data-w]');if(!b||b.disabled)return;const w=b.dataset.w;if(w=='x'){close();return}
if(w=='txt'){open(chat+'?text='+encodeURIComponent(txt),'_blank','noopener,noreferrer');lg(d,'WhatsApp text opened');touch(d);close();return}
const bs=[...o.querySelectorAll('[data-w]')],st=o.querySelector('#wst'),go=o.querySelector('#wgo');bs.forEach(x=>x.disabled=true);st.textContent='Preparing the '+(w=='pdf'?'PDF':'image')+'…';
try{const blob=w=='pdf'?(await pdfMake(d)).output('blob'):await renderImg(paper(d)),mime=w=='pdf'?'application/pdf':'image/png',mob=isNat()||(mobileUA()&&!!navigator.canShare);
await saveFile(base+(w=='pdf'?'.pdf':'.png'),blob,mime,T+' '+(no(d)||''));
let cp=false;if(w=='img'&&!mob){try{await navigator.clipboard.write([new ClipboardItem({'image/png':blob})]);cp=true}catch{}}
lg(d,'WhatsApp '+(w=='pdf'?'PDF':'image')+' prepared');touch(d);
st.textContent=mob?'Pick WhatsApp in the share list, then choose '+(d.cust||'the customer')+'. If you closed it, tap Open WhatsApp chat and attach the file.':(w=='pdf'?'The PDF was saved to your Downloads. ':'The image was saved to your Downloads'+(cp?' and copied (press Ctrl+V in the chat). ':'. '))+'Now click Open WhatsApp chat and attach it with the paperclip.';go.href=chat;go.hidden=false}
catch(x){console.warn(x);st.textContent='Could not prepare the file. Please try again.'}
bs.forEach(x=>x.disabled=false)})}

/* ===== Calendar: who pays on which day ===== */
const calL=()=>S.set.cal.filter(x=>!x.del),cdue=()=>calL().filter(x=>!x.ok&&x.d<=today()).sort((a,b)=>a.d<b.d?-1:a.d>b.d?1:a.n.localeCompare(b.n));
const calAmt=(id,t)=>{const d=S.docs.find(x=>x.id==id&&!x.del);return d?(t=='full'?tot(d):t=='half'?r2(tot(d)/2):t=='bal'?bal(d):0):0};
async function calDone(id){const x=S.set.cal.find(y=>y.id==id);if(!x)return false;let rec=false;const d=x.doc&&S.docs.find(z=>z.id==x.doc&&!z.del);
if(d&&x.a>0&&bal(d)>.005){const v=r2(Math.min(x.a,bal(d)));if(confirm('Also add ₹ '+n2(v)+' as a payment on '+no(d)+'?\n\nOK = add the payment to the bill\nCancel = only mark as received')){d.pay.push({d:today(),a:v,m:'Cash'});lg(d,'Payment ₹'+n2(v)+' received (Cash, from Calendar)');touch(d);if(!d.billNo)await pull();fix(d);touch(d);rec=true}}
x.ok=1;x.u=Date.now();sch();return rec}
let remHide=false;
function RB(){if(remHide)return'';const L=cdue();if(!L.length)return'';const t=today(),nt=L.filter(x=>x.d===t).length,od=L.length-nt;
return `<div class="rb"><div class="rbh"><b>${nt?'Collect money today ('+nt+')':'Missed collections ('+od+')'}${nt&&od?' + '+od+' missed':''}</b><button class="ghost sm" data-rh="1">Hide</button></div>${L.slice(0,8).map(x=>{const w=waNum(x.ph);return `<div class="rbr"><div><b>${e(x.n)}</b> · ₹ ${n2(x.a)} <small>${CTL[x.t]}${x.d<t?' · missed '+dm(x.d):''}${x.ph?' · '+e(x.ph):''}</small></div><div class="act">${x.ph?`<a class="btn sm" href="tel:${e(telH(x.ph))}">Call</a>`:''}${w?`<a class="btn ghost sm" target="_blank" rel="noopener noreferrer" href="https://wa.me/${w}">WhatsApp</a>`:''}<button class="ghost sm" data-bok="${e(x.id)}">Received</button></div></div>`}).join('')}${L.length>8?`<small>and ${L.length-8} more in Calendar</small>`:''}</div>`}
document.addEventListener('click',async ev=>{const b=ev.target.closest&&ev.target.closest('[data-bok]');if(b){b.disabled=true;const rec=await calDone(b.dataset.bok),r=document.querySelector('.rb');if(r)r.outerHTML=RB();if(rec&&['#/h','#/s',''].includes(location.hash))route();return}
const h=ev.target.closest&&ev.target.closest('[data-rh]');if(h){remHide=true;const r=h.closest('.rb');if(r)r.remove()}});
/* ===== Notifications that also work when the app is closed =====
   Android / iPhone app : reminders are scheduled with the phone's own alarm system (Capacitor Local Notifications), so they appear with the app closed.
   Windows / Mac / Linux: the app keeps running in the tray when its window is closed and shows a normal system notification.
   Browser / web app    : shown while the app is open; installed Chrome/Edge apps also get a background check (Periodic Background Sync). */
const LN=()=>{try{const C=window.Capacitor;if(!isNat())return null;return(C.Plugins&&C.Plugins.LocalNotifications)||(C.registerPlugin&&C.registerPlugin('LocalNotifications'))||null}catch{return null}},isDesk=()=>/Electron\//.test(navigator.userAgent);
async function notePerm(){const L=LN();if(L){try{const r=await L.checkPermissions();return r.display=='granted'?'granted':r.display=='denied'?'denied':'prompt'}catch{return'none'}}
if(!window.Notification)return'none';return Notification.permission=='default'?'prompt':Notification.permission}
async function noteAsk(){const L=LN();if(L){try{await L.requestPermissions()}catch{}}else if(window.Notification){try{await Notification.requestPermission()}catch{}}return notePerm()}
const permTxt=p=>p=='none'?'This device or browser cannot show notifications. The "Collect money today" box still appears inside the app.':p=='denied'?(LN()?'Notifications are off. Turn them on for Ad ZoneX Billing in your phone: Settings > Apps > Ad ZoneX Billing > Notifications.':'Notifications are blocked. Allow them for this site in the browser settings.'):p=='granted'?(LN()?'Notifications are on. You get one on the day, at the time above, even when the app is closed.':isDesk()?'Notifications are on. You get one on the day, at the time above. Closing the window keeps the app running in the tray so reminders still arrive. Quit it from the tray icon.':'Notifications are on. You get one on the day, at the time above, while the app or browser is open. Installed Chrome and Edge apps also check in the background. For reminders with the app fully closed on a phone, use the Android app.'):'Notifications are not turned on yet.';
function fireNote(t,o){o=o||{};const L=LN();
if(L){L.schedule({notifications:[{id:1,title:t,body:o.body||'',schedule:{at:new Date(Date.now()+1500)},channelId:'pay',smallIcon:'ic_stat_zx',extra:{go:'#/c'}}]}).catch(x=>console.warn('note',x));return}
if(!window.Notification||Notification.permission!='granted')return;
const direct=()=>{try{const n=new Notification(t,o);n.onclick=()=>{try{window.focus()}catch{}location.hash='#/c'}}catch{}};
if(location.protocol.startsWith('http')&&navigator.serviceWorker)navigator.serviceWorker.getRegistration().then(r=>r?r.showNotification(t,o):direct()).catch(direct);else direct()}
const hmOf=()=>/^\d{2}:\d{2}$/.test(S.set.rt||'')?S.set.rt:'09:00',noteLine=x=>x.n+' - ₹'+n2(x.a)+(x.ph?' ('+x.ph+')':'');
function remCheck(){if(LN())return;const L=cdue().filter(x=>x.d===today());if(!L.length||!window.Notification||Notification.permission!='granted'||S.set.rn===today())return;const n=new Date(),hm=String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');if(hm<hmOf())return;S.set.rn=today();save();
fireNote('Collect money today ('+L.length+')',{body:L.map(noteLine).join('\n'),icon:'icon-192.png',tag:'zx-pay-'+today()});noteCache()}
/* browser only: hand the list to the service worker so it can notify without the page */
async function noteCache(){try{if(LN()||!window.caches||!location.protocol.startsWith('http'))return;const c=await caches.open('zx-note');let old='';try{const r=await c.match('due.json');if(r)old=(await r.json()).last||''}catch{}
await c.put('due.json',new Response(JSON.stringify({rt:hmOf(),last:[old,S.set.rn||''].sort().pop(),list:calL().filter(x=>!x.ok).map(x=>({d:x.d,n:x.n,a:x.a,ph:x.ph}))})))}catch{}}
function noteBg(){try{if(LN()||!navigator.serviceWorker||!location.protocol.startsWith('http'))return;navigator.serviceWorker.ready.then(r=>r.periodicSync&&r.periodicSync.register('zx-due',{minInterval:3600e3})).catch(()=>{})}catch{}}
/* phone app: schedule one alarm per day that has someone to collect from (next 60 days). Run again after every change. */
let schT=0;function schedNote(){clearTimeout(schT);schT=setTimeout(schedNote0,1200)}
async function schedNote0(){noteCache();const L=LN();if(!L){if(window.Notification&&Notification.permission=='granted')noteBg();return}
try{if(await notePerm()!=='granted')return;
await L.createChannel({id:'pay',name:'Payment reminders',description:'Tells you who is due to pay today',importance:4,visibility:1,vibration:true});
const pn=await L.getPending();if(pn&&pn.notifications&&pn.notifications.length)await L.cancel({notifications:pn.notifications.map(n=>({id:n.id}))});
const hm=hmOf(),now=Date.now(),by={};calL().filter(x=>!x.ok&&x.d>=today()).forEach(x=>(by[x.d]=by[x.d]||[]).push(x));
const list=Object.keys(by).sort().map(d=>({d,at:new Date(d+'T'+hm+':00'),L:by[d]})).filter(g=>+g.at>now+5000).slice(0,60).map(g=>({id:+g.d.replace(/-/g,''),title:'Collect money today ('+g.L.length+')',body:g.L.map(noteLine).join(', '),largeBody:g.L.map(noteLine).join('\n'),schedule:{at:g.at,allowWhileIdle:true},channelId:'pay',smallIcon:'ic_stat_zx',extra:{go:'#/c'}}));
if(list.length)await L.schedule({notifications:list})}catch(x){console.warn('schedule notifications',x)}}
async function exactAsk(){const L=LN();if(!L||!L.checkExactNotificationSetting)return;try{const r=await L.checkExactNotificationSetting();if(r&&r.exact_alarm==='denied'&&!localStorage.getItem('zx-exact')){localStorage.setItem('zx-exact','1');if(confirm('To get the reminder exactly on time, allow "Alarms & reminders" for this app on the next screen.'))await L.changeExactNotificationSetting()}}catch{}}
setTimeout(()=>{const L=LN();if(L&&L.addListener){try{L.addListener('localNotificationActionPerformed',()=>{if(location.hash=='#/c')route();else location.hash='#/c'})}catch{}}},800);setTimeout(schedNote0,2500);
let cY=new Date().getFullYear(),cM=new Date().getMonth(),cSel=today(),cEd=null,cF={t:'bal'};
function cal(){const T=today(),all=calL(),by={};all.forEach(x=>(by[x.d]=by[x.d]||[]).push(x));
const mm=String(cM+1).padStart(2,'0'),pre=cY+'-'+mm,f0=new Date(cY,cM,1).getDay(),nd=new Date(cY,cM+1,0).getDate();let cells='';
for(let i=0;i<f0;i++)cells+='<div class="cd z"></div>';
for(let n=1;n<=nd;n++){const k=pre+'-'+String(n).padStart(2,'0'),L=by[k]||[],pn=L.filter(x=>!x.ok);cells+=`<div class="cd${k==T?' t':''}${k==cSel?' s':''}${pn.length?' p':''}" role="button" tabindex="0" data-cd="${k}" aria-label="${n} ${MN[cM]}${pn.length?', '+pn.length+' to collect':''}"><span class="cn">${n}</span>${L.slice(0,2).map(x=>`<span class="ce${x.ok?' dn':''}">${e(x.n)} ₹${n2(x.a).replace('.00','')}</span>`).join('')}${L.length>2?`<span class="ce more">+${L.length-2} more</span>`:''}</div>`}
const ml=all.filter(x=>x.d.startsWith(pre)),exp1=ml.filter(x=>!x.ok).reduce((a,x)=>a+x.a,0),got=ml.filter(x=>x.ok).reduce((a,x)=>a+x.a,0);
const DL=(by[cSel]||[]).slice().sort((a,b)=>a.u-b.u),dd=new Date(cSel+'T00:00:00').toLocaleDateString('en-IN',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
const ds=S.docs.filter(d=>!d.del&&(!isBill(d)||bal(d)>.005)).sort((a,b)=>b.u-a.u).slice(0,300);if(cF.doc&&!ds.find(d=>d.id==cF.doc)){const d=S.docs.find(x=>x.id==cF.doc&&!x.del);if(d)ds.unshift(d)}
const custs=[...new Set(S.docs.filter(d=>!d.del&&d.cust).map(d=>d.cust))].slice(0,500),sel=(v,x)=>v==x?' selected':'';
const ent=x=>{const w=waNum(x.ph),dc=x.doc&&S.docs.find(z=>z.id==x.doc&&!z.del);return `<div class="ent${x.ok?' dn':''}"><div><b>${e(x.n)}</b> <span class="chip">${CTL[x.t]}</span> <b class="am">₹ ${n2(x.a)}</b>${x.ok?' <span class="tick">✓</span>':''}<br><small>${x.ph?e(x.ph):''}${dc?(x.ph?' · ':'')+e(no(dc)):''}${x.note?((x.ph||dc)?' · ':'')+e(x.note):''}</small></div><div class="act">${x.ph?`<a class="btn ghost sm" href="tel:${e(telH(x.ph))}">Call</a>`:''}${w?`<a class="btn ghost sm" target="_blank" rel="noopener noreferrer" href="https://wa.me/${w}">WhatsApp</a>`:''}${x.ok?`<button class="ghost sm" data-cun="${e(x.id)}">Undo</button>`:`<button class="sm" data-cdn="${e(x.id)}">Received</button>`}<button class="ghost sm" data-ced="${e(x.id)}">Edit</button><button class="ghost sm" data-cdel="${e(x.id)}" aria-label="Delete entry">✕</button></div></div>`};
const perm='';
app.innerHTML=`<div class="state"><h1>Calendar</h1><small>To collect this month: <b>₹ ${n2(exp1)}</b> · Received: <b>₹ ${n2(got)}</b></small></div>
<div class="card"><div class="cmh"><div class="act"><button class="ghost" data-cn="-1" aria-label="Previous month">‹</button><button class="ghost" data-cn="0">Today</button><button class="ghost" data-cn="1" aria-label="Next month">›</button></div><h2>${MN[cM]} ${cY}</h2></div>
<div class="cal">${['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(x=>`<div class="cdh">${x}</div>`).join('')}${cells}</div><p class="hint">Click a date to note who will pay that day. Dates with money to collect have a green border.</p></div>
<div class="card"><h2>${e(dd)}</h2>${DL.length?DL.map(ent).join(''):'<p class="hint" style="margin:0">Nobody is noted for this day yet.</p>'}</div>
<div class="card"><h2>${cEd?'Edit entry':'Add who pays on this day'}</h2><datalist id="cl">${custs.map(c=>`<option value="${e(c)}">`).join('')}</datalist><div class="cg">
<div class="s2"><label>Customer name<input id="cn" list="cl" autocomplete="off" value="${e(cF.n||'')}"></label></div><div><label>Phone<input id="cp" type="tel" value="${e(cF.ph||'')}"></label></div>
<div><label>Link a bill (optional)<select id="cb"><option value="">No bill</option>${ds.map(d=>`<option value="${e(d.id)}"${sel(cF.doc,d.id)}>${e(no(d))} · ${e(d.cust||'-')} · ${isBill(d)?'Balance ₹ '+n2(bal(d)):'Estimate ₹ '+n2(tot(d))}</option>`).join('')}</select></label></div>
<div><label>Will pay<select id="ct"><option value="full"${sel(cF.t,'full')}>Full amount</option><option value="half"${sel(cF.t,'half')}>Half (50%)</option><option value="bal"${sel(cF.t,'bal')}>Balance</option><option value="custom"${sel(cF.t,'custom')}>Any other amount</option></select></label></div>
<div><label>Amount (₹)<input id="ca" type="number" min="0" step="any" inputmode="decimal" value="${e(cF.a||'')}"></label></div><div class="s2"><label>Note (optional)<input id="cno" value="${e(cF.note||'')}"></label></div></div>
<p class="hint">Link a bill and Full, Half or Balance fills the amount for you. For any other amount, type it.</p><div class="act"><button data-ca="save">${cEd?'Update entry':'Add to calendar'}</button>${cEd?'<button class="ghost" data-ca="cancel">Cancel</button>':''}</div></div>
<div class="card"><h2>Reminder</h2><p class="hint" style="margin-top:0">On the day, every page shows a "Collect money today" box with Call and WhatsApp buttons for each person. You can also get a notification at this time:</p><div class="act" style="align-items:flex-end"><label style="width:150px">Remind me at<input type="time" id="rt" value="${e(S.set.rt||'09:00')}"></label><button class="ghost" data-nt="1">Turn on notifications</button></div><p class="hint" id="nts">${perm}</p></div>`;
notePerm().then(p=>{const n=$('#nts');if(n)n.textContent=permTxt(p)});
const recalc=()=>{const id=$('#cb').value,t=$('#ct').value;if(id&&t!='custom'){const v=calAmt(id,t);$('#ca').value=v>0?v:''}};
const save1=()=>{const n=$('#cn').value.trim(),a=+$('#ca').value;if(!n){alert('Enter the customer name.');return}if(!(a>0)||!isFinite(a)||a>=1e10){alert('Enter the amount this customer will pay.');return}
const o=okCal({id:cEd||uid(),d:cSel,n,ph:$('#cp').value.trim(),t:$('#ct').value,a:r2(a),doc:$('#cb').value,note:$('#cno').value.trim(),ok:0,u:Date.now()}),i=S.set.cal.findIndex(x=>x.id==cEd);
if(i>=0){o.ok=S.set.cal[i].ok;S.set.cal[i]=o}else S.set.cal.push(o);cEd=null;cF={t:'bal'};sch();cal()};
app.onfocusout=null;
app.oninput=ev=>{const t=ev.target;if(t.id=='cn'){const nm=t.value.trim().toLowerCase();if(!nm)return;const m=S.docs.filter(d=>!d.del&&String(d.cust||'').trim().toLowerCase()==nm).sort((a,b)=>b.u-a.u);if(!m.length)return;if(!$('#cp').value)$('#cp').value=m[0].phone||'';const due=m.find(d=>!isBill(d)||bal(d)>.005);if(due&&!$('#cb').value){$('#cb').value=due.id;if($('#cb').value)recalc()}}};
app.onchange=ev=>{const t=ev.target;if(t.id=='cb'){const d=S.docs.find(x=>x.id==t.value&&!x.del);if(d){if(!$('#cn').value)$('#cn').value=d.cust||'';if(!$('#cp').value)$('#cp').value=d.phone||''}recalc()}else if(t.id=='ct')recalc();else if(t.id=='rt'){S.set.rt=/^\d{2}:\d{2}$/.test(t.value)?t.value:'09:00';S.set.rn='';save();schedNote()}};
app.onkeydown=ev=>{const t=ev.target;if(ev.key!='Enter')return;if(t.dataset.cd){cSel=t.dataset.cd;cEd=null;cF={t:'bal'};cal()}else if(['cn','cp','ca','cno'].includes(t.id)){ev.preventDefault();save1()}};
app.onclick=async ev=>{const b=ev.target.closest('[data-cd],[data-cn],[data-ca],[data-ced],[data-cdel],[data-cdn],[data-cun],[data-nt]');if(!b)return;const D=b.dataset;
if(D.cd){cSel=D.cd;cEd=null;cF={t:'bal'};cal();return}
if(D.cn!==undefined){if(D.cn=='0'){cY=new Date().getFullYear();cM=new Date().getMonth();cSel=today()}else{cM+=+D.cn;if(cM<0){cM=11;cY--}if(cM>11){cM=0;cY++}}cal();return}
if(D.ca=='save'){save1();return}if(D.ca=='cancel'){cEd=null;cF={t:'bal'};cal();return}
if(D.ced){const x=S.set.cal.find(y=>y.id==D.ced);if(x){cEd=x.id;cSel=x.d;cF={n:x.n,ph:x.ph,doc:x.doc,t:x.t,a:x.a,note:x.note};cal();scrollTo(0,document.body.scrollHeight)}return}
if(D.cdel){if(confirm('Delete this entry?')){const x=S.set.cal.find(y=>y.id==D.cdel);if(x){x.del=1;x.u=Date.now();sch();cal()}}return}
if(D.cdn){b.disabled=true;await calDone(D.cdn);cal();return}
if(D.cun){const x=S.set.cal.find(y=>y.id==D.cun);if(x){x.ok=0;x.u=Date.now();sch();cal()}return}
if(D.nt){const p0=await notePerm();if(p0=='none'){alert('This device or browser cannot show notifications.');return}
const p=p0=='denied'&&!LN()?'denied':await noteAsk();if(p=='granted'){fireNote('Notifications are on',{body:'You will be reminded on the day someone is due to pay.',icon:'icon-192.png'});await exactAsk();schedNote0();noteBg()}else alert(permTxt(p));cal()}}}

/* ===== Expenses ===== */
let xT='today',xF=today(),xTo=today(),xEd=null,xFm={};
const XC=['Material','Transport','Fuel','Salary','Rent','Electricity','Food & Tea','Internet & Phone','Repairs','Other'],XM=['Cash','UPI','Bank','Card'],xAll=()=>S.set.exp.filter(x=>!x.del);
function xRange(){const t=today(),y=t.slice(0,4),m=t.slice(5,7);if(xT=='today')return[t,t,'Today ('+dr(t)+')'];if(xT=='month')return[y+'-'+m+'-01',y+'-'+m+'-31',MN[+m-1]+' '+y];if(xT=='all')return['0000-01-01','9999-12-31','All dates'];
let a=dOk(xF)?xF:t,b=dOk(xTo)?xTo:t;if(a>b)[a,b]=[b,a];return[a,b,a==b?dr(a):dr(a)+' to '+dr(b)]}
const xList=()=>{const[a,b]=xRange();return xAll().filter(x=>x.d>=a&&x.d<=b).sort((p,q)=>p.d<q.d?1:p.d>q.d?-1:q.u-p.u)};
function expPaper(L,lab){const s=S.set,C=s.colors||DC,hd=hx(C.hd,DC.hd),ac=hx(C.ac,DC.ac),th=hx(C.th,DC.th),tt=hx(C.tt,DC.tt),logo=(lumOf(hd)>.6?window.ZX_LOGO_D:window.ZX_LOGO)||'',T=L.reduce((a,x)=>a+x.a,0),cs={};L.forEach(x=>{const c=x.c||'Other';cs[c]=(cs[c]||0)+x.a});
return `<div class="zp${s.bw?' bw':''}" style="--hd:${hd};--ac:${ac};--th:${th};--tt:${tt};--hf:${fgOf(hd)};--thf:${fgOf(th)};--ttf:${fgOf(tt)}"><style>${PCSS}</style>
<div class="ph"><img class="plogo" src="${logo}" alt="${e(s.name)}"><div class="pco"><b>${e(s.name)}</b><div class="pl">${e(s.addr)}</div>Phone : ${e(s.phone)}<br>${e(s.email)}</div></div><div class="pac"></div>
<div class="pbody"><h3 class="ptt">Expense Report</h3><div class="pinfo"><div class="pbt"><small>PERIOD</small><b>${e(lab)}</b></div><div class="pmeta"><div><span>Entries</span><b>${L.length}</b></div><div><span>Total spent</span><b>₹ ${n2(T)}</b></div></div></div>
<table class="pq"><thead><tr><th>#<th>Date<th>Category<th>Description<th>Mode<th class="r">Amount</tr></thead><tbody>${L.map((x,k)=>`<tr><td>${k+1}<td class="nw">${dm(x.d)}<td>${e(x.c)}<td>${e(x.n)}<td>${e(x.m)}<td class="r nw">₹ ${n2(x.a)}</tr>`).join('')}</tbody></table>
<div class="pbot"><div class="pw2"><b>By category</b>${Object.keys(cs).sort((a,b)=>cs[b]-cs[a]).map(c=>`<p>${e(c)} : ₹ ${n2(cs[c])}</p>`).join('')}</div><div class="ptot"><div class="gr">Total<span>₹ ${n2(T)}</span></div></div></div></div>
<div class="pft">Generated on ${dr(today())}</div></div>`}
function expText(L,lab){const T=L.reduce((a,x)=>a+x.a,0),cs={};L.forEach(x=>{const c=x.c||'Other';cs[c]=(cs[c]||0)+x.a});
return [S.set.name+' - Expenses','Period: '+lab,'',...L.map(x=>dr(x.d)+' | '+(x.c||'Other')+' | '+(x.n||'-')+' | '+(x.m||'-')+' | ₹ '+n2(x.a)),'','By category:',...Object.keys(cs).sort((a,b)=>cs[b]-cs[a]).map(c=>'  '+c+': ₹ '+n2(cs[c])),'','Total: ₹ '+n2(T)+' ('+L.length+' entries)'].join('\n')+'\n'}
async function xExport(k,b){const L=xList().slice().sort((p,q)=>p.d<q.d?-1:p.d>q.d?1:p.u-q.u),lab=xRange()[2];if(!L.length){alert('There are no expenses in this period.');return}
const base='Expenses-'+lab.replace(/[^\w]+/g,'-').replace(/^-|-$/g,''),html=expPaper(L,lab);b.disabled=true;
try{if(k=='txt')await saveFile(base+'.txt',new Blob([expText(L,lab)],{type:'text/plain;charset=utf-8'}),'text/plain','Expenses '+lab);
else if(k=='pdf'){const P=await renderPdf(html,'Expenses '+lab);await saveFile(base+'.pdf',P.output('blob'),'application/pdf','Expenses '+lab)}
else if(k=='img')await saveFile(base+'.png',await renderImg(html),'image/png','Expenses '+lab);
else if(k=='prn'){if(isNat()){const P=await renderPdf(html,'Expenses '+lab);await saveFile(base+'.pdf',P.output('blob'),'application/pdf','Expenses '+lab,true)}else pj(html)}}
catch(x){console.warn(x);if(!x||x.name!='AbortError')alert('Could not create the file. Please try again.')}finally{b.disabled=false}}
// Remember what is typed in the form, only when the page is redrawn for another reason (tab, date range, delete).
const xSnap=()=>{if($('#xa'))xFm={d:$('#xd').value,c:$('#xc').value,n:$('#xn').value,a:$('#xa').value,m:$('#xm').value}};
function expn(){
const L=xList(),TT=L.reduce((a,x)=>a+x.a,0),T=today(),td=xAll().filter(x=>x.d==T).reduce((a,x)=>a+x.a,0),mo=xAll().filter(x=>x.d.startsWith(T.slice(0,7))).reduce((a,x)=>a+x.a,0),lab=xRange()[2],cats=[...new Set([...XC,...xAll().map(x=>x.c).filter(Boolean)])],cs={};L.forEach(x=>{const c=x.c||'Other';cs[c]=(cs[c]||0)+x.a});
const f=xFm,fd=dOk(f.d)?f.d:T,TABS=[['today','Today'],['month','This month'],['all','All'],['range','Pick dates']];
app.innerHTML=RB()+`<div class="state"><h1>Expenses</h1><div class="act"><button class="ghost" data-xe="pdf">PDF</button><button class="ghost" data-xe="img">Image</button><button class="ghost" data-xe="txt">Text</button><button data-xe="prn">Print</button></div></div>
<div class="stats"><div class="hero"><small>${e(lab)}</small><b>₹ ${n2(TT)}</b></div><div><small>Spent today</small><b>₹ ${n2(td)}</b></div><div><small>Spent this month</small><b>₹ ${n2(mo)}</b></div></div>
<div class="card"><h2>${xEd?'Edit expense':'Add expense'}</h2><datalist id="xcl">${cats.map(c=>`<option value="${e(c)}">`).join('')}</datalist><div class="cg"><div><label>Date<input id="xd" type="date" value="${e(fd)}"></label></div><div><label>Category<input id="xc" list="xcl" autocomplete="off" value="${e(f.c||'')}" placeholder="e.g. Fuel"></label></div><div class="s2"><label>What was it for<input id="xn" value="${e(f.n||'')}" placeholder="e.g. Petrol for the van"></label></div><div><label>Amount (₹)<input id="xa" type="number" min="0" step="any" inputmode="decimal" value="${e(f.a||'')}"></label></div><div><label>Paid by<select id="xm">${XM.map(m=>`<option${m==(f.m||'Cash')?' selected':''}>${m}`).join('')}</select></label></div></div>
<div class="act" style="margin-top:12px"><button data-xa="add">${xEd?'Update expense':'Add expense'}</button>${xEd?'<button class="ghost" data-xa="cancel">Cancel</button>':''}</div></div>
<div class="bar tabs">${TABS.map(t=>`<button class="${xT==t[0]?'on':''}" data-xt="${t[0]}">${t[1]}</button>`).join('')}</div>
${xT=='range'?`<div class="bar finder" style="grid-template-columns:1fr 1fr"><label>From<input type="date" id="xf" value="${e(xF)}"></label><label>To<input type="date" id="xto" value="${e(xTo)}"></label></div>`:''}
${L.length?`<div class="sw"><table class="lt"><tr><th>Date<th>Category<th>Description<th>Paid by<th class="r">Amount<th></tr>${L.map(x=>`<tr><td>${dm(x.d)}<td>${e(x.c)||'-'}<td class="wr">${e(x.n)||'-'}<td>${e(x.m)}<td class="r">₹ ${n2(x.a)}<td class="nw"><button class="ghost sm" data-xed="${e(x.id)}">Edit</button> <button class="ghost sm" data-xdel="${e(x.id)}" aria-label="Delete expense">✕</button></tr>`).join('')}</table></div>
<div class="tt" style="margin-top:14px"><div class="gr">Total spent<span>₹ ${n2(TT)}</span></div></div><div class="xcat">${Object.keys(cs).sort((a,b)=>cs[b]-cs[a]).map(c=>`<span class="chip">${e(c)} ₹ ${n2(cs[c])}</span>`).join('')}</div>`:'<div class="empty">No expenses for this period. Add one above.</div>'}`;
app.onfocusout=null;
const sv1=()=>{const a=+$('#xa').value,d=$('#xd').value;if(!dOk(d)){alert('Pick the date.');return}if(!(a>0)||!isFinite(a)||a>=1e10){alert('Enter the amount spent.');return}
const o=okExp({id:xEd||uid(),d,c:$('#xc').value.trim()||'Other',n:$('#xn').value.trim(),a:r2(a),m:$('#xm').value,u:Date.now()}),i=S.set.exp.findIndex(x=>x.id==xEd);if(i>=0)S.set.exp[i]=o;else S.set.exp.push(o);
xEd=null;xFm={d:d,m:o.m};sch();expn();const n=$('#xn');n&&n.focus()};
app.oninput=null;
app.onchange=ev=>{const t=ev.target;if(t.id=='xf'||t.id=='xto'){xSnap();xF=$('#xf').value;xTo=$('#xto').value;expn()}};
app.onkeydown=ev=>{if(ev.key=='Enter'&&['xd','xc','xn','xa'].includes(ev.target.id)){ev.preventDefault();sv1()}};
app.onclick=ev=>{const b=ev.target.closest('[data-xa],[data-xt],[data-xe],[data-xed],[data-xdel]');if(!b)return;const D=b.dataset;
if(D.xt){xSnap();xT=D.xt;expn();return}if(D.xa=='add'){sv1();return}if(D.xa=='cancel'){xEd=null;xFm={};expn();return}
if(D.xed){const x=S.set.exp.find(y=>y.id==D.xed);if(x){xEd=x.id;xFm={d:x.d,c:x.c,n:x.n,a:x.a,m:x.m};expn();scrollTo(0,0)}return}
if(D.xdel){if(confirm('Delete this expense?')){const x=S.set.exp.find(y=>y.id==D.xdel);if(x){x.del=1;x.u=Date.now();xSnap();if(xEd==x.id){xEd=null;xFm={}}sch();expn()}}return}
if(D.xe)xExport(D.xe,b)}}

function route(){const h=location.hash;scrollTo(0,0);acHide();
if(h=='#/h')hist();else if(h=='#/c')cal();else if(h=='#/x')expn();else if(h=='#/s')sets();else if(h.startsWith('#/d/')&&S.docs.find(x=>x.id==h.slice(4)&&!x.del))bill(S.docs.find(x=>x.id==h.slice(4)&&!x.del));else bill(null)
const on=['#/s','#/h','#/c','#/x'].includes(h)?h:h.startsWith('#/d/')?'#/h':'#/';document.querySelectorAll('[data-nav]').forEach(a=>a.classList.toggle('on',a.getAttribute('href')==on))}
const bl2=$('#blogo');if(bl2&&window.ZX_LOGO)bl2.src=ZX_LOGO;
addEventListener('hashchange',route);route();setInterval(remCheck,60000);setTimeout(remCheck,1500);
function showLogin(){if(FRAMED||$('#zxl'))return;const o=document.createElement('div');o.id='zxl';o.className='zxl';
o.innerHTML=`<form class="zxc"><img src="${window.ZX_LOGO||''}" alt="Ad ZoneX"><h2>Sign in</h2><label>Email<input type="email" name="email" autocomplete="username" required></label><label>Password<input type="password" name="password" autocomplete="current-password" required></label><p class="zxe" id="zxe"></p><button type="submit">Sign in</button></form>`;document.body.append(o);const sh=$('.shell');if(sh)sh.inert=true;const f1=o.querySelector('input');if(f1)f1.focus();
if(!sb){$('#zxe').textContent='Could not load the cloud library. Reload the page.';return}
o.querySelector('form').onsubmit=async ev=>{ev.preventDefault();const f=ev.target,b=f.querySelector('button'),m=$('#zxe');b.disabled=true;m.textContent='';
try{const r=await sb.auth.signInWithPassword({email:f.email.value.trim(),password:f.password.value});if(r.error)m.textContent=r.error.message}catch(x){m.textContent='No connection. Try again.'}b.disabled=false}}
const hideLogin=()=>{const o=$('#zxl');if(o)o.remove();const sh=$('.shell');if(sh)sh.inert=false};
if(sb)sb.auth.onAuthStateChange((ev,ss)=>{const was=SES;SES=ss;if(!ss||!was){SCHEMA=null;LEGACY=false;MEMBER=null}if(ss){hideLogin();if(!was)setTimeout(()=>pull().then(()=>{if(['#/h','#/s','#/c','#/x'].includes(location.hash))route()}),0)}else{setTimeout(showLogin,0)}});else showLogin();
addEventListener('focus',()=>{remCheck();if(cloud())pull()});addEventListener('online',()=>cloud()&&pull());addEventListener('scroll',acPos,true);addEventListener('resize',acPos);if(window.visualViewport)visualViewport.addEventListener('resize',acPos);
document.addEventListener('click',ev=>{const a=ev.target.closest('a[href="#/"]');if(a&&['','#/'].includes(location.hash)){ev.preventDefault();route()}});
if('serviceWorker'in navigator&&location.protocol.startsWith('http')&&!isNat())navigator.serviceWorker.register('sw.js').catch(()=>{});
