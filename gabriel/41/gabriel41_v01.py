"""Video 41 · "El cliente que todavia no tiene marca" (Huel) · v01
Formato pantalla verde, historia de una marca (guia de Gabriel, VIDEO HUEL) + todo lo que Gabriel fue corrigiendo en el 38-40:
- Gabriel cambia de lugar toma a toma (CI / CD / C) y el video termina con su voz (DUR = crudo, sin cola).
- Hook 0-7 s con videos (Danone: gente comiendo, la heladera con sus yogures; Huel desenfocado) y la foto de Ozempic en medio.
- Videos antes que graficos: ningun grafico propio dura mas de ~3,5 s seguido.
- Huel no se nombra ni se lee antes de "Huel llevaba anos..." (29,72 s): los videos de Huel van desenfocados y en las capturas de
  prensa cada "Huel" va tapado (rectangulos medidos, frases_todas).
- Marcas rojas solo sobre rectangulos medidos (pagina_entera.js FRASES) y revisadas con revisar_marcas.py.
Regla 12: nada de Huel junto a medicamentos, sin anuncios de Huel que hablen de bajar de peso (se descartaron 1081914421425045,
1214119060794363, 4239632006288183, 834873872595898 y 967905472378239), sin promesas de salud.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v41')
RAW = f'{A}/dl/crudo41.mp4'
DUR = 71.03                  # termina con la voz (crudo de 71,03 s)
CABEZA = 735
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (120, 120, 118)
HUEL_LOGO = Image.open(f'{A}/cap/huel_logo.png').convert('RGBA')      # SVG del encabezado de huel.com


class ClipBorroso(Clip):
    """Video de Huel antes de la revelacion: desenfocado entero (que no se lea la marca)."""
    def __init__(self, *a, sigma=26, **k):
        super().__init__(*a, **k); self.sigma = sigma

    def frame(self, tl, T, seq=True):
        fr, tr = super().frame(tl, T, seq=seq)
        return cv2.GaussianBlur(np.ascontiguousarray(fr), (0, 0), self.sigma), tr


class ClipZona(Clip):
    """Video con una zona desenfocada (rect en px de pantalla): tapa un texto que nombra a la marca."""
    def __init__(self, *a, zona=(0, 0, 0, 0), **k):
        super().__init__(*a, **k); self.zona = zona

    def frame(self, tl, T, seq=True):
        fr, tr = super().frame(tl, T, seq=seq); fr = np.ascontiguousarray(fr).copy(); x, y, w, h = self.zona
        fr[y:y + h, x:x + w] = cv2.GaussianBlur(fr[y:y + h, x:x + w], (0, 0), 24); return fr, tr


def borroso(i, ss, **k):
    usar('anuncio-video:' + i); return ClipBorroso(ad(i, 'mp4'), ss, **k)


DAN = dict(recorte=(1920, 680, 0, 200), entero=270)                       # video corporativo de danone.com (16:9 con franjas negras)
dan = lambda ss, escena, **k: clip('danone_corp', ss, nombre='danone.com: video corporativo, escena ' + escena, **dict(DAN, **k))


def panel(im, y=300, ancho=W, sigma=40):
    k = ancho / im.width; f = im.resize((ancho, int(im.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(sigma)); c.paste(f, ((W - ancho) // 2, y)); return c


# ------------------------------------------------------------ graficos propios (contenido entre y 180 y 730)
def _texto(s, tam, col=TINTA, peso='ExtraBold'):
    f = font(tam, peso); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _caja(lineas, w=300, h=150, col=(255, 255, 255), tam=46, tinta=TINTA):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=col + (255,), outline=TINTA + (255,), width=6)
    lh = tam * 1.12; y0 = h / 2 - lh * (len(lineas) - 1) / 2
    for i, s in enumerate(lineas): d.text((w / 2, y0 + i * lh), s, font=font(tam), fill=tinta + (255,), anchor='mm')
    return c


def _tarro(col, tam=170, txt=None):
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([w * .1, h * .08, w * .9, h * .98], radius=24, fill=col + (255,), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .06, 0, w * .94, h * .16], radius=14, fill=(250, 250, 248, 255), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .2, h * .40, w * .8, h * .68], radius=10, fill=(255, 255, 255, 255))
    if txt: d.text((w / 2, h * .54), txt, font=font(int(tam * .14)), fill=TINTA + (255,), anchor='mm')
    return c


def _persona(col=TINTA, tam=170):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.28], 180, 360, fill=col + (255,)); return c
PER = _persona()
hlogo = lambda w: HUEL_LOGO.resize((w, int(HUEL_LOGO.height * w / HUEL_LOGO.width)), Image.LANCZOS)


# Coordinador (revision del 41): "graficos chicos con mucho blanco" -> todo llena y 170-730, figuras >= 200 px, textos >= 60 px.
def g_plato(tl, T):                  # "si comes menos (12.08), cada comida tiene que valer por dos (13.52)" (10.56-13.78)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    r = lerp(270, 190, ease((tl - 1.52) / 0.5)) * pop(tl, 0.05)        # el plato se achica en "comes menos"
    if r > 0:
        d.ellipse([540 - r, 450 - r, 540 + r, 450 + r], fill=(255, 255, 255), outline=TINTA, width=12)
        d.ellipse([540 - r * .74, 450 - r * .74, 540 + r * .74, 450 + r * .74], outline=(205, 205, 200), width=8)
    if 1.52 < tl < 2.0: pegar(im, pastilla('Comes menos', 64, fondo=GRIS), 540, 450, pop(tl, 1.52))
    if tl > 2.0: pegar(im, pastilla('Proteína', 66, fondo=VERDE_OSC), 540, 380, lerp(0.7, 1, pop(tl, 2.0)))
    if tl > 2.3: pegar(im, pastilla('Nutrientes', 66, fondo=VERDE_OSC), 540, 520, lerp(0.7, 1, pop(tl, 2.3)))
    if tl > 2.96: pegar(im, _texto('x2', 200, ROJO), 900, 270, lerp(0.6, 1, pop(tl, 2.96)))
    return im


def g_complicado(tl, T):             # "porque sus planes de alimentacion eran demasiado complicados" (22.42-25.90)
    im = fondo_grafico(); d = ImageDraw.Draw(im); rnd = np.random.default_rng(3)
    for k in range(6):
        t0 = 0.05 + k * 0.2
        if tl < t0: continue
        x, y = 200 + (k % 3) * 340, 300 + (k // 3) * 250; ang = rnd.uniform(-12, 12)
        hoja = Image.new('RGBA', (290, 220), (0, 0, 0, 0)); dh = ImageDraw.Draw(hoja)
        dh.rounded_rectangle([0, 0, 289, 219], radius=22, fill=((250, 236, 200) if k % 2 else (236, 236, 232)) + (255,), outline=TINTA + (255,), width=7)
        dh.text((145, 52), 'Plan ' + str(k + 1), font=font(60), fill=TINTA + (255,), anchor='mm')
        for q in range(3): dh.rounded_rectangle([34, 104 + q * 34, 256 - q * 40, 120 + q * 34], radius=8, fill=(190, 190, 186, 255))
        pegar(im, hoja.rotate(ang, expand=True, resample=Image.BICUBIC), x, y, pop(tl, t0))
    if tl > 1.4:
        p = ease((tl - 1.4) / 0.6)
        for a, b in (((120, 200), (960, 680)), ((960, 200), (120, 680)), ((540, 180), (540, 700)), ((100, 440), (980, 440))):
            d.line([a, (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)], fill=ROJO, width=12)
    if tl > 2.86: pegar(im, pastilla('Demasiado complicado', 72, fondo=ROJO), 540, 440, lerp(0.8, 1, pop(tl, 2.86)))
    return im


TARROS = [_tarro(c, 230) for c in ((236, 196, 120), (180, 210, 230), (214, 120, 110), (150, 200, 150))]


def _bolsa(w=330):
    c = Image.new('RGBA', (w, int(w * 1.35)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); W_, H_ = c.size
    d.polygon([(W_ * .12, H_ * .1), (W_ * .88, H_ * .1), (W_ * .95, H_ * .98), (W_ * .05, H_ * .98)], fill=(17, 17, 20, 255))
    d.rectangle([W_ * .12, H_ * .02, W_ * .88, H_ * .12], fill=(40, 40, 44, 255))
    d.rounded_rectangle([W_ * .16, H_ * .40, W_ * .84, H_ * .64], radius=12, fill=(255, 255, 255, 255))
    d.text((W_ / 2, H_ * .52), 'Todo en 1', font=font(62), fill=TINTA + (255,), anchor='mm'); return c
BOLSA = _bolsa()


def g_uno(tl, T):                    # 25.90-29.72: "se arriesgo por lo simple (27.42), todos los nutrientes (27.92) en un solo producto (29.38)"
    im = fondo_grafico()
    p = ease((tl - 2.4) / 0.5)
    for k, t in enumerate(TARROS):
        x0 = 150 + k * 260
        if p < 1: pegar(im, t, lerp(x0, 540, p), lerp(400, 450, p), pop(tl, 0.05 + k * 0.15) * lerp(1, 0.3, p))
    if 1.4 < tl < 2.0: pegar(im, pastilla('Por lo simple', 66, fondo=TINTA), 540, 660, pop(tl, 1.4))
    if 2.0 < tl < 2.75: pegar(im, pastilla('Todos los nutrientes', 64, fondo=GRIS), 540, 660, pop(tl, 2.0))
    if tl > 2.7: pegar(im, BOLSA, 540, 420, lerp(0.6, 1, pop(tl, 2.7)))
    if tl > 3.3: pegar(im, pastilla('Un solo producto', 66, fondo=VERDE_OSC), 540, 690, pop(tl, 3.3))
    return im


def _pieza(txt, col, w=430, h=260, lado='d'):
    c = Image.new('RGBA', (w + 70, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    if lado == 'd':
        d.rounded_rectangle([0, 0, w, h - 1], radius=30, fill=col + (255,), outline=TINTA + (255,), width=8)
        d.ellipse([w - 40, h / 2 - 48, w + 52, h / 2 + 48], fill=col + (255,), outline=TINTA + (255,), width=8)
        d.rectangle([w - 46, h / 2 - 40, w - 4, h / 2 + 40], fill=col + (255,))
        for k, t in enumerate(txt): d.text((w / 2, h / 2 + (k - (len(txt) - 1) / 2) * 70), t, font=font(62), fill=TINTA + (255,), anchor='mm')
    else:
        d.rounded_rectangle([70, 0, w + 69, h - 1], radius=30, fill=col + (255,), outline=TINTA + (255,), width=8)
        d.ellipse([70 - 48, h / 2 - 48, 70 + 48, h / 2 + 48], fill=(250, 250, 248, 255), outline=TINTA + (255,), width=8)
        for k, t in enumerate(txt): d.text((70 + w / 2 + 16, h / 2 + (k - (len(txt) - 1) / 2) * 70), t, font=font(62), fill=TINTA + (255,), anchor='mm')
    return c
P_SUPER, P_DIRECTA = _pieza(['Super-', 'mercados'], (226, 236, 250)), _pieza(['Venta', 'directa'], (212, 240, 224), lado='i')


def g_rompecabezas(tl, T):           # "Y era justo lo que le faltaba a Danone" (46.62-48.32)
    im = fondo_grafico(); p = ease((tl - 0.6) / 0.5)
    pegar(im, P_SUPER, lerp(230, 300, p), 470, pop(tl, 0.05)); pegar(im, P_DIRECTA, lerp(850, 780, p), 470, pop(tl, 0.2))
    pegar(im, pastilla('Danone', 64, fondo=(0, 84, 166)), 270, 250, pop(tl, 0.1)); pegar(im, pastilla('Huel', 64, fondo=TINTA), 810, 250, pop(tl, 0.25))
    if tl > 1.1: pegar(im, _texto('✓', 150, VERDE_OSC), 540, 680, pop(tl, 1.1))
    return im


def _etiqueta(w=380, h=230):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=8)
    for x in range(40, w - 40, 40): d.line([(x, h / 2), (x + 20, h / 2)], fill=(190, 190, 186, 255), width=8)
    return c
ETIQ = _etiqueta()
PER_G = _persona(tam=300)


def g_cliente(tl, T):                # "nace un cliente nuevo (52.12) que todavia no tiene una marca (53.48)" + "la primera marca que lo identifica (54.74) se lo lleva (55.96)"
    im = fondo_grafico()
    pegar(im, PER_G, 280, 470, pop(tl, 0.05)); pegar(im, _texto('?', 190, ROJO), 280, 240, pop(tl, 0.3))
    pegar(im, ETIQ, 780, 430, pop(tl, 0.5))
    if 0.9 < tl < 2.6: pegar(im, pastilla('Sin marca', 66, fondo=TINTA), 780, 640, pop(tl, 0.9))
    if tl > 3.24:                                                          # 54.28 "primera marca"
        pegar(im, hlogo(300), 780, 430, lerp(0.6, 1, pop(tl, 3.24)))
        pegar(im, pastilla('Se lo lleva', 66, fondo=VERDE_OSC), 780, 640, pop(tl, 3.6))
    return im


def g_pasos(tl, T):                  # "la marca que sepa leer esos cambios (63.96) ... a tiempo (65.72) ... la delantera (67.34)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pasos = [(['Cambia el hábito'], 0.05, (236, 236, 232)), (['La marca lo lee'], 1.34, (250, 236, 200)), (['Toma la delantera'], 4.72, (212, 240, 224))]
    for i, (s, t0, col) in enumerate(pasos):
        if tl < t0: continue
        y = 250 + i * 200
        if i: flecha_recta(d, (540, y - 200 + 70), (540, y - 72), ease((tl - t0) / 0.18))
        pegar(im, _caja(s, 760, 140, col, 66), 540, y, lerp(0.86, 1, pop(tl, t0)))
    return im


def desfase(fn, dt):
    return Grafico(lambda tl, T: fn(tl + dt, T))


def _perfil():
    """Perfil real de Instagram de Gabriel (vista publica en celular, sin sesion: ahi no aparece el boton) con el boton
    "Seguir" dibujado debajo del encabezado; la marca roja va sobre ese boton (rectangulo conocido porque lo dibujamos)."""
    ig = Image.open(f'{A}/cap/ig.png').convert('RGB').crop((0, 170, 1290, 725)); k = W / ig.width; ig = ig.resize((W, int(ig.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (255, 255, 255)); c.paste(ig, (0, 90)); d = ImageDraw.Draw(c)
    y0 = 90 + ig.height + 10; d.rounded_rectangle([60, y0, 1020, y0 + 96], radius=18, fill=(0, 149, 246))
    d.text((540, y0 + 48), 'Seguir', font=font(46), fill=(255, 255, 255), anchor='mm')
    return c, (60, y0, 960, 96)
PERFIL, R_SEGUIR = _perfil()


# ------------------------------------------------------------ capturas (2 px por px CSS)
J = lambda n: json.load(open(f'{A}/cap/{n}.json'))
P2 = lambda r: tuple(v * 2 for v in r)
_une = lambda rs: (min(r[0] for r in rs), min(r[1] for r in rs), max(r[0] + r[2] for r in rs) - min(r[0] for r in rs), max(r[1] + r[3] for r in rs) - min(r[1] for r in rs))


def tapada(n):
    """Captura con cada "Huel" tapado (antes de la revelacion)."""
    c = Image.open(f'{A}/cap/{n}.png').convert('RGB'); d = ImageDraw.Draw(c)
    for r in J(n)['frases_todas']['Huel']:
        x, y, w, h = P2(r[0]); d.rounded_rectangle([x - 4, y - 2, x + w + 4, y + h + 2], radius=8, fill=TINTA)
    return np.asarray(c)
RTE, RTEJ = tapada('rte'), J('rte')
FD, FDJ = tapada('fd'), J('fd')
BLK, BLKJ = img(f'{A}/cap/black.png'), J('black')
DANP, DANJ = img(f'{A}/cap/dan.png'), J('dan')
F_BILLION = P2(RTEJ['frases']['close to €1 billion'][0])
F_GLP = [P2(r) for r in FDJ['frases']['consumers on GLP-1s, who have suppressed appetites but still need to ensure they receive their complete nutrients']]
F_4M = P2(_une(BLKJ['frases']['4,000,000 satisfied customers']))
F_DTC = P2(DANJ['frases']['strong digital direct-to-consumer sales'][0])
OZ = panel(Image.open(f'{A}/cap/ozempic.jpg').convert('RGB'), y=330)


# ------------------------------------------------------------ notas como tarjeta (coordinador: "nada de paginas enteras de texto chico")
# Capturas a ancho de celular (390 px CSS, 3 px por px CSS, pagina_movil.js con FRASES medidas en el mismo momento).
M = lambda n: json.load(open(f'{A}/cap/{n}.json'))


def _tapar3(n):
    c = Image.open(f'{A}/cap/{n}.png').convert('RGB'); d = ImageDraw.Draw(c)
    for r in (M(n).get('frases_todas', {}).get('Huel') or []):
        x, y, w, h = [v * 3 for v in r[0]]; d.rounded_rectangle([x - 6, y - 3, x + w + 6, y + h + 3], radius=10, fill=TINTA)
    return c


def tarjeta_nota(fondo, piezas, y0=170, y1=730, sigma=34, etiqueta=None):
    """fondo: PIL real (se desenfoca y oscurece). piezas: [(PIL captura, caja px, ancho en pantalla)].
    Devuelve (lienzo PIL 1080x1920, mapeos) donde mapeos[i](rect_css) -> rect en pantalla (captura 3x)."""
    bg = Image.fromarray(cubrir(fondo)).filter(ImageFilter.GaussianBlur(sigma)); bg = Image.fromarray((np.asarray(bg) * 0.6).astype(np.uint8))
    hs = [(c.crop(b), b, w) for c, b, w in piezas]; alto = sum(int(cc.height * w / cc.width) for cc, b, w in hs) + 24 * (len(hs) - 1) + 60
    if etiqueta is not None: alto += etiqueta.height + 24
    y = y0 + max(0, (y1 - y0 - alto) // 2); cw = max(w for _, _, w in hs) + 60
    d = ImageDraw.Draw(bg); d.rounded_rectangle([(W - cw) / 2, y, (W + cw) / 2, y + alto], radius=34, fill=(255, 255, 255))
    y += 30; mapeos = []
    if etiqueta is not None: bg.paste(etiqueta, (int((W - etiqueta.width) / 2), y), etiqueta); y += etiqueta.height + 24
    for cc, b, w in hs:
        k = w / cc.width; im = cc.resize((w, int(cc.height * k)), Image.LANCZOS); x = (W - w) // 2; bg.paste(im, (x, y))
        mapeos.append(lambda r, x=x, y=y, k=k, b=b: (x + (r[0] * 3 - b[0]) * k, y + (r[1] * 3 - b[1]) * k, r[2] * 3 * k, r[3] * 3 * k))
        y += im.height + 24
    return bg, mapeos


_rte = _tapar3('n_rte')                                                      # 320 px CSS de ancho: la letra queda mas grande
NOTA_RTE, MAP_RTE = tarjeta_nota(_rte.crop((0, 1110, 960, 1660)), [(_rte, (330, 0, 640, 110), 220), (_rte, (0, 600, 960, 890), 960)], y0=150, y1=500)
F_BILLION = MAP_RTE[1](M('n_rte')['frases']['close to €1 billion'][0])
_fd = _tapar3('n_fd')
_bgfd = Image.open(f'{A}/cap/bg_dan16.jpg').convert('RGB').crop((0, 200, 1920, 880))
NOTA_FD0, _ = tarjeta_nota(_bgfd, [(_fd, (30, 330, 960, 710), 960)], etiqueta=pastilla('Food Dive', 50, fondo=(0, 92, 120)))     # titular
NOTA_FD, MAP_FD = tarjeta_nota(_bgfd, [(_fd, (30, 6785, 960, 7105), 1040)], etiqueta=pastilla('Food Dive', 50, fondo=(0, 92, 120)))   # el parrafo
F_GLP = [MAP_FD[0](r) for r in M('n_fd')['frases']['consumers on GLP-1s, who have suppressed appetites but still need to ensure they receive their complete nutrients']]
_bk = Image.open(f'{A}/cap/n_black.png').convert('RGB')
NOTA_BK, MAP_BK = tarjeta_nota(Image.open(f'{A}/cap/bg_glass.jpg').convert('RGB'), [(_bk, (30, 1320, 900, 1470), 960), (_bk, (30, 1505, 820, 1598), 520)],
                               y0=160, y1=600, etiqueta=hlogo(220))
F_4M = _une([MAP_BK[0](r) for r in M('n_black')['frases']['4,000,000 satisfied customers']])

# ------------------------------------------------------------ tomas
toma('01', 0.00, 2.04, Serie([(0.00, dan(26.8, '26.7')), (1.02, dan(28.5, '28.5', vel=0.75))]), GAB)              # "millones de personas empezaban a comer menos"
toma('02', 2.04, 3.58, lienzo(OZ, (0, 0, W), (120, 210, W - 240), nombre='commons.wikimedia.org: Ozempic (foto)'), GAB)  # "por medicamentos como Ozempic"
toma('03', 3.58, 4.54, dan(0.3, '0.0'), GAB)                                                                            # "Danone, la de los yogures" (heladera con Activia y Danone)
toma('04', 4.54, 7.18, borroso('1595225641819088', 1.0), GAB, T_(['¿Cuál?'], 300, 90, t0=0.5))                         # "buscaba una marca..." (Huel desenfocado)
toma('05', 7.18, 10.56, lienzo(NOTA_RTE, (0, 0, W), (20, 30, W - 40), [('caja', F_BILLION, 1.90)], nombre='rte.ie: Danone compra por casi €1.000 M (Huel tapado)'), GAB,
     contador_toma(1000, 1.98, cy=672, prefijo='Casi €', sufijo=' M', tam=82))
toma('06', 10.56, 13.78, Grafico(g_plato), GAB)
toma('07', 13.78, 15.00, dan(10.0, '9.7'), GAB)                                                                         # "Su director general tenia claro..."
toma('08', 15.00, 18.44, Serie([(0.00, lienzo(NOTA_FD0, (0, 0, W), (10, 15, W - 20), nombre='fooddive.com: titular (Huel tapado)')),
                                (0.54, lienzo(NOTA_FD, (0, 0, W), (10, 15, W - 20), [('sub', r, 0.12) for r in F_GLP], nombre='fooddive.com: consumidores de GLP-1'))]), GAB)
toma('09', 18.44, 20.38, borroso('897943063070733', 22.0), GAB)                                                         # "no es una marca que salio de la nada"
usar('anuncio-video:2143082343178303')
toma('10', 20.38, 22.42, ClipZona(ad('2143082343178303', 'mp4'), 5.8, zona=(0, 860, 860, 420)), GAB,                   # el fundador (rotulo "Founder of Huel" tapado)
     varios(contador_toma(80000, 1.08, cy=470, prefijo='-£', tam=110), entre(1.1, 9, lambda pil, tl, T: pegar(pil, pastilla('Fuente: The Grocer', 40, fondo=(236, 236, 232), color=GRIS, pad=(30, 16)), 540, 610))))
toma('11', 22.42, 25.90, Grafico(g_complicado), GAB)
toma('13', 25.90, 29.72, Grafico(g_uno), GAB)
toma('14', 29.72, 30.62, Grafico(lambda tl, T: (lambda im: (pegar(im, hlogo(int(lerp(760, 840, ease(tl / 0.4)))), 540, 450, 1.0), im)[1])(fondo_grafico())), GAB)
S[-1]['fuentes'] = ['logo de huel.com']
toma('15', 30.62, 34.92, clip('3000851350254150', 19.0), GAB)                                                           # "comidas completas en polvo con 40 gramos de proteina" (vaso con "40g protein" desde 32.6)
toma('17', 34.92, 37.90, Serie([(0.00, dan(14.5, '14.4')), (1.75, dan(16.6, '16.6'))]), GAB)                           # "la estrategia de Danone iba mas alla"
toma('18', 37.90, 40.88, Serie([(0.00, dan(53.2, '53.2', vel=0.7)), (1.14, dan(17.8, '17.8', vel=0.7)), (2.42, dan(19.3, '19.2'))]), GAB)   # "Danone vende sobre todo en supermercados"
toma('19', 40.88, 43.76, clip('1139302692155017', 25.0), GAB, T_(['Venta directa por internet'], 200, 62, t0=1.86))     # s25: "Huel shipped directly to your door"
toma('21', 43.76, 46.62, lienzo(NOTA_BK, (0, 0, W), (20, 30, W - 40), [('caja', F_4M, 1.70)], nombre='uk.huel.com: 4.000.000 de clientes'), GAB,
     contador_toma(4, 1.74, cy=680, prefijo='+', sufijo=' millones de clientes', tam=66))
toma('22', 46.62, 48.32, Grafico(g_rompecabezas), GAB)
toma('23', 48.32, 51.54, Serie([(0.00, dan(57.75, '57.7', vel=0.65)), (1.74, dan(47.9, '47.8')), (2.28, dan(12.6, '12.4')), (2.82, dan(27.7, '27.6'))]), GAB,
     varios(entre(1.74, 2.28, T_(['Come'], 200, 64)), entre(2.28, 2.82, T_(['Duerme'], 200, 64)), entre(2.82, 9, T_(['Se cuida'], 200, 64))))  # come 50.06 / duerme 50.60 / se cuida 51.14
toma('24', 51.54, 53.64, Grafico(g_cliente), GAB)
toma('25', 53.64, 54.70, dan(122.9, '122.8'), GAB)
toma('26', 54.70, 56.14, desfase(g_cliente, 3.16), GAB)
toma('27', 56.14, 57.72, clip('1547645686825388', 0.0, vel=0.8), GAB)                                                     # "Huel no tuvo que cambiar su producto" (la caja de prueba)
toma('28', 57.72, 60.14, clip('1318473731360637', 9.0), GAB)                                                              # "la forma de comer de ese tipo de clientes"
toma('29', 60.14, 62.62, Serie([(0.00, dan(29.35, '29.3')), (0.62, dan(61.1, '61.0')), (1.24, dan(65.0, '64.9')), (1.86, dan(54.7, '54.6'))]), GAB)   # rafaga de habitos
toma('30', 62.62, 65.00, Grafico(g_pasos), GAB)
toma('31', 65.00, 66.30, dan(127.75, '127.7', vel=0.77), GAB)
toma('32', 66.30, 67.68, desfase(g_pasos, 3.68), GAB)
toma('33', 67.68, 69.62, clip('1780988933101495', 10.0), GAB)                                                             # "Mandaselo a esa persona..." (tomando Huel)
toma('34', 69.62, 71.03, lienzo(PERFIL, (0, 0, W), (30, 40, W - 60), [('caja', R_SEGUIR, 0.25)], nombre='instagram.com/gabriel.growthp (perfil)'), GAB)  # "y sigueme"

LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'Mientras millones de personas', 'empezaban a comer *menos', 'por medicamentos como *Ozempic,', 'Danone, ~ la de los *yogures', 'buscaba una marca que tuviera', 'algo que esa gente', 'iba a *necesitar',
 'Y la encontró en *Inglaterra,', 'acordó ~ pagar', 'mil millones de *euros', 'por *ella',
 'Y tiene lógica la *inversión,', 'si comes menos', 'cada comida tiene', 'que valer por *dos',
 'Su director general', 'tenía *claro', 'que la gente que usaba', 'estos medicamentos', 'necesitaba alimentos', 'con muchos más *nutrientes',
 'Sin embargo no es una marca', 'que salió de la *nada,', 'su fundador ya había perdido', '80 mil *libras', 'intentando algo *parecido', 'porque sus planes de alimentación', 'eran demasiado *complicados',
 'Pero esta segunda vez', 'se arriesgó por lo *simple,', 'todos los nutrientes', 'en un solo *producto',
 '*Huel', 'llevaba años vendiendo', 'justo *eso,', 'comidas completas en *polvo', 'con 40 gramos de *proteína', 'por cada *porción',
 'Pero la estrategia de *Danone', 'iba más allá que solo', 'llevarse el *producto',
 'Como ya te habrás dado cuenta,', 'Danone vende sobre todo', 'en *supermercados',
 'Huel trajo con ella', 'la especialidad de la', 'venta directa por *internet',
 'Y según la marca', 'ya son más de', '4 millones de *clientes',
 'Y era justo lo que', 'le faltaba a *Danone',
 'Cada vez que algo cambia', 'la forma en que la gente *come,', 'duerme o se *cuida,', 'nace un cliente *nuevo', 'que todavía no tiene una *marca',
 'Y la primera marca', 'que lo *identifica', 'es la que se lo *lleva',
 'Huel no tuvo que cambiar', 'su *producto,', 'lo que cambió fue', 'la forma de *comer', 'de ese tipo de *clientes',
 'Los hábitos de las personas', 'están cambiando más', 'rápido que *nunca',
 'Y la marca que sepa', 'leer esos *cambios', 'y posicionar su producto', 'a *tiempo', 'va a ser la que tome', 'la *delantera',
 'Mándaselo a esa persona', 'que lo necesita *escuchar', 'y sígueme para más', 'videos como *este',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal41.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
