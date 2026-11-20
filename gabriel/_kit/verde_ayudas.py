"""Ayudas comunes para las listas de tomas del formato pantalla verde (desde el video 33).

Uso en un config:
    from verde_ayudas import *
    configurar(A, logo=<PIL del logo de la marca>)
    toma('01', 0.0, 1.1, clip('123', 7.6, nombre='portada'), 'PL', T_([...], 208, 66, t0=-1))
    ...
    SHOTS = S

Cada constructor anota que fuente usa, y `toma()` las junta: asi `render_verde.py --control` puede avisar
si un visual se repite (regla de Gabriel: ningun B-roll o captura mas de una vez por video).
"""
import math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from render_verde import *

A = '.'
LOGO = None
GRIS = (120, 124, 132)
VERDE_OSC = (30, 150, 90)
BASE = BASE2 = BASE_SIN_LOGO = None
S = []
_usos = []
_img = {}


def usar(*nombres): _usos.extend(nombres)


def toma(i, t0, t1, fondo, gab, texto=None, antes=None):
    fu = list(_usos); _usos.clear()
    S.append(dict(id=i, t0=t0, t1=t1, fondo=fondo, gab=gab, texto=texto, antes=antes, fuentes=fu))


def _puntos(logo):
    im = Image.new('RGB', (W, H), (250, 250, 248)); d = ImageDraw.Draw(im)
    for yy in range(30, H, 44):
        for xx in range(30, W, 44): d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=(214, 214, 210))
    if logo is not None:
        lg = logo.resize((int(logo.width * 104 / logo.height), 104), Image.LANCZOS)
        im.paste(lg, ((W - lg.width) // 2, 76), lg if lg.mode == 'RGBA' else None)
    return im


def configurar(assets, logo=None):
    """assets: carpeta de trabajo (dl/, cap/, ads/). logo: PIL del logo de la marca para los graficos propios."""
    global A, LOGO, BASE, BASE2, BASE_SIN_LOGO
    A = assets; LOGO = logo
    BASE = _puntos(None); BASE_SIN_LOGO = BASE; BASE2 = _puntos(logo)


def fondo_grafico():
    """Fondo punteado sin logo para dibujar un grafico propio (usar esto, no BASE: `import *` copia BASE antes de configurar)."""
    return BASE.copy()


def ad(i, e='jpg'): return f'{A}/ads/{i}.{e}'


def img(path):
    if path not in _img: _img[path] = np.asarray(Image.open(path).convert('RGB'))
    return _img[path]


# ------------------------------------------------------------ fondos
def anuncio(i, z=0.03, marcas_rel=(), nombre=None, encaje=None):
    """Anuncio en imagen a pantalla completa. Si no es 9:16 va entero sobre su version desenfocada.
    marcas_rel: [(tipo, (x, y, w, h) en fraccion de la imagen original, t0[, t1])]."""
    usar(nombre or f'anuncio-imagen:{i}')
    im = Image.open(ad(i)).convert('RGB')
    if encaje:            # (escala, y): la imagen entera, mas chica, sobre su version desenfocada (portada con titulo arriba)
        k, y = encaje; c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(42)).point(lambda v: int(v * 0.62))
        ch = Image.fromarray(cubrir(im)).resize((int(W * k), int(H * k)), Image.LANCZOS); x0 = (W - ch.width) // 2; c.paste(ch, (x0, y))
        s = max(W / im.width, H / im.height) * k; ox = (im.width * s - ch.width) / 2; oy = (im.height * s - ch.height) / 2
        ms = [(m[0], (x0 + m[1][0] * im.width * s - ox, y + m[1][1] * im.height * s - oy, m[1][2] * im.width * s, m[1][3] * im.height * s), *m[2:]) for m in marcas_rel]
        return Lienzo(c, (0, 0, W), (W * z / 2, H * z * 0.35, W * (1 - z)), ms)
    if im.height / im.width >= 1.7:
        s = max(W / im.width, H / im.height); ox = (im.width * s - W) / 2; oy = (im.height * s - H) / 2
        c = Image.fromarray(cubrir(im))
    else:
        s = W / im.width; ox = 0; oy = -150
        c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.62))
        c.paste(im.resize((W, int(im.height * s)), Image.LANCZOS), (0, 150))
    ms = [(m[0], (m[1][0] * im.width * s - ox, m[1][1] * im.height * s - oy, m[1][2] * im.width * s, m[1][3] * im.height * s), *m[2:]) for m in marcas_rel]
    return Lienzo(c, (0, 0, W), (W * z / 2, H * z * 0.35, W * (1 - z)), ms)


def clip(i, ss, nombre=None, **k):
    usar(nombre or f'anuncio-video:{i}')
    return Clip(ad(i, 'mp4'), ss, **k)


def lienzo(fuente, v0, v1=None, marcas=(), nombre=None, **k):
    """Lienzo generico (np o PIL) con registro de la fuente."""
    if nombre: usar(nombre)
    return Lienzo(fuente, v0, v1, marcas, **k)


