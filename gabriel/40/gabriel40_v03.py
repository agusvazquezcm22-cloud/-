"""Video 40 · "Lo prestado se devuelve" (Ghost) · v03
v03 (correcciones de Gabriel por WhatsApp, 2026-11-23; ver correcciones_para_v03.md): videos en vez de imagenes en
0-3 s (dos cortes), 3-5 s, 12-15 s (fabrica de suplementos + I+D de un sabor nuevo de Oreo), 15-17 s (alguien comiendo los dulces),
17-19 s (Sour Patch Kids), 19-25 s (Oreo), 34 s (revelacion de Ghost), 35-37 s y 47-49 s. Fuentes: Biblioteca de Anuncios
(Mondelez, BPW LAB, Ghost) y videos oficiales de oreo.com.
v02 (feedback de Gabriel en la web de revision, 2026-11-23):
  8,2 s: "dos imagenes, una de un fisicoculturista y un instructor de vuelo" -> fotos (Wikimedia Commons) en "fisicoculturista" y "vuelo".
  11,7 s: "algo relacionado con suplementos deportivos, gente haciendo ejercicio, cortes rapidos" -> cortes de gente entrenando.
  14,1 s: "dejar de inventar sabores... un video de una fabrica de suplementos o algo asi" -> no hay video de fabrica: video de la fruta
          con la que se hace un sabor (trycreate.co) y se aviso.
  40 y 52-70 s: "mas videos... meter videos de la publicidad de ellos... ir turnando graficos con videos" -> anuncios de Ghost
          (Biblioteca de Anuncios) intercalados con los graficos.
  0 s: "cambiar la ubicacion de mi silueta" -> Gabriel cambia de lugar toma a toma. Termina con la voz (sin cola).
Formato pantalla verde, historia de una marca con giro (guia de Gabriel, VIDEO 40) + todo lo que Gabriel y Agus fueron
corrigiendo: Gabriel fijo abajo al centro; portada grande; nada repetido (la portada no vuelve al final: la guia pedia
repetirla nitida, va en su lugar el logo/producto nitido en la revelacion y un cierre con personas de Ghost); marcas rojas
solo sobre rectangulos medidos; cierre con cola.
- La marca se revela en "Les estoy hablando de Ghost" (34,94 s). Antes, el logo de Ghost no se lee: en las fotos de producto
  va desenfocado por zonas (rectangulos medidos sobre cada foto) y en el comunicado de Keurig Dr Pepper va tapado.
- Material real: fotos oficiales de los productos Ghost x Sour Patch Kids / Swedish Fish / Oreo (notas de Stack3d, la tienda
  ya no los tiene), comunicado de KDP, NutraIngredients, Stack3d, Yahoo Finance (Men's Fitness), pagina de marcas de Mondelez,
  logo de Ghost (SVG de su sitio), un sabor propio de Ghost (su tienda) y un anuncio de Ghost (Biblioteca de Anuncios).
- No se consiguio (avisar): foto de los fundadores (va un grafico con su historia), comercial de Oreo (no se baja de YouTube),
  estante de farmacia y busqueda de Mercado Libre (pide iniciar sesion) -> graficos propios; clips de gente tomando Ghost
  (los anuncios activos de Ghost son de ropa).
- Regla 12: sin promesas de energia ni de salud, sin el documento de la demanda, nada que diga que a Ghost le fue mal.
Tiempos de la transcripcion del crudo (84,53 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v40')
RAW = f'{A}/dl/crudo40.mp4'
DUR = 84.53                  # termina con la voz (v02)
CABEZA = 735
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (120, 120, 118)
S3 = lambda n: Image.open(f'{A}/s3d/{n}.jpg').convert('RGB')


# ------------------------------------------------------------ fotos de producto con el logo de Ghost desenfocado (antes de la revelacion)
def tapar(im, rects, sigma=26):
    """Desenfoca solo las zonas del logo de Ghost (rectangulos medidos sobre la foto, en px de la foto)."""
    im = im.copy()
    for x, y, w, h in rects:
        z = im.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(sigma)); im.paste(z, (x, y))
    return im


def sobre_blanco(path):
    """Foto de producto de la tienda (fondo transparente) sobre blanco: sin esto el fondo sale negro."""
    im = Image.open(path).convert('RGBA'); c = Image.new('RGBA', im.size, (255, 255, 255, 255)); c.alpha_composite(im); return c.convert('RGB')


def panel(im, y=300, ancho=W, fondo_sigma=40):
    """La foto a todo el ancho, sobre su version desenfocada (pantalla completa)."""
    k = ancho / im.width; f = im.resize((ancho, int(im.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(fondo_sigma)); c.paste(f, ((W - ancho) // 2, y)); return c


SPK_BCAA = tapar(S3('where-to-buy-sour-patch-ghost-bcaa'), [(190, 280, 420, 240), (700, 280, 420, 240), (60, 400, 150, 140)])
OREO_WHEY = tapar(S3('where-to-buy-oreo-cookie-ghost-whey'), [(630, 390, 370, 188)])
F_OREO_TUB = (789, 581, 161, 54)          # "OREO" en el tarro, medido por pixeles (componentes blancos de las letras)
SPK_RED = S3('sour-patch-kids-redberry-ghost-legend')
SPK_LEMON = S3('sour-patch-kids-strawberry-lemonade-ghost-legend')
SPK_CAN = S3('sour-patch-kids-ghost-energy')
HIDRA = S3('sour-patch-blue-raspberry-ghost-hydration-drink')

# ------------------------------------------------------------ logos
GLOGO = Image.open(f'{A}/ghost/ghost_logo.png').convert('RGBA')                       # SVG de ghostlifestyle.com
MD = img(f'{A}/cap/mdlz2.png')                                                       # marcas de Mondelez (2 px por px CSS)
MDJ = json.load(open(f'{A}/cap/mdlz2.json'))
_circ = lambda x0, y0, x1, y1: Image.fromarray(MD[y0:y1, x0:x1]).convert('RGBA')
LOGO_OREO, LOGO_SPK = _circ(112, 7368, 431, 7696), _circ(114, 8668, 433, 8997)         # circulos medidos por pixeles


def chip_txt(s, col, tam=46, fg=(255, 255, 255)):
    return pastilla(s, tam, fondo=col, color=fg, pad=(40, 24))
MDLZ, KDP = chip_txt('Mondelēz', (79, 33, 112)), chip_txt('Keurig Dr Pepper', (200, 16, 46))


def glogo(w):
    return GLOGO.resize((w, int(GLOGO.height * w / GLOGO.width)), Image.LANCZOS)


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


def _tarro(col, tam=200, txt=None):
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([w * .1, h * .08, w * .9, h * .98], radius=26, fill=col + (255,), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .06, 0, w * .94, h * .16], radius=16, fill=(250, 250, 248, 255), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .2, h * .40, w * .8, h * .68], radius=12, fill=(255, 255, 255, 255))
    if txt: d.text((w / 2, h * .54), txt, font=font(int(tam * .13)), fill=TINTA + (255,), anchor='mm')
    return c


def g_fundadores(tl, T):             # "La arrancaron en 2016 dos amigos, uno fisicoculturista y el otro instructor de vuelo"
    im = fondo_grafico()
    pegar(im, _texto('2016', 150, VERDE_OSC), 540, 280, lerp(0.86, 1, pop(tl, 0.6)))
    if tl > 1.3: pegar(im, pastilla('2 amigos', 54, fondo=TINTA), 540, 420, pop(tl, 1.3))
    if tl > 2.5: pegar(im, _caja(['Fisicoculturista'], 440, 120, (250, 236, 200), 46), 280, 600, lerp(0.86, 1, pop(tl, 2.5)))
    if tl > 3.7: pegar(im, _caja(['Instructor', 'de vuelo'], 380, 150, (212, 230, 246), 46), 820, 600, lerp(0.86, 1, pop(tl, 3.7)))
    return im


TARROS = [_tarro(c) for c in ((180, 180, 176), (150, 150, 146), (200, 200, 196), (165, 165, 160), (190, 190, 186))]


def g_una_mas(tl, T):                # "en sus inicios era una marca de suplementos deportivos" (sin estante real: grafico)
    im = fondo_grafico()
    for i in range(5): pegar(im, TARROS[i], 140 + i * 200, 420 + (i % 2) * 40, pop(tl, 0.05 + i * 0.12))
    if tl > 1.4: pegar(im, pastilla('Una marca más', 54, fondo=TINTA), 540, 680, pop(tl, 1.4))
    return im


T_VAI, T_CHO = _tarro((246, 236, 205), 230, 'Vainilla'), _tarro((150, 105, 80), 230, 'Chocolate')


def g_sabores(tl, T):                # "dejar de inventar sabores" (13.86-14.66): vainilla y chocolate se tachan
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, T_VAI, 340, 430, pop(tl, 0.05)); pegar(im, T_CHO, 740, 430, pop(tl, 0.2))
    for x, t0 in ((340, 1.72), (740, 2.10)):
        p = ease((tl - t0) / 0.22)
        if p > 0: d.line([(x - 130, 300), (x - 130 + 260 * p, 300 + 260 * p)], fill=ROJO, width=16); d.line([(x + 130, 300), (x + 130 - 260 * p, 300 + 260 * p)], fill=ROJO, width=16)
    return im


def g_x4(tl, T):                     # "A la gente le encanto y en tres anos cuadruplicaron sus ventas"
    im = fondo_grafico(); d = ImageDraw.Draw(im); base = 690
    for i, (alto, t0) in enumerate(((90, 0.2), (180, 0.8), (270, 1.3), (360, 1.75))):
        p = ease((tl - t0) / 0.3)
        if p > 0:
            x = 220 + i * 210; d.rounded_rectangle([x - 70, base - alto * p, x + 70, base], radius=14, fill=VERDE_OSC if i == 3 else (200, 220, 208))
    if tl > 1.68: pegar(im, _texto('x4', 140, VERDE_OSC), 300, 300, lerp(0.86, 1, pop(tl, 1.68)))
    if tl > 1.9: pegar(im, pastilla('en 3 años', 48, fondo=TINTA), 300, 420, pop(tl, 1.9))
    return im


def g_licencia(tl, T):               # "al momento que fue vendida, Mondelez dijo que esa licencia no venia incluida"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, glogo(300), 220, 300, pop(tl, 0.05))
    if tl > 1.3: flecha_recta(d, (400, 300), (560, 300), ease((tl - 1.3) / 0.2)); pegar(im, KDP, 820, 300, pop(tl, 1.5))
    if tl > 2.2:
        pegar(im, MDLZ, 540, 470, pop(tl, 2.2))
        pegar(im, LOGO_OREO.resize((170, 175), Image.LANCZOS), 420, 610, pop(tl, 2.4)); pegar(im, LOGO_SPK.resize((170, 175), Image.LANCZOS), 660, 610, pop(tl, 2.55))
    if tl > 2.9: pegar(im, pastilla('La licencia no venía incluida', 42, fondo=ROJO), 540, 720, pop(tl, 2.9))
    return im


CLIENTE = _texto('🙂', 10)


def _persona(col=TINTA, tam=150):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.28], 180, 360, fill=col + (255,)); return c
PER = _persona()
DULCE = LOGO_SPK.resize((190, 195), Image.LANCZOS)


def g_cliente(tl, T):                # "Si tu cliente te compra por algo que no es tuyo, en realidad nunca fue tu cliente"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, PER, 200, 360, pop(tl, 0.05)); pegar(im, pastilla('Tu cliente', 40, fondo=TINTA), 200, 500, pop(tl, 0.1))
    if tl > 1.7: pegar(im, _caja(['Tu marca'], 260, 110, (236, 236, 232), 44, GRIS), 580, 250, pop(tl, 1.7))
    if tl > 2.0: pegar(im, DULCE, 860, 400, pop(tl, 2.0)); flecha_recta(d, (300, 380), (740, 400), ease((tl - 2.2) / 0.25))
    if tl > 4.9: pegar(im, pastilla('No es tu cliente', 54, fondo=ROJO), 540, 640, lerp(0.86, 1, pop(tl, 4.9)))
    return im


def g_tienda(tl, T):                 # "Es el cliente de otra marca que por ahora esta pasando por tu tienda"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, _caja(['Tu tienda'], 300, 150, (250, 236, 200), 50), 540, 330, pop(tl, 0.05))
    pegar(im, DULCE, 900, 330, pop(tl, 0.7))
    x = lerp(140, 900, ease((tl - 1.0) / 2.2)); pegar(im, PER, x, 560, 1.0)
    flecha_recta(d, (140, 660), (840, 660), ease((tl - 1.0) / 2.2))
    if tl > 0.7: pegar(im, pastilla('Otra marca', 40, fondo=TINTA), 900, 470, pop(tl, 0.75))
    return im


def g_prestado(tl, T):               # "Lo prestado te sirve para que te prueben; lo que hace que vuelvan a comprar tiene que ser tuyo"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    filas = [(300, 'Te prueban', 'Prestado', 1.80, (236, 236, 232)), (560, 'Te vuelven a comprar', 'Tuyo', 2.84, (212, 240, 224))]
    for y, a, b, t0, col in filas:
        if tl < t0: continue
        pegar(im, _caja([a], 470, 130, (255, 255, 255), 44), 290, y, lerp(0.86, 1, pop(tl, t0)))
        tb = t0 + (0.0 if y == 300 else 1.68)
        if tl > tb:
            flecha_recta(d, (535, y), (640, y), ease((tl - tb) / 0.18)); pegar(im, _caja([b], 330, 130, col, 50), 840, y, lerp(0.86, 1, pop(tl, tb + 0.1)))
    return im


def g_marketplace(tl, T):            # "cuando casi todo lo que vendes lo haces por Amazon o Mercado Libre" (sin captura: grafico)
    im = fondo_grafico()
    pegar(im, _tarro((200, 200, 196), 200, 'Tu marca'), 540, 300, pop(tl, 0.05))
    if tl > 2.34: pegar(im, _caja(['Amazon'], 340, 130, (35, 47, 62), 54, (255, 255, 255)), 300, 600, lerp(0.86, 1, pop(tl, 2.34)))
    if tl > 2.84: pegar(im, _caja(['Mercado Libre'], 420, 130, (255, 230, 0), 50, (45, 50, 119)), 780, 600, lerp(0.86, 1, pop(tl, 2.84)))
    return im


def g_datos(tl, T):                  # "ellos se quedan con sus datos y aparte te cobran una comision"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, PER, 200, 330, pop(tl, 0.05)); pegar(im, _caja(['Marketplace'], 380, 130, (236, 236, 232), 46), 760, 330, pop(tl, 0.2))
    if tl > 1.9: flecha_recta(d, (300, 330), (560, 330), ease((tl - 1.9) / 0.2)); pegar(im, pastilla('Sus datos', 44, fondo=TINTA), 430, 250, pop(tl, 1.9))
    if tl > 3.3: pegar(im, pastilla('+ comisión', 56, fondo=ROJO), 760, 520, lerp(0.86, 1, pop(tl, 3.3)))
    return im


def g_tuyo(tl, T):                   # "Vender ahi esta bien para que te conozcan, pero ese cliente lo tienes que llevar a algo tuyo" + "tu tienda, tu WhatsApp, tus correos"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, _caja(['Amazon /', 'Mercado Libre'], 380, 150, (236, 236, 232), 44), 240, 400, pop(tl, 0.05))
    if tl > 1.48: pegar(im, pastilla('Te conocen', 40, fondo=TINTA), 240, 560, pop(tl, 1.48))
    if tl > 3.3:
        flecha_recta(d, (440, 400), (600, 400), ease((tl - 3.3) / 0.2))
        k = pop(tl, 3.5); r = 175 * lerp(0.86, 1, k)
        if k > 0: d.ellipse([800 - r, 400 - r, 800 + r, 400 + r], fill=VERDE_OSC, outline=TINTA, width=7); d.text((800, 400 if tl < 4.1 else 300), 'Tuyo', font=font(64), fill=(255, 255, 255), anchor='mm')
    for i, (e, t0) in enumerate((('🛒', 4.12), ('💬', 4.66), ('✉️', 5.26))):
        if tl > t0: pegar(im, emoji(e, 90), 700 + i * 100, 430, pop(tl, t0))
    return im


# ------------------------------------------------------------ capturas
KD = img(f'{A}/cap/kdp_full.png'); KDJ = json.load(open(f'{A}/cap/kdp_full.json'))   # comunicado de KDP (2 px por px CSS)


def _kdp_tapado():
    """El comunicado con cada GHOST tapado (rectangulos medidos por pagina_entera.js, frases_todas['GHOST']): la marca se
    revela despues ("Les estoy hablando de Ghost")."""
    c = Image.fromarray(KD).convert('RGB'); d = ImageDraw.Draw(c)
    for r in KDJ['frases_todas']['GHOST'] + (KDJ['frases_todas'].get('Ghost') or []):
        x, y, w, h = [v * 2 for v in r[0]]; d.rounded_rectangle([x - 4, y - 2, x + w + 4, y + h + 2], radius=8, fill=TINTA)
    return np.asarray(c)
KDT = _kdp_tapado()
P2 = lambda r: tuple(v * 2 for v in r)
F_990, F_60 = P2(KDJ['frases_todas']['$990 million'][0][0]), P2(KDJ['frases_todas']['60%'][1][0])     # el 60 % de la misma frase que los US$990 M
NU, NUJ = img(f'{A}/cap/nut_t.png'), json.load(open(f'{A}/cap/nutmeta.json'))       # NutraIngredients (3 px por px CSS)
SK, SKJ = img(f'{A}/cap/s3d_t.png').copy(), json.load(open(f'{A}/cap/s3dmeta.json'))
SK[990:, 1635:] = 255; SK[270:745, :] = 255                                                                # columna derecha de Stack3d: publicidad de otras marcas
YA, YAJ = img(f'{A}/cap/yah2_a.png'), json.load(open(f'{A}/cap/yah2meta.json'))     # Yahoo Finance / Men's Fitness (3 px)
P3 = lambda r: tuple(v * 3 for v in r)
_une = lambda *rs: (min(r[0] for r in rs), min(r[1] for r in rs), max(r[0] + r[2] for r in rs) - min(r[0] for r in rs), max(r[1] + r[3] for r in rs) - min(r[1] for r in rs))
F_OREO_MD = _une((112, 7368, 319, 328), P2(MDJ['frases']['OREO'][0]))               # circulo + nombre OREO en la pagina de Mondelez


def _oscurece(im, t0, dur):
    base = np.asarray(im).astype(np.float32)
    return Grafico(lambda tl, T: Image.fromarray((base * lerp(1.0, 0.35, ease((tl - t0) / dur))).astype(np.uint8)))


def desfase(fn, d):
    """El mismo grafico, pero arrancando d segundos mas adelante (cuando la toma empieza despues de un video)."""
    return Grafico(lambda tl, T: fn(tl + d, T))


# ------------------------------------------------------------ tomas
PORT = panel(SPK_BCAA.crop((60, 0, 1200, 840)), y=290)
toma('01', 0.00, 2.88, Serie([(0.00, clip('1076201771972003', 1.0, nombre='anuncio-video:1076201771972003 (fabrica de suplementos BPW LAB)')),
                                (1.44, clip('oreo1', 2.0, nombre='oreo.com: video oficial (cinta de galletas)'))]), GAB,
     T_(['Casi US$1.000 millones'], 180, 76, t0=-1.0, clave={'US$1.000'}))
S[-1]['fuentes'] = ['stack3d.com: Ghost BCAA Sour Patch Kids / Swedish Fish (logo de Ghost desenfocado)']
toma('02', 2.88, 5.34, clip('oreo2', 0.3, nombre='oreo.com: video oficial (galletas en la mano)'), GAB)
FOTO_BB = Image.open(f'{A}/wiki/fuller.jpg').convert('RGB')                          # fisicoculturista (Wikimedia Commons, 960 px)
FOTO_PI = Image.open(f'{A}/wiki/piloto.jpg').convert('RGB')                          # piloto (Wikimedia Commons)
toma('03', 5.34, 9.92, Serie([
    (0.00, Grafico(g_fundadores)),                                                                                 # "La arrancaron en 2016 dos amigos"
    (2.30, lienzo(panel(FOTO_BB, y=200, ancho=760), (0, 0, W), (30, 50, W - 60), nombre='commons.wikimedia.org: fisicoculturista')),   # "fisicoculturista"
    (3.40, lienzo(panel(FOTO_PI, y=200, ancho=900), (0, 0, W), (30, 50, W - 60), nombre='commons.wikimedia.org: piloto')),            # "instructor de vuelo"
]), GAB, varios(entre(2.30, 3.40, T_(['Fisicoculturista'], 180, 66)), entre(3.40, 9, T_(['Instructor de vuelo'], 180, 66))))
toma('04', 9.92, 12.16, Serie([(0.00, clip('c12', 0.3, nombre='video: gente entrenando (corte 1)')), (0.56, clip('c12', 2.6, nombre='video: gente entrenando (corte 2)')),
                                (1.12, clip('c12', 5.0, nombre='video: gente entrenando (corte 3)')), (1.68, clip('c12', 7.4, nombre='video: gente entrenando (corte 4)'))]), GAB)
toma('05', 12.16, 14.98, Serie([(0.00, clip('1682018132853811', 0.3, nombre='anuncio-video:1682018132853811 (fabrica de suplementos BPW LAB)')),
                                  (1.54, clip('1085634730925120', 18.7, nombre='anuncio-video:1085634730925120 (Mondelez: meses de I+D para un sabor de Oreo)'))]), GAB)
toma('06', 14.98, 16.86, clip('1164922273154531', 39.0, nombre='anuncio-video:1164922273154531 (comiendo Chips Ahoy)'), GAB)
toma('07', 16.86, 18.92, clip('1164922273154531', 49.3, nombre='anuncio-video:1164922273154531 (Sour Patch Kids)'), GAB)   # "Sour Patch Kids"
OW = panel(OREO_WHEY.crop((300, 300, 1320, 1000)), y=260); kow = W / 1020
toma('08', 18.92, 22.14, Serie([(0.00, clip('1164922273154531', 59.0, nombre='anuncio-video:1164922273154531 (comiendo Oreo)')),
                                (1.60, clip('oreo5', 1.0, nombre='oreo.com: anuncio oficial de Oreo'))]), GAB)    # "y Oreo" ... "como Oreo"    # "y Oreo" ... "como Oreo"
toma('09', 22.14, 25.32, clip('oreo4', 0.5, nombre='oreo.com: video oficial (galleta en leche)'), GAB)
toma('10', 25.32, 28.32, Grafico(g_x4), GAB)
toma('11', 28.32, 34.10, Serie([
    (0.00, lienzo(KDT, (0, 150, 1640), (60, 200, 1420), nombre='news.keurigdrpepper.com: titulo (GHOST tapado)')),                                  # "la empresa duena de Dr Pepper"
    (2.34, lienzo(KDT, (640, 2566, 1000), None, [('caja', F_990, 0.78)], nombre='news.keurigdrpepper.com: US$990 M')),                              # "pagara casi mil millones"
    (4.26, Lienzo(KDT, (640, 2566, 1000), (0, 2566, 1000), [('caja', F_60, 0.90)], dur_mov=0.4)),                                                   # "con mas de la mitad"
]), GAB)
toma('12', 34.10, 35.24, Serie([(0.00, lienzo(np.asarray(Image.fromarray(np.asarray(PORT)).filter(ImageFilter.GaussianBlur(30))), (0, 0, W), nombre='portada desenfocada')),
                                (0.84, clip('1521932906196474', 1.0, nombre='anuncio-video:1521932906196474 (Ghost, revelacion)'))]), GAB,
     entre(0.84, 9, lambda pil, tl, T: pegar(pil, glogo(int(lerp(700, 760, ease(tl / 0.3)))), 540, 330, 1.0)))
S[-1]['fuentes'] = ['logo de ghostlifestyle.com']
toma('13', 35.24, 37.02, clip('2447289685760086', 28.0, nombre='anuncio-video:2447289685760086 (Mondelez: sus marcas en la tienda)'), GAB)
toma('14', 37.02, 39.68, Serie([
    (0.00, lienzo(MD, (0, 0, 1640), None, nombre='mondelezinternational.com: nuestras marcas')),
    (0.70, lienzo(MD, (0, 7150, 1200), None, [('caja', F_OREO_MD, 0.26)], nombre='mondelezinternational.com: Oreo')),        # "la duena de Oreo"
]), GAB)
toma('15', 39.68, 43.96, Grafico(g_licencia), GAB)
toma('16', 43.96, 47.04, Serie([
    (0.00, lienzo(NU, (0, 974, 1300), None, [('sub', P3(NUJ['t_1'][0]), 0.66)], nombre='nutraingredients.com: demanda')),                        # "los demando"
    (1.30, lienzo(SK, (0, 700, 2460), None, [('sub', P3(SKJ['t'][0]), 0.98)], nombre='stack3d.com: fin de la alianza')),                         # "la alianza termino"
]), GAB)
toma('17', 47.04, 49.00, clip('5575098182714271', 5.0, nombre='anuncio-video:5575098182714271 (Ghost)'), GAB)
toma('18', 49.00, 52.42, lienzo(YA, (0, 1000, 1500), (0, 1100, 1500), [('caja', P3(YAJ['a'][0]), 1.52, 2.64), ('caja', P3(YAJ['a_1'][0]), 2.64)], nombre='finance.yahoo.com: Applied Nutrition + Sour Patch Kids', dur_mov=0.5), GAB)
toma('19', 52.42, 54.06, clip('1030353103112065', 5.0, nombre='anuncio-video:1030353103112065 (Ghost)'), GAB)
toma('19b', 54.06, 57.60, desfase(g_cliente, 1.64), GAB)
toma('20', 57.60, 60.56, Grafico(g_tienda), GAB)
toma('21', 60.56, 62.72, clip('1883242572837077', 1.0, nombre='anuncio-video:1883242572837077 (Ghost)'), GAB)
toma('21b', 62.72, 65.20, desfase(g_prestado, 2.16), GAB)
toma('22', 65.20, 68.54, Grafico(g_marketplace), GAB)
toma('23', 68.54, 70.30, clip('2412614689247319', 3.0, nombre='anuncio-video:2412614689247319 (Ghost)'), GAB)
toma('23b', 70.30, 72.24, desfase(g_datos, 1.76), GAB)
toma('24', 72.24, 74.30, clip('1552565936020274', 0.5, nombre='anuncio-video:1552565936020274 (Ghost)'), GAB)
toma('24b', 74.30, 77.94, desfase(g_tuyo, 2.06), GAB)
toma('25', 77.94, 80.16, lienzo(panel(sobre_blanco(f'{A}/ghost/ghost-legend-v4-blue-raspberry_0.jpg'), y=200), (0, 0, W), (40, 60, W - 80), nombre='ghostlifestyle.com: Legend Blue Raspberry (sabor propio)'), GAB)
toma('26', 80.16, 85.43, Serie([
    (0.00, lienzo(Image.fromarray(cubrir(Image.open(f'{A}/ghost/blog/022_Bulking_Szn_Blog_Cover.png').convert('RGB'), ancla=(0.42, 0.5))), (0, 0, W), (30, 50, W - 60), nombre='ghostlifestyle.com (blog): clienta con Ghost')),
    (2.30, clip('1556799275853120', 2.0, nombre='anuncio-video:1556799275853120 (Ghost)')),
]), GAB, T_(['¿Tendrías con qué seguir?'], 180, 74, t0=2.3, emo='👇'))
# v02: Gabriel cambia de lugar toma a toma (izquierda / derecha / centro)
LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'A una marca de *suplementos', 'le pagaron casi', 'mil millones de *dólares', 'y meses después', 'le quitaron los *sabores', 'con los que se hizo *famosa',
 'La arrancaron en *2016', 'dos *amigos,', 'uno había sido ~ *fisicoculturista', 'y el otro instructor de *vuelo',
 'En sus inicios era', 'una marca de suplementos *deportivos',
 'Hasta que se les ocurrió', 'algo muy *simple,', 'dejar de inventar *sabores', 'y usar los *dulces', 'que la gente ya *amaba',
 'Entre ellos Sour Patch *Kids', 'y *Oreo',
 'Y piénsalo,', 'si ves una *proteína', 'con un sabor que ya conoces', 'como *Oreo', 'no tienes que *convencerte', 'de que es *rica', 'Eso ya lo sabes desde *niño',
 'A la gente le *encantó', 'y en tres años', 'cuadruplicaron sus *ventas',
 'Esto causó que en *2024', 'la empresa dueña de Dr *Pepper', 'pagara casi mil millones de *dólares', 'por quedarse con más', 'de la mitad de la *marca',
 'Les estoy hablando de *Ghost,', 'pero esos sabores', 'nunca fueron *suyos',
 'Mondelēz, la dueña de *Oreo,', 'se los prestaba', 'con una *licencia',
 'Lo que ellos no esperaban', 'es que al momento', 'que fue *vendida,', 'Mondelēz dijo que esa *licencia', 'no venía *incluida',
 'Incluso los *demandó', 'y en 2025', 'la alianza *terminó',
 'Ghost se quedó sin', 'sus sabores *estrella', 'y en *2026', 'como era de *esperarse,', 'otra marca de *suplementos', 'firmó con *ellos',
 'Y esto es lo que más', 'me deja *pensando', 'Si tu cliente te compra', 'por algo que no es *tuyo,', 'en realidad nunca fue tu *cliente',
 'Es el cliente de otra *marca', 'que por ahora está pasando', 'por tu *tienda',
 'Lo *prestado', 'te puede servir', 'para que te *prueben,', 'pero lo que hace que', 'vuelvan a *comprar', 'tiene que ser *tuyo',
 'Y pasa igual cuando', 'casi todo lo que vendes', 'lo haces por *Amazon', 'o Mercado *Libre',
 'Si el cliente compra ahí,', 'ellos se quedan con sus *datos', 'y aparte te cobran', 'una *comisión',
 'Vender ahí está bien', 'para que te *conozcan,', 'pero ese cliente lo tienes', 'que llevar a algo *tuyo',
 'Tu tienda, tu WhatsApp, tus *correos',
 'Ghost tuvo que salir', 'a crear sus propios *sabores',
 'Si tú te has preguntado', 'si te sacan mañana', 'de *Amazon,', '¿tendrías con qué *seguir?', 'Te leo en los *comentarios',
]
# las ultimas 5 palabras de la transcripcion repiten "Te leo en los comentarios" (error de la transcripcion): se descartan
SUBS = armar_tarjetas(json.load(open(f'{A}/pal40.json'))[:-5], GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
