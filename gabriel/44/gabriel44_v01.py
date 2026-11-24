"""Video 44 · "Veinte y no cien" (Bloom Life) · v01
Formato pantalla verde, historia de una marca (guia de Gabriel, "VEINTE Y NO CIEN") + todo lo que Gabriel fue corrigiendo:
Gabriel cambia de lugar toma a toma (CI / CD / C); termina con su voz (sin cola); hook con dos cortes de video en los
primeros 2 s; nunca mas de ~4 s de grafico propio seguido (se intercalan anuncios reales de Bloom Life); cifras con contador;
marcas rojas solo sobre rectangulos medidos (frase.js) y revisadas con revisar_marcas.py.
- La marca se revela en "Asi nacio en Argentina Bloom Life" (22,52 s). Antes, el logo no se lee: la foto de los fundadores
  va con el cartel y las remeras desenfocados (rectangulos medidos sobre la foto), los frascos desenfocados, la nota de Forbes
  recortada debajo de su volanta "Bloomlife".
- Material real: anuncios de Bloom Life de la Biblioteca de Anuncios (busqueda por texto, pais AR), Forbes Argentina,
  iProfesional y las fotos de producto de su tienda oficial en Mercado Libre (sin la pagina, que tiene promesas de salud).
- Regla 12: de los anuncios se usan solo tramos sin promesas (sus subtitulos hablan de estres, concentracion, etc.).
- No se consiguio (avisar): publicaciones reales de Flor Raggi y Pia Slapka con el producto (Instagram pide sesion y los anuncios
  activos no las muestran) -> sus nombres se marcan en la nota de Forbes; la captura del perfil de Gabriel con "Seguir"
  (Instagram pide sesion) -> el cierre es una clienta con los frascos.
Tiempos de la transcripcion del crudo (67,97 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v44')
RAW = f'{A}/dl/crudo44.mp4'
DUR = 67.97                  # termina con la voz (sin cola)
CABEZA = 690                 # fila del crudo donde esta el tope de su cabeza (medido: 682-712)
CENTRO = 505
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (150, 150, 146)
VERDE_B = (98, 140, 120)                                                 # verde de Bloom Life
LOGO = Image.open(f'{A}/cap/logo_t.png').convert('RGBA')


def logo(w):
    return LOGO.resize((w, int(LOGO.height * w / LOGO.width)), Image.LANCZOS)


def panel(im, y=300, ancho=W, sigma=40):
    """La foto a todo el ancho, sobre su version desenfocada (pantalla completa)."""
    k = ancho / im.width; f = im.resize((ancho, int(im.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(sigma)); c.paste(f, ((W - ancho) // 2, y)); return c


def tapar(im, rects, sigma=24):
    im = im.copy()
    for x, y, w, h in rects:
        im.paste(im.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(sigma)), (x, y))
    return im


def _texto(s, tam, col=TINTA, peso='ExtraBold'):
    f = font(tam, peso); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


# ------------------------------------------------------------ figuras
def _persona(col, tam=60):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.3], 180, 360, fill=col + (255,)); return c
P_ON, P_OFF, P_ROJA = _persona(VERDE_B), _persona((214, 214, 210)), _persona(ROJO)
P_GRANDE = _persona(VERDE_B, 150)
POCAS = [(3, 2), (6, 4), (1, 6), (8, 7), (5, 8)]                          # celdas que quedan encendidas en "unas pocas"
VEINTE = set(np.random.default_rng(4).choice(100, 21, replace=False).tolist())


def grilla(im, encendidas, t_llenado=None, tl=0.0, y0=180, paso=44, grandes=()):
    """10 x 10 perfiles. encendidas: conjunto de indices (o 'todas'); t_llenado: se van prendiendo en ese tiempo."""
    for i in range(100):
        r, c = divmod(i, 10); x = 540 + (c - 4.5) * paso * 2.0; y = y0 + r * paso
        on = (encendidas == 'todas' or i in encendidas)
        if t_llenado is not None and i / 100 * t_llenado[1] > tl - t_llenado[0]: on = False
        if (c, r) in grandes: pegar(im, P_GRANDE, x, y, 0.62); continue
        pegar(im, P_ON if on else P_OFF, x, y, 1.0)


def g_cien(tl, T):                    # "podria tener 100 influencers" -> se llena; "tienen poco mas de 20" -> quedan 20
    im = fondo_grafico()
    if tl < 1.30: grilla(im, 'todas', (0.0, 0.9), tl)
    else: grilla(im, VEINTE)
    c100 = contador(100, 0.0, dur=0.9, prefijo='', tam=110, color=VERDE_B)
    if tl < 1.30: c100(im, tl, 540, 640)
    else: contador(20, 1.30, dur=0.5, prefijo='', desde=100, tam=110, color=VERDE_B)(im, tl, 540, 640)
    return im


def g_selectivos(tl, T):              # "Pero ellos fueron muy selectivos": de las 100 quedan unas 20
    im = fondo_grafico(); grilla(im, 'todas' if tl < 0.5 else VEINTE)
    if tl > 0.7: pegar(im, pastilla('Muy selectivos', 48, fondo=VERDE_B), 540, 660, pop(tl, 0.7))
    return im


def g_todas(tl, T):                   # "lo mas facil era mandarle frascos a todos los influencers posibles"
    im = fondo_grafico(); grilla(im, 'todas', (0.0, 0.8), tl); return im


def g_pocas(tl, T):                   # "o cuando es suficiente con unas pocas que viven en carne propia el problema"
    im = fondo_grafico(); grilla(im, set(), None, tl, grandes=POCAS if tl > 0.35 else ())
    if tl > 0.6: pegar(im, pastilla('Viven el problema', 44, fondo=VERDE_B), 540, 660, pop(tl, 0.6))
    return im


def g_contra(tl, T):                  # "porque si escoges mal puede jugar en tu contra"
    im = fondo_grafico(); p = ease((tl - 0.3) / 0.5)
    for i in range(100):
        r, c = divmod(i, 10); x = 540 + (c - 4.5) * 88; y = 180 + r * 44
        pegar(im, P_ROJA if (i * 37 % 100) / 100 < p else P_OFF, x, y, 1.0)
    if tl > 0.9: pegar(im, pastilla('Puede jugar en tu contra', 46, fondo=ROJO), 540, 660, pop(tl, 0.9))
    return im


def g_mapa(tl, T):                    # "ni siquiera iba a vender en Argentina, la marca nacio en Estados Unidos" (flecha que no llega)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    a, b = (330, 300), (720, 620)
    pegar(im, emoji('🇺🇸', 150), *a, pop(tl, 0.05)); pegar(im, pastilla('Estados Unidos', 40, fondo=TINTA), a[0], a[1] + 115, pop(tl, 0.15))
    pegar(im, emoji('🇦🇷', 150), *b, pop(tl, 0.9)); pegar(im, pastilla('Argentina', 40, fondo=(120, 170, 220)), b[0], b[1] + 115 - 230, pop(tl, 1.0))
    _punteada(d, a, b, min(0.55, ease((tl - 1.6) / 0.8)))
    if tl > 2.0: pegar(im, pastilla('Nació acá', 38, fondo=VERDE_B), a[0], a[1] - 110, pop(tl, 2.0))
    return im


def _punteada(d, a, b, p):
    n = 22
    for i in range(int(n * p)):
        if i % 2: continue
        t0, t1 = i / n, (i + 1) / n
        d.line([(a[0] + (b[0] - a[0]) * t0 + 60, a[1] + (b[1] - a[1]) * t0 + 40), (a[0] + (b[0] - a[0]) * t1 + 60, a[1] + (b[1] - a[1]) * t1 + 40)], fill=ROJO, width=10)


def g_llega(tl, T):                   # "...hay una oportunidad enorme de mercado": la flecha punteada llega a Argentina
    im = fondo_grafico(); d = ImageDraw.Draw(im); a, b = (330, 300), (720, 620)
    pegar(im, emoji('🇺🇸', 150), *a); pegar(im, emoji('🇦🇷', 150), *b)
    _punteada(d, a, b, lerp(0.55, 1.0, ease(tl / 0.6)))
    if tl > 0.6: pegar(im, pastilla('Hay mercado', 52, fondo=VERDE_B), 540, 700, lerp(0.86, 1, pop(tl, 0.6)))
    return im


TEL = None
def _telefono():
    c = Image.new('RGBA', (400, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, 399, 639], radius=56, fill=TINTA + (255,)); d.rounded_rectangle([16, 16, 383, 623], radius=44, fill=(236, 230, 222, 255))
    for i in range(3): d.rounded_rectangle([40 + i * 110, 40, 140 + i * 110, 48], radius=4, fill=(255, 255, 255, 255) if i == 0 else (200, 196, 190, 255))
    d.ellipse([40, 64, 100, 124], fill=(214, 214, 210, 255))                                                      # perfil generico, sin cara
    d.rounded_rectangle([114, 84, 260, 104], radius=10, fill=(200, 196, 190, 255))
    return c


def g_historia(tl, T):                # "Ella lo subio a sus redes y la respuesta fue tan rapida" (historia generica, sin cara ni nombre)
    global TEL
    TEL = TEL or _telefono(); im = fondo_grafico(); pegar(im, TEL, 540, 450, pop(tl, 0.05))
    fr = Image.open(f'{A}/press/ipro_609704.jpg').convert('RGB').resize((300, 375), Image.LANCZOS)
    im.paste(fr, (390, 290))
    for k in range(7):
        t0 = 0.5 + k * 0.17
        if tl > t0: pegar(im, emoji('❤️', 70), 800 + 30 * math.sin(k * 1.7), 640 - (tl - t0) * 260 - k * 10, 1.0)
    return im


def g_95(tl, T):                      # "El 95% son mujeres entre 30 y 60 anos"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for i in range(20):
        r, c = divmod(i, 10); x = 540 + (c - 4.5) * 92; y = 290 + r * 110
        pegar(im, _persona(VERDE_B if i < 19 else (214, 214, 210), 86), x, y, pop(tl, 0.05 + i * 0.03))
    contador(95, 0.16, dur=0.8, prefijo='', sufijo='%', tam=130, color=VERDE_B)(im, tl, 540, 520)
    if tl > 1.8: pegar(im, pastilla('mujeres de 30 a 60 años', 46, fondo=TINTA), 540, 650, pop(tl, 1.8))
    return im


def g_confian(tl, T):                 # "...que le recomendara alguien en quien esas mujeres ya confiaran"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, P_GRANDE, 240, 380, pop(tl, 0.05)); pegar(im, pastilla('Embajadora', 40, fondo=VERDE_B), 240, 500, pop(tl, 0.15))
    for k in range(6):
        pegar(im, _persona((120, 120, 116), 80), 720 + (k % 3) * 110, 320 + (k // 3) * 140, pop(tl, 0.4 + k * 0.08))
    if tl > 0.9: flecha_recta(d, (330, 400), (600, 400), ease((tl - 0.9) / 0.3))
    if tl > 1.4: pegar(im, emoji('❤️', 70), 470, 330, pop(tl, 1.4))
    if tl > 1.7: pegar(im, pastilla('Ya confían en ella', 44, fondo=TINTA), 540, 650, pop(tl, 1.7))
    return im


# ------------------------------------------------------------ capturas (frase.js: 2460x4374, 3 px por px CSS)
J = lambda n: json.load(open(f'{A}/cap/{n}meta.json'))
P3 = lambda r: tuple(v * 3 for v in r)
FBJ = J('fb'); FB2J = J('fb2'); IPJ = J('ip')


def zona(png, y0, y1):
    """Captura entera (3 px por px CSS) con todo lo de arriba de y0 y lo de abajo de y1 (px) tapado en blanco: solo queda la
    frase y sus lineas vecinas (sin la marca antes de tiempo, sin promesas de salud ni precios alrededor)."""
    a = img(png).copy(); a[:y0] = 255; a[y1:] = 255; return a
R3 = lambda r: tuple(v * 3 for v in r)                       # rect CSS -> px de la captura


def tira(png, y0, y1, oy=330):
    """Franja de una captura (px de la captura, 3 px por px CSS) a todo el ancho sobre fondo blanco, desde y=oy de pantalla.
    Devuelve (lona, convertidor de rectangulo CSS -> lona)."""
    im = Image.open(png).convert('RGB').crop((0, y0, 2460, y1)); k = W / 2460
    t = im.resize((W, int(im.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (255, 255, 255)); c.paste(t, (0, oy))
    conv = lambda r: ((r[0] * 3) * k, oy + (r[1] * 3 - y0) * k, r[2] * 3 * k, r[3] * 3 * k)
    return c, conv
# Forbes: titulo desde y CSS 510 (debajo de la volanta "Bloomlife" de y 476 y del rotulo BLOOMLIFE: la marca no se ve aun)
FB_T, cFT = tira(f'{A}/cap/fb_t.png', 1530, 1745, 300)
FB_E, cFE = tira(f'{A}/cap/fb2_emb.png', 1500, 1780, 300)
IP_M, cIM = tira(f'{A}/cap/ip_mer.png', 1470, 1760, 300)                   # desde y CSS 490: la linea de "...se llama Bloom" queda afuera
IP_P, cIP = tira(f'{A}/cap/ip_pref.png', 540, 800, 330)
IP_C, cIC = tira(f'{A}/cap/ip_cin.png', 1530, 1760, 300)
_une = lambda rs: (min(r[0] for r in rs), min(r[1] for r in rs), max(r[0] + r[2] for r in rs) - min(r[0] for r in rs), max(r[1] + r[3] for r in rs) - min(r[1] for r in rs))

# ------------------------------------------------------------ notas como tarjeta (pedido del coordinador: sin hueco blanco gigante,
# texto grande, nunca cortado por un borde). Capturas a ancho de celular (capm/, frase_movil.js: Forbes 280 px CSS, iProfesional
# 320 px CSS, 3 px por px CSS) para que cada linea entre entera; la tarjeta llena y 150-730 sobre una foto real desenfocada.
JM = lambda n: json.load(open(f'{A}/capm/{n}meta.json'))
FBM, IPM = JM('fb'), JM('ip')


def tarjeta_nota(png, y0, y1, medio, fondo, sigma=34, ytop=150, ybot=730, x0=36, ancho=1008, pad=24):
    """Tarjeta blanca redondeada con el nombre del medio arriba y las lineas y0-y1 (px CSS) de la captura debajo, a todo el
    ancho de la tarjeta. fondo: PIL (foto real) que va desenfocada detras. Devuelve (lona PIL, conv rect CSS -> lona)."""
    cap = Image.open(png).convert('RGB'); k = (ancho - 2 * pad) / cap.width
    cuerpo = cap.crop((0, int(y0 * 3), cap.width, int(y1 * 3))); cuerpo = cuerpo.resize((ancho - 2 * pad, int(cuerpo.height * k)), Image.LANCZOS)
    cab = 74; alto = cab + cuerpo.height + pad; yc = ytop + max(0, (ybot - ytop - alto) // 2)
    assert yc + alto <= ybot + 2, ('la tarjeta no entra', png, alto)
    c = Image.fromarray(cubrir(fondo)).filter(ImageFilter.GaussianBlur(sigma)); c = Image.blend(c, Image.new('RGB', c.size, (0, 0, 0)), 0.18)
    m = Image.new('L', (ancho, alto), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ancho - 1, alto - 1], radius=34, fill=255)
    t = Image.new('RGB', (ancho, alto), (255, 255, 255)); d = ImageDraw.Draw(t)
    d.text((pad + 4, cab // 2 + 4), medio, font=font(40), fill=TINTA, anchor='lm'); d.line([(pad, cab - 6), (ancho - pad, cab - 6)], fill=(226, 226, 222), width=3)
    t.paste(cuerpo, (pad, cab)); c.paste(t, (x0, yc), m)
    conv = lambda r: (x0 + pad + r[0] * 3 * k, yc + cab + (r[1] - y0) * 3 * k, r[2] * 3 * k, r[3] * 3 * k)
    return c, conv
FONDO_A = Image.open(f'{A}/press/ipro_609704.jpg').convert('RGB')                     # mano con una gomita (sin logo)
FONDO_B = Image.open(f'{A}/press/ipro_609707.jpg').convert('RGB')
FONDO_C = Image.open(f'{A}/prod/hi/p01.webp').convert('RGB')
N_FT, cNFT = tarjeta_nota(f'{A}/capm/fb_t.png', 165, 258, 'Forbes Argentina', FONDO_A, sigma=40)
N_FE, cNFE = tarjeta_nota(f'{A}/capm/fb_emb.png', 170, 308, 'Forbes Argentina', FONDO_C)
N_IM, cNIM = tarjeta_nota(f'{A}/capm/ip_mer.png', 188, 332, 'iProfesional', FONDO_A, sigma=40)
N_IP, cNIP = tarjeta_nota(f'{A}/capm/ip_pref.png', 186, 334, 'iProfesional', FONDO_B)
N_IC, cNIC = tarjeta_nota(f'{A}/capm/ip_cin.png', 188, 332, 'iProfesional', FONDO_C)
VISTA = ((0, 0, W), (16, 28, W - 32))                                                # empuje leve


# ------------------------------------------------------------ fotos
FUND = tapar(Image.open(f'{A}/press/forbes_fund.jpg').convert('RGB'), [(1100, 400, 700, 160), (890, 720, 230, 150), (1420, 770, 230, 130)]).crop((700, 250, 1900, 1500))
FRASCOS = Image.open(f'{A}/press/ipro_609703.jpg').convert('RGB').filter(ImageFilter.GaussianBlur(9))      # etiquetas ilegibles
PR = lambda n: Image.open(f'{A}/prod/hi/{n}.webp').convert('RGB')


def blanco(im, y=260, ancho=900):
    c = Image.new('RGB', (W, H), (255, 255, 255)); k = ancho / im.width; f = im.resize((ancho, int(im.height * k)), Image.LANCZOS)
    c.paste(f, ((W - ancho) // 2, y)); return c


def g_logo(tl, T):
    im = Image.new('RGB', (W, H), (255, 255, 255)); pegar(im, logo(int(lerp(760, 820, ease(tl / 0.3)))), 540, 420, 1.0); return im


# ------------------------------------------------------------ tomas
toma('01', 0.00, 1.68, Serie([(0.00, clip('1100049709572980', 2.3, nombre='anuncio-video:1100049709572980 (s2: gomitas en la mano)')),
                              (0.84, clip('1100049709572980', 8.7, nombre='anuncio-video:1100049709572980 (s9: gomitas entre los dedos)'))]), GAB,
     T_(['100 influencers'], 180, 76, t0=-1.0, clave={'100'}))
toma('02', 1.68, 4.28, Grafico(lambda tl, T: g_cien(tl + 0.0, T)), GAB)                                                         # "100 influencers... poco mas de 20"
toma('03', 4.28, 6.36, lienzo(N_FT, *VISTA, [('caja', cNFT(FBM['t'][0]), 0.94)], nombre='forbesargentina.com: titulo 15% al mes'), GAB,
     contador_toma(15, 0.94, cy=1180, prefijo='+', sufijo='% cada mes', tam=80))
toma('04', 6.36, 8.56, lienzo(panel(FUND, y=260), (0, 0, W), (30, 40, W - 60), nombre='forbesargentina.com: los fundadores (logo desenfocado)'), GAB,
     contador_toma(20000, 1.22, cy=200, sufijo='', tam=96))
toma('05', 8.56, 10.24, lienzo(panel(FRASCOS, y=300), (0, 0, W), (40, 60, W - 80), nombre='iprofesional.com: frascos (desenfocados)'), GAB)
toma('06', 10.24, 13.58, Grafico(g_mapa), GAB)
toma('07', 13.58, 15.36, clip('1003093062812851b', 5.1, nombre='anuncio-video:1003093062812851 (s5: el frasco en la mano; su subtitulo "de Bloom Life" desenfocado)'), GAB)
toma('08', 15.36, 16.46, clip('1100049709572980', 9.9, nombre='anuncio-video:1100049709572980 (s10: la creadora)'), GAB)
toma('09', 16.46, 17.70, Grafico(g_historia), GAB)
S[-1]['fuentes'] = ['grafico: historia de Instagram generica (foto de iprofesional.com)']
toma('10', 17.70, 20.16, lienzo(N_IM, *VISTA, [('caja', cNIM(r), 0.05) for r in IPM['mer']], nombre='iprofesional.com: hay mercado'), GAB)
toma('11', 20.16, 21.48, Grafico(g_llega), GAB)
toma('12', 21.48, 26.78, Serie([
    (0.00, clip('1514823533995674', 5.3, nombre='anuncio-video:1514823533995674 (s5: abre la bolsa, sin logo)')),               # "Asi nacio en Argentina"
    (0.92, Grafico(g_logo)),                                                                                                     # "Bloom Life"
    (1.98, lienzo(blanco(PR('p17'), 300), (0, 0, W), (40, 60, W - 80), nombre='mercadolibre: gomitas')),                        # "gomitas"
    (2.38, lienzo(blanco(PR('p06'), 220, 560), (0, 0, W), (60, 60, W - 120), nombre='mercadolibre: capsulas')),                # "y capsulas con hongos"
    (3.12, lienzo(blanco(PR('p10'), 220, 600), (0, 0, W), (60, 60, W - 120), nombre='mercadolibre: melena de leon')),          # "como la melena de leon"
    (4.62, clip('1100049709572980', 24.3, nombre='anuncio-video:1100049709572980 (s24: ashwagandha)')),                         # "la ashwagandha"
]), GAB)
S[-1]['fuentes'] += ['logo de Bloom Life (mercadolibre.com.ar)']
toma('13', 26.78, 28.54, clip('1514823533995674', 20.7, nombre='anuncio-video:1514823533995674 (s20: creadora con reishi)'), GAB)
toma('14', 28.54, 30.54, Grafico(g_todas), GAB)
toma('15', 30.54, 32.30, Grafico(g_selectivos), GAB)
toma('16', 32.30, 36.78, lienzo(N_FE, *VISTA, [('caja', cNFE(FBM['emb_1'][0]), 0.60, 1.46), ('caja', cNFE(FBM['emb_2'][0]), 1.46, 2.30),
                                                                    ('caja', cNFE(FBM['emb'][0]), 2.30)], nombre='forbesargentina.com: embajadoras'), GAB)
toma('17', 36.78, 38.94, clip('1003093062812851', 21.0, nombre='anuncio-video:1003093062812851 (s21: clienta con dos frascos)'), GAB)
toma('18', 38.94, 42.04, Grafico(g_95), GAB)
toma('19', 42.04, 43.40, clip('1100049709572980', 5.5, nombre='anuncio-video:1100049709572980 (s5: la creadora hablando)'), GAB)
toma('20', 43.40, 45.20, Grafico(g_confian), GAB)
toma('21', 45.20, 46.80, clip('1003093062812851', 4.1, nombre='anuncio-video:1003093062812851 (s4: capsulas en la mano)'), GAB)
toma('22', 46.80, 51.36, lienzo(N_IP, *VISTA, [('caja', cNIP(r), 1.82) for r in IPM['pref']], nombre='iprofesional.com: preferimos vender menos'), GAB)
toma('23', 51.36, 53.00, lienzo(panel(Image.open(f'{A}/press/ipro_609707.jpg').convert('RGB'), y=180, ancho=760), (0, 0, W), (40, 60, W - 80), nombre='iprofesional.com: frasco en la cama'), GAB)
toma('24', 53.00, 55.74, lienzo(N_IC, *VISTA, [('caja', cNIC(r), 1.10) for r in IPM['cin']], nombre='iprofesional.com: hasta 50% mas'), GAB,
     contador_toma(50, 1.48, cy=1180, prefijo='hasta ', sufijo='% más', tam=80))
toma('25', 55.74, 59.36, Serie([(0.00, clip('1514823533995674', 22.0, nombre='anuncio-video:1514823533995674 (s22)')),
                                (0.90, clip('1100049709572980', 13.2, nombre='anuncio-video:1100049709572980 (s13)')),
                                (1.80, clip('1436292494786093', 5.0, nombre='anuncio-video:1436292494786093 (s5)')),
                                (2.70, clip('1003093062812851', 0.1, nombre='anuncio-video:1003093062812851 (s0: frascos en la mesa)'))]), GAB)
toma('26', 59.36, 61.00, Grafico(g_pocas), GAB)
toma('27', 61.00, 62.92, clip('1100049709572980', 15.4, nombre='anuncio-video:1100049709572980 (s15)'), GAB)
toma('28', 62.92, 65.00, Grafico(g_contra), GAB)
toma('29', 65.00, 67.97, Serie([(0.00, clip('1003093062812851', 19.2, nombre='anuncio-video:1003093062812851 (s19: frascos en la mesa)')),
                                (1.40, clip('1514823533995674', 23.4, nombre='anuncio-video:1514823533995674 (s23: con sus gomitas)'))]), GAB,
     T_(['Mándaselo a quien lo necesita'], 180, 64, t0=0.2, emo='👇'))
LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'Esta marca de suplementos', 'podría tener 100 *influencers', 'hablando de *ella', 'y tienen poco más de *20',
 'y aún así crece ~ *15%', 'cada *mes',
 '~ Empezó con dos *amigos,', '20 mil *dólares', 'y un frasco que le mandaron', 'a una *conocida',
 'Su plan ni siquiera ~ era', 'vender en *Argentina,', 'la marca nació', 'en Estados *Unidos',
 'Pero uno de los *fundadores', 'le mandó unos *frascos', 'a una influencer que *conocían',
 'Ella lo subió a sus *redes', 'y la respuesta fue tan *rápida', 'que ahí mismo se dieron cuenta', 'que había una *oportunidad', 'enorme de *mercado',
 'Así nació en *Argentina', 'Bloom *Life,', 'gomitas y *cápsulas', 'con hongos como la melena de *león', 'y plantas como la *ashwagandha',
 'Con una respuesta así', 'lo más fácil era', 'mandarle *frascos', 'a todos los influencers *posibles',
 'Pero ellos fueron muy *selectivos', 'y sumaron mujeres como', 'Flor *Raggi', 'y Pía *Slapka',
 'Pero no lo hicieron porque', 'no quisieran ser más *reconocidos',
 'La razón tiene que ver', 'con quiénes les *compran',
 'El ~ *95%', 'son *mujeres', 'entre 30 y 60 *años', 'y la idea era que les', 'recomendara a alguien', 'en quien esas mujeres', 'ya *confiaran',
 'Lo resumen en una sola *frase', 'que pocas marcas se atreverían', 'a decir en voz *alta',
 'Preferimos vender menos *unidades', 'pero muy bien *cuidadas',
 'Según ellos quien encuentra', 'una marca así', 'está dispuesto a *pagar', 'hasta un ~ *50%', '*más',
 'Tienes que saber *diferenciar', 'cuándo te conviene tener', 'miles de personas', 'mostrando tu *producto',
 'O cuándo es suficiente', 'con unas *pocas', 'que viven en carne propia', 'el problema que *resuelves',
 'Porque si escoges *mal', 'puede jugar en tu *contra',
 'Mándaselo a quien necesita', 'escuchar *esto', 'y sígueme para más', 'videos como *este',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal44.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
