// Capturas de la Biblioteca de Anuncios de Meta (2 px por px CSS).
// Uso:  node biblioteca_capturas.js <id_de_pagina> <carpeta> '<json>' [filtro] [prefijo]
//   json:    {"<library id>": "frase exacta a subrayar"}  -> tarjeta de ese anuncio
//            {"<library id>": ["frase 1", "frase 2", ...]}  -> idem, y en fbmeta.json cards[id].frases[frase] = rectangulos EXACTOS
//            (usar SIEMPRE esto para cada recuadro o subrayado: nunca calcular la posicion de una frase a ojo)
//            {"*": "frase", "max": 8}                     -> las primeras tarjetas que traen esa frase
//   filtro:  parte final de la URL. Por defecto "&search_type=page&media_type=all".
//            Solo videos: "&search_type=page&media_type=video".  Por texto: "&search_type=keyword_unordered&media_type=all&q=Sold%20out"
//   prefijo: para no pisar capturas de otra corrida (por defecto "").
// Sale: <prefijo>fbg0..3.png (grilla), <prefijo>card_<id>.png y <prefijo>fbmeta.json con: contador de resultados, fechas de inicio,
//       y por tarjeta la frase, el boton y el encabezado ("Fulano with Marca").
// Ojo: la barra de busqueda es fija y se repite arriba de fbg1..3, y la grilla puede terminar antes de fbg3.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [pid, dir, json, filtro, pref0] = process.argv.slice(2);
  const want = JSON.parse(json || '{}'); const pref = pref0 || '';
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 1440, height: 2400 }, deviceScaleFactor: 2, locale: 'en-US',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  await p.goto('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id=' + pid + (filtro || '&search_type=page&media_type=all'), { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(7000);
  // La Biblioteca a veces responde "No ads match" aunque haya anuncios: reintentar antes de darlo por vacio.
  for (let k = 0; k < 3; k++) {
    const vacio = await p.evaluate(() => /No ads match/.test(document.body.innerText));
    if (!vacio) break;
    console.log('respuesta vacia, reintento', k + 1); await p.waitForTimeout(15000); await p.reload({ waitUntil: 'domcontentloaded' }).catch(() => {}); await p.waitForTimeout(8000);
  }
  const ok = p.getByRole('button', { name: 'OK' }).first(); if (await ok.count()) await ok.click().catch(() => {});
  await p.waitForTimeout(800);
  for (let i = 0; i < 5; i++) { await p.mouse.wheel(0, 2200); await p.waitForTimeout(2200); }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(2500);
  const meta = { cards: {} };
  meta.results = await p.evaluate(() => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) if (/results?$/.test(n.textContent.trim())) { const r = n.parentElement.getBoundingClientRect(); return [r.left, r.top + scrollY, r.width, r.height, n.textContent.trim()]; } });
  meta.alto = await p.evaluate(() => document.documentElement.scrollHeight);
  // fechas de inicio de cada anuncio (para subrayarlas en la grilla): [x, y de pagina, ancho, alto, texto]
  meta.fechas = await p.evaluate(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) if (/^Started running on/.test(n.textContent.trim())) { const r = n.parentElement.getBoundingClientRect(); if (r.width > 5) out.push([r.left, r.top + scrollY, r.width, r.height, n.textContent.trim()]); } return out; });
  for (let k = 0; k < 4; k++) { await p.evaluate(y => window.scrollTo(0, y), k * 2400); await p.waitForTimeout(2500); await p.screenshot({ path: `${dir}/${pref}fbg${k}.png` }); }
  let lista = Object.entries(want).filter(([k]) => k != '*' && k != 'max');
  if (want['*']) {
    const ids = await p.evaluate((frase) => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while (n = w.nextNode()) { const m = n.textContent.match(/Library ID: (\d+)/); if (!m) continue; let card = n.parentElement;
        for (let k = 0; k < 12 && card.parentElement; k++) { const rr = card.getBoundingClientRect(); if (rr.width > 380 && rr.height > 300) break; card = card.parentElement; }
        if ((card.innerText || '').includes(frase) && !out.includes(m[1])) out.push(m[1]); }
      return out; }, want['*']);
    lista = lista.concat(ids.slice(0, want.max || 8).map(i => [i, want['*']]));
  }
  for (const [id, phrase] of lista) {
    const r = await p.evaluate(async ([id, phrase]) => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, card = null;
      while (n = w.nextNode()) if (n.textContent.includes(id)) { card = n.parentElement; break; }
      if (!card) return null;
      for (let k = 0; k < 12 && card.parentElement; k++) { const rr = card.getBoundingClientRect(); if (rr.width > 380 && rr.height > 300) break; card = card.parentElement; }
      card.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 1500));
      card.setAttribute('data-pick', id);
      const cr = card.getBoundingClientRect(); const out = { w: cr.width, h: cr.height, phr: [], frases: {}, cta: null, quien: null, nombre: '' };
      const lista = Array.isArray(phrase) ? phrase : [phrase]; phrase = lista[0];
      const rel = q => [q.left - cr.left, q.top - cr.top, q.width, q.height];
      const w2 = document.createTreeWalker(card, NodeFilter.SHOW_TEXT);
      while (n = w2.nextNode()) { const t = n.textContent; const i = t.indexOf(phrase);
        if (i >= 0 && !out.phr.length) { const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + phrase.length); for (const q of rg.getClientRects()) out.phr.push(rel(q)); }
        for (const f of lista) { const j = t.indexOf(f); if (j < 0 || out.frases[f]) continue;                 // cada frase pedida, con su rectangulo exacto
          const rg = document.createRange(); rg.setStart(n, j); rg.setEnd(n, j + f.length); out.frases[f] = [...rg.getClientRects()].filter(q => q.width > 1).map(rel); }
        if (/^(Shop now|Shop Now|Learn more|Learn More|Get offer|Sign up|Order now)$/i.test(t.trim())) out.cta = rel(n.parentElement.getBoundingClientRect());
        if (t.trim() == 'Sponsored' && !out.quien) { let h = n.parentElement; for (let k = 0; k < 4 && h.parentElement; k++) { h = h.parentElement; if ((h.innerText || '').trim().split('\n').length >= 2) break; }
          out.quien = rel(h.getBoundingClientRect()); out.nombre = (h.innerText || '').split('\n')[0].trim(); } }
      return out;
    }, [id, phrase]);
    if (!r) { console.log('sin tarjeta', id); continue; }
    await p.locator(`[data-pick="${id}"]`).screenshot({ path: `${dir}/${pref}card_${id}.png` });
    meta.cards[id] = r; console.log(id, Math.round(r.w), Math.round(r.h), 'frase', r.phr.length, 'boton', !!r.cta, '|', r.nombre);
  }
  fs.writeFileSync(`${dir}/${pref}fbmeta.json`, JSON.stringify(meta)); console.log(JSON.stringify(meta.results), 'alto', meta.alto);
  await b.close();
})();
