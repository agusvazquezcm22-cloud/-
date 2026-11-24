"""Video 46 · "Creadores que se quedan" (Liquid I.V. + Bloom Nutrition) · v01
Formato pantalla verde, tema general con dos marcas como prueba (guia de Gabriel, "CREADORES QUE SE QUEDAN") + todo lo que
Gabriel fue corrigiendo en el 38, 39 y 40:
- Hook 0-6 s: rafaga de VIDEOS reales de creadores (dos cortes en los primeros 3 s), no un grafico.
- Gabriel cambia de lugar toma a toma (CI / CD / C). Termina con su voz (DUR = crudo, sin cola).
- Nunca mas de ~4 s de grafico propio seguido: cada consejo (1 a 4) va como etiqueta sobre un video real de creador y el
  grafico solo para la idea que no tiene imagen (perfil chico vs cuenta enorme, $ por venta / cada mes).
- Marcas rojas solo sobre rectangulos medidos: tarjeta real de la Biblioteca (#LiquidIVPartner, "Edward Digges with
  Liquid I.V."), frase.js en Entrepreneur ("over $1 billion worth of retail sales", "one-to-one relationship", ...).
- Cifras con contador (US$1.000 M; 10.000 -> 20.000 muestras al mes).
No se muestra: promesas de salud (hidratacion "faster than water", energia, digestion, "debloat") ni cifras de ventas de Bloom.
Tiempos de la transcripcion del crudo (77,9 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v46')
RAW = f'{A}/dl/crudo46.mp4'
DUR = 77.9                   # termina con la voz (el crudo termina con la ultima palabra)
CABEZA = 815                 # fila del crudo donde esta el tope de su cabeza (medido: 808-832)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)

# ------------------------------------------------------------ videos reales
# Liquid I.V. (Biblioteca de Anuncios, pagina 609555915738248): creadores y producto
L = dict(cocina='2064995610880775', papa='979279478106524', rosa='2440830770065387', bolsas='1819767002307520', depto='1138556758762193',
         naranja='2616181155474182', rayas='1492782046029620', manager='1806890497201184', meta='1570533914202443', choco='1598571368973671')
# Bloom Nutrition (Biblioteca de Anuncios, pagina de @bloomsupps): se completa con los ids cosechados
B = {}


# ------------------------------------------------------------ logos
def _chip(path, caja, alto=104):
    """Logo real de la marca recortado de uno de sus anuncios, en pastilla redondeada."""
    lg = Image.open(path).convert('RGB').crop(caja); lg = lg.resize((int(lg.width * alto / lg.height), alto), Image.LANCZOS)
    m = Image.new('L', lg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, lg.width - 1, lg.height - 1], radius=26, fill=255)
    c = Image.new('RGBA', lg.size, (0, 0, 0, 0)); c.paste(lg, (0, 0), m); return c
CHIP_L = _chip(ad('1828405711682374'), (36, 232, 548, 362))          # "LIQUID I.V." sobre su azul (anuncio real)
VERDE_B = (31, 87, 60)


def _chip_bloom(alto=104):
    """Logo de bloomnu.com (SVG blanco) sobre el verde de la marca."""
    lg = Image.open(f'{A}/bloom/bloom_logo.png').convert('RGBA'); lg = lg.crop(lg.getbbox())
    k = (alto - 34) / lg.height; lg = lg.resize((int(lg.width * k), alto - 34), Image.LANCZOS)
    c = Image.new('RGBA', (lg.width + 64, alto), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, alto - 1], radius=30, fill=VERDE_B + (255,))
    c.alpha_composite(lg, (32, 17)); return c
CHIP_B = _chip_bloom()


def logo_arriba(chip, t0=0.0, cy=230):
    f = lambda pil, tl, T: pegar(pil, chip, 540, cy, lerp(0.86, 1, pop(tl, t0))) if tl >= t0 else None
    f.caja_titulo = (540 - chip.width / 2, cy - chip.height / 2, 540 + chip.width / 2, cy + chip.height / 2)
    return f


# ------------------------------------------------------------ mosaico de videos (un grupo de creadores)
class Mosaico(Mitades):
    """2x2 videos reales recortados al centro, en y 170-1110 (arriba de la franja de subtitulos lo justo; Gabriel abajo).
    `marca`: indice del cuadro que lleva el check verde ('este vende') desde t_marca."""

    def __init__(self, clips, marca=None, t_marca=0.0):
        self.clips = clips; self.marca = marca; self.t_marca = t_marca
        self.izq = Serie([(0, c) for c in clips[:2]]); self.der = Serie([(0, c) for c in clips[2:]])   # para que _clips() los encuentre

    def frame(self, tl, T, seq=True):
        out = np.full((H, W, 3), 245, np.uint8); tw, th = 516, 452
        for n, c in enumerate(self.clips):
            fr, _ = c.frame(tl, T, seq=seq); fr = np.asarray(fr)
            s = cv2.resize(fr, (tw, int(H * tw / W)), interpolation=cv2.INTER_AREA); y0 = (s.shape[0] - th) // 2
            x, y = 16 + (n % 2) * (tw + 16), 170 + (n // 2) * (th + 16)
            out[y:y + th, x:x + tw] = s[y0:y0 + th]
            if self.marca == n and tl >= self.t_marca:
                pil = Image.fromarray(out); d = ImageDraw.Draw(pil); k = pop(tl, self.t_marca)
                d.rounded_rectangle([x - 6, y - 6, x + tw + 6, y + th + 6], radius=10, outline=VERDE_OSC, width=int(10 * k) or 1)
                pegar(pil, CHECK, x + tw - 60, y + 60, k); out = np.asarray(pil).copy()
        return out, None


def _check(tam=110):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.ellipse([0, 0, tam - 1, tam - 1], fill=VERDE_OSC + (255,))
    d.line([(tam * .26, tam * .52), (tam * .44, tam * .70), (tam * .76, tam * .32)], fill=(255, 255, 255, 255), width=13, joint='curve'); return c
CHECK = _check()


# ------------------------------------------------------------ graficos propios (contenido entre y 180 y 730)
def _persona(col=TINTA, tam=120):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.3], 180, 360, fill=col + (255,)); return c
GENTE = [_persona((60, 60, 66)), _persona((95, 95, 102)), _persona((40, 40, 48))]
GRISP = _persona((200, 200, 198))


def _foco(tam=200):
    c = Image.new('RGBA', (tam, int(tam * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .1, 0, tam * .9, tam * .8], fill=(255, 205, 60, 255), outline=TINTA + (255,), width=7)
    d.rounded_rectangle([tam * .32, tam * .78, tam * .68, tam * 1.05], radius=10, fill=(150, 150, 150, 255), outline=TINTA + (255,), width=6)
    for a in range(-60, 241, 50):
        import math as _m
        x0, y0 = tam / 2 + tam * .48 * _m.cos(_m.radians(a)), tam * .4 - tam * .48 * _m.sin(_m.radians(a))
    return c
FOCO = _foco()


def g_ideas(chip):
    """Un grupo chico de fanaticos -> flechas -> una idea (foco), con o sin el logo de la marca."""
    def f(tl, T):
        im = fondo_grafico(); d = ImageDraw.Draw(im)
        for i in range(5):
            pegar(im, GENTE[i % 3], 170 + (i % 3) * 120, 360 + (i // 3) * 150 + (60 if i >= 3 else 0), pop(tl, 0.03 + i * 0.06))
        p = ease((tl - 0.35) / 0.25)
        if p > 0:
            for yy in (330, 470): flecha_recta(d, (470, yy), (640, 410), p)
        if tl > 0.5: pegar(im, FOCO, 800, 400, lerp(0.8, 1, pop(tl, 0.5)))
        if chip is not None and tl > 0.6: pegar(im, chip.resize((int(chip.width * 0.8), int(chip.height * 0.8)), Image.LANCZOS), 800, 640, pop(tl, 0.6))
        return im
    return f


def _caja_muestra(tam=120):
    c = Image.new('RGBA', (tam, int(tam * .8)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rectangle([4, h * .25, w - 4, h - 4], fill=(214, 178, 130, 255), outline=TINTA + (255,), width=5)
    d.polygon([(4, h * .25), (w / 2, h * .05), (w - 4, h * .25)], fill=(232, 200, 155, 255), outline=TINTA + (255,))
    d.line([(w / 2, h * .25), (w / 2, h - 4)], fill=TINTA + (255,), width=4); return c
CAJA = _caja_muestra()
C_MUESTRAS = contador(20000, 0.15, dur=1.8, prefijo='10.000 – ', sufijo='', tam=96, desde=10000)


def g_muestras(tl, T):                # "Llego a mandar entre 10 mil y 20 mil muestras al mes" (27.10-29.32)
    im = fondo_grafico()
    pegar(im, CHIP_B, 540, 200, pop(tl, 0.0))
    n = int(min(18, max(0, (tl - 0.05) / 0.09)))
    for i in range(n):
        x = 250 + (i % 6) * 116; y = 640 - (i // 6) * 92
        pegar(im, CAJA, x, y, 1.0)
    C_MUESTRAS(im, tl, 540, 330)
    if tl > 0.6: pegar(im, pastilla('muestras al mes', 44, fondo=TINTA), 540, 445, pop(tl, 0.6))
    return im


def g_un_video(tl, T):                # "el problema real era que siguieran publicando" (31.98-33.96): la mayoria se apaga
    im = fondo_grafico()
    for i in range(12):
        x = 180 + (i % 6) * 144; y = 330 + (i // 6) * 170
        gris = tl > 0.6 + (i % 7) * 0.08 and i not in (2, 9)
        pegar(im, GRISP if gris else GENTE[i % 3], x, y, pop(tl, 0.02 + i * 0.03))
    if tl > 1.1: pegar(im, pastilla('1 video y chao', 56, fondo=ROJO), 540, 660, lerp(0.86, 1, pop(tl, 1.1)))
    return im


def g_cuatro(tl, T):                  # "hay cuatro cosas que te pueden ahorrar mucha plata" (47.84-51.80)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for i in range(4):
        k = pop(tl, 0.1 + i * 0.15)
        if k <= 0: continue
        x = 165 + i * 250; y = 380
        d.rounded_rectangle([x - 100, y - 100, x + 100, y + 100], radius=26, fill=(255, 255, 255), outline=TINTA, width=7)
        d.text((x, y), str(i + 1), font=font(110), fill=VERDE_OSC, anchor='mm')
    if tl > 1.9: pegar(im, pastilla('4 cosas', 60, fondo=TINTA), 540, 580, pop(tl, 1.9))
    lluvia_billetes(im, tl - 3.0)                                                     # "ahorrar mucha plata" (50.94)
    return im


def _perfil(chico=True):
    w, h = (300, 330) if chico else (300, 330)
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    p = _persona((236, 72, 150) if chico else (120, 120, 118), 130); c.alpha_composite(p, ((w - 130) // 2, 30))
    if chico:
        d.text((w / 2, 230), '♥', font=font(64), fill=ROJO + (255,), anchor='mm'); d.text((w / 2, 290), 'vive el problema', font=font(30), fill=TINTA + (255,), anchor='mm')
    else:
        d.text((w / 2, 230), '1M', font=font(70), fill=TINTA + (255,), anchor='mm'); d.text((w / 2, 290), 'seguidores', font=font(32), fill=GRIS + (255,), anchor='mm')
    return c
P_CHICO, P_GRANDE = _perfil(True), _perfil(False)


def g_perfiles(tl, T):                # "...convence mucho mas que una cuenta enorme que nunca lo ha vivido" (57.30-59.02)
    im = fondo_grafico()
    pegar(im, P_GRANDE, 760, 420, lerp(1.25, 0.85, ease((tl - 0.8) / 0.4)) * pop(tl, 0.0))
    pegar(im, P_CHICO, 300, 420, lerp(0.75, 1.15, ease((tl - 0.8) / 0.4)) * pop(tl, 0.1))
    if tl > 1.0: pegar(im, _texto_g('>', 120, VERDE_OSC), 530, 420, pop(tl, 1.0))
    return im


def _texto_g(s, tam, col=TINTA):
    f = font(tam); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _calendario(tam=230):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 20, tam - 1, tam - 1], radius=24, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    d.rectangle([3, 23, tam - 4, 75], fill=ROJO + (255,))
    for r in range(3):
        for k in range(4): d.rounded_rectangle([22 + k * 50, 92 + r * 44, 54 + k * 50, 120 + r * 44], radius=6, fill=(220, 220, 216, 255))
    d.ellipse([22 + 2 * 50 - 6, 92 + 44 - 6, 54 + 2 * 50 + 6, 120 + 44 + 6], outline=VERDE_OSC + (255,), width=6); return c
CAL = _calendario()


def _moneda(tam=200):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=(255, 205, 60, 255), outline=TINTA + (255,), width=7)
    d.text((tam / 2, tam / 2), '$', font=font(int(tam * .6)), fill=TINTA + (255,), anchor='mm'); return c
MONEDA_G = _moneda()


def g_razon(tl, T):                   # "ganar algo por cada venta (70.62) o volver a trabajar contigo cada mes (72.16)"
    im = fondo_grafico()
    if tl > 0.15: pegar(im, MONEDA_G, 290, 380, lerp(0.8, 1, pop(tl, 0.15))); pegar(im, pastilla('$ por venta', 46, fondo=VERDE_OSC), 290, 580, pop(tl, 0.35))
    if tl > 1.76: pegar(im, CAL, 790, 380, lerp(0.8, 1, pop(tl, 1.76))); pegar(im, pastilla('cada mes', 46, fondo=TINTA), 790, 580, pop(tl, 1.96))
    return im


_BILLETE = None
def lluvia_billetes(im, tl, n=14):
    """Billetes verdes que caen girando desde arriba (dibujados, sin fotos de stock)."""
    global _BILLETE
    if tl <= 0: return
    if _BILLETE is None:
        b = Image.new('RGBA', (150, 72), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.rounded_rectangle([0, 0, 149, 71], radius=8, fill=(76, 160, 96, 255), outline=(30, 100, 50, 255), width=4)
        d.ellipse([52, 13, 98, 59], outline=(220, 245, 225, 255), width=4); d.text((75, 36), '$', font=font(34), fill=(255, 255, 255, 255), anchor='mm')
        _BILLETE = b
    rnd = np.random.default_rng(11)
    for k in range(n):
        x0 = rnd.uniform(40, 1040); v = rnd.uniform(520, 780); fase = rnd.uniform(0, 0.5); ang0 = rnd.uniform(-40, 40); giro = rnd.uniform(-160, 160)
        t = tl - fase
        if t <= 0: continue
        y = -60 + v * t; x = x0 + 40 * math.sin(t * 3 + k)
        if y > 760: continue
        r = _BILLETE.rotate(ang0 + giro * t, expand=True, resample=Image.BICUBIC); im.paste(r, (int(x - r.width / 2), int(y - r.height / 2)), r)


def g_ejemplo(thumbs):
    """'Los videos que mas venden se vuelven el ejemplo que los demas repiten': una miniatura con check al centro y flechas
    hacia las demas (cuadros reales de los videos de creadoras)."""
    def f(tl, T):
        im = fondo_grafico(); d = ImageDraw.Draw(im)
        c0 = thumbs[0]; pegar(im, c0, 540, 300, lerp(0.85, 1, pop(tl, 0.0))); pegar(im, CHECK, 540 + c0.width // 2 - 30, 300 - c0.height // 2 + 30, pop(tl, 0.15))
        for i, t in enumerate(thumbs[1:4]):
            x = 210 + i * 330; t0 = 0.4 + i * 0.12
            if tl > t0:
                flecha_recta(d, (540 + (x - 540) * 0.25, 300 + c0.height // 2 + 6), (x, 520), ease((tl - t0) / 0.18))
                pegar(im, t, x, 640, pop(tl, t0 + 0.1))
        return im
    return f


def _thumb(i, ss, w=230, h=230):
    """Cuadro real de un video, recortado al centro (para los graficos con miniaturas)."""
    import subprocess as sp
    raw = sp.run(['ffmpeg', '-v', '0', '-ss', str(ss), '-i', ad(i, 'mp4'), '-frames:v', '1', '-vf', f'scale={w}:-2', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    hh = len(raw) // (w * 3); a = np.frombuffer(raw[:w * 3 * hh], np.uint8).reshape(hh, w, 3); y0 = (hh - h) // 2
    t = Image.fromarray(a[y0:y0 + h]).convert('RGBA'); m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=24, fill=255)
    c = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, w + 11, h + 11], radius=28, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=5)
    c.paste(t, (6, 6), m); return c


def g_grupo(tl, T):                   # "Asi que junto a todos en un mismo grupo y cada semana les hace llamadas" (33.96-36.96)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([150, 240, 930, 560], radius=36, outline=TINTA, width=7, fill=(255, 255, 255))
    d.text((540, 280), 'Grupo de creadores', font=font(44), fill=TINTA, anchor='mm')
    for i in range(10):
        x0, y0 = (80 + (i % 5) * 230, 690 if i < 5 else 150)
        x1, y1 = 260 + (i % 5) * 140, 380 + (i // 5) * 120
        p = ease((tl - 0.1 - i * 0.05) / 0.35)
        pegar(im, GENTE[i % 3], lerp(x0, x1, p), lerp(y0, y1, p), 0.8)
    if tl > 1.82: pegar(im, CAL.resize((170, 170), Image.LANCZOS), 540, 670, pop(tl, 1.82)); pegar(im, pastilla('llamada cada semana', 38, fondo=ROJO), 820, 670, pop(tl, 2.0))
    return im


# ------------------------------------------------------------ capturas
EJ = json.load(open(f'{A}/cap/entmeta.json')); EJ3 = json.load(open(f'{A}/cap/ent3meta.json')); EJ2 = json.load(open(f'{A}/cap/ent2meta.json'))
LP = json.load(open(f'{A}/cap/lp_fbmeta.json'))['cards']['979279478106524']
