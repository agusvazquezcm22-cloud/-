// Pagina de producto de una tienda (video 34, The Everyday Lab): precios, paquetes y caja de suscripcion.
// Uso: node ejemplo_producto_tel.js <url> <carpeta> [regex de los textos a ubicar]
// Sale: prod_top.png y prod_compra.png (820x1458 px CSS, 3 px por px CSS) y prodhits.json con los rectangulos
// [x, y, ancho, alto, texto] en px CSS de cada texto que coincide (para armar los recuadros rojos).
// OJO: la columna de compra es `position: sticky`. Aca se oculta SOLO lo `fixed` (barras y avisos): si se oculta
// tambien lo pegajoso, la columna desaparece de la captura.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [url, dir, patron] = process.argv.slice(2); const re = new RegExp(patron || '\\$\\d|% OFF|frasco|SUSCR|AGREGAR', 'i');
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 820, height: 1458 }, deviceScaleFactor: 3, locale: 'es-MX', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(6000);
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < Math.min(H, 9000); y += 900) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(350); }   // que carguen las imagenes
  await p.evaluate(() => { document.querySelectorAll('body *').forEach(el => { if (getComputedStyle(el).position == 'fixed') el.style.setProperty('display', 'none', 'important'); }); window.scrollTo(0, 0); });
  await p.waitForTimeout(1200);
  const hits = await p.evaluate(src => { const re = new RegExp(src, 'i'); const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { const t = n.textContent.trim(); if (!re.test(t) || t.length > 60) continue; const r = n.parentElement.getBoundingClientRect(); if (r.width < 3 || r.height < 3) continue;
      out.push([Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height), t]); }
    return out; }, re.source);
  console.log('alto', H); console.log(hits.map(h => h.join(' ')).join('\n').slice(0, 2500));
  const yPrecio = (hits.find(h => /^\$\d/.test(h[4])) || [0, 600])[1];
  for (const [n, y] of [['top', 0], ['compra', Math.max(0, yPrecio - 520)]]) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(900); await p.screenshot({ path: `${dir}/prod_${n}.png` }); }
  fs.writeFileSync(`${dir}/prodhits.json`, JSON.stringify({ hits, y_compra: Math.max(0, yPrecio - 520) }));
  await b.close(); })();
