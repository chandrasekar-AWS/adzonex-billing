// Runs Code.gs inside a sandbox that imitates Google Apps Script, then attacks it.
const fs = require('fs'), vm = require('vm');
const file = process.argv[2];
let R = [];
const check = (n, c, info) => { R.push(c); console.log((c ? 'PASS ' : 'FAIL ') + n + (c ? '' : '  -> ' + info)); };

function sandbox(users) {                       // users: token -> supabase user object
  const sent = [], props = {}, fetched = [];
  const ctx = {
    console, JSON, Date, String, Number, Array, Object, RegExp, Math, Error, Buffer,
    ContentService: { MimeType: { JSON: 'json' }, createTextOutput: t => ({ text: t, setMimeType() { return this; } }) },
    LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
    PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] ?? null, setProperties: o => Object.assign(props, o) }) },
    UrlFetchApp: { fetch: (url, o) => { fetched.push(url); const t = (o.headers.Authorization || '').replace('Bearer ', ''); const u = users[t];
        return { getResponseCode: () => u ? 200 : 401, getContentText: () => JSON.stringify(u || { msg: 'bad jwt' }) }; } },
    MailApp: { sendEmail: o => sent.push(o), getRemainingDailyQuota: () => 100 },
    Utilities: { newBlob: (d, t, n) => ({ d, t, n, getAs() { return { setName: () => ({ t: 'pdf-from-html' }) }; } }), base64Decode: s => Buffer.from(s, 'base64') },
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(file, 'utf8') + '\n;this.doPost=doPost;', ctx);
  return { ctx, sent, props, fetched };
}
const tok = (n) => `aaa.bbb.${n}`;
const users = {
  [tok('owner')]: { aud: 'authenticated', email: 'chandru24025@gmail.com' },
  [tok('OWNERCASE')]: { aud: 'authenticated', email: 'ChanDru24025@Gmail.com' },
  [tok('stranger')]: { aud: 'authenticated', email: 'stranger@evil.com' },
  [tok('anon')]: { aud: 'authenticated', email: 'chandru24025@gmail.com', is_anonymous: true },
  [tok('wrongaud')]: { aud: 'anon', email: 'chandru24025@gmail.com' },
};
const call = (sb, body) => JSON.parse(sb.ctx.doPost({ postData: { contents: typeof body === 'string' ? body : JSON.stringify(body) } }).text);
const good = (o = {}) => ({ jwt: tok('owner'), a: 'mail', to: 'cust@example.com', subject: 'Invoice 1', file: 'INV1', html: '<p>hi</p>', ...o });

let sb = sandbox(users);
check('valid owner can send', call(sb, good()).ok === 1 && sb.sent.length === 1);
check('login email match is case-insensitive', call(sandbox(users), good({ jwt: tok('OWNERCASE') })).ok === 1);
sb = sandbox(users); check('stranger with a valid Supabase login is refused', call(sb, good({ jwt: tok('stranger') })).err && !sb.sent.length);
sb = sandbox(users); check('no token is refused', call(sb, good({ jwt: undefined })).err && !sb.sent.length);
sb = sandbox(users); check('forged/unknown token is refused', call(sb, good({ jwt: tok('forged') })).err && !sb.sent.length);
sb = sandbox(users); const rr = call(sb, good({ jwt: "x.y.z'; DROP" })); check('non-JWT-shaped token never reaches Supabase', rr.err && !sb.fetched.length, sb.fetched);
sb = sandbox(users); check('anonymous-session token is refused', call(sb, good({ jwt: tok('anon') })).err && !sb.sent.length, 'anon accepted');
sb = sandbox(users); check('token not issued for a signed-in user (aud=anon) is refused', call(sb, good({ jwt: tok('wrongaud') })).err && !sb.sent.length, 'wrong aud accepted');
sb = sandbox(users); check('garbage body does not crash', call(sb, 'not json').err === 'Bad request');
sb = sandbox(users); check('empty body does not crash', JSON.parse(sb.ctx.doPost({}).text).err === 'Bad request');
sb = sandbox(users); check('unknown action refused', call(sb, good({ a: 'delete' })).err === 'Unknown action' && !sb.sent.length);
for (const bad of ['a@b.com,b@c.com,c@d.com,e@f.com', 'x', 'a@b.com;b@c.com', 'bcc@evil.com\nBcc: x@y.com', '<a@b.com>', 'a@b', '"a b"@c.com', 'a(b)@c.com', ''])
  { sb = sandbox(users); check('bad recipient rejected: ' + JSON.stringify(bad).slice(0, 40), call(sb, good({ to: bad })).err && !sb.sent.length, JSON.stringify(sb.sent[0])); }
sb = sandbox(users); call(sb, good({ subject: 'Hello\r\nBcc: attacker@evil.com' })); check('header injection via subject neutralised', sb.sent[0] && !/[\r\n]/.test(sb.sent[0].subject), sb.sent[0] && JSON.stringify(sb.sent[0].subject));
sb = sandbox(users); call(sb, good({ file: '../../etc/passwd\r\n' })); check('attachment name cannot contain path/newlines', sb.sent[0] && sb.sent[0].attachments && !/[\/\\\r\n]/.test(sb.sent[0].attachments[0].n), sb.sent[0] && sb.sent[0].attachments && sb.sent[0].attachments[0].n);
sb = sandbox(users); check('huge HTML refused', call(sb, good({ html: 'x'.repeat(400001) })).err && !sb.sent.length);
sb = sandbox(users); sb.props.day = new Date().toISOString().slice(0, 10); sb.props.n = '99'; check('daily limit enforced (99 + 2 > 100)', call(sb, good({ to: 'a@b.com,c@d.com' })).err === 'Daily email limit reached' && !sb.sent.length);
sb = sandbox(users); sb.ctx.MailApp.sendEmail = () => { throw new Error('Service invoked too many times: SECRET-INTERNAL-DETAIL at line 99'); }; const e1 = call(sb, good());
check('internal errors are not leaked to the caller', e1.err && !/SECRET-INTERNAL|line 99|Error:/.test(e1.err), e1.err);
sb = sandbox(users); sb.ctx.MailApp.sendEmail = () => { throw new Error('boom'); }; call(sb, good()); check('a failed send does not use up the daily allowance', !sb.props.n || sb.props.n === '0', sb.props.n);
sb = sandbox(users); call(sb, good({ pdf: Buffer.from('%PDF-1.4 test').toString('base64') })); check('app-made PDF is attached when supplied', sb.sent[0] && sb.sent[0].attachments[0].t === 'application/pdf');
sb = sandbox(users); call(sb, good({ pdf: '<script>alert(1)</script>' })); check('non-base64 "pdf" field falls back safely (no crash, still one mail)', sb.sent.length === 1);
const ok = R.filter(Boolean).length; console.log(`\n${ok}/${R.length} passed  (${file.split('/').pop()})`);
