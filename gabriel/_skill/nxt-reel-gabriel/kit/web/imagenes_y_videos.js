// Lista las imagenes grandes (>= 500 px) y los videos que carga una pagina: sirve para encontrar material oficial de la marca en su sitio.
// Uso: node imagenes_y_videos.js <url>   (los videos de cdn.shopify.com se bajan con curl)
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1440, height: 1200 } })).newPage(); const vids = new Set();
  p.on('response', r => { if (/\.mp4|\.m3u8|\.webm/.test(r.url())) vids.add(r.url().slice(0, 220)); });
  await p.goto(process.argv[2], { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(5000);
  const H = await p.evaluate(() => document.documentElement.scrollHeight); for (let y = 0; y < Math.min(H, 16000); y += 1000) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(350); }
  const r = await p.evaluate(() => ({ im: [...document.querySelectorAll('img')].map(i => [i.currentSrc || i.src, i.naturalWidth, i.naturalHeight, (i.alt || '').slice(0, 50)]).filter(i => i[1] >= 500), v: [...document.querySelectorAll('video, video source')].map(v => (v.currentSrc || v.src || '').slice(0, 220)).filter(Boolean) }));
  console.log(r.im.map(i => i.join(' | ').slice(0, 230)).join('\n')); console.log('VIDEOS', [...new Set([...r.v, ...vids])].join('\n')); await b.close(); })();
