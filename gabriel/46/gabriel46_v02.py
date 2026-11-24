"""Video 46 · "Creadores que se quedan" (Liquid I.V. + Bloom Nutrition) · v02
v02 (feedback de Gabriel en la web, 2026-11-24): 17,6 s "aqui ya usamos dos imagenes de texto antes, pongamos algo mas visual,
puede ser de ellos hablando con sus clientes" -> las tres tarjetas de Entrepreneur de 15-18,7 s y la de 18,7-21 s pasan a videos
reales (clientas/creadoras hablando, un anuncio de Liquid I.V.); quedan solo dos tarjetas de texto (la etiqueta de colaboracion
pagada y los US$1.000 M). Reglas fijas: todo a pantalla completa (el mosaico 2x2 ahora llena la pantalla; las tarjetas van
sobre un fondo real nitido, no desenfocado).
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
B1, B2 = '1085973624189294', '1807342620573473'   # creadoras de Bloom (anuncios de la pagina 655412221523654, @bloomsupps)


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
        out = np.zeros((H, W, 3), np.uint8); tw, th = W // 2, H // 2                     # v02: el mosaico llena la pantalla
        for n, c in enumerate(self.clips):
            fr, _ = c.frame(tl, T, seq=seq); fr = np.asarray(fr)
            s = cv2.resize(fr, (tw, int(H * tw / W)), interpolation=cv2.INTER_AREA); y0 = max(0, (s.shape[0] - th) // 2)
            x, y = (n % 2) * tw, (n // 2) * th
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
GENTE = [_persona((60, 60, 66), 170), _persona((95, 95, 102), 170), _persona((40, 40, 48), 170)]
GRISP = _persona((200, 200, 198), 170)


def _foco(tam=200):
    c = Image.new('RGBA', (tam, int(tam * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .1, 0, tam * .9, tam * .8], fill=(255, 205, 60, 255), outline=TINTA + (255,), width=7)
    d.rounded_rectangle([tam * .32, tam * .78, tam * .68, tam * 1.05], radius=10, fill=(150, 150, 150, 255), outline=TINTA + (255,), width=6)
    for a in range(-60, 241, 50):
        import math as _m
        x0, y0 = tam / 2 + tam * .48 * _m.cos(_m.radians(a)), tam * .4 - tam * .48 * _m.sin(_m.radians(a))
    return c
FOCO = _foco()


def g_ideas(chip, etiqueta=None):
    """Un grupo chico de fanaticos -> flechas -> una idea (foco), con o sin el logo de la marca."""
    def f(tl, T):
        im = fondo_grafico(); d = ImageDraw.Draw(im)
        for i in range(5):
            pegar(im, GENTE[i % 3], 130 + (i % 3) * 160 + (80 if i >= 3 else 0), 300 + (i // 3) * 210, pop(tl, 0.03 + i * 0.06))
        p = ease((tl - 0.3) / 0.25)
        if p > 0:
            for yy in (330, 530): flecha_recta(d, (480, yy), (650, 430), p)
        if tl > 0.45: pegar(im, FOCO.resize((260, 338), Image.LANCZOS), 820, 410, lerp(0.8, 1, pop(tl, 0.45)))
        if chip is not None and tl > 0.55: pegar(im, chip, 820, 650, pop(tl, 0.55))
        if etiqueta and tl > 0.55: pegar(im, pastilla(etiqueta, 60, fondo=VERDE_OSC), 700, 670, pop(tl, 0.55))
        return im
    return f


def _caja_muestra(tam=120):
    c = Image.new('RGBA', (tam, int(tam * .8)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rectangle([4, h * .25, w - 4, h - 4], fill=(214, 178, 130, 255), outline=TINTA + (255,), width=5)
    d.polygon([(4, h * .25), (w / 2, h * .05), (w - 4, h * .25)], fill=(232, 200, 155, 255), outline=TINTA + (255,))
    d.line([(w / 2, h * .25), (w / 2, h - 4)], fill=TINTA + (255,), width=4); return c
CAJA = _caja_muestra(165)
C_MUESTRAS = contador(20000, 0.15, dur=1.8, prefijo='10.000 – ', sufijo='', tam=120, desde=10000)


def g_muestras(tl, T):                # "Llego a mandar entre 10 mil y 20 mil muestras al mes" (27.10-29.32)
    im = fondo_grafico()
    pegar(im, CHIP_B, 540, 215, pop(tl, 0.0))
    C_MUESTRAS(im, tl, 540, 345)
    if tl > 0.5: pegar(im, pastilla('muestras al mes', 62, fondo=TINTA), 540, 470, pop(tl, 0.5))
    n = int(min(10, max(0, (tl - 0.05) / 0.12)))
    for i in range(n):
        x = 150 + (i % 5) * 195; y = 690 - (i // 5) * 140
        pegar(im, CAJA, x, y, 1.0)
    return im


def g_un_video(tl, T):                # "el problema real era que siguieran publicando" (31.98-33.96): la mayoria se apaga
    im = fondo_grafico()
    for i in range(10):
        x = 150 + (i % 5) * 195; y = 300 + (i // 5) * 210
        gris = tl > 0.55 + (i % 7) * 0.07 and i not in (2, 8)
        pegar(im, GRISP if gris else GENTE[i % 3], x, y, pop(tl, 0.02 + i * 0.03))
    if tl > 1.05: pegar(im, pastilla('1 video y chao', 66, fondo=ROJO), 540, 655, lerp(0.86, 1, pop(tl, 1.05)))
    return im


def g_cuatro(tl, T):                  # "hay cuatro cosas que te pueden ahorrar mucha plata" (47.84-51.80)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for i in range(4):
        k = pop(tl, 0.1 + i * 0.15)
        if k <= 0: continue
        x = 160 + i * 253; y = 400
        d.rounded_rectangle([x - 115, y - 140, x + 115, y + 140], radius=30, fill=(255, 255, 255), outline=TINTA, width=8)
        d.text((x, y), str(i + 1), font=font(150), fill=VERDE_OSC, anchor='mm')
    if tl > 1.9: pegar(im, pastilla('4 cosas', 76, fondo=TINTA), 540, 650, pop(tl, 1.9))
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
P_CHICO, P_GRANDE = (p.resize((380, 418), Image.LANCZOS) for p in (P_CHICO, P_GRANDE))


def g_perfiles(tl, T):                # "...convence mucho mas que una cuenta enorme que nunca lo ha vivido" (57.30-59.02)
    im = fondo_grafico()
    pegar(im, P_GRANDE, 790, 450, lerp(1.25, 0.85, ease((tl - 0.8) / 0.4)) * pop(tl, 0.0))
    pegar(im, P_CHICO, 280, 450, lerp(0.75, 1.15, ease((tl - 0.8) / 0.4)) * pop(tl, 0.1))
    if tl > 1.0: pegar(im, _texto_g('>', 150, VERDE_OSC), 535, 450, pop(tl, 1.0))
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
CAL = _calendario(280)


def _moneda(tam=200):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=(255, 205, 60, 255), outline=TINTA + (255,), width=7)
    d.text((tam / 2, tam / 2), '$', font=font(int(tam * .6)), fill=TINTA + (255,), anchor='mm'); return c
MONEDA_G = _moneda(280)


def g_razon(tl, T):                   # "ganar algo por cada venta (70.62) o volver a trabajar contigo cada mes (72.16)"
    im = fondo_grafico()
    if tl > 0.15: pegar(im, MONEDA_G, 290, 380, lerp(0.8, 1, pop(tl, 0.15))); pegar(im, pastilla('$ por venta', 62, fondo=VERDE_OSC), 290, 610, pop(tl, 0.35))
    if tl > 1.76: pegar(im, CAL, 790, 380, lerp(0.8, 1, pop(tl, 1.76))); pegar(im, pastilla('cada mes', 62, fondo=TINTA), 790, 610, pop(tl, 1.96))
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
        c0 = thumbs[0]; pegar(im, c0, 540, 320, lerp(0.85, 1, pop(tl, 0.0))); pegar(im, CHECK, 540 + c0.width // 2 - 30, 320 - c0.height // 2 + 30, pop(tl, 0.15))
        for i, t in enumerate(thumbs[1:4]):
            x = 210 + i * 330; t0 = 0.4 + i * 0.12
            if tl > t0:
                flecha_recta(d, (540 + (x - 540) * 0.25, 320 + c0.height // 2 + 6), (x, 505), ease((tl - t0) / 0.18))
                pegar(im, t, x, 620, pop(tl, t0 + 0.1))
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


class Nota:
    """Nota de prensa como TARJETA (pedido de revision: frase grande, nunca la pagina entera de letra chica ni una tira sobre blanco):
    una ventana de la captura (frase.js, 3 px por px CSS) ampliada en una tarjeta de 1040x560 en y 180, sobre un fondo real
    desenfocado. v0 / v1 = (centro x, centro y, ancho) de la ventana en px de la captura; las marcas van en px de la captura."""
    CX, CY, CW, CH = 20, 180, 1040, 560

    def __init__(self, png, v0, v1, marcas, fondo, dur_mov=0.6, t_mov=0.0):
        self.im = np.asarray(Image.open(png).convert('RGB')); self.v0, self.v1 = v0, v1 or v0; self.marcas = list(marcas)
        self.fondo = fondo; self.dur_mov = dur_mov; self.t_mov = t_mov

    def _vista(self, tl):
        p = ease((tl - self.t_mov) / self.dur_mov) if self.dur_mov else 0
        return [lerp(a, b, p) for a, b in zip(self.v0, self.v1)]

    def frame(self, tl, T):
        cx, cy, w = self._vista(tl); s = self.CW / w; x0, y0 = cx - w / 2, cy - (self.CH / s) / 2
        M = np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])
        card = cv2.warpAffine(self.im, M, (self.CW, self.CH), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        out = self.fondo.copy(); pil = Image.fromarray(out); d = ImageDraw.Draw(pil)
        d.rounded_rectangle([self.CX - 10, self.CY - 10, self.CX + self.CW + 9, self.CY + self.CH + 9], radius=28, fill=(255, 255, 255))
        out = np.asarray(pil).copy(); out[self.CY:self.CY + self.CH, self.CX:self.CX + self.CW] = card
        return out, (x0, y0, s)

    def a_pantalla(self, rect, tr):
        x0, y0, s = tr; x, y, w, h = rect
        return ((x - x0) * s + self.CX, (y - y0) * s + self.CY, w * s, h * s)


def fondo_real(i, ss):
    """Cuadro real de un video, desenfocado y oscurecido (fondo de las tarjetas)."""
    import subprocess as sp
    raw = sp.run(['ffmpeg', '-v', '0', '-ss', str(ss), '-i', ad(i, 'mp4'), '-frames:v', '1', '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
                  '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    im = Image.frombytes('RGB', (W, H), raw).filter(ImageFilter.GaussianBlur(1.5))     # v02: nitido (Gabriel no quiere fondos borrosos)
    return (np.asarray(im).astype(np.float32) * 0.72).astype(np.uint8)


C3 = lambda r: tuple(v * 3 for v in r)                     # rect CSS de frase.js -> px de la captura
_une = lambda *rs: (min(r[0] for r in rs), min(r[1] for r in rs), max(r[0] + r[2] for r in rs) - min(r[0] for r in rs), max(r[1] + r[3] for r in rs) - min(r[1] for r in rs))
F_BIL = C3(_une(*EJ['bil']))                               # "over $1 billion worth of" + "retail sales" (misma linea)
F_UNO, F_IDEAS, F_MENTE = C3(EJ3['u'][0]), C3(EJ3['u_1'][0]), C3(EJ3['u_2'][1])   # "one-to-one relationship", "sharing ideas with them", "on our minds" (2a linea de la frase)
EJ4 = json.load(open(f'{A}/cap/ent4meta.json'))
F_INS, F_MKT = C3(EJ4['m'][0]), C3(EJ4['m_1'][0])          # "most powerful insights", "connections to marketing"
cen = lambda r: (r[0] + r[2] / 2, r[1] + r[3] / 2)


# ------------------------------------------------------------ fondos y miniaturas
FONDO_P = fondo_real('1061262113579933', 2.0)              # fondo real desenfocado (anuncio de producto de Liquid I.V.) para las tarjetas
FONDO_L = FONDO_P
THUMBS = [_thumb(B1, 30.0, 270, 270), _thumb(L['rosa'], 9.0, 220, 220), _thumb(B2, 24.0, 220, 220), _thumb(L['bolsas'], 12.0, 220, 220)]
bl = lambda h: lienzo(Image.open(f'{A}/bloom/{h}_w.jpg').convert('RGB'), (0, 0, 1400), (70, 70, 1260), nombre=f'bloomnu.com: {h}')
EN = 'www.entrepreneur.com: entrevista al CEO de Liquid I.V.'
EP = f'{A}/cap'
# "Edward Digges with Liquid I.V." MEDIDO por pixeles en la captura (filas 385-411, x 117-489): el rect 'quien' del json cayo una
# linea mas abajo, sobre "Sponsored" (revisar_marcas.py lo mostro).
LPC = (117, 385, 373, 27)
LPF = tuple(2 * v for v in LP['frases']['#LiquidIVPartner'][0])                                   # "#LiquidIVPartner" (medido)
seg = lambda i, ss, txt, **k: clip(i, ss, nombre=f'anuncio-video:{i} (s{ss:g}: {txt})', **k)

# ------------------------------------------------------------ tomas
toma('01', 0.00, 2.10, Serie([(0.00, seg('2383146145805609', 0.2, 'deportista tomando Liquid I.V.')),          # hook: 2 cortes en los primeros 2 s
                              (1.05, seg(B1, 36.0, 'creadora con una lata de Bloom'))]), GAB,
     T_(['Creadores que se quedan'], 190, 74, t0=-1.0, clave={'quedan'}))
toma('02', 2.10, 3.86, Serie([(0.00, Nota(f'{EP}/lp_card_979279478106524.png', (cen(LPC)[0], cen(LPC)[1] + 20, 800), None, [('caja', LPC, 0.25)], FONDO_P)),
                             (0.90, Nota(f'{EP}/lp_card_979279478106524.png', (cen(LPF)[0] + 150, cen(LPF)[1], 520), None, [('sub', LPF, 0.05)], FONDO_P))]), GAB)
S[-1]['fuentes'] = ['tarjeta-biblioteca:979279478106524 (Edward Digges with Liquid I.V.)']
toma('03', 3.86, 6.94, Serie([(0.00, seg(L['bolsas'], 2.0, 'creadora con sobres')), (0.77, seg(B2, 7.0, 'creadora de Bloom en su estudio')),
                              (1.54, seg(L['rayas'], 10.0, 'creadora en la cocina')), (2.31, seg('2027745281964723', 2.0, 'creadora de Liquid I.V.'))]), GAB,
     T_(['¿Qué la hace efectiva?'], 200, 70, t0=0.1, clave={'efectiva?'}))
toma('04', 6.94, 8.70, seg('28530720373295972', 1.0, 'producto de Liquid I.V.'), GAB, logo_arriba(CHIP_L, 0.0, 215))
usar(EN + ' (US$1.000 M)')
toma('05', 8.70, 11.26, Nota(f'{EP}/ent_bil.png', (cen(F_BIL)[0], cen(F_BIL)[1], 1500), (cen(F_BIL)[0], cen(F_BIL)[1], 900), [('caja', F_BIL, 1.05)], FONDO_L, dur_mov=0.7, t_mov=0.2), GAB,
     varios(contador_toma(1000, 1.02, cy=1150, sufijo=' M', tam=100), entre(1.2, 9, lambda pil, tl, T: pegar(pil, pastilla('según su director', 40, fondo=(236, 236, 232), color=GRIS, pad=(30, 16)), 800, 690))))
toma('06', 11.26, 12.92, seg(L['papa'], 2.0, 'creador de Liquid I.V. (papa)'), GAB)
toma('07', 12.92, 15.00, seg(L['rosa'], 1.0, 'creadora preparando Liquid I.V.'), GAB)
usar(EN + ' (one-to-one relationship)')
toma('08', 15.00, 18.66, Serie([(0.00, seg('1094155246768851', 2.4, 'sobre de Liquid I.V. en la botella')),               # "con los que hablan uno a uno"
                                (1.04, seg('1089803047221823', 1.6, 'clienta tomando Liquid I.V.')),                            # "les cuentan ideas en las que estan trabajando"
                                (2.24, seg('1482949820426574', 1.6, 'cliente sonriendo'))]), GAB)                       # "y les preguntan que tienen en la cabeza"
toma('09', 18.66, 20.98, seg('2019305582089395', 0.6, 'anuncio de Liquid I.V. con un equipo de carreras'), GAB)       # "sus mejores ideas de marketing"
toma('10', 20.98, 22.08, Grafico(g_ideas(CHIP_L)), GAB)
toma('11', 22.08, 23.42, seg(B1, 89.0, 'creadora de Bloom con la lata, afuera'), GAB, logo_arriba(CHIP_B, 0.3, 215))
toma('12', 23.42, 24.40, bl('sparkling-energy_1'), GAB)                                                                  # "bebidas energeticas"
toma('13', 24.40, 25.16, Serie([(0.00, bl('protein_0')), (0.38, bl('creatine-gummies_0'))]), GAB)                       # "y suplementos"
toma('14', 25.16, 27.10, Serie([(0.00, seg(B1, 52.0, 'creadora de Bloom en el pasillo')), (0.44, seg(B1, 12.5, 'canasto con latas de Bloom'))]), GAB)   # "para mujeres" / "a lo grande"
toma('15', 27.10, 29.32, Grafico(g_muestras), GAB)
toma('16', 29.32, 30.42, seg(B2, 5.5, 'creadora agarra una lata de Bloom'), GAB)
toma('17', 30.42, 31.98, Serie([(0.00, seg(B1, 17.0, 'creadora de Bloom en la tienda')), (0.52, seg(B1, 2.0, 'creadora de Bloom en el auto')), (1.04, seg(B2, 22.0, 'creadora de Bloom en el escritorio'))]), GAB)
toma('18', 31.98, 33.96, Grafico(g_un_video), GAB)
toma('19', 33.96, 36.96, Mosaico([seg(L['naranja'], 0.5, 'creadora reponiendo Liquid I.V.'), seg(L['depto'], 4.0, 'creador en su depto'),
                                  seg(L['rayas'], 30.0, 'cartera con sobres'), seg(L['cocina'], 0.5, 'creadora en la cocina')]), GAB,
     varios(entre(0, 1.82, T_(['1 grupo'], 200, 72, t0=0.05)), entre(1.82, 9, T_(['Llamada cada semana'], 200, 64, emo='📅'))))
toma('20', 36.96, 39.20, seg(B1, 70.0, 'creadora de Bloom hablando a camara'), GAB,
     entre(0.9, 9, lambda pil, tl, T: (pegar(pil, CHECK, 820, 330, pop(tl, 0)), pegar(pil, pastilla('Este vende', 60, fondo=VERDE_OSC), 820, 470, pop(tl, 0.1)))))
toma('21', 39.20, 40.70, Grafico(g_ejemplo(THUMBS)), GAB)
toma('22', 40.70, 42.76, Serie([(0.00, seg(L['choco'], 1.0, 'manos con taza')), (0.69, seg('1001821399664769', 1.0, 'sobres de Liquid I.V.')),
                                (1.38, seg(B2, 18.2, 'lata de Bloom de cerca'))]), GAB)
toma('23', 42.76, 46.08, seg(B1, 44.0, 'creadora de Bloom hablando con la lata'), GAB)
toma('24', 46.08, 47.84, seg('1693636698843470', 0.9, 'creador sonriendo'), GAB)
toma('25', 47.84, 51.80, Grafico(g_cuatro), GAB)
toma('26', 51.80, 54.94, seg(L['manager'], 8.0, 'creadora Hydration Manager'), GAB, T_(['1 · A quién le habla', '> cuántos seguidores'], 230, 60, t0=0.0, clave={'habla'}))
toma('27', 54.94, 57.30, seg(L['cocina'], 5.8, 'clienta preparando su vaso'), GAB)
toma('28', 57.30, 59.02, Grafico(g_perfiles), GAB)
toma('29', 59.02, 60.80, seg(L['papa'], 10.0, 'creador de Liquid I.V. con gorro'), GAB, T_(['2 · Enséñales qué vende'], 210, 62, t0=0.0, clave={'vende'}))
toma('30', 60.80, 63.18, Mosaico([seg(L['manager'], 50.0, 'creadora Hydration Manager con gorra'), seg(L['rosa'], 10.4, 'creadora con su bebe'),
                                  seg(L['bolsas'], 8.0, 'creadora mostrando sobres'), seg(B1, 80.0, 'creadora de Bloom corriendo')], marca=0, t_marca=0.94), GAB)
toma('31', 63.18, 66.30, seg('1418322423102928', 23.0, 'creadora con su taza'), GAB, T_(['3 · Escúchalos'], 210, 66, t0=0.0, clave={'Escúchalos'}))
toma('32', 66.30, 68.56, Grafico(g_ideas(None, 'Tu próximo anuncio')), GAB)
toma('33', 68.56, 70.40, seg(B2, 28.0, 'creadora de Bloom en el escritorio con la lata'), GAB, T_(['4 · Una razón para seguir'], 210, 60, t0=0.0, clave={'seguir'}))
toma('34', 70.40, 73.56, Grafico(g_razon), GAB)
toma('35', 73.56, 76.26, seg(B1, 22.0, 'creadora de Bloom en la caja de la tienda'), GAB,
     T_(['Guárdalo'], 200, 76, t0=0.05, emo='📌'))
toma('36', 76.26, 77.90, seg(B1, 93.0, 'creadora de Bloom brindando con la lata'), GAB, T_(['Sígueme para más'], 200, 70, t0=0.2, emo='👇'))

# Gabriel cambia de lugar toma a toma (izquierda / derecha / centro)
LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'Ya nos acostumbramos a ver', 'gente hablando de *productos', 'y todos sabemos que son', 'colaboraciones *pagas',
 'Pero entonces,', '¿qué hace que una estrategia', 'de creadores sea', 'realmente *efectiva?',
 'Liquid_I.V., la marca', 'de *electrolitos,', 'que según su director', 'ya pasaba los mil millones', 'de dólares en *ventas,',
 'trata a los suyos', 'como parte de su *equipo',
 'Tienen un grupo chico', 'de clientes *fanáticos', 'con los que hablan', 'uno a *uno',
 'Les cuentan *ideas', 'en las que están trabajando', 'y les preguntan', 'qué tienen en la *cabeza',
 'Su director dice que', 'algunas de sus mejores', 'ideas de *marketing', 'salieron justo de *ahí',
 'Por otro lado, *Bloom,', 'la marca de bebidas *energéticas', 'y *suplementos', 'para *mujeres,',
 'hace algo parecido,', 'pero a lo *grande',
 'Llegó a mandar entre', '10 mil y 20 mil', '*muestras', 'al mes y se dio', 'cuenta de algo',
 'Conseguir *creadores', 'no era el problema,', 'el problema real', 'era que siguieran *publicando',
 'Así que juntó a todos', 'en un mismo *grupo', 'y cada semana', 'les hace *llamadas', 'para mostrarles', 'qué videos están *vendiendo', 'y por qué',
 'Y los videos que más *venden', 'se vuelven el *ejemplo', 'que los demás repiten', 'a su manera',
 'Así, quienes hablan', 'de estas marcas', 'no sienten que les pagaron', 'por un *anuncio,', 'sienten que las están', 'construyendo con ellas',
 'Si vas a armar', 'tu propio grupo de *creadores,', 'hay cuatro cosas', 'que te pueden ahorrar', 'mucha *plata',
 'Primero, escógelos por', 'a quién le van a *hablar,', 'no por cuántos seguidores tienen',
 'Una clienta que vive', 'el *problema', 'convence mucho más', 'que una cuenta *enorme', 'que nunca lo ha *vivido',
 'Segundo, enséñales', 'lo que está *funcionando,', 'muéstrales cada semana', 'qué video *vendió', 'y qué tenía',
 'Tercero, *escúchalos', 'realmente,', 'los que más hablan', 'de tu marca', 'suelen tener las mejores *ideas', 'para tu próximo *anuncio',
 'Y cuarto, dales', 'una razón para *seguir,', 'ya sea ganar algo', 'por cada *venta', 'o volver a trabajar', 'contigo cada *mes',
 'Guárdalo para cuando vayas', 'a contactar a tus', 'próximos *creadores', 'y sígueme para más', 'tips como *este',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal46.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
