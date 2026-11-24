"""Video 43 · VS "Dirtea vs Let Loose" (los correos) · v01
Guia de Gabriel (VS "DIRTEA VS LET LOOSE") + todo lo que fue corrigiendo en el 38-40:
- Hook con videos reales (foto de Bear Grylls, video oficial de Dirtea, hongos); Gabriel cambia de lugar toma a toma
  (CI / CD / C); el video termina con su voz (DUR = crudo, sin cola); nunca mas de ~3,5 s de grafico propio seguido.
- Dirtea siempre primero / a la izquierda, Let Loose despues / a la derecha (logo de cada una arriba de su lado).
- Regla de oro de la guia: antes de "el correo" (44,28 s) ningun correo se ve como correo: solo recortes de la oferta.
  Desde ahi, correos completos.
- Correos: imagenes que paso Gabriel (Drive "Referencias email - Let Loose y Dirtea"). Los de Dirtea son cuadros del reel de
  la autopsia de su Black Friday con una presentadora delante: solo se usan los recortes de los correos que quedan arriba de
  ella ("aqui podriamos coger recortes de los emails que salen arriba de ella"), nunca ella.
- Regla 12: en los correos de Let Loose se desenfocan las frases sobre digestion ("bloated, blocked", "flush out waste"...).
- The Grocer tiene verificacion anti-bots (Human Verification): el "x3 en dos anos" va como grafico con "Fuente: The Grocer".
  Las cifras de Let Loose salen solo del video de su agencia en YouTube (no se baja): graficos con "segun su agencia".
- Marcas rojas medidas por pixeles sobre las imagenes de Gabriel (ver F_40 y F_FUNDADOR).
Tiempos de la transcripcion del crudo (71,93 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v43')
E = os.path.join(A, '..', 'emails_ref')
RAW = f'{A}/dl/crudo43.mp4'
DUR = 71.93                  # termina con la voz
CABEZA = 735
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (120, 120, 118)
LIMA = (226, 247, 120)
NARANJA = (246, 120, 30)
FUENTE = lambda s: pastilla(s, 34, fondo=(236, 236, 232), color=GRIS, pad=(30, 16))

# ------------------------------------------------------------ chips de marca (Dirtea a la izquierda, Let Loose a la derecha)
CH_D = pastilla('DIRTEA', 50, fondo=TINTA, color=LIMA)
CH_L = pastilla('Let Loose', 50, fondo=NARANJA, color=(255, 255, 255))
logo_d = lambda t0=0.0: (lambda pil, tl, T: pegar(pil, CH_D, 40 + CH_D.width // 2, 110, pop(tl, t0)) if tl >= t0 else None)
logo_l = lambda t0=0.0: (lambda pil, tl, T: pegar(pil, CH_L, W - 40 - CH_L.width // 2, 110, pop(tl, t0)) if tl >= t0 else None)


# ------------------------------------------------------------ imagenes
def abrir(p): return Image.open(p).convert('RGB')


def desenfocar(im, cajas, s=14):
    im = im.copy()
    for x0, y0, x1, y1 in cajas: im.paste(im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(s)), (x0, y0))
    return im


def panel(im, y=300, ancho=W, fondo_sigma=40):
    """La imagen a `ancho`, sobre su version desenfocada a pantalla completa. Devuelve (lona, a_lona(rect_en_im))."""
    k = ancho / im.width; f = im.resize((ancho, int(im.height * k)), Image.LANCZOS); x = (W - ancho) // 2
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(fondo_sigma)); c = c.point(lambda v: int(v * 0.8)); c.paste(f, (x, y))
    return c, (lambda r: (x + r[0] * k, y + r[1] * k, r[2] * k, r[3] * k))


D1, D2 = abrir(f'{E}/dirtea1.jpg'), abrir(f'{E}/dirtea2.jpg')                     # cuadros del reel de la autopsia (1080x1920)
# Let Loose: frases de digestion desenfocadas (px de cada imagen, medidos sobre la grilla)
L1 = desenfocar(abrir(f'{E}/letloose1.jpg'), [(30, 1060, 640, 1160), (60, 1285, 610, 1370), (60, 1940, 640, 1980), (60, 2680, 640, 2720)])
L2 = desenfocar(abrir(f'{E}/letloose2.jpg'), [(40, 330, 630, 895)])
L3 = abrir(f'{E}/letloose3.jpg')
L4 = desenfocar(abrir(f'{E}/letloose4.jpg'), [(180, 1000, 420, 1080)])            # "Less Bloating" de la etiqueta
BG = abrir(f'{A}/wiki/Bear_Grylls_2014.jpg')                                      # Wikimedia Commons
DP = f'{A}/dprod'

# Marcas MEDIDAS por pixeles: "40% OFF & FREE GIFTS" en dirtea1 = columnas 305-616 y filas 240-265 de texto oscuro (<90) en la
# cabecera amarilla del correo del medio; "Alexandra – Founder" en letloose2 = columnas 50-273, filas 951-966 (texto <110).
F_40 = (305, 240, 312, 26)
F_FUNDADOR = (50, 951, 224, 16)


# ------------------------------------------------------------ graficos propios (contenido entre y 180 y 730)
def _texto(s, tam, col=TINTA):
    f = font(tam); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _persona(col=TINTA, tam=150):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.28], 180, 360, fill=col + (255,)); return c
PER = _persona()
C_X3 = contador(3, 1.28, dur=0.8, prefijo='x', tam=170, desde=1)


def g_x3(tl, T):                     # "y ha triplicado (0.28) sus ventas en los ultimos dos anos (2.42)"
    im = fondo_grafico(); d = ImageDraw.Draw(im); pegar(im, CH_D, 40 + CH_D.width // 2, 110, 1.0)
    for i, (h, t0) in enumerate(((120, 0.1), (360, 0.7))):
        p = ease((tl - t0) / 0.4)
        if p > 0: x = 220 + i * 230; d.rounded_rectangle([x - 80, 690 - h * p, x + 80, 690], radius=16, fill=VERDE_OSC if i else (200, 220, 208))
    C_X3(im, tl, 790, 380)
    if tl > 1.9: pegar(im, pastilla('en 2 años', 46, fondo=TINTA), 790, 530, pop(tl, 1.9))
    pegar(im, FUENTE('Fuente: The Grocer'), 790, 640, pop(tl, 0.2))
    return im


C_2M = contador(2, 0.34, dur=1.0, prefijo='US$', sufijo=' M', tam=170)


def g_2m(tl, T):                     # "vendio casi (0.34) 2 millones de dolares en 6 meses (1.66)"
    im = fondo_grafico(); pegar(im, CH_L, W - 40 - CH_L.width // 2, 110, 1.0)
    if tl > 0.3: pegar(im, _texto('Casi', 60, GRIS), 540, 250, pop(tl, 0.3))
    C_2M(im, tl, 540, 380)
    if tl > 2.0: pegar(im, pastilla('en 6 meses', 50, fondo=TINTA), 540, 530, pop(tl, 2.0))
    pegar(im, FUENTE('según su agencia'), 540, 650, pop(tl, 0.4))
    return im


C_50 = contador(50, 1.08, dur=0.7, prefijo='', sufijo='%', tam=190, desde=40, color=TINTA)


def g_50(tl, T):                     # "y dias despues (0.16) llego hasta un 50% (1.08) en toda la tienda (2.08)"
    im = fondo_grafico(); d = ImageDraw.Draw(im); pegar(im, CH_D, 40 + CH_D.width // 2, 110, 1.0)
    if tl > 0.1:                     # calendario simple: los dias pasan
        k = pop(tl, 0.1); cal = Image.new('RGBA', (220, 200), (0, 0, 0, 0)); dc = ImageDraw.Draw(cal)
        dc.rounded_rectangle([0, 20, 219, 199], radius=20, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
        dc.rectangle([3, 23, 216, 70], fill=ROJO + (255,))
        n = min(6, int((tl - 0.1) / 0.15) + 1)
        for j in range(n): dc.line([(28 + j * 30, 100), (48 + j * 30, 150)], fill=TINTA + (255,), width=6)
        pegar(im, cal, 240, 380, k)
    if tl > 1.08:
        dd = ImageDraw.Draw(im); dd.rounded_rectangle([520, 280, 1000, 500], radius=30, fill=LIMA)
        C_50(im, tl, 760, 390)
    if tl > 2.08: pegar(im, pastilla('en toda la tienda', 48, fondo=TINTA), 760, 580, pop(tl, 2.08))
    return im


def _etiqueta(s, col=LIMA, tc=TINTA, tam=58):
    return pastilla(s, tam, fondo=col, color=tc)
E40, E50, EN = _etiqueta('40%'), _etiqueta('50%'), _etiqueta('¿la siguiente?', (236, 236, 232), GRIS, 46)
INTERROG = _texto('?', 170, ROJO)


def g_cuando(tl, T):                 # "Con el 40 (0.24), con el 50 (1.02) o mejor esperaba las siguientes (1.88)"
    im = fondo_grafico(); d = ImageDraw.Draw(im); pegar(im, CH_D, 40 + CH_D.width // 2, 110, 1.0)
    d.line([(90, 330), (990, 330)], fill=(200, 200, 196), width=10)
    for x, e, t0 in ((220, E40, 0.24), (530, E50, 1.02), (840, EN, 1.88)):
        if tl > t0: d.ellipse([x - 16, 314, x + 16, 346], fill=TINTA); pegar(im, e, x, 250, pop(tl, t0))
    pegar(im, PER, 540, 560, pop(tl, 0.05))
    if tl > 0.6: pegar(im, INTERROG, 660, 520, pop(tl, 0.6))
    return im


def _fila(nombre, col, leido=False, w=880):
    c = Image.new('RGBA', (w, 118), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, 117], radius=18, fill=(255, 255, 255, 255), outline=(222, 222, 218, 255), width=3)
    d.ellipse([24, 30, 82, 88], fill=col + (255,))
    if nombre: d.text((104, 22), nombre, font=font(40), fill=TINTA + (255,))
    else: d.rounded_rectangle([104, 30, 330, 58], radius=10, fill=(214, 214, 210, 255))
    d.rounded_rectangle([104, 74, w - 160 if nombre else w - 260, 92], radius=8, fill=(232, 232, 228, 255))
    if not leido: d.ellipse([w - 60, 48, w - 38, 70], fill=(40, 120, 240, 255))
    return c
FILAS = [_fila(None, (200, 200, 196)), _fila('DIRTEA', TINTA), _fila(None, (200, 200, 196)), _fila('Let Loose', NARANJA), _fila(None, (200, 200, 196))]


def _sobre(tam=150):
    c = Image.new('RGBA', (tam, int(tam * 0.72)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=12, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=7)
    d.line([(6, 8), (w / 2, h * .58), (w - 6, 8)], fill=TINTA + (255,), width=7); return c
SOBRE = _sobre()


def g_bandeja(tl, T):                # "en un lugar que casi todas las marcas tienen olvidado (0.32-1.74), el correo (2.42)"
    im = fondo_grafico()
    for i, f in enumerate(FILAS):
        if tl > 0.05 + i * 0.12: pegar(im, f, 540, 230 + i * 118, pop(tl, 0.05 + i * 0.12))
    if tl > 2.42:
        pegar(im, SOBRE, 540, 470, lerp(0.7, 1.15, pop(tl, 2.42))); pegar(im, pastilla('El correo', 60, fondo=ROJO), 540, 610, pop(tl, 2.5))
    return im


SOBRE_CHICO = SOBRE.resize((92, 66), Image.LANCZOS)
C_9 = contador(9, 2.36, dur=0.45, prefijo='', sufijo=' correos', tam=110, color=(255, 255, 255), desde=1)


def texto_9(pil, tl, T):             # "le mandaba 9 (2.36) pero uno detras de otro (3.18)"
    if tl >= 2.36:
        d = ImageDraw.Draw(pil); d.rounded_rectangle([250, 1105, 830, 1260], radius=34, fill=TINTA); C_9(pil, tl, 540, 1182)
    for j in range(9):
        t0 = 3.18 + j * 0.09
        if tl > t0: pegar(pil, SOBRE_CHICO, 108 + j * 108, 200, pop(tl, t0, 0.12))
texto_9.caja_titulo = (100, 150, 980, 260)
C_32 = contador(32, 0.72, dur=0.8, prefijo='', sufijo=' correos', tam=110, color=(255, 255, 255), desde=1)


def texto_32(pil, tl, T):            # "mando 32 correos (0.72) en 30 dias (2.04)"
    if tl >= 0.72:
        d = ImageDraw.Draw(pil); d.rounded_rectangle([210, 1105, 870, 1260], radius=34, fill=TINTA); C_32(pil, tl, 540, 1182)
    if tl > 2.04: pegar(pil, pastilla('en 30 días', 52, fondo=ROJO), 540, 200, pop(tl, 2.04))
texto_32.caja_titulo = (300, 140, 780, 260)


def pregunta(pil, tl, T):            # "?" entre las dos marcas en la pantalla dividida
    k = pop(tl, 0.2)
    if k > 0:
        d = ImageDraw.Draw(pil); r = 70 * lerp(0.8, 1, k); d.ellipse([540 - r, 650 - r, 540 + r, 650 + r], fill=ROJO, outline=(255, 255, 255), width=6)
        d.text((540, 650), '?', font=font(90), fill=(255, 255, 255), anchor='mm')


# ------------------------------------------------------------ tomas
def L(im, nombre, v1=None, marcas=(), y=300, ancho=W, dur_mov=None):
    c, _ = panel(im, y=y, ancho=ancho); return lienzo(c, (0, 0, W), v1 or (20, 36, W - 40), marcas, nombre=nombre, dur_mov=dur_mov)


toma('01', 0.00, 3.38, Serie([
    (0.00, lienzo(Image.fromarray(cubrir(BG, ancla=(0.5, 0.1))), (0, 0, W), (60, 40, W - 120), nombre='commons.wikimedia.org: Bear Grylls')),            # "el de «A prueba de todo»"
    (1.28, clip('d9', 1.35, nombre='dirteaworld.com: video d9 (caja DIRTEA)')),                                    # "invirtiendo dinero"
    (2.40, clip('d10', 48.6, nombre='dirteaworld.com: video d10 (DIRTEA en polvo)', recorte=(1920, 880, 0, 0))),                                         # "hongos en polvo"
]), GAB, T_(['¿Qué hace Bear Grylls', 'invirtiendo en hongos?'], 200, 64, t0=-1.0, clave={'Bear', 'Grylls'}, emo='🍄'))
toma('02', 3.38, 6.04, Serie([
    (0.00, clip('d2', 36.5, nombre='dirteaworld.com: video d2 (preparando)')),                                    # "DIRTEA convierte hongos"
    (1.40, L(abrir(f'{DP}/dirtea-chai_1.jpg'), 'dirteaworld.com: chai', y=330)),                                  # "en chai"
    (1.82, L(abrir(f'{DP}/dirtea-cacao-super-blend_3.jpg').crop((0, 300, 1000, 1000)), 'dirteaworld.com: cacao', y=380)),   # "cacao"
    (2.28, L(abrir(f'{DP}/calm-gummies_0.jpg'), 'dirteaworld.com: gomitas', y=330)),                             # "y gomitas"
]), GAB, logo_d())
toma('03', 6.04, 8.72, Grafico(g_x3), GAB)
toma('04', 8.72, 11.20, Serie([
    (0.00, clip('1670865851304920', 6.0, nombre='anuncio-video:1670865851304920 (Let Loose)')),                   # "Por otro lado, Let Loose"
    (1.40, L(L4.crop((0, 400, 667, 1140)), 'letloose (correo 4): frasco', y=260, v1=(40, 60, W - 80))),           # "con un suplemento"
]), GAB, logo_l(0.72))
toma('05', 11.20, 13.84, Grafico(g_2m), GAB)
toma('06', 13.84, 17.66, Mitades(clip('d7', 24.0, nombre='dirteaworld.com: video d7 (frasco)'),
                                 clip('1096568496337879', 10.6, nombre='anuncio-video:1096568496337879 (producto)')), 'C',
     varios(logo_d(), logo_l(), pregunta))
toma('07', 17.66, 21.88, Serie([
    (0.00, clip('d10', 57.6, nombre='dirteaworld.com: video d10 (s58)', recorte=(1920, 880, 0, 0))),                                         # "DIRTEA aposto por lo que haria..."
    (1.38, L(D1.crop((677, 340, 1037, 660)), 'dirtea (autopsia): recorte Black Friday', y=230)),                  # "en Black Friday, ofertas por todos lados"
]), GAB, logo_d())
_c8, _f8 = panel(D1.crop((282, 150, 640, 335)), y=330)
toma('08', 21.88, 23.70, lienzo(_c8, (0, 0, W), (20, 36, W - 40), [('caja', _f8((F_40[0] - 282, F_40[1] - 150, F_40[2], F_40[3])), 0.44)],
                                nombre='dirtea (autopsia): recorte 40% off & free gifts'), GAB,
     varios(logo_d(), T_(['40% + regalos'], 1180, 60, t0=1.34)))
toma('09', 23.70, 26.36, Grafico(g_50), GAB)
toma('10', 26.36, 28.68, L(D2.crop((323, 387, 961, 820)), 'dirtea (autopsia): recorte chai 24 horas', y=300), GAB,
     varios(logo_d(), T_(['Y otra más…'], 1180, 60, t0=0.58)))
toma('11', 28.68, 31.74, clip('d7', 8.4, nombre='dirteaworld.com: video d7 (clienta con el frasco)'), GAB)
toma('12', 31.74, 34.96, Grafico(g_cuando), GAB)
toma('13', 34.96, 37.46, clip('2569635836834382', 19.0, nombre='anuncio-video:2569635836834382 (Let Loose)'), GAB, logo_l())
toma('14', 37.46, 39.98, L(L2.crop((0, 1100, 667, 1700)), 'letloose (correo 2): foto de la fundadora', y=260), GAB,
     varios(logo_l(), T_(['Una historia'], 1180, 60, t0=1.56)))
toma('15', 39.98, 41.74, clip('1096568496337879', 6.6, nombre='anuncio-video:1096568496337879 (fundadora)'), GAB, logo_l())
toma('15b', 41.74, 44.66, Grafico(g_bandeja), GAB)
toma('16', 44.66, 49.28, L(D1.crop((0, 150, 1080, 820)), 'dirtea (autopsia): correos completos', y=290, v1=(40, 70, W - 80)), GAB,
     varios(logo_d(), texto_32))
_c17, _ = panel(L1, y=0)
toma('17', 49.28, 53.36, lienzo(_c17, (0, 0, W), (0, 1150, W), nombre='letloose (correo 1): bienvenida', dur_mov=4.0), GAB, varios(logo_l(), texto_9))
toma('18', 53.36, 58.78, Serie([
    (0.00, L(L4.crop((0, 0, 667, 460)), 'letloose (correo 4): 20% off', y=150)),                                  # "y cada uno decia una sola cosa"
    (1.92, clip('1498433648773565', 7.6, nombre='anuncio-video:1498433648773565 (fundadora: I created)')),        # "¿Quien la creo?"
    (2.80, L(L1.crop((0, 3120, 667, 3290)), 'letloose (correo 1): certificaciones', y=380)),                      # "¿Por que funciona?"
    (3.58, L(L3.crop((0, 150, 667, 340)), 'letloose (correo 3): what we are / what we are not', y=380)),           # "¿En que se diferencia?"
    (4.42, L(L1.crop((0, 2990, 667, 3110)), 'letloose (correo 1): 4,84 estrellas', y=400)),                       # "¿Que dicen sus clientes?"
]), GAB, varios(logo_l(), entre(1.92, 2.80, T_(['Quién la creó'], 230, 58)), entre(2.80, 3.58, T_(['Por qué funciona'], 230, 58)),
                entre(3.58, 4.42, T_(['En qué se diferencia'], 230, 58)), entre(4.42, 9, T_(['Qué dicen sus clientes'], 230, 58))))
_c19, _f19 = panel(L2.crop((0, 0, 667, 1000)), y=200, ancho=900)
toma('19', 58.78, 62.06, lienzo(_c19, (0, 0, W), (40, 220, W - 80), [('caja', _f19(F_FUNDADOR), 1.02)], nombre='letloose (correo 2): mensaje de la fundadora', dur_mov=0.8),
     GAB, logo_l())
_c20, _ = panel(D1.crop((0, 700, 245, 1300)), y=0)
toma('20', 62.06, 66.10, Mitades(lienzo(_c20, (0, 0, W), (60, 120, W - 120), nombre='dirtea (autopsia): precios'),
                                 clip('1670865851304920', 14.0, nombre='anuncio-video:1670865851304920 (s14: caja de regalo)')), 'C',
     varios(logo_d(), logo_l()))
toma('21', 66.10, 71.93, Mitades(clip('d9', 12.0, nombre='dirteaworld.com: video d9 (s12: tomando DIRTEA)'),
                                 clip('2569635836834382', 30.5, nombre='anuncio-video:2569635836834382 (s30: con el frasco)')), 'C',
     varios(logo_d(), logo_l(), T_(['¿Cuál prefieres?'], 1190, 66, t0=0.9, emo='👇')))

# Gabriel cambia de lugar toma a toma; en las pantallas divididas va al centro
LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S):
    if _sh['gab'] != 'C' or not isinstance(_sh['fondo'], Mitades): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 '¿Qué hace el de_«A prueba de todo»', 'invirtiendo dinero en una', 'marca de hongos en *polvo?',
 'DIRTEA convierte *hongos', 'en chai, cacao y *gomitas', 'y ha *triplicado', 'sus ventas en los últimos dos *años.',
 'Por otro lado, ~ *Let_Loose', 'con un suplemento', 'para la digestión', 'vendió casi 2 millones de *dólares', 'en 6 *meses.',
 'Las dos tienen un enfoque', 'muy *especial', 'pero lo usan de forma', 'totalmente *diferente.',
 '*DIRTEA', 'apostó por lo que haría', 'casi cualquier marca', 'en Black *Friday,', 'ofertas por todos *lados.',
 'Arrancó con 40% ~ y *regalos', 'y días después llegó', 'hasta un 50% ~', 'en toda la *tienda.',
 'Y cuando eso *terminó,', 'siguió con otras *promociones.',
 'Pero ponte en el lugar', 'del *cliente,', '¿cuándo le convenía *comprar?', 'Con el *40,', 'con el *50', 'o mejor esperaba', 'las siguientes que *salieran.',
 'Mientras que ~ *Let_Loose', 'se fue por un lado', 'totalmente *diferente.',
 'En vez de cambiar el *número', 'le contó una *historia', 'a su *cliente.',
 'Pero lo interesante', 'es dónde pasó *esto,', 'en un lugar que casi', 'todas las marcas tienen olvidado,', 'el *correo.',
 'DIRTEA mandó 32 *correos', 'en 30 *días', 'y el número de la oferta', 'fue cambiando por el *camino.',
 'Mientras que ~ *Let_Loose', 'cuando le dejaban los *datos', 'le mandaba *9', 'pero uno detrás de *otro', 'y cada uno decía', 'una sola *cosa.',
 '¿Quién la *creó?', '¿Por qué *funciona?', '¿En qué se *diferencia?', '¿Qué dicen sus *clientes?',
 'Y el último lo escribe', 'el *fundador', 'con un mensaje personal', 'con la *garantía.',
 'Una te habla en todo', 'momento de *precios', 'y la otra te cuenta una *historia', 'y te acompaña después', 'de la *compra.',
 'Si fueras su cliente, ¿qué *prefieres?', '¿Una marca con muchos *descuentos', 'o una con la que', 'conectas *perfectamente?', 'Déjamelo en los *comentarios.',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal43.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
