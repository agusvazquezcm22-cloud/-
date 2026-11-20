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
  for (let y = 0; y < H; y += 1000) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(400); }
  // hide promo banners / sticky bars / % chips
  const hidden = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('body *').forEach(el => {
      const st = getComputedStyle(el); const r = el.getBoundingClientRect(); const t = (el.innerText || '').trim();
      if ((st.position == 'fixed' || st.position == 'sticky') && r.height < 400) { if (/BLACK FRIDAY|ANNIVERSARY|cookie|CLAIM|SALE/i.test(t) || r.top + scrollY < 60 && /BIGGEST/i.test(t)) { out.push('fix:' + t.slice(0, 40)); el.style.setProperty('display', 'none', 'important'); } }
      if (t.length < 80 && el.children.length <= 2 && (/^\d+% (felt|reported)/i.test(t) || /^(EARLY ACCESS|BLACK FRIDAY)/i.test(t))) { out.push('chip:' + t.slice(0, 40)); el.style.setProperty('visibility', 'hidden', 'important'); }
    });
    return out;
  });
  console.log(hidden.join(' | ').slice(0, 900));
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);
  const find = async () => p.evaluate(() => {
    const rx = /(AG1|money-back|Trusted by|Free shipping|Welcome Kit|90-Day Supply|Replaces 16|replaces 16|NSF Certified|David Beckham|Nine organ|Clinically proven|3rd month)/;
    const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { const t = n.textContent.trim(); if (t.length < 130 && rx.test(t)) { const r = n.parentElement.getBoundingClientRect(); if (r.width > 0 && r.height > 0) out.push([Math.round(r.top + scrollY), Math.round(r.left), Math.round(r.width), Math.round(r.height), t.slice(0, 90)]); } }
    return out;
  });
  // open the AG1 FAQ
  const faq = p.getByText('greens powders like AG1').first(); if (await faq.count()) { await faq.scrollIntoViewIfNeeded(); await faq.click().catch(() => {}); await p.waitForTimeout(900); }
  const boxes = await find(); fs.writeFileSync('cap/im8/boxes.json', JSON.stringify(boxes));
  H = await p.evaluate(() => document.documentElement.scrollHeight);
  const ys = [0, 700, 1500, 2650, 3650, 4600, 5400, 6200, 7200, 7950, 8650, 10100, 11100, 11900];
  const faqY = (boxes.find(b => /greens powders like AG1/.test(b[4])) || [12500])[0]; ys.push(Math.max(0, faqY - 500));
  for (const y of ys) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(1200); const yy = await p.evaluate(() => scrollY); await p.screenshot({ path: `cap/im8/y${String(yy).padStart(5, '0')}.png` }); }
  console.log('H', H, 'faqY', faqY, 'boxes', boxes.length);
  await b.close();
})();
