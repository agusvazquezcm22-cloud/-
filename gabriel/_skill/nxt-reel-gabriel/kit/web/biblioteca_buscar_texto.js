// Recorre la Biblioteca de Anuncios de Meta de una pagina y guarda las respuestas que traen los anuncios
// (texto, imagen original y video HD). Despues: python3 ../bajar_anuncios.py <salida.txt> <carpeta>
// VARIANTE: busca por texto en TODA la Biblioteca (cualquier anunciante), solo videos.
// Uso:  node biblioteca_buscar_texto.js x <salida.txt> "frase 1,frase 2"
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 1440, height: 1800 }, locale: 'en-US',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage();
  const bodies = [];
  p.on('response', async r => { const u = r.url(); if (!/facebook\.com/.test(u)) return; const t = r.request().resourceType(); if (t != 'document' && t != 'xhr' && t != 'fetch') return; try { const s = await r.text(); if (/ad_archive_id/.test(s)) bodies.push(s); } catch (e) {} });
  const base = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&media_type=video';
  for (const q of (process.argv[4] || '').split(',').filter(Boolean)) {
    const url = q ? base + '&search_type=keyword_unordered&q=' + encodeURIComponent(q) : base + '&search_type=page';
    await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('ERR', e.message.slice(0, 100)));
    await p.waitForTimeout(6000);
    for (let i = 0; i < (q ? 4 : 12); i++) { await p.mouse.wheel(0, 2500); await p.waitForTimeout(1500); }
    console.log(q || 'all', bodies.length);
  }
  fs.writeFileSync(process.argv[3], bodies.join('\n#####\n'));
  await b.close();
})();
