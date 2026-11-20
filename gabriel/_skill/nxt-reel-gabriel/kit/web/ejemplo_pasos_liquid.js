// Ejemplo (video 35): un armador por pasos. Captura y rectangulos medidos EN EL MISMO momento (si se miden antes, la pagina se corre y los recuadros caen mal), y un clic para abrir el paso oculto. Uso: node ejemplo_pasos_liquid.js <carpeta>
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 820, height: 1458 }, deviceScaleFactor: 3, locale: 'en-US', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage(); await p.goto('https://www.liquid-iv.com/pages/subscriptions', { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(6000);
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < Math.min(H, 9000); y += 900) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(300); }
  await p.evaluate(() => { document.querySelectorAll('body *').forEach(el => { const st = getComputedStyle(el); const r = el.getBoundingClientRect();
    if (st.position == 'fixed' || (st.position == 'sticky' && r.height < 200)) el.style.setProperty('display', 'none', 'important'); }); });
  const medir = () => p.evaluate(() => { const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase().replace(/[?®]/g, ''); const out = {};
    const pats = { titulo: ['build your subscription'], frec: ['how often do you want them delivered'], pildora: ['delivered every month'], benef: ['what benefit are you looking for'], sabor: ['what flavor do you like'],
      b1: ['hydration multiplier', 'see flavors'], b2: ['sugar-free hydration', 'see flavors'], b3: ['sugar-free energy', 'see flavors'], b4: ['hydration +energy', 'see flavors'], b5: ['hydration +immune support', 'see flavors'],
      p1: ['add first pouch', 'sticks'], p2: ['add second pouch', 'sticks'], p3: ['add third pouch', 'sticks'], p4: ['add fourth pouch', 'sticks'], carrito: ['add subscription to cart'],
      s1: ['popsicle firecracker'], s2: ['orange vanilla dream'], s3: ['açai berry'], s4: ['arctic raspberry'], s5: ['cotton candy'], s6: ['lemon lime'], sN: ['watermelon'] };
    for (const [k, v] of Object.entries(pats)) { let best = null;
      document.querySelectorAll('body *').forEach(el => { const t = norm(el.textContent); if (!t.startsWith(v[0]) || (v[1] && !t.includes(v[1])) || t.length > v[0].length + 40) return; const r = el.getBoundingClientRect(); if (r.width < 5 || r.height < 5) return;
        const st = getComputedStyle(el); if (st.visibility == 'hidden' || st.display == 'none' || +st.opacity < 0.1) return;
        const a = r.width * r.height; if (!best || (v[1] ? a > best.a : a < best.a)) best = { a, r: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)] }; });
      out[k] = best && best.r; }
    return out; });
  const m0 = await medir(); const y0 = m0.titulo ? m0.titulo[1] + await p.evaluate(() => scrollY) - 40 : 1900;
  await p.evaluate(y => window.scrollTo(0, y), y0); await p.waitForTimeout(1200);
  const m1 = await medir(); await p.screenshot({ path: (process.argv[2] || 'cap') + '/liqb_0.png' }); console.log('A', JSON.stringify(m1));
  // abrir el paso de sabores: clic en el primer beneficio
  let m2 = null;
  if (m1.b1) { await p.mouse.click(m1.b1[0] + 60, m1.b1[1] + m1.b1[3] / 2); await p.waitForTimeout(1800); m2 = await medir();
    if (m2.sabor) { const dy = m2.sabor[1] - 90; await p.evaluate(dy => window.scrollBy(0, dy), dy); await p.waitForTimeout(900); m2 = await medir(); }
    await p.screenshot({ path: (process.argv[2] || 'cap') + '/liqb_1.png' }); console.log('B', JSON.stringify(m2)); }
  fs.writeFileSync((process.argv[2] || 'cap') + '/liqbmeta.json', JSON.stringify({ a: m1, b: m2 }));
  await b.close(); })();
