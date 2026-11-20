// Captura una pagina web con una frase a la vista y devuelve donde quedo la frase (para el recuadro rojo).
// Uso:  node frase.js <url> <carpeta_salida> <prefijo> '{"cac":"$285","x41":"approximately 4.1x"}'
// Sale: <carpeta>/<prefijo>_<clave>.png (2460x4374, 9:16, 3 px por px CSS) y <carpeta>/<prefijo>meta.json
//       con los rectangulos de cada frase en px CSS de la captura.
// Solo acepta una coincidencia que este realmente visible: las paginas repiten texto en bloques ocultos
// y, si se mide ahi, el recuadro cae sobre otra frase (paso en el video 32).
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [url, dir, pref, json] = process.argv.slice(2);
  const want = JSON.parse(json);
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 820, height: 1458 }, deviceScaleFactor: 3, locale: 'en-US',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(6000);
  await p.evaluate(() => document.querySelectorAll('body *').forEach(el => { const s = getComputedStyle(el); if (s.position == 'fixed' || s.position == 'sticky') el.style.setProperty('display', 'none', 'important'); }));
  await p.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
  const mf = `${dir}/${pref}meta.json`;
  const meta = fs.existsSync(mf) ? JSON.parse(fs.readFileSync(mf)) : {};
  for (const [k, phrase] of Object.entries(want)) {
    const r = await p.evaluate(async (phrase) => {
      const norm = s => s.replace(/[ \s]+/g, ' ');
      const cands = [];
      document.querySelectorAll('p,h1,h2,h3,li,td,div,span,em,i,b,strong,a').forEach(el => { if (el.getBoundingClientRect().width < 5) return; if (norm(el.textContent).includes(phrase)) cands.push(el); });
      cands.sort((a, b) => a.textContent.length - b.textContent.length);
      for (const best of cands) {
        if (!best.offsetParent) continue;
        const nodes = []; const w = document.createTreeWalker(best, NodeFilter.SHOW_TEXT); let n, full = '';
        while (n = w.nextNode()) { const t = n.textContent.replace(/ /g, ' '); nodes.push([n, full.length, t.length]); full += t; }
        const i = full.indexOf(phrase); if (i < 0) continue;
        const loc = pos => { for (const [nd, st, ln] of nodes) if (pos >= st && pos <= st + ln) return [nd, pos - st]; };
        const rg = document.createRange(); const a = loc(i), z = loc(i + phrase.length); rg.setStart(a[0], a[1]); rg.setEnd(z[0], z[1]);
        let r0 = rg.getBoundingClientRect(); if (r0.height < 5) continue;
        window.scrollTo(0, r0.top + scrollY - 520); await new Promise(r => setTimeout(r, 900));
        r0 = rg.getBoundingClientRect();
        if (r0.top < 0 || r0.top > innerHeight) continue;
        return [...rg.getClientRects()].map(q => [q.left, q.top, q.width, q.height]);
      }
      return null;
    }, phrase);
    if (!r) { console.log('NO ENCONTRADA (visible):', k, phrase); continue; }
    await p.screenshot({ path: `${dir}/${pref}_${k}.png` }); meta[k] = r;
    console.log(k, JSON.stringify(r.map(q => q.map(Math.round))));
  }
  fs.writeFileSync(mf, JSON.stringify(meta));
  await b.close();
})();
