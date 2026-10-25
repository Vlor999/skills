#!/usr/bin/env node
// Lists what a web page contacts and stores on load: hosts requested, cookies, browser storage keys.
// Usage: node site-requests.js <url | directory> [--lang fr] [--wait 3000]
// A directory is served on a local port (static files only). Needs Playwright (npm i -D playwright).
const http = require('http');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const target = args.find(a => !a.startsWith('--'));
const opt = (name, dflt) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : dflt; };
if (!target) { console.error('usage: node site-requests.js <url | directory> [--lang fr] [--wait 3000]'); process.exit(2); }

let chromium;
try { ({ chromium } = require('playwright')); }
catch { console.error('Playwright not found: npm i -D playwright && npx playwright install chromium'); process.exit(2); }

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

function serve(dir) {
  const root = path.resolve(dir);
  const server = http.createServer((req, res) => {
    let p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(root)) { res.writeHead(403); return res.end(); }
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    if (!fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)));
}

(async () => {
  let server, url = target;
  if (!/^https?:\/\//.test(target)) {
    server = await serve(target);
    url = `http://127.0.0.1:${server.address().port}/`;
  }
  const firstParty = new URL(url).host;
  const browser = await chromium.launch();
  const context = await browser.newContext({ locale: opt('lang', 'en-US') });
  const page = await context.newPage();
  const hosts = new Map();
  page.on('request', req => {
    let h; try { h = new URL(req.url()).host; } catch { return; }
    if (!h) return;
    const e = hosts.get(h) || { count: 0, types: new Set(), sample: req.url() };
    e.count++; e.types.add(req.resourceType()); hosts.set(h, e);
  });
  await page.goto(url, { waitUntil: 'networkidle' }).catch(e => console.error('load:', e.message));
  // Scroll and open collapsed sections so lazy content loads too.
  await page.evaluate(async () => {
    document.querySelectorAll('details').forEach(d => { d.open = true; });
    for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
  }).catch(() => {});
  await page.waitForTimeout(Number(opt('wait', 3000)));

  const storage = await page.evaluate(() => ({
    localStorage: Object.keys(localStorage), sessionStorage: Object.keys(sessionStorage),
  })).catch(() => ({ localStorage: [], sessionStorage: [] }));
  const cookies = (await context.cookies()).map(c => ({ name: c.name, domain: c.domain, expires: c.expires }));
  await browser.close();
  if (server) server.close();

  const list = [...hosts].map(([host, e]) => ({ host, thirdParty: host !== firstParty, count: e.count, types: [...e.types], sample: e.sample }));
  console.log(`Page: ${url}`);
  console.log(`First party: ${firstParty}`);
  console.log('\nThird-party hosts:');
  const third = list.filter(h => h.thirdParty);
  if (!third.length) console.log('  none');
  third.forEach(h => console.log(`  ${h.host}  (${h.count} req, ${h.types.join(', ')})  e.g. ${h.sample}`));
  console.log('\nCookies:', cookies.length ? '' : 'none');
  cookies.forEach(c => console.log(`  ${c.name} @ ${c.domain}`));
  console.log('localStorage keys:', storage.localStorage.join(', ') || 'none');
  console.log('sessionStorage keys:', storage.sessionStorage.join(', ') || 'none');
  console.log('\nJSON:', JSON.stringify({ url, firstParty, hosts: list, cookies, storage }));
})();
