// Captura una pagina entera por tramos (820 px CSS de ancho, 2 px por px CSS) para armar desplazamientos.
// Uso: node pagina_larga.js <url> <carpeta> <prefijo> [max_tramos]
// Sale: <prefijo>_00.png, _01.png ... (cada uno 1640x2916, solapados) y <prefijo>_larga.json {alto, tramos, titulos:[y, texto], corte, paso}.
// Oculta lo fijo (barras, avisos) y el encabezado pegajoso; la columna de compra, que tambien es "sticky", se deja.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [url, dir, pref, max] = process.argv.slice(2); const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 820, height: 1458 }, deviceScaleFactor: 2, locale: 'es-MX', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage(); await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(6000);
  let H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 900) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(300); }
  await p.evaluate(() => { window.scrollTo(0, 600); document.querySelectorAll('body *').forEach(el => { const st = getComputedStyle(el); const r = el.getBoundingClientRect();
    // fuera: lo fijo y el encabezado pegajoso (bajo, arriba de todo), que si no se repite en cada tramo. La columna de compra (alta) se queda.
    if (st.position == 'fixed' || (st.position == 'sticky' && r.height < 160 && r.top < 20)) el.style.setProperty('display', 'none', 'important'); }); window.scrollTo(0, 0); });
  H = await p.evaluate(() => document.documentElement.scrollHeight);
  const titulos = await p.evaluate(() => [...document.querySelectorAll('h1,h2,h3')].map(h => [Math.round(h.getBoundingClientRect().top + scrollY), h.innerText.trim().replace(/\s+/g, ' ').slice(0, 70)]).filter(t => t[1]));
  // Si el encabezado queda pegado arriba en cada tramo, los tramos se solapan `corte` px CSS y al unirlos se descarta
  // esa franja de arriba en todos menos el primero:  tira = tramo0 + tramo_k[corte*2:]  (ver _larga.json).
  const corte = 110, paso = 1458 - corte;
  const n = Math.min(Math.ceil((H - corte) / paso), +(max || 12));
  for (let k = 0; k < n; k++) { await p.evaluate(y => window.scrollTo(0, y), k * paso); await p.waitForTimeout(700); await p.screenshot({ path: `${dir}/${pref}_${String(k).padStart(2, '0')}.png` }); }
  fs.writeFileSync(`${dir}/${pref}_larga.json`, JSON.stringify({ alto: H, tramos: n, titulos, corte, paso })); console.log('alto', H, 'tramos', n); console.log(titulos.map(t => t.join(' ')).join('\n').slice(0, 1500));
  await b.close(); })();
