// Recorre un test con una lista de acciones y en CADA pantalla guarda: captura (430x764 CSS, 3 px por px), y los rectangulos de todos
// los textos visibles (para armar recuadros sin volver a entrar). Uso: node quiz_cap.js <url> <carpeta> <prefijo> '<json de acciones>'
// accion: "texto parcial" -> clic en el boton/opcion que lo contiene | {"espera": ms} | {"pagina": true} (captura de pagina entera)
//         {"ir": "texto", "dy": 150} -> desliza hasta dejar ese texto a dy px del borde de arriba y captura
//         {"raspar": true} -> arrastra el dedo en zigzag sobre el lienzo mas grande (tarjeta de raspar)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [url, dir, pref, js] = process.argv.slice(2); const acc = JSON.parse(js); const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 430, height: 764 }, deviceScaleFactor: 3, locale: 'es-CO', isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1' });
  // el sitio reparte variantes de portada: se reintenta (contexto nuevo) hasta que aparezca la frase pedida en el 5o argumento
  let p = await c.newPage(); const pide = process.argv[6];
  for (let i = 0; i < 8; i++) { await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(4500);
    if (!pide || (await p.evaluate(() => document.body.innerText)).includes(pide)) break; console.log('   otra variante, reintento'); await c.clearCookies(); await p.evaluate(() => { try { localStorage.clear(); sessionStorage.clear(); } catch (e) {} }); }
  const textos = () => p.evaluate(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue; const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect(); const s = getComputedStyle(n.parentElement);
      if (r.width < 3 || r.height < 3 || s.visibility == 'hidden' || +s.opacity < 0.2) continue; out.push([t.slice(0, 90), Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]); }
    return { url: location.href, alto: document.documentElement.scrollHeight, y: scrollY, t: out }; });
  const meta = []; let k = 0;
  const foto = async (pagina) => { const m = await textos(); const f = `${pref}_${String(k).padStart(2, '0')}.png`; await p.screenshot({ path: `${dir}/${f}`, fullPage: !!pagina }); m.png = f; m.pagina = !!pagina; meta.push(m);
    console.log(`${k} alto ${m.alto} | ${m.t.map(x => x[0]).join(' | ').slice(0, 260)}`); k++; };
  await foto();
  for (const a of acc) {
    if (typeof a == 'string') { const ok = await p.evaluate(q => { const els = [...document.querySelectorAll('button, [role=button], a, label, li')].filter(e => (e.innerText || '').toLowerCase().includes(q.toLowerCase()) && e.getBoundingClientRect().width > 20);
        if (!els.length) return false; els.sort((x, y) => x.innerText.length - y.innerText.length); els[0].scrollIntoView({ block: 'center' }); const r = els[0].getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }, a);
      if (!ok) { console.log('   NO ENCONTRE:', a); continue; } await p.mouse.click(ok[0], ok[1]); await p.waitForTimeout(1700); await foto(); }
    else if (a.ir) { const ok = await p.evaluate(([q, dy]) => { const els = [...document.querySelectorAll('body *')].filter(e => (e.textContent || '').toLowerCase().includes(q.toLowerCase()) && e.getBoundingClientRect().width > 10);
        if (!els.length) return false; els.sort((x, y) => x.textContent.length - y.textContent.length); const el = els[0]; el.scrollIntoView({ block: 'start' });
        let sc = el.parentElement; while (sc && !(sc.scrollHeight > sc.clientHeight + 40 && /auto|scroll/.test(getComputedStyle(sc).overflowY))) sc = sc.parentElement; (sc || document.scrollingElement).scrollBy(0, -dy); return true; }, [a.ir, a.dy || 150]);
      if (!ok) { console.log('   NO ENCONTRE:', a.ir); continue; } await p.waitForTimeout(1200); await foto(); }
    else if (a.espera) { await p.waitForTimeout(a.espera); await foto(); }
    else if (a.pagina) { await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(500); await foto(true); }
    else if (a.raspar) { const r = await p.evaluate(() => { const cs = [...document.querySelectorAll('canvas')].map(e => e.getBoundingClientRect()).filter(r => r.width > 80); cs.sort((x, y) => y.width * y.height - x.width * x.height); if (!cs.length) return null; const q = cs[0]; return [q.left, q.top, q.width, q.height]; });
      console.log('   lienzo', JSON.stringify(r)); if (r) { await p.mouse.move(r[0] + 8, r[1] + 8); await p.mouse.down(); for (let i = 0; i <= 14; i++) { const y = r[1] + 8 + (r[3] - 16) * i / 14; await p.mouse.move(i % 2 ? r[0] + r[2] - 8 : r[0] + 8, y, { steps: 6 }); if (i == 5) { await p.mouse.up(); await foto(); await p.mouse.down(); } } await p.mouse.up(); await p.waitForTimeout(1500); await foto(); } }
  }
  fs.writeFileSync(`${dir}/${pref}_meta.json`, JSON.stringify(meta)); await b.close(); })();
