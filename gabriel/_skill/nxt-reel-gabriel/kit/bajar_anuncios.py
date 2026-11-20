"""Baja los anuncios cosechados con web/biblioteca_cosechar.js y arma hojas de contacto para elegir.
Uso:  python3 bajar_anuncios.py <salida_de_cosechar.txt> <carpeta>
Deja: <carpeta>/<library id>.jpg|.mp4, anuncios.json (texto y enlaces), hoja_jpg.jpg, hoja_mp4.jpg,
      idx_jpg.json / idx_mp4.json (el numero de la hoja -> library id).
Los enlaces vencen en horas: bajar apenas se cosecha. Si un host fbcdn sale rechazado por la red,
pedirlo con update_environment (los nombres cambian: scontent-xxx, video-xxx).
"""
import re, json, subprocess, os, sys, collections
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out + '/th', exist_ok=True)
s = open(src).read(); ads = {}
for m in re.finditer(r'"ad_archive_id":"(\d+)"', s):
    i = m.group(1); seg = s[m.start():m.start() + 30000]; d = ads.setdefault(i, {})
    for k in ['video_hd_url', 'video_sd_url', 'original_image_url']:
        mm = re.search('"%s":"(http[^"]+)"' % k, seg)
        if mm and k not in d: d[k] = mm.group(1).replace('\\/', '/')
    mm = re.search(r'"body":\{"text":"((?:[^"\\]|\\.)*)"', seg)
    if mm and 'body' not in d:
        try: d['body'] = json.loads('"' + mm.group(1) + '"')
        except Exception: d['body'] = mm.group(1)
seen = {}; fallos = collections.Counter(); filas = []
for i, d in ads.items():
    for k, ext in (('original_image_url', 'jpg'), ('video_hd_url', 'mp4')):
        u = d.get(k)
        if not u: continue
        clave = u.split('?')[0].split('/')[-1]
        if clave in seen: continue            # el mismo creativo se repite en muchos anuncios
        dst = f'{out}/{i}.{ext}'
        r = subprocess.run(['curl', '-sS', '-m', '90', '-o', dst, '-w', '%{http_code}', u], capture_output=True, text=True)
        if r.stdout.strip() == '200' and os.path.getsize(dst) > 5000: seen[clave] = dst; d[ext] = dst; filas.append((ext, i))
        else:
            fallos[u.split('/')[2]] += 1
            if os.path.exists(dst): os.remove(dst)
json.dump(ads, open(out + '/anuncios.json', 'w'), ensure_ascii=False, indent=1)
for kind in ('jpg', 'mp4'):
    items = [i for e, i in filas if e == kind]; cols, W, H = 13, 150, 267
    if not items: continue
    hoja = Image.new('RGB', (cols * W, ((len(items) + cols - 1) // cols) * H), 'white')
    for n, i in enumerate(items):
        p = f'{out}/{i}.{kind}'
        if kind == 'mp4':
            t = f'{out}/th/{i}.jpg'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2', '-i', p, '-frames:v', '1', t]); p = t
        try: im = Image.open(p).convert('RGB')
        except Exception: continue
        im.thumbnail((W, H - 17)); hoja.paste(im, ((n % cols) * W, (n // cols) * H + 17))
        ImageDraw.Draw(hoja).text(((n % cols) * W + 3, (n // cols) * H + 3), f'{kind[0]}{n}', fill='red')
    hoja.save(f'{out}/hoja_{kind}.jpg', quality=80); json.dump(items, open(f'{out}/idx_{kind}.json', 'w'))
print('anuncios', len(ads), 'archivos', len(filas), 'hosts rechazados', dict(fallos))
