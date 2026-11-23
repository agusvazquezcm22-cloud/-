"""Revisa TODAS las marcas rojas (recuadro, subrayado, flecha) de un config antes de renderizar.

Pedido de Agus (2026-11-23): "cuando marcas algo en rojo, que sea lo que dice, porque hay veces que marcas las cosas erroneas…
que no vuelva a pasar". Para cada marca saca el cuadro compuesto (con subtitulo, titulo y Gabriel) en el momento en que aparece,
recorta la zona de la marca y escribe debajo lo que dice el subtitulo en ese segundo. Ademas avisa solo si la marca:
  - queda FUERA de la pantalla (cortada por un borde),
  - queda TAPADA por el titulo de arriba, por la franja de subtitulos o por Gabriel.

Uso:  python3 revisar_marcas.py <config.py> <hoja.jpg>
Mirar la hoja ENTERA y leer, en cada recorte, que la marca este sobre las palabras exactas que dice el subtitulo. Si una marca
se ubico a ojo (sin medir el texto en la pagina), rehacerla con el rectangulo medido (frase.js, pagina_entera.js FRASES=…,
biblioteca_capturas.js con lista de frases).
"""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, __import__('os').path.dirname(__file__))
import render_verde as rv
sys.modules.setdefault('render_verde', rv)


def _texto_en(subs, t):
    for c in subs or []:
        if c['t0'] <= t < c['t1']:
            return ((c.get('simples') or '') + ' ' + (c.get('clave') or '')).strip()
    return ''


def main():
    cfg = rv.cargar(sys.argv[1]); out = sys.argv[2]
    for k in ('CABEZA', 'Y0', 'CENTRO'):
        if hasattr(cfg, k): setattr(rv, k, getattr(cfg, k))
    items = []
    for sh in cfg.SHOTS:
        T = sh['t1'] - sh['t0']; src = sh['fondo']
        partes = src.partes if isinstance(src, rv.Serie) else [(0.0, src)]
        for n, (p0, f) in enumerate(partes):
            p1 = partes[n + 1][0] if n + 1 < len(partes) else T
            for m in getattr(f, 'marcas', None) or []:
                tipo, rect, t0 = m[0], m[1], m[2]
                t1 = m[3] if len(m) > 3 and m[3] is not None else (p1 - p0)
                tl = min(t0 + 0.35, (t0 + t1) / 2, p1 - p0 - 0.04)
                if tl < 0: continue
                items.append((sh, p0, f, p1 - p0, tipo, rect, tl))
    tiles, avisos = [], []
    for sh, p0, f, PT, tipo, rect, tl in items:
        tg = sh['t0'] + p0 + tl
        _, tr = f.frame(tl, PT)
        x, y, w, h = f.a_pantalla(rect, tr)
        raw = subprocess.run(rv.leer_crudo(cfg.RAW, tg, 1), capture_output=True).stdout
        crudo = np.frombuffer(raw, np.uint8).reshape(rv.H, rv.W, 3)
        fr = rv.componer(cfg, sh, tg, crudo, seq=False)
        dice = _texto_en(getattr(cfg, 'SUBS', None), tg)
        prob = []
        if x < -2 or y < -2 or x + w > rv.W + 2 or y + h > rv.H + 2: prob.append('FUERA DE PANTALLA')
        cx, cy = x + w / 2, y + h / 2
        tt = getattr(sh.get('texto'), 'caja_titulo', None)                                   # T_ guarda donde dibujo su caja
        if tt and not (y + h < tt[1] or y > tt[3] or x + w < tt[0] or x > tt[2]): prob.append('BAJO EL TITULO')
        if y + h > 735 and y < 1060: prob.append('EN LA FRANJA DE SUBTITULOS')
        gx = {'CI': 290, 'CD': 790}.get(sh.get('gab'), 540)                                # centro de la cabeza segun el lugar de Gabriel
        if cy > 1240 and gx - 240 < cx < gx + 240: prob.append('DETRAS DE GABRIEL')
        mx = 140; x0, y0 = max(0, int(x - mx)), max(0, int(y - mx)); x1, y1 = min(rv.W, int(x + w + mx)), min(rv.H, int(y + h + mx))
        crop = Image.fromarray(fr).crop((x0, y0, max(x1, x0 + 40), max(y1, y0 + 40)))
        k = min(520 / crop.width, 300 / crop.height); crop = crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))))
        tile = Image.new('RGB', (540, 420), (30, 30, 30)); tile.paste(crop, ((540 - crop.width) // 2, 50)); d = ImageDraw.Draw(tile)
        d.text((8, 6), f"toma {sh['id']} · {tg:.2f} s · {tipo}", fill=(255, 255, 0))
        d.text((8, 24), ('!! ' + ', '.join(prob)) if prob else 'ubicacion ok', fill=(255, 80, 80) if prob else (120, 230, 120))
        d.text((8, 362), 'dice: ' + dice[:70], fill=(255, 255, 255))
        tiles.append(tile)
        print(f"{sh['id']:>4} {tg:6.2f}s {tipo:9s} | dice: {dice[:60]:60s} | {'!! ' + ', '.join(prob) if prob else 'ok'}")
        if prob: avisos.append((sh['id'], tg, prob))
    if not tiles: print('sin marcas'); return
    cols = 5; filas = (len(tiles) + cols - 1) // cols; hoja = Image.new('RGB', (cols * 540, filas * 420), (0, 0, 0))
    for i, t in enumerate(tiles): hoja.paste(t, ((i % cols) * 540, (i // cols) * 420))
    hoja.save(out, quality=85)
    print(f'{len(tiles)} marcas revisadas · {len(avisos)} con aviso · hoja: {out}')


if __name__ == '__main__':
    main()
