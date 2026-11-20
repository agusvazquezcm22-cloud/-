const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 1280, height: 1600 }, deviceScaleFactor: 3, locale: 'en-US',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  await p.goto('https://im8health.com/products/essentials-pro', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(5000);
  const dec = p.getByRole('button', { name: /decline/i }).first(); if (await dec.count()) await dec.click().catch(() => {});
  let H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 1000) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(350); }
  await p.evaluate(() => {
    document.querySelectorAll('body *').forEach(el => {
      const st = getComputedStyle(el); const r = el.getBoundingClientRect(); const t = (el.innerText || '').trim();
      if ((st.position == 'fixed' || st.position == 'sticky') && r.height < 400) { if (/BLACK FRIDAY|ANNIVERSARY|cookie|CLAIM|SALE/i.test(t) || /BIGGEST/i.test(t)) el.style.setProperty('display', 'none', 'important'); }
    });
  });
  // sacar la pregunta de Black Friday de la lista de FAQs
  const quitado = await p.evaluate(() => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, k = 0;
    while (n = w.nextNode()) if (/Is Black Friday the best time/i.test(n.textContent)) { let el = n.parentElement; for (let i = 0; i < 6 && el.parentElement; i++) { if (el.parentElement.children.length >= 6) break; el = el.parentElement; } el.style.setProperty('display', 'none', 'important'); k++; }
    return k; });
  const rects = async (frases) => p.evaluate((frases) => { const out = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) for (const f of frases) { const i = n.textContent.indexOf(f); if (i >= 0 && !out[f]) { const pr = n.parentElement.getBoundingClientRect(); if (pr.width < 5 || pr.height < 5 || pr.top < 0 || pr.top > innerHeight) continue; const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + f.length); out[f] = [...rg.getClientRects()].map(q => [q.left, q.top, q.width, q.height]); } }
    return out; }, frases);
  const meta = { quitado };
  const abrir = async (txt, nombre, frases) => {
    const q = p.getByText(txt).first(); await q.scrollIntoViewIfNeeded(); await q.click().catch(() => {}); await p.waitForTimeout(1000);
    const y = await q.evaluate(el => el.getBoundingClientRect().top + scrollY);
    await p.evaluate(y => window.scrollTo(0, y - 500), y); await p.waitForTimeout(900);
    meta[nombre] = await rects(frases); meta[nombre + '_ans'] = await p.evaluate((t) => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) if (n.textContent.includes(t)) { let el = n.parentElement; for (let i = 0; i < 4; i++) el = el.parentElement; return el.innerText.slice(0, 600); } }, txt.slice(0, 25));
    await p.screenshot({ path: `cap/im8/faq_${nombre}.png` });
    await q.click().catch(() => {}); await p.waitForTimeout(700);
  };
  await abrir('greens powders like AG1', 'ag1', ['What’s the difference between IM8 Essentials Pro and greens powders like AG1?', 'greens powders like']);
  await abrir('What if IM8 doesn', 'gar', ['backed by our 90-day money-back guarantee', 'What if IM8 doesn’t work for me?', '90-day', '90 days', 'money-back', 'refund']);
  fs.writeFileSync('cap/im8/faqmeta.json', JSON.stringify(meta)); console.log(JSON.stringify(meta).slice(0, 1800));
  await b.close();
})();
