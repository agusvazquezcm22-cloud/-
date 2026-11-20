// Capturas de la Biblioteca de Anuncios: grilla (fbg0..3.png, 2 px por px CSS), tarjetas de anuncios puntuales
// (card_<id>.png) y fbmeta.json con: donde esta el contador de resultados, la frase a subrayar y el boton de cada tarjeta.
// Uso:  node biblioteca_capturas.js <id_de_pagina> <carpeta> '{"<library id>":"frase exacta del texto del anuncio"}'
// Ojo: la barra de busqueda es fija y se repite arriba de fbg1..3; usar vistas que no pasen de una captura a otra.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 1440, height: 2400 }, deviceScaleFactor: 2, locale: 'en-US',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  await p.goto('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id=' + process.argv[2] + '&search_type=page&media_type=all', { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(7000);
  const ok = p.getByRole('button', { name: 'OK' }).first(); if (await ok.count()) await ok.click().catch(() => {});
  await p.waitForTimeout(800);
  for (let i = 0; i < 5; i++) { await p.mouse.wheel(0, 2200); await p.waitForTimeout(2200); }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(2500);
  const meta = { cards: {} };
  meta.results = await p.evaluate(() => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) if (/results$/.test(n.textContent.trim())) { const r = n.parentElement.getBoundingClientRect(); return [r.left, r.top + scrollY, r.width, r.height, n.textContent.trim()]; } });
  // tall grid: 3 viewport shots
  for (let k = 0; k < 4; k++) { await p.evaluate(y => window.scrollTo(0, y), k * 2400); await p.waitForTimeout(2500); await p.screenshot({ path: `${process.argv[3]}/fbg${k}.png` }); }
  const want = JSON.parse(process.argv[4] || '{}');
  for (const [id, phrase] of Object.entries(want)) {
    const r = await p.evaluate(async ([id, phrase]) => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, card = null;
      while (n = w.nextNode()) if (n.textContent.includes(id)) { card = n.parentElement; break; }
      if (!card) return null;
      for (let k = 0; k < 12 && card.parentElement; k++) { const rr = card.getBoundingClientRect(); if (rr.width > 380 && rr.height > 300) break; card = card.parentElement; }
      card.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 1500));
      card.setAttribute('data-pick', id);
      const cr = card.getBoundingClientRect(); const out = { w: cr.width, h: cr.height, phr: [], cta: null };
      const w2 = document.createTreeWalker(card, NodeFilter.SHOW_TEXT);
      while (n = w2.nextNode()) { const i = n.textContent.indexOf(phrase); if (i >= 0) { const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + phrase.length); for (const q of rg.getClientRects()) out.phr.push([q.left - cr.left, q.top - cr.top, q.width, q.height]); }
        if (/^(Shop now|Shop Now|Learn more|Get offer)$/i.test(n.textContent.trim())) { const q = n.parentElement.getBoundingClientRect(); out.cta = [q.left - cr.left, q.top - cr.top, q.width, q.height]; } }
      return out;
    }, [id, phrase]);
    if (!r) { console.log('no card', id); continue; }
    await p.locator(`[data-pick="${id}"]`).screenshot({ path: `${process.argv[3]}/card_${id}.png` });
    meta.cards[id] = r; console.log(id, Math.round(r.w), Math.round(r.h), r.phr.length, !!r.cta);
  }
  fs.writeFileSync(process.argv[3] + '/fbmeta.json', JSON.stringify(meta)); console.log(JSON.stringify(meta.results));
  await b.close();
})();
