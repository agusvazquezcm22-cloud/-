// Pagina entera en UNA captura (fullPage, 820 px CSS de ancho, 2 px por px CSS) + rectangulos de cada texto visible.
// Uso: node pagina_entera.js <url> <salida.png> [regex de lo que NO se puede ver] [alto maximo en px CSS]
// - Oculta lo fijo (barras, avisos, popups) y el encabezado pegajoso.
// - Con el regex, oculta la tarjeta (el contenedor mas chico, de menos de 520 px de ancho) que contiene ese texto: asi se saca un
//   producto prohibido de una grilla (en Mumu, "Desinflama"). Tambien borra el texto suelto que coincide fuera de tarjetas.
// Variables: FRASES (ver abajo) y OCULTAR_IMG="y0-y1" (oculta imagenes en esa banda de px CSS).
// Sale <salida.png> y <salida>.json: {alto, textos: [[texto, x, y, w, h], ...]} en px CSS.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [url, out, prohibido, maxAlto] = process.argv.slice(2); const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 820, height: 1458 }, deviceScaleFactor: 2, locale: 'es-CO', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage(); await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(6000);
  let H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < Math.min(H, +(maxAlto || 14000)); y += 700) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(250); }
  await p.evaluate(([re]) => { window.scrollTo(0, 0);
    document.querySelectorAll('body *').forEach(el => { const st = getComputedStyle(el); const r = el.getBoundingClientRect();
      if (st.position == 'fixed' || (st.position == 'sticky' && r.height < 220)) el.style.setProperty('display', 'none', 'important'); });
    if (re) { const R = new RegExp(re, 'i');
      [...document.querySelectorAll('body *')].filter(e => R.test(e.innerText || '') && e.getBoundingClientRect().width > 40)
        .sort((a, b) => a.getBoundingClientRect().width * a.getBoundingClientRect().height - b.getBoundingClientRect().width * b.getBoundingClientRect().height)
        .forEach(e => { let x = e; while (x.parentElement && x.parentElement.getBoundingClientRect().width < 520 && x.parentElement.getBoundingClientRect().height < 1100) x = x.parentElement;
          if (x.getBoundingClientRect().width < 520) x.style.setProperty('display', 'none', 'important'); }); } }, [prohibido || '']);
  if (process.env.OCULTAR_IMG) { const [y0, y1] = process.env.OCULTAR_IMG.split('-').map(Number);       // banda (px CSS) donde se ocultan las imagenes (ej. un antes y despues)
    await p.evaluate(([y0, y1]) => document.querySelectorAll('img, picture, video').forEach(i => { const r = i.getBoundingClientRect(); const y = r.top + scrollY;
      if (y + r.height > y0 && y < y1) i.style.setProperty('visibility', 'hidden', 'important'); }), [y0, y1]); }
  await p.waitForTimeout(1500); H = Math.min(await p.evaluate(() => document.documentElement.scrollHeight), +(maxAlto || 14000));
  const textos = await p.evaluate(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue; const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect(); const s = getComputedStyle(n.parentElement);
      if (r.width < 3 || r.height < 3 || s.visibility == 'hidden' || +s.opacity < 0.2) continue; out.push([t.slice(0, 100), Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]); }
    return out; });
  const frases = {};                                                                                    // FRASES='["frase 1","frase 2"]': rectangulo de cada frase (puede ser parte de un texto)
  for (const f of JSON.parse(process.env.FRASES || '[]')) frases[f] = await p.evaluate(f => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { const i = n.textContent.indexOf(f); if (i < 0) continue; const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + f.length);
      const rs = [...rg.getClientRects()].filter(r => r.width > 2); if (!rs.length) continue; return rs.map(r => [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]); }
    return null; }, f);
  await p.screenshot({ path: out, fullPage: true, clip: { x: 0, y: 0, width: 820, height: H } });
  fs.writeFileSync(out.replace(/\.png$/, '.json'), JSON.stringify({ alto: H, textos, frases })); console.log('alto', H, 'textos', textos.length); await b.close(); })();
