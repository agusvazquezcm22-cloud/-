// Para MIRAR un reel publico de Instagram que Agus pasa como referencia (vista embed, sin iniciar sesion).
// Uso: node reel_referencia.js https://www.instagram.com/reel/<id> <carpeta>
// Sale: embed.png (primer cuadro) y vids.json con la direccion del video; se baja con curl y se saca una hoja de cuadros:
//   curl -sL -o ref.mp4 "<url de vids.json>" ; ffmpeg -i ref.mp4 -vf "fps=32/<duracion>,scale=270:480,tile=8x4" -frames:v 1 hoja.jpg
// El entorno tiene que permitir www.instagram.com, static.cdninstagram.com y scontent-*.cdninstagram.com (el script lista los que fallan).
// Es solo para estudiar el encuadre y el ritmo: ese video no se usa en ninguna edicion.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [url, dir] = process.argv.slice(2); const b = await chromium.launch();
  const c = await b.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, locale: 'es-AR', userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' });
  const p = await c.newPage(); const vids = new Set(); const bloq = new Set();
  p.on('response', r => { const u = r.url(); if (/\.mp4/.test(u) && r.status() < 400) vids.add(u); });
  p.on('requestfailed', r => { try { bloq.add(new URL(r.url()).host); } catch (e) {} });
  await p.goto(url.replace(/\/?$/, '/') + 'embed/', { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto', e.message.slice(0, 80)));
  await p.waitForTimeout(5000); await p.screenshot({ path: `${dir}/embed.png` });
  const html = await p.content(); const m = [...html.matchAll(/https:[^"'\s]+?\.mp4[^"'\s]*/g)].map(x => x[0].replace(/\\u0026/g, '&').replace(/\\\//g, '/').replace(/&amp;/g, '&'));
  m.forEach(u => vids.add(u));
  const info = await p.evaluate(() => ({ videos: [...document.querySelectorAll('video')].map(v => [v.currentSrc.slice(0, 90), v.videoWidth, v.videoHeight, v.duration]), imgs: [...document.querySelectorAll('img')].map(i => [i.src.slice(0, 90), i.naturalWidth, i.naturalHeight]).filter(i => i[1] > 300).slice(0, 5) }));
  console.log(JSON.stringify(info));
  fs.writeFileSync(`${dir}/vids.json`, JSON.stringify([...vids])); console.log('videos', vids.size, 'hosts que fallaron', [...bloq].join(' '));
  await b.close(); })();
