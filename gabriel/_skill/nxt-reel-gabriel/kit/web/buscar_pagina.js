// Uso: node buscar_pagina.js "<marca + producto>"  -> lista id y nombre de las paginas anunciantes que aparecen (el id va a biblioteca_cosechar.js y biblioteca_capturas.js).
const { chromium } = require('playwright');
(async () => { const q = process.argv[2]; const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1440, height: 2000 }, locale: 'en-US' })).newPage(); let todo = '';
  p.on('response', async r => { try { const ct = r.headers()['content-type'] || ''; if (/json|javascript|html|text/.test(ct)) todo += await r.text(); } catch (e) {} });
  await p.goto(`https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=${encodeURIComponent(q)}&search_type=keyword_unordered&media_type=all`, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(8000); for (let i = 0; i < 3; i++) { await p.mouse.wheel(0, 3000); await p.waitForTimeout(1500); }
  todo += await p.content(); const c = {};
  for (const m of todo.matchAll(/"page_id":"?(\d{6,})"?/g)) c[m[1]] = (c[m[1]] || 0) + 1;
  const top = Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 8);
  for (const [id, n] of top) { const i = todo.indexOf(`"page_id":"${id}"`); const ctx = todo.slice(Math.max(0, i - 600), i + 600); const nm = (ctx.match(/"page_name":"([^"]+)"/) || [])[1]; console.log(id, 'x' + n, nm || '?'); }
  console.log('texto:', (await p.evaluate(() => document.body.innerText)).replace(/\s+/g, ' ').slice(0, 200)); await b.close(); })();