def tarjeta(png, marcas_css, z=0.04, nombre=None):
    """Tarjeta de la Biblioteca de Anuncios (captura a 2 px por px CSS) sobre el gris de la Biblioteca."""
    usar(nombre or 'tarjeta:' + png.split('/')[-1])
    card = Image.open(png).convert('RGB'); k = 980 / card.width
    card = card.resize((980, int(card.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (240, 242, 245)); c.paste(card, (50, 110)); f = 2 * k
    ms = [(m[0], (50 + m[1][0] * f, 110 + m[1][1] * f, m[1][2] * f, m[1][3] * f), *m[2:]) for m in marcas_css]
    return Lienzo(c, (0, 0, W), (W * z / 2, H * z * 0.25, W * (1 - z)), ms)


def captura(png, cajas, w0=2100, w1=1500, yrel=0.29, nombre=None, dur_mov=0.55, escala=3):
    """Captura de una nota (frase.js, 2460x4374, 3 px por px CSS) con zoom a la frase.
    cajas: [(rects_css, t0, t1 o None, flecha o None)] - cada grupo es una frase (una caja si cabe en una linea)."""
    usar(nombre or 'captura:' + png.split('/')[-1])
    im = Image.open(png).convert('RGB'); ms = []; cx = cy = None
    for rects, t0, t1, flecha in cajas:
        rs = [[v * escala for v in r] for r in rects]
        x0 = min(r[0] for r in rs); y0 = min(r[1] for r in rs); x1 = max(r[0] + r[2] for r in rs); y1 = max(r[1] + r[3] for r in rs)
        if cx is None: cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        una = abs(y1 - y0) < 30 * escala
        for r in ([(x0, y0, x1 - x0, y1 - y0)] if una else [tuple(r) for r in rs]): ms.append(('caja', r, t0, t1))
        if flecha: ms.append((flecha, (x0, y0, x1 - x0, y1 - y0) if una else tuple(rs[0]), t0, t1))
    def v(w):
        return (min(max(cx - w / 2, 0), im.width - w), max(0, cy - yrel * w * 16 / 9), w)
    return Lienzo(im, v(w0), v(w1), ms, dur_mov=dur_mov)


# ------------------------------------------------------------ graficos propios
def G(fn, y1=1100, k=0.66, y=196, logo=True):
    """Grafico propio: fn(tl, T) dibuja sobre BASE.copy() en la franja y 290..y1; aca se achica y se sube para
    dejar libre la franja de subtitulos. logo=False si el grafico ya muestra la marca."""
    usar('grafico:' + fn.__name__)
    def f(tl, T):
        g = fn(tl, T).crop((0, 290, W, y1)); g = g.resize((int(W * k), int((y1 - 290) * k)), Image.LANCZOS)
        im = (BASE2 if logo else BASE_SIN_LOGO).copy(); im.paste(g, ((W - g.width) // 2, y)); return im
    return Grafico(f)


def txt(d, xy, s, tam, color=TINTA, peso='ExtraBold', ancla='mm'):
    d.text(xy, s, font=font(tam, peso), fill=color, anchor=ancla)


def pop(tl, t0, dur=0.18): return ease((tl - t0) / dur)


def pegar(im, capa, cx, cy, k=1.0):
    if k <= 0.02: return
    if k != 1.0: capa = capa.resize((max(1, int(capa.width * k)), max(1, int(capa.height * k))), Image.LANCZOS)
    im.paste(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)), capa if capa.mode == 'RGBA' else None)


def flecha_recta(d, a, b, prog, color=ROJO, ancho=12):
    if prog <= 0: return
    ex, ey = a[0] + (b[0] - a[0]) * prog, a[1] + (b[1] - a[1]) * prog
    d.line([a, (ex, ey)], fill=color, width=ancho)
    if prog > 0.5:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for da in (2.55, -2.55):
            d.line([(ex, ey), (ex + 40 * math.cos(ang + da), ey + 40 * math.sin(ang + da))], fill=color, width=ancho)


def pastilla(texto, tam=56, fondo=TINTA, color=(255, 255, 255), borde=None, pad=(44, 26)):
    f = font(tam); w = int(f.getlength(texto)) + 2 * pad[0]; h = int(tam * 1.1) + 2 * pad[1]
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=fondo + (255,), outline=(borde + (255,)) if borde else None, width=6 if borde else 0)
    d.text((w / 2, h / 2), texto, font=f, fill=color + (255,), anchor='mm')
    return c


# ------------------------------------------------------------ textos por encima
def T_(lineas, cy, tam=74, t0=0.0, **kw):
    """Etiqueta en caja oscura. t0=-1 la deja fija desde el cuadro 0 (portada)."""
    return lambda pil, tl, T: etiqueta(pil, lineas, cy, tam, tl - t0, **kw) if tl >= t0 else None


def varios(*fs):
    def f(pil, tl, T):
        for g in fs: g(pil, tl, T)
    return f


def entre(t0, t1, fn): return lambda pil, tl, T: fn(pil, tl - t0, T) if t0 <= tl < t1 else None
