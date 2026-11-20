"""Video 32 · "Las 6 piezas del sistema" (IM8) · v01
Formato pantalla verde (referencia Chase Chappell). Tiempos tomados de la
transcripcion palabra por palabra del crudo (76,5 s).
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from render_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad')
RAW = f'{A}/dl/crudo32.mp4'
DUR = 76.5
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'

ad = lambda i, e='jpg': f'{A}/ads/{i}.{e}'
LOGO = Image.open(f'{A}/dl/im8logo.png').convert('RGBA')
LOGO_B = LOGO.copy(); LOGO_B.putdata([(255, 255, 255, p[3]) for p in LOGO.getdata()])
GRIS = (120, 124, 132)
VERDE_OSC = (30, 150, 90)


# ------------------------------------------------------------ ayudas de fondo
def anuncio(i, z=0.03):
    """Anuncio en imagen a pantalla completa; si no es 9:16 va entero sobre su version desenfocada."""
    im = Image.open(ad(i)).convert('RGB')
    if im.height / im.width >= 1.7:
        c = Image.fromarray(cubrir(im))
    else:
        c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.62))
        f = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
        c.paste(f, (0, 150))
    return Lienzo(c, (0, 0, W), (W * z / 2, H * z * 0.35, W * (1 - z)))


def tarjeta(i, marcas_css, z=0.04):
    """Tarjeta real de la Biblioteca de Anuncios sobre el gris de la Biblioteca."""
    card = Image.open(f'{A}/cap/card_{i}.png').convert('RGB')
    k = 980 / card.width
    card = card.resize((980, int(card.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (240, 242, 245)); c.paste(card, (50, 110))
    f = 2 * k
    ms = [(t, (50 + r[0] * f, 110 + r[1] * f, r[2] * f, r[3] * f), t0) for t, r, t0 in marcas_css]
    return Lienzo(c, (0, 0, W), (W * z / 2, H * z * 0.25, W * (1 - z)), ms)


FBM = json.load(open(f'{A}/cap/fbmeta.json'))
STM = json.load(open(f'{A}/cap/stmeta.json'))


def comunicado(k, t_marca=0.25, flecha='flecha_ai', w1=1500, yrel=0.36, w0=2100):
    """Captura del comunicado (StockTitan) con zoom a la frase y recuadro rojo."""
    im = Image.open(f'{A}/cap/st_{k}.png').convert('RGB')
    rs = [[v * 3 for v in r] for r in STM[k]]
    x0 = min(r[0] for r in rs); y0 = min(r[1] for r in rs); x1 = max(r[0] + r[2] for r in rs); y1 = max(r[1] + r[3] for r in rs)
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    def v(w):
        vx = min(max(cx - w / 2, 0), 2460 - w); return (vx, max(0, cy - yrel * w * 16 / 9), w)
    ms = [('caja', (r[0], r[1], r[2], r[3]), t_marca) for r in rs]
    if flecha: ms.append((flecha, tuple(rs[0]), t_marca))
    return Lienzo(im, v(w0), v(w1), ms, dur_mov=0.55)


_cache = {}
def img(path):
    if path not in _cache: _cache[path] = np.asarray(Image.open(path).convert('RGB'))
    return _cache[path]


def im8(archivo, vista0, vista1=None, marcas=(), dur_mov=None):
    """Captura de im8health.com (3 px por px CSS). Vistas y marcas en px CSS del archivo."""
    k = 3
    ms = [(m[0], tuple(v * k for v in m[1]), *m[2:]) for m in marcas]
    v1 = vista1 or vista0
    return Lienzo(img(f'{A}/cap/im8/{archivo}.png'), tuple(v * k for v in vista0), tuple(v * k for v in v1), ms, dur_mov=dur_mov)


def _tira_pagina():
    a = img(f'{A}/cap/im8/y03650.png'); b = img(f'{A}/cap/im8/y04600.png'); c = img(f'{A}/cap/im8/y06200.png')
    t = np.concatenate([a, b[(5250 - 4600) * 3:], c[:2400]], 0)
    return cv2.resize(t, (1920, t.shape[0] // 2), interpolation=cv2.INTER_AREA)   # 1,5 px por px CSS; y CSS 3650..
TIRA = _tira_pagina()
FB = np.concatenate([img(f'{A}/cap/fbg{i}.png') for i in range(4)], 0)            # 2 px por px CSS


def panel(archivo, rec, caja, ancho=1010, y=250):
    """Recorte de la pagina sobre su propio color de fondo (para tapar lo que no se puede mostrar)."""
    src = Image.fromarray(img(f'{A}/cap/im8/{archivo}.png'))
    x, yy, w, h = [v * 3 for v in rec]
    cr = src.crop((x, yy, x + w, yy + h)); k = ancho / w
    cr = cr.resize((ancho, int(h * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), cr.getpixel((4, 4))); c.paste(cr, ((W - ancho) // 2, y))
    f = 3 * k; ox = (W - ancho) // 2
    m = ('caja', (ox + (caja[0] - rec[0]) * f, y + (caja[1] - rec[1]) * f, caja[2] * f, caja[3] * f), 0.08)
    return Lienzo(c, (0, 0, W), (20, 20, W - 40), [m])


# ------------------------------------------------------------ graficos propios
def lienzo_puntos():
    im = Image.new('RGB', (W, H), (250, 250, 248)); d = ImageDraw.Draw(im)
    for yy in range(30, H, 44):
        for xx in range(30, W, 44):
            d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=(214, 214, 210))
    lg = LOGO.resize((300, int(300 * LOGO.height / LOGO.width)), Image.LANCZOS)
    im.paste(lg, ((W - 300) // 2, 150), lg)
    return im
BASE = lienzo_puntos()


def txt(d, xy, s, tam, color=TINTA, peso='ExtraBold', ancla='mm'):
    d.text(xy, s, font=font(tam, peso), fill=color, anchor=ancla)


def pop(tl, t0, dur=0.18):
    return ease((tl - t0) / dur)


def pegar(im, capa, cx, cy, k=1.0):
    if k <= 0.02: return
    if k != 1.0: capa = capa.resize((max(1, int(capa.width * k)), max(1, int(capa.height * k))), Image.LANCZOS)
    im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa if capa.mode == 'RGBA' else None)


def flecha_recta(d, a, b, prog, color=ROJO, ancho=12):
    ex, ey = a[0] + (b[0] - a[0]) * prog, a[1] + (b[1] - a[1]) * prog
    d.line([a, (ex, ey)], fill=color, width=ancho)
    if prog > 0.5:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for da in (2.55, -2.55):
            d.line([(ex, ey), (ex + 40 * math.cos(ang + da), ey + 40 * math.sin(ang + da))], fill=color, width=ancho)


def moneda(col=VERDE_OSC, tam=150):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=col + (255,)); txt(d, (tam / 2, tam / 2 + 2), '$', int(tam * 0.66), (255, 255, 255))
    return c


def caja_im8(tam=230):
    c = Image.new('RGBA', (tam, int(tam * 1.12)), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, tam - 1, c.height - 1], radius=26, fill=(160, 22, 40, 255))
    d.rounded_rectangle([0, 0, tam - 1, 46], radius=26, fill=(128, 14, 30, 255)); d.rectangle([0, 26, tam - 1, 46], fill=(128, 14, 30, 255))
    lg = LOGO_B.resize((int(tam * 0.62), int(tam * 0.62 * LOGO.height / LOGO.width)), Image.LANCZOS)
    c.alpha_composite(lg, ((tam - lg.width) // 2, int(c.height * 0.46)))
    return c


def frasco(tam=96):
    c = Image.new('RGBA', (tam, int(tam * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([tam * 0.28, 0, tam * 0.72, tam * 0.3], radius=6, fill=(96, 100, 110, 255))
    d.rounded_rectangle([tam * 0.08, tam * 0.24, tam * 0.92, c.height - 1], radius=16, fill=(176, 180, 190, 255))
    d.rounded_rectangle([tam * 0.08, tam * 0.62, tam * 0.92, tam * 1.1], radius=0, fill=(238, 238, 240, 255))
    return c


def sobre(tam=250):
    c = Image.new('RGBA', (tam, int(tam * 2.1)), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, tam - 1, c.height - 1], radius=22, fill=(168, 24, 44, 255))
    d.rectangle([0, 34, tam - 1, 40], fill=(120, 12, 28, 255))
    lg = LOGO_B.resize((int(tam * 0.7), int(tam * 0.7 * LOGO.height / LOGO.width)), Image.LANCZOS)
    c.alpha_composite(lg, ((tam - lg.width) // 2, int(c.height * 0.4)))
    return c
MON, MON_R, CAJA, FRASCO, SOBRE = moneda(), moneda(ROJO), caja_im8(), frasco(), sobre()


def g_linea_tiempo(tl, T):            # toma 3
    im = BASE.copy(); d = ImageDraw.Draw(im)
    p = ease(tl / 0.6); x0, x1, y = 190, 890, 640
    d.line([(x0, y), (x0 + (x1 - x0) * p, y)], fill=TINTA, width=10)
    d.ellipse([x0 - 24, y - 24, x0 + 24, y + 24], fill=TINTA)
    txt(d, (x0 + 10, y - 86), 'Nov 2024', 58); txt(d, (x0 + 10, y + 78), 'Lanzamiento', 44, GRIS, 'SemiBold')
    k = pop(tl, 0.55)
    if k > 0:
        r = 30 * k; d.ellipse([x1 - r, y - r, x1 + r, y + r], fill=ROJO)
        txt(d, (x1 - 60, y - 86), 'Sep 2026', 58)
        txt(d, (x1 - 100, y + 92), 'US$23,7 M', int(84 * lerp(0.8, 1, k)), ROJO); txt(d, (x1 - 100, y + 168), 'en un mes', 46, GRIS, 'SemiBold')
    txt(d, (W / 2, 400), 'Menos de 2 años', 70)
    return im


def g_16_a_1(tl, T):                  # toma 4b
    im = BASE.copy(); d = ImageDraw.Draw(im)
    for i in range(16):
        k = 1 - ease((tl - 0.04 - i * 0.022) / 0.16)
        pegar(im, FRASCO, 232 + (i % 4) * 205, 430 + (i // 4) * 205, k)
    k = pop(tl, 0.45, 0.22)
    pegar(im, SOBRE, W / 2, 700, k)
    if k > 0.5: txt(d, (W / 2, 1050), '16 suplementos → 1 sobre', 62)
    return im


def g_problema(tl, T):                # toma 8
    im = BASE.copy(); d = ImageDraw.Draw(im)
    txt(d, (W / 2, 400), 'Sus anuncios le hablan a…', 54, GRIS, 'SemiBold')
    k = pop(tl, 1.38)
    if k > 0: txt(d, (W / 2, 560), 'Tu problema', int(128 * lerp(0.85, 1, k)), VERDE_OSC, 'Black')
    k2 = pop(tl, 2.36)
    if k2 > 0:
        txt(d, (W / 2, 780), 'Su producto', 100, GRIS)
        p = ease((tl - 2.62) / 0.2); w = font(100).getlength('Su producto')
        if p > 0: d.line([(W / 2 - w / 2 - 16, 786), (W / 2 - w / 2 - 16 + (w + 32) * p, 786)], fill=ROJO, width=14)
    return im


MIN_ADS = [Image.open(ad(i)).convert('RGB').resize((216, 384), Image.LANCZOS) for i in ('1734476664479571', '996683953451195', '2302752947125995')]
def _mini_pagina():
    t = Image.fromarray(TIRA[:1920 * 1]).resize((500, 500), Image.LANCZOS)
    c = Image.new('RGB', (520, 520), TINTA); c.paste(t, (10, 10)); return c
MIN_PAG = _mini_pagina()


def g_tres_a_una(tl, T):              # toma 15
    im = BASE.copy(); d = ImageDraw.Draw(im)
    xs = [220, 540, 860]
    for i, x in enumerate(xs):
        k = pop(tl, 0.02 + i * 0.16)
        if k > 0:
            m = MIN_ADS[i]; d.rectangle([x - 114, 490 - 198, x + 114, 490 + 198], fill=TINTA); pegar(im, m, x, 490, 1.0 if k > 0.99 else lerp(0.8, 1, k))
    kp = pop(tl, 0.5)
    if kp > 0: pegar(im, MIN_PAG, W / 2, 1100, lerp(0.85, 1, kp))
    for i, x in enumerate(xs):
        p = ease((tl - 0.55 - i * 0.1) / 0.22)
        if p > 0: flecha_recta(d, (x, 700), (W / 2 + (x - W / 2) * 0.28, 828), p)
    return im


def g_calendario(tl, T):              # toma 21b
    im = BASE.copy(); d = ImageDraw.Draw(im)
    txt(d, (W / 2, 380), 'Recuperan lo que cuesta un cliente en', 46, GRIS, 'SemiBold')
    for i in range(6):
        x = 150 + (i % 3) * 270; y = 470 + (i // 3) * 270
        lleno = pop(tl, 0.1 + i * 0.2, 0.14)
        d.rounded_rectangle([x, y, x + 240, y + 240], radius=26, fill=(255, 255, 255), outline=TINTA, width=6)
        d.rounded_rectangle([x, y, x + 240, y + 62], radius=26, fill=TINTA); d.rectangle([x, y + 36, x + 240, y + 62], fill=TINTA)
        txt(d, (x + 120, y + 31), f'MES {i + 1}', 34, (255, 255, 255))
        if lleno > 0:
            r = 62 * lleno; d.ellipse([x + 120 - r, y + 150 - r, x + 120 + r, y + 150 + r], fill=ROJO if i < 5 else VERDE_OSC)
            if lleno > 0.6: txt(d, (x + 120, y + 152), '−$' if i < 5 else '✓', 54, (255, 255, 255)) if i < 5 else txt(d, (x + 120, y + 152), '$', 70, (255, 255, 255))
    return im


def _eje(d, y=700):
    xs = [210, 540, 870]
    d.line([(xs[0], y), (xs[2], y)], fill=TINTA, width=8)
    for x, s in zip(xs, ['1ª compra', 'Mes 3', 'Mes 6']):
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=TINTA); txt(d, (x, y + 70), s, 46, GRIS, 'SemiBold')
    return xs


def g_mayoria(tl, T):                 # toma 22
    im = BASE.copy(); d = ImageDraw.Draw(im)
    txt(d, (W / 2, 400), 'La mayoría de marcas', 74)
    xs = _eje(d)
    pegar(im, MON, xs[0], 560, pop(tl, 0.9, 0.2))
    return im


def g_contrario(tl, T):               # toma 23
    im = BASE.copy(); d = ImageDraw.Draw(im)
    lg = LOGO.resize((360, int(360 * LOGO.height / LOGO.width)), Image.LANCZOS)
    d.rectangle([300, 120, 780, 250], fill=(250, 250, 248)); im.paste(lg, ((W - 360) // 2, 345), lg)
    xs = _eje(d)
    a = 1 - pop(tl, 0.15, 0.2)
    if a > 0.02: pegar(im, MON, xs[0], 560, a)
    else: pegar(im, MON_R, xs[0], 560, pop(tl, 0.36) * 0.8);
    pegar(im, MON, xs[1], 560, pop(tl, 0.75)); pegar(im, MON, xs[2], 560, pop(tl, 1.0))
    p = ease((tl - 0.5) / 0.3)
    if p > 0: flecha_recta(d, (xs[0] + 80, 880), (xs[2], 880), p)
    return im


def g_tres_cajas(tl, T):              # toma 26
    im = BASE.copy()
    for i, t0 in enumerate([0.02, 1.25, 1.6]):
        pegar(im, CAJA, 260 + i * 280, 600, pop(tl, t0, 0.2))
    return im


def g_cada_3(tl, T):                  # toma 28
    im = BASE.copy(); d = ImageDraw.Draw(im)
    y = 700; xs = [150, 345, 540, 735, 930]
    d.line([(xs[0], y), (xs[-1] + 50, y)], fill=TINTA, width=8)
    for i, x in enumerate(xs):
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=TINTA); txt(d, (x, y + 64), f'Mes {i * 3}' if i else 'Día 1', 40, GRIS, 'SemiBold')
        pegar(im, MON, x, y - 130, pop(tl, 1.3 + i * 0.22) * 0.86)
    return im


def g_costo(tl, T):                   # toma 32
    im = BASE.copy(); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 170, 900, 920, 380
    d.line([(x0, y1 - 40), (x0, y0), (x1 + 20, y0)], fill=TINTA, width=8)
    p = ease((tl - 1.0) / 1.2); n = 40; pts = []
    for i in range(int(n * p) + 1):
        u = i / n; pts.append((x0 + 30 + (x1 - x0 - 60) * u, y0 - 40 - (y0 - y1 - 60) * (u ** 2.2)))
    if len(pts) > 1:
        d.line(pts, fill=ROJO, width=16, joint='curve')
        if p > 0.3:
            (ax, ay), (bx, by) = pts[-2], pts[-1]; ang = math.atan2(by - ay, bx - ax)
            for da in (2.5, -2.5): d.line([(bx, by), (bx + 54 * math.cos(ang + da), by + 54 * math.sin(ang + da))], fill=ROJO, width=16)
    txt(d, (W / 2 + 30, 330), 'Costo de cada anuncio', 60)
    txt(d, (x1 - 60, y0 + 46), 'tiempo →', 38, GRIS, 'SemiBold')
    return im


# ------------------------------------------------------------ portada / cierre
_bk = Image.open(f'{A}/dl/beckham.jpg').convert('RGB')
HERO = Image.fromarray(cubrir(_bk, ancla=(0.62, 0.3))).filter(ImageFilter.UnsharpMask(3, 60, 2))


def T_(lineas, cy, tam=74, t0=0.0, **kw):
    return lambda pil, tl, T: etiqueta(pil, lineas, cy, tam, tl - t0, **kw) if tl >= t0 else None


def varios(*fs):
    def f(pil, tl, T):
        for g in fs: g(pil, tl, T)
    return f


def entre(t0, t1, fn):
    return lambda pil, tl, T: fn(pil, tl - t0, T) if t0 <= tl < t1 else None


BUY = dict(plan=(676, 112, 556, 44), kit=(680, 207, 300, 26), envio=(922, 828, 90, 30), gar=(680, 280, 330, 26))
V_BUY = (640, 40, 620)

S = []
def toma(i, t0, t1, fondo, gab, texto=None, antes=None):
    S.append(dict(id=i, t0=t0, t1=t1, fondo=fondo, gab=gab, texto=texto, antes=antes))


toma('01', 0.00, 1.56, Lienzo(HERO, (0, 0, W), (22, 30, W - 44)), 'PL',
     T_(['La estrategia de', '23,7M en un mes', 'de IM8'], 330, 80, clave={'23,7M'}, emo='🤯', logo=LOGO))
toma('02', 1.56, 4.06, comunicado('arr', flecha='flecha_ai'), 'MR', T_(['≈ US$23,7 M al mes'], 830, 70, t0=0.9, clave={'US$23,7', 'M'}))
toma('03', 4.06, 5.52, Grafico(g_linea_tiempo), 'G')
toma('04', 5.52, 7.84, tarjeta('2184389968845356', [('sub', FBM['cards']['2184389968845356']['phr'][0], 0.75)]), 'PR')
toma('04b', 7.84, 8.88, Grafico(g_16_a_1), 'PR')
toma('05', 8.88, 10.20, Serie([(0, anuncio('1734476664479571')), (0.66, anuncio('1737856330622361'))]), lambda tl: 'PL' if tl < 0.66 else 'PR')
toma('06', 10.20, 11.44, Clip(ad('1737856330622361', 'mp4'), 4.4), 'G')
toma('07', 11.44, 12.54, Lienzo(FB, (340, 500, 2200), (340, 880, 2200)), 'ML')
toma('08', 12.54, 15.74, Grafico(g_problema), 'G')
toma('09', 15.74, 18.40, Serie([(0, anuncio('2977008649326655')), (1.18, Clip(ad('1093623876505524', 'mp4'), 1.2)), (1.74, anuncio('996683953451195')), (2.18, anuncio('2302752947125995'))]), 'PL',
     varios(entre(0.3, 1.18, T_(['Articulaciones'], 1290, 76)), entre(1.18, 1.74, T_(['Cansancio'], 1290, 76)), entre(1.74, 2.18, T_(['Digestión'], 1290, 76)), entre(2.18, 9, T_(['Menopausia'], 1290, 76))))
toma('10', 18.40, 20.50, tarjeta('2054169488625776', [('sub', FBM['cards']['2054169488625776']['phr'][0], 0.35)]), 'PR')
_r = [v * 2 for v in FBM['results'][:4]]
toma('11', 20.50, 21.96, Lienzo(FB, (0, 0, 2880), (0, 300, 1500), [('caja', tuple(_r), 0.3), ('flecha_ad', tuple(_r), 0.3)], dur_mov=0.5), 'ML')
toma('12', 21.96, 23.86, Lienzo(FB, (60, 5300, 1900), (940, 6300, 1900)), 'PR')
toma('13', 23.86, 24.74, Clip(ad('1737856330622361', 'mp4'), 1.7), 'G', T_(['¿Por qué?'], 520, 110))
_c = FBM['cards']['1657783909037027']['cta']
toma('14', 24.74, 26.88, tarjeta('1657783909037027', [('caja', _c, 0.7), ('flecha_ai', _c, 0.7)]), 'PL')
toma('15', 26.88, 28.14, Grafico(g_tres_a_una), 'PR')
toma('16', 28.14, 29.12, Lienzo(TIRA, (0, 300, 1920), (0, 1000, 1920)), 'PR')
toma('17', 29.12, 33.84, Serie([
    (0.00, panel('y02650', (20, 76, 640, 262), (36, 112, 470, 150))),
    (0.68, im8('y08650', (250, 20, 780), (270, 30, 740), [('caja', (352, 98, 576, 60), 0.08)])),
    (1.18, im8('y05400', (400, 70, 700), (410, 80, 680), [('caja', (650, 250, 385, 640), 0.08)])),
    (1.68, im8('y11817', (0, 380, 640), (10, 390, 620), [('caja_b', (16, 494, 566, 52), 0.1)])),
    (3.18, im8('y00700', V_BUY, (650, 50, 600), [('caja', BUY['gar'], 0.1)])),
]), lambda tl: 'PL' if tl < 1.68 else ('PR' if tl < 3.18 else 'PL'))
toma('18', 33.84, 36.24, Lienzo(TIRA, (60, 40, 1800), (0, 0, 1920)), 'G', T_(['Cero dudas'], 560, 120, t0=1.5, clave={'Cero'}))
toma('19', 36.24, 37.40, Clip(ad('1737856330622361', 'mp4'), 0.3), 'G')
toma('20', 37.40, 40.30, comunicado('cac', t_marca=1.3, flecha='flecha_ai'), 'ML')
toma('21', 40.30, 43.42, Serie([(0, comunicado('six', t_marca=0.9, flecha='flecha_ad')), (1.56, Grafico(g_calendario))]), 'PR', entre(2.1, 9, T_(['6 meses'], 1130, 96)))
toma('22', 43.42, 45.48, Grafico(g_mayoria), 'G')
toma('23', 45.48, 47.24, Grafico(g_contrario), 'G')
toma('24', 47.24, 48.52, im8('y00700', (620, 20, 660), V_BUY, dur_mov=0.6), 'PR')
toma('25', 48.52, 51.94, im8('y00700', V_BUY, V_BUY, [('caja', BUY['plan'], 0.0, 1.44), ('caja', BUY['kit'], 1.44, 2.12), ('caja', BUY['envio'], 2.12, 2.86), ('caja', BUY['gar'], 2.86, None)]), 'PR')
toma('26', 51.94, 55.36, Grafico(g_tres_cajas), 'G', T_(['Día 1 = 3 meses'], 880, 84, t0=1.9, clave={'3', 'meses'}))
toma('27', 55.36, 57.40, comunicado('cac', t_marca=0.15, flecha=None, w0=1500, w1=1420), 'G')
toma('28', 57.40, 60.18, Grafico(g_cada_3), 'PR', T_(['Cada 3 meses'], 1010, 88, t0=1.9, clave={'3', 'meses'}))
toma('29', 60.18, 60.82, Clip(ad('39553911627540676', 'mp4'), 4.3), 'ML')
toma('30', 60.82, 64.10, comunicado('x41', t_marca=1.2, flecha='flecha_ad'), 'MR', T_(['4 veces lo que', 'costó traerlos'], 880, 74, t0=1.75, clave={'4', 'veces'}))
toma('31', 64.10, 66.38, Clip(ad('28878752765118956', 'mp4'), 6.0), 'G')
toma('32', 66.38, 69.24, Grafico(g_costo), 'G')
toma('33', 69.24, 75.22, Serie([
    (0.00, anuncio('1734476664479571', 0)), (0.62, anuncio('2977008649326655', 0)), (1.24, anuncio('996683953451195', 0)),
    (1.86, Lienzo(FB, (240, 5150, 2400), (240, 5330, 2400))),
    (2.88, Lienzo(TIRA, (0, 0, 1920), (0, 260, 1920))),
    (3.54, im8('y00700', V_BUY, V_BUY, [('caja', BUY['plan'], 0.05)])),
    (4.06, comunicado('cac', t_marca=0.05, flecha=None, w0=1500, w1=1460)),
    (5.00, comunicado('x41', t_marca=0.05, flecha=None, w0=1500, w1=1460)),
]), lambda tl: ['PL', 'PR', 'PL', 'PR', 'PL', 'PR', 'PL', 'PR'][sum(tl >= x for x in (0.62, 1.24, 1.86, 2.88, 3.54, 4.06, 5.00))])
toma('34', 75.22, 76.50, Lienzo(HERO, (22, 30, W - 44), (0, 0, W)), 'G', T_(['Comenta “BECKHAM”'], 520, 86, clave={'“BECKHAM”'}, emo='👇'))
SHOTS = S
