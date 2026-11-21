"""Video 37 · "Lemme vs IM8: ¿quién tiene mejor estrategia?" · v02
Formato VS (como el 35). Lemme SIEMPRE a la izquierda, IM8 a la derecha. Gabriel fijo abajo al centro en todas las tomas.
OJO: la guia de Gabriel no trae este video ("VIDEO 37" esta vacio en el documento): la lista de tomas sale de lo que dice
en el crudo y de las reglas del 35. Tiempos de la transcripcion del crudo (71,27 s).
v02 (pedido de Agus): cierre con cola (el crudo entero + 0,9 s sobre la portada) y sonidos nuevos (ver sonido37_v02.py).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v37')
I8 = os.environ.get('GAB_IM8', os.path.join(A, '..'))          # material de IM8 juntado para el video 32 (cap/im8, dl/)
RAW = f'{A}/dl/crudo37.mp4'
DUR = 72.15                  # 71,27 del crudo + 0,88 de cola
CABEZA = 615                 # fila del crudo donde esta el tope de su cabeza (medido: 599-634)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)

L = dict(purr_mano='4656954237957048', todo25='1784818685904862', debloat_mano='2771485959914179', hinchada='1415643273607782', torta='1162548296330796',
         frasco='1762866821460385', brunch='1546668280292013')
I = dict(medicos='2165878043993348', kit='2184389968845356', sueno='2017776215600223', botella='1636883441125367', prueba='1030426816693865', beckham='961654143231799',
         articulaciones='1134488486192618', almuerzo='996683953451195',
         v_sabalenka='2370251763783969', v_creador='2115444616000712', v_famosos='2302752947125995', v_vaso='1737856330622361', v_creadora='1096216096310988',
         v_rodillas='29066418076358871', v_giannis='997930503365973')

# ------------------------------------------------------------ logos
def _chip_i():
    lg = Image.open(f'{I8}/dl/im8logo.png').convert('RGBA'); lg = lg.resize((int(lg.width * 62 / lg.height), 62), Image.LANCZOS)
    c = Image.new('RGBA', (lg.width + 70, 104), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, 103], radius=28, fill=(255, 255, 255, 255), outline=(225, 225, 220, 255), width=3)
    c.paste(lg, (35, 21), lg); return c
CHIP_I = _chip_i()
CHIP_L = pastilla('lemme', 62, fondo=(203, 178, 232), color=TINTA, pad=(46, 18))      # no hay archivo del logo: va el nombre en su lila


def G2(fn, chip=None, y1=1100, k=0.86, y=196):
    usar('grafico:' + fn.__name__); base = _va._puntos(chip)
    def f(tl, T):
        g = fn(tl, T).crop((0, 290, W, y1)); g = g.resize((int(W * k), int((y1 - 290) * k)), Image.LANCZOS)
        im = base.copy(); im.paste(g, ((W - g.width) // 2, y)); return im
    return Grafico(f)


# ------------------------------------------------------------ portada: los dos productos
def _producto(im, caja, alto):
    fondo = Image.fromarray(cubrir(im, W // 2, H)).filter(ImageFilter.GaussianBlur(46)); w0, h0 = im.size
    p = im.crop((int(caja[0] * w0), int(caja[1] * h0), int(caja[2] * w0), int(caja[3] * h0))); p = p.resize((int(p.width * alto / p.height), alto), Image.LANCZOS)
    m = Image.new('L', p.size, 0); ImageDraw.Draw(m).rounded_rectangle([14, 14, p.width - 15, p.height - 15], radius=40, fill=255); m = m.filter(ImageFilter.GaussianBlur(12))
    fondo.paste(p, ((W // 2 - p.width) // 2, 312), m); return fondo


def _vs():
    lem = Image.open(f'{A}/cap/lps_00.png').convert('RGB').crop((0, 430, 1640, 1730))
    c = Image.new('RGB', (W, H)); c.paste(_producto(lem, (0.20, 0.03, 0.80, 0.97), 468), (0, 0)); c.paste(_producto(Image.open(ad(I['prueba'])).convert('RGB'), (0.20, 0.09, 0.80, 0.47), 468), (W // 2, 0))
    d = ImageDraw.Draw(c); d.rectangle([W // 2 - 3, 0, W // 2 + 2, H], fill=(255, 255, 255))
    d.ellipse([W // 2 - 62, 484, W // 2 + 62, 608], fill=TINTA, outline=(255, 255, 255), width=6); d.text((W // 2, 546), 'VS', font=font(60), fill=(255, 255, 255), anchor='mm')
    return c
VS = _vs()
PORTADA = lambda: lienzo(VS, (0, 0, W), (16, 20, W - 32), nombre='portada')


# ------------------------------------------------------------ graficos propios
def _mini(png, y0, w=280):
    t = Image.fromarray(img(png)[y0:y0 + 1700]).resize((w, int(1700 * w / 1640)), Image.LANCZOS)
    c = Image.new('RGBA', (w + 16, t.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], radius=30, fill=TINTA + (255,))
    m = Image.new('L', t.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, t.width - 1, t.height - 1], radius=24, fill=255); c.paste(t, (8, 8), m); return c
PAGS = [(_mini(f'{A}/cap/lpd_00.png', 512), 'Debloat', 0.55), (_mini(f'{A}/cap/lpp_00.png', 432), 'Purr', 1.05), (_mini(f'{A}/cap/lps_00.png', 432), 'Sleep', 1.5)]


def g_paginas(tl, T):                # "una pagina distinta para cada producto"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n, (mi, nombre, t0) in enumerate(PAGS):
        x = 205 + n * 335; k = pop(tl, t0)
        if k > 0: pegar(im, mi, x, 600, lerp(0.86, 1, k))
        if k > 0.6: txt(d, (x, 830), nombre, 56, TINTA)
    return im


def _persona(col=TINTA, tam=96):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.ellipse([tam * .32, tam * .06, tam * .68, tam * .42], fill=col + (255,)); d.pieslice([tam * .1, tam * .48, tam * .9, tam * 1.5], 180, 360, fill=col + (255,)); return c
PERS = _persona()


def g_tiktok(tl, T):                 # "13 millones de dolares en TikTok Shop en un solo mes ... miles de creadores ganando comision"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    k = pop(tl, 0.80, 0.2)
    if k > 0:
        c = Image.new('RGBA', (900, 240), (0, 0, 0, 0)); ImageDraw.Draw(c).text((450, 120), 'US$13 M', font=font(196), fill=TINTA + (255,), anchor='mm'); pegar(im, c, 540, 440, lerp(0.86, 1, k))
    if tl > 1.95: txt(d, (540, 600), 'en TikTok Shop · en un mes', 54, GRIS, 'SemiBold')
    for n in range(9):
        kk = pop(tl, 3.36 + 0.07 * n, 0.14)
        if kk > 0: pegar(im, PERS, 140 + n * 100, 760, kk)
    if tl > 4.7: pegar(im, pastilla('% por cada venta', 52, fondo=VERDE_OSC), 540, 900, lerp(0.85, 1, pop(tl, 4.7)))
    return im


def _caja(s, w=330, h=160, col=(255, 255, 255), tam=52):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=col + (255,), outline=TINTA + (255,), width=7)
    d.text((w / 2, h / 2), s, font=font(tam), fill=TINTA + (255,), anchor='mm'); return c
C_CRECE, C_GANAN, C_TT, C_META = _caja('La marca crece', 470), _caja('Ellos ganan', 400, col=(212, 240, 224)), _caja('TikTok Shop', 380), _caja('Meta', 300, col=(214, 228, 250))


def g_crece(tl, T):                  # "si la marca crece, ellos tambien ganan"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_CRECE, 540, 430, pop(tl, 0.5)); flecha_recta(d, (540, 525), (540, 660), ease((tl - 1.5) / 0.22), color=VERDE_OSC); pegar(im, C_GANAN, 540, 760, pop(tl, 1.7))
    return im


def g_llevar(tl, T):                 # "Lemme podria llevar los videos de sus creadores a Meta"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_TT, 290, 600, pop(tl, 0.1)); flecha_recta(d, (495, 600), (640, 600), ease((tl - 1.0) / 0.25)); pegar(im, C_META, 810, 600, pop(tl, 1.55))
    return im


def _hoja(tam=120):
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.rounded_rectangle([0, 0, tam - 1, c.height - 1], radius=16, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=7)
    d.rectangle([14, 14, tam - 15, 46], fill=TINTA + (255,))
    for y in (68, 92, 116): d.line([(16, y), (tam - 30, y)], fill=GRIS + (255,), width=7)
    return c
HOJA = _hoja(); PERS3 = [_persona(c, 120) for c in ((120, 124, 132), (30, 150, 90), (227, 38, 46))]


def g_avatar(tl, T):                 # "una pagina distinta segun el avatar al que se le habla"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n in range(3):
        x = 240 + n * 300; t0 = 0.9 + 0.5 * n
        pegar(im, PERS3[n], x, 420, pop(tl, 0.1 + 0.12 * n)); flecha_recta(d, (x, 500), (x, 620), ease((tl - t0) / 0.2), ancho=10); pegar(im, HOJA, x, 730, pop(tl, t0 + 0.15))
    return im


# ------------------------------------------------------------ capturas
LM = json.load(open(f'{A}/cap/l_fbmeta.json')); IM = json.load(open(f'{A}/cap/i_fbmeta.json')); DEB = json.load(open(f'{A}/cap/debmeta.json'))
LG, IG = img(f'{A}/cap/l_fbg0.png'), img(f'{A}/cap/i_fbg0.png')
_rl = tuple(v * 2 for v in LM['results'][:4]); _ri = tuple(v * 2 for v in IM['results'][:4])
BUYP = img(f'{I8}/cap/im8/y00700.png'); P3 = lambda r: tuple(v * 3 for v in r)
V_BUY = (640, 40, 620); BUY = dict(plan=(676, 112, 556, 44), kit=(680, 207, 300, 26))
def _tira():
    a = img(f'{I8}/cap/im8/y03650.png'); b = img(f'{I8}/cap/im8/y04600.png'); c = img(f'{I8}/cap/im8/y06200.png')
    t = np.concatenate([a, b[(5250 - 4600) * 3:], c[:2400]], 0); return cv2.resize(t, (1920, t.shape[0] // 2), interpolation=cv2.INTER_AREA)
TIRA = _tira()

# ------------------------------------------------------------ tomas
toma('01', 0.00, 3.84, PORTADA(), GAB, T_(['Lemme vs IM8: ¿quién', 'tiene mejor estrategia?'], 196, 60, t0=-1.0, clave={'vs'}, emo='🤯'))
toma('02', 3.84, 8.66, Serie([(0, lienzo(LG, (0, 0, 1700), (0, 300, 1500), [('caja', _rl, 0.7), ('flecha_ad', _rl, 0.7)], nombre='biblioteca Lemme:cabecera', dur_mov=0.6)),
                              (2.96, anuncio(L['frasco'], 0.03)), (3.60, anuncio(L['hinchada'], 0.03)), (4.30, anuncio(L['todo25'], 0.03))]), GAB)
toma('03', 8.66, 11.86, lienzo(IG, (0, 0, 1700), (0, 300, 1500), [('caja', _ri, 1.1), ('flecha_ad', _ri, 1.1)], nombre='biblioteca IM8:cabecera', dur_mov=0.7), GAB)
toma('04', 11.86, 17.70, Serie([(0, clip(I['v_creadora'], 3.0)), (0.78, anuncio(I['medicos'], 0.03, [('caja', (0.20, 0.045, 0.72, 0.125), 0.2)])), (1.78, anuncio(I['beckham'], 0.03)), (2.42, clip(I['v_rodillas'], 1.5, subir=260))]), GAB)
toma('05', 17.70, 19.06, Mitades(anuncio(L['debloat_mano'], 0), clip(I['v_vaso'], 4.4)), GAB)
toma('06', 19.06, 21.50, G2(g_paginas, CHIP_L, k=0.84), GAB)
toma('07', 21.50, 26.40, Serie([(0, anuncio(L['brunch'], 0.03)),
                                (1.50, captura(f'{A}/cap/deb_jeans.png', [(DEB['jeans'], 1.9, None, None)], nombre='lemmelive.com:debloat'))]), GAB)
toma('08', 26.40, 29.20, Serie([(0, anuncio(I['almuerzo'], 0)), (1.40, anuncio(I['articulaciones'], 0))]), GAB)
toma('09', 29.20, 35.24, Serie([(0, lienzo(BUYP, P3((620, 20, 660)), P3(V_BUY), nombre='im8health.com:caja de compra', dur_mov=0.6)),
                                (2.40, Lienzo(BUYP, P3(V_BUY), None, [('caja', P3(BUY['plan']), 0.1, 2.5), ('caja', P3(BUY['kit']), 2.5), ('flecha_ad', P3(BUY['kit']), 2.5)]))]), GAB)
toma('10', 35.24, 37.52, anuncio(I['kit'], 0.03, [('caja', (0.17, 0.222, 0.66, 0.045), 0.9)]), GAB)
toma('11', 37.52, 38.74, Mitades(anuncio(L['purr_mano'], 0), clip(I['v_creador'], 2.0)), GAB)
toma('12', 38.74, 44.66, G2(g_tiktok, CHIP_L), GAB)
toma('13', 44.66, 49.76, lienzo(LG, (0, 560, 1700), (0, 1500, 1700), nombre='biblioteca Lemme:grilla', dur_mov=4.6), GAB)
toma('14', 49.76, 51.18, clip(I['v_famosos'], 2.0), GAB)
toma('15', 51.18, 57.00, Serie([(0, clip(I['v_giannis'], 2.0)), (0.80, clip(I['v_sabalenka'], 3.0, subir=220)),
                                (1.82, lienzo(TIRA, (210, 1425, 1500), (210, 1990, 1500), nombre='im8health.com:ligas y socios', dur_mov=1.4)), (3.30, G2(g_crece, CHIP_I))]), GAB)
toma('16', 57.00, 60.52, PORTADA(), GAB)
toma('17', 60.52, 62.82, G2(g_llevar, CHIP_L), GAB)
toma('18', 62.82, 66.36, G2(g_avatar, CHIP_I), GAB)
toma('19', 66.36, 72.15, PORTADA(), GAB, T_(['¿Cuál es más efectiva?'], 196, 68, t0=0.25, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {'portada': 'formato VS: la pantalla dividida del inicio vuelve a mitad y en el cierre (como en la guia del 35)'}

GUION = [
 '¿Quién tiene mejor *estrategia?', 'Lemme de Kourtney Kardashian', 'o IM8 ~ de David Beckham',
 'Lemme tiene unos *500', 'anuncios activos en Meta', 'enfocados en sus productos,', 'sus beneficios', 'y sus *descuentos',
 'Pero IM8 ~ tiene', 'unos *1.500', 'con muchísima más *variedad',
 'Creadores,', 'estudios clínicos,', 'David Beckham', 'y anuncios que arrancan', 'directo con tu *problema', 'como el dolor', 'de las *articulaciones',
 'Ahora miremos', 'a dónde te *llevan',
 'Lemme te manda', 'una página distinta', 'para cada *producto',
 'Y cada una arranca', 'con algo que reconoces', 'al *instante', 'En este caso los *jeans', 'que te aprietan', 'después de comer',
 'IM8 ~ hace todo', 'lo *contrario,', 'te habla de muchos *problemas',
 'Pero casi todos', 'sus enlaces terminan', 'en la misma *página', 'con el plan de 3 *meses', 'ya marcado',
 'Y con ese plan', 'te regala un *kit', 'de bienvenida',
 'Así tu primera compra', 'ya no es de un mes,', 'sino de *3',
 'Ahora hablemos', 'de los *creadores',
 'Lemme vendió', '13 *millones', 'de dólares en TikTok Shop', 'en un solo mes', 'Con miles de creadores', 'ganando *comisión', 'por cada venta',
 'Mi mayor duda es', 'por qué no vemos', 'parte de esos *lives', 'en sus anuncios de Meta', 'Ahí se están dejando', 'muchísimo contenido', 'sin *usar',
 'IM8 ~ va por otro *camino', 'Con Giannis,', 'Sabalenka,', 'hasta el Inter de Miami', 'les dio *acciones',
 'De esta manera', 'si la marca crece,', 'ellos también *ganan',
 'Por más que sean', 'dos marcas muy exitosas,', 'las dos podrían aprender', 'mucho de la *otra',
 'Lemme podría llevar', 'los videos', 'de sus creadores a *Meta',
 'E IM8 ~ podría tener', 'una página distinta', 'según el *avatar', 'al que se le habla',
 '¿Qué estrategia de crecimiento', 'crees que es más *efectiva?', '¿La de Lemme', 'o la de IM8? ~', 'Te leo en los *comentarios',
]
_pal = [x for x in json.load(open(f'{A}/pal37.json')) if x['s'] < 70.95]
SUBS = armar_tarjetas(_pal, GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
