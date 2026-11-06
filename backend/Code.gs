// Ad ZoneX Billing: optional email sender (Google Apps Script).
// Only the logins listed in ALLOWED_EMAILS can use it. No shared secret is stored in the app.
//
// Security notes:
//  * Every request must carry a valid Supabase login token. The script asks Supabase who the token belongs to and
//    only continues if that person is in ALLOWED_EMAILS (and the token was issued for a signed-in user, not the public key).
//  * Mail goes only to real-looking addresses, at most 3 per request, at most MAX_PER_DAY per day.
//  * Errors are logged inside Apps Script (View > Executions) and the app only gets a short, generic message.

const SUPABASE_URL = 'https://krfjrasoihxhxnjskrhi.supabase.co';
const SUPABASE_KEY = 'sb_publishable_E9aUji5CGt6_MPWWzfMJbw_tw8NXJ1s'; // publishable key (public)
const ALLOWED_EMAILS = ['chandru24025@gmail.com'];  // logins allowed to send mail. Add your friend's login email too, e.g. ['you@x.com','friend@x.com']
const MAX_PER_DAY  = 100;                        // safety limit
const FROM_NAME    = 'Ad ZoneX';

const out = o => ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
const EMAIL_RE = /^[^\s@,;<>"()\[\]\\]+@[^\s@,;<>"()\[\]\\]+\.[^\s@,;<>"()\[\]\\]+$/;
const JWT_RE = /^[\w-]+\.[\w-]+\.[\w-]+$/;

function verifyOwner_(jwt) {
  if (!jwt || typeof jwt !== 'string' || jwt.length > 4000 || !JWT_RE.test(jwt)) return false;
  const r = UrlFetchApp.fetch(SUPABASE_URL + '/auth/v1/user', {
    method: 'get', muteHttpExceptions: true,
    headers: { apikey: SUPABASE_KEY, Authorization: 'Bearer ' + jwt }
  });
  if (r.getResponseCode() !== 200) return false;
  const u = JSON.parse(r.getContentText());
  if (!u || u.aud !== 'authenticated' || u.is_anonymous === true) return false;
  return ALLOWED_EMAILS.map(x => String(x).toLowerCase()).indexOf(String(u.email || '').toLowerCase()) >= 0;
}

function doPost(ev) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (x) {
    return out({ err: 'Busy, please try again.' });
  }
  try {
    if (!ev || !ev.postData || String(ev.postData.contents || '').length > 20000000) return out({ err: 'Bad request' });
    let p;
    try { p = JSON.parse(ev.postData.contents); } catch (x) { return out({ err: 'Bad request' }); }
    if (!p || typeof p !== 'object') return out({ err: 'Bad request' });
    if (!verifyOwner_(p.jwt)) return out({ err: 'Not allowed. Sign in to the app first.' });
    if (p.a !== 'mail') return out({ err: 'Unknown action' });

    const to = String(p.to || '').split(',').map(x => x.trim()).filter(Boolean);
    if (!to.length || to.length > 3 || !to.every(x => x.length <= 254 && EMAIL_RE.test(x))) return out({ err: 'Invalid email address' });
    const html = String(p.html || ''), subject = String(p.subject || '').replace(/[\r\n]+/g, ' ').slice(0, 200);
    const file = String(p.file || 'bill').replace(/[^\w.\- ]/g, '-').slice(0, 80);
    if (html.length > 400000) return out({ err: 'Bill is too large to email' });

    const props = PropertiesService.getScriptProperties(), day = new Date().toISOString().slice(0, 10);
    const n = (props.getProperty('day') === day ? +props.getProperty('n') || 0 : 0) + to.length;
    if (n > MAX_PER_DAY) return out({ err: 'Daily email limit reached' });
    if (MailApp.getRemainingDailyQuota() < to.length) return out({ err: 'Google daily email quota reached' });

    const o = { to: to.join(','), subject: subject, htmlBody: html, name: FROM_NAME };
    // Best quality: the PDF made by the app itself (same as the Download PDF button). Fallback: convert the HTML.
    const pdfB64 = typeof p.pdf === 'string' && /^[A-Za-z0-9+\/=]+$/.test(p.pdf) ? p.pdf : '';
    try {
      if (pdfB64 && pdfB64.length < 14000000) o.attachments = [Utilities.newBlob(Utilities.base64Decode(pdfB64), 'application/pdf', file + '.pdf')];
      else o.attachments = [Utilities.newBlob(html, 'text/html', file + '.html').getAs('application/pdf').setName(file + '.pdf')];
    } catch (x) { console.error('attachment failed: ' + x); }
    MailApp.sendEmail(o);
    props.setProperties({ day: day, n: String(n) });   // count only mails that were really sent
    return out({ ok: 1 });
  } catch (x) {
    console.error('doPost failed: ' + x);
    return out({ err: 'Could not send the email. Try again in a moment.' });
  } finally {
    lock.releaseLock();
  }
}
