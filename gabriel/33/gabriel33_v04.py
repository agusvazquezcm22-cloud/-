"""Video 33 · "La estrategia de anuncios de 600M de AG1" · v04
Igual que la v01 (aprobada por Agus: "Top") con el recorte de Gabriel FIJO donde Agus lo marco con una captura del 34 v01
(2026-11-20): "Tiene que estar en esa ubicacion, no mas abajo". Abajo al centro, mismo tamano y altura en todo el video ('C').
Tomas, subtitulos y sonidos son los de la v01.
v04: correcciones de Gabriel (2026-11-21): en el segundo 21, en vez de una segunda captura de la Biblioteca va el VIDEO real de esa
creadora (el anuncio 1124980317094382). Cierre con cola y receta 2 de sonido (reglas de Agus). Lo demas, igual.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v33')
RAW = f'{A}/dl/crudo33.mp4'
DUR = 59.0                   # 58,13 del crudo + 0,87 de cola
CABEZA = 735                 # fila del crudo donde esta el tope de su cabeza (medido: 716-753)
CENTRO = 528                 # columna del centro de su cabeza (medido: 503-546)
T_FIN = 53.92                # desde aca (cierre) va el plano mas grande al centro
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'

# logo de AG1: avatar de su pagina en la Biblioteca de Anuncios (circulo)
_av = Image.open(f'{A}/cap/vid_fbg0.png').convert('RGB').crop((72, 282, 248, 458))
_m = Image.new('L', _av.size, 0); ImageDraw.Draw(_m).ellipse([2, 2, _av.width - 3, _av.height - 3], fill=255)
_av.putalpha(_m)
configurar(A, logo=_av)

FT = json.load(open(f'{A}/cap/ftmeta.json'))
VIDM = json.load(open(f'{A}/cap/vid_fbmeta.json'))
SOM = json.load(open(f'{A}/cap/so_fbmeta.json'))
VID = np.concatenate([img(f'{A}/cap/vid_fbg{i}.png') for i in range(2)], 0)      # Biblioteca, filtro "videos" (2 px por px CSS)
SO = np.concatenate([img(f'{A}/cap/so_fbg{i}.png') for i in range(2)], 0)        # Biblioteca, busqueda del texto repetido
CARD = lambda i: f'{A}/cap/so_card_{i}.png'
FRASE = (26, 270, 215, 14); QUIEN = (62, 245, 361, 16)                          # dentro de cada tarjeta, en px CSS


def _mosaico(ids):
    """Cuatro anuncios de creadores distintos, uno debajo del otro: mismo texto, distinta cuenta."""
    usar(*[f'tarjeta:{i}' for i in ids])
    c = Image.new('RGB', (W, H), (240, 242, 245)); pos = []
    for n, i in enumerate(ids):
        t = Image.open(CARD(i)).convert('RGB').crop((16, 440, 876, 664)); k = 1000 / t.width
        t = t.resize((1000, int(t.height * k)), Image.LANCZOS); y = 150 + n * (t.height + 34)
        d = ImageDraw.Draw(c); d.rounded_rectangle([34, y - 6, 1046, y + t.height + 6], radius=22, fill=(255, 255, 255))
        c.paste(t, (40, y)); pos.append((y, 2 * k))
    return c, pos
MOS, _pos = _mosaico(['1401150738351533', '1456556149769437', '1117535974329466', '1596436251777812'])
def _en_mosaico(rect, n):
    y, f = _pos[n]; return (40 + (rect[0] - 8) * f, y + (rect[1] - 220) * f, rect[2] * f, rect[3] * f)
SUBRAYADOS = [('sub', _en_mosaico(FRASE, n), 0.45 + 0.28 * n) for n in range(4)]
NOMBRE = (62, 226, 372, 20)          # renglon "Fulano with AG1 by Athletic Greens"
NOMBRES = [('caja', _en_mosaico(NOMBRE if n < 3 else (22, 226, 412, 20), n), 0.12 + 0.3 * n) for n in range(4)]   # la 4a tarjeta no tiene avatar: el nombre empieza mas a la izquierda


# ------------------------------------------------------------ graficos propios
def _mic(tam=124):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=TINTA + (255,))
    d.rounded_rectangle([tam * .40, tam * .20, tam * .60, tam * .58], radius=12, fill=(255, 255, 255, 255))
    d.arc([tam * .30, tam * .30, tam * .70, tam * .70], 0, 180, fill=(255, 255, 255, 255), width=6)
    d.line([(tam * .5, tam * .70), (tam * .5, tam * .82)], fill=(255, 255, 255, 255), width=6)
    d.line([(tam * .38, tam * .82), (tam * .62, tam * .82)], fill=(255, 255, 255, 255), width=6)
    return c
def _pagina(col, w=250, h=150):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=18, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([0, 0, w - 1, 34], radius=18, fill=TINTA + (255,)); d.rectangle([0, 20, w - 1, 34], fill=TINTA + (255,))
    d.ellipse([18, 52, 62, 96], fill=col + (255,))
    for i, lw in enumerate((130, 100)): d.rounded_rectangle([78, 56 + i * 24, 78 + lw, 68 + i * 24], radius=6, fill=(205, 208, 214, 255))
    d.rounded_rectangle([18, 108, 120, 134], radius=10, fill=col + (255,))
    return c
MIC = _mic(); PAGS = [_pagina(c) for c in ((30, 150, 90), (60, 110, 200), (217, 119, 87))]


def g_podcasts(tl, T):                # "dependiendo del podcast ... una pagina hecha solo para ti"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    txt(d, (W / 2, 390), 'Cada podcast, su propia página', 54, GRIS, 'SemiBold')
    for n in range(3):
        y = 560 + n * 190; t0 = 0.15 + n * 0.55
        pegar(im, MIC, 230, y, pop(tl, t0))
        flecha_recta(d, (330, y), (640, y), ease((tl - t0 - 0.15) / 0.22))
        pegar(im, PAGS[n], 800, y, pop(tl, t0 + 0.3))
    return im


def g_publicos(tl, T):                # "otros publicos con dolores parecidos"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, pastilla('El mismo mensaje', 62), W / 2, 470)
    for n, (x, s) in enumerate(((200, 'Militares'), (540, 'Viajeros'), (880, 'Primera compra'))):
        t0 = 0.55 + n * 0.3
        flecha_recta(d, (W / 2 + (x - W / 2) * 0.25, 560), (x, 770), ease((tl - t0) / 0.22))
        pegar(im, pastilla(s, 44, fondo=(255, 255, 255), color=TINTA, borde=TINTA, pad=(30, 22)), x, 850, pop(tl, t0 + 0.15))
    return im


def g_guardar(tl, T):                 # "guarda este video"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    k = pop(tl, 0.05, 0.2); lleno = tl >= 0.42
    w, h = int(300 * lerp(0.86, 1, k)), int(400 * lerp(0.86, 1, k)); x0, y0 = (W - w) // 2, 690 - h // 2
    pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0 + w // 2, y0 + h - int(h * 0.26)), (x0, y0 + h)]
    if lleno: d.polygon(pts, fill=TINTA)
    d.line(pts + [pts[0]], fill=TINTA, width=22, joint='curve')
    return im


def chip_claude(pil, tl, T):
    k = pop(tl, 0.68)                 # aparece cuando lo nombra, chico, arriba de Gabriel
    if k > 0 and tl < 1.60: pegar(pil, _CLAUDE, 540, 1172, lerp(0.85, 1, k))     # justo arriba de la cabeza de Gabriel
_CLAUDE = pastilla('Claude', 58, fondo=(217, 119, 87))


PORTADA = lambda: clip('2196762624580910', 1.0, nombre='portada', encaje=(0.68, 330))      # anuncio limpio (batido verde en el shaker), entero, con el titulo arriba

# ------------------------------------------------------------ tomas
toma('01', 0.00, 1.10, PORTADA(), 'PL', T_(['La estrategia de anuncios', 'de 600M de AG1'], 208, 66, t0=-1.0, clave={'600M'}, emo='🤯'))
toma('02', 1.10, 2.54, captura(f'{A}/cap/ft_m600.png', [(FT['m600'], 0.3, None, None)], w0=2460, w1=2240, nombre='fortune:600M'), 'G')
toma('03', 2.54, 4.30, Serie([(0, clip('1601980348350474', 1.0)), (0.90, clip('2337369557048219', 1.0))]), lambda tl: 'PR' if tl < 0.90 else 'PL')
toma('04', 4.30, 5.50, clip('1456556149769437', 7.4), 'PR')
toma('05', 5.50, 8.84, Serie([(0, lienzo(VID, (340, 700, 2200), (340, 889, 2200), nombre='biblioteca-videos:filas 1-3')),
                               (1.84, lienzo(VID, (60, 5200, 1900), (940, 5220, 1900), nombre='biblioteca-videos:filas 4-6'))]), lambda tl: 'ML' if tl < 1.84 else 'MR')
_r = [v * 2 for v in VIDM['results'][:4]]
toma('06', 8.84, 10.20, lienzo(VID, (0, 0, 1700), (0, 300, 1500), [('caja', tuple(_r), 0.3), ('flecha_ad', tuple(_r), 0.3)], nombre='biblioteca-videos:cabecera', dur_mov=0.5), 'ML')
toma('07', 10.20, 11.30, clip('1499240032112635', 0.8), 'G')
toma('08', 11.30, 14.52, Serie([(0, clip('1728922928202874', 1.0)), (1.60, lienzo(SO, (340, 5100, 2200), (340, 5500, 2200), nombre='biblioteca-texto:filas 4-6'))]),
     lambda tl: 'PL' if tl < 1.60 else 'PR', chip_claude)
toma('09', 14.52, 18.04, Lienzo(MOS, (0, 0, W), (20, 16, W - 40), SUBRAYADOS), 'PR')
toma('10', 18.04, 19.80, Lienzo(MOS, (0, 70, 800), (0, 285, 780), NOMBRES, dur_mov=1.0), 'PR')
toma('11', 19.80, 22.98, Serie([(0, tarjeta(CARD('1451810420413126'), [('caja', NOMBRE, 0.2)])),
                                (1.59, clip('1124980317094382', 31.0))]), lambda tl: 'PL' if tl < 1.59 else 'PR')
toma('12', 22.98, 24.14, tarjeta(CARD('3459371154253454'), [('caja', FRASE, 0.15)]), 'PL')
toma('13', 24.14, 25.54, Serie([(0, clip('1770995120621934', 1.0)), (0.35, clip('1131363089942395', 1.0)), (0.70, clip('2124813031574283', 5.0)), (1.05, clip('1409776720886079', 1.0))]), 'PR')
toma('14', 25.54, 28.18, Serie([(0, clip('1461710955927501', 1.0)), (1.06, anuncio('1596436251777812', 0)), (1.86, anuncio('2347218269151991', 0))]),
     lambda tl: 'PL' if tl < 1.06 else ('PR' if tl < 1.86 else 'PL'))
toma('15', 28.18, 30.02, clip('1013212934837198', 0.5), 'PR')
toma('16', 30.02, 32.16, anuncio('2337369557048219', 0.03, [('caja', (0.17, 0.795, 0.68, 0.115), 1.3)]), 'PL')
toma('17', 32.16, 34.84, Serie([(0, anuncio('29384670931142984', 0.04)), (1.22, anuncio('1147667207657446', 0.03))]), lambda tl: 'PR' if tl < 1.22 else 'PL')
toma('18', 34.84, 36.18, clip('1401150738351533', 7.6), 'G')
toma('19', 36.18, 41.12, Serie([(0, captura(f'{A}/cap/ft_eps.png', [(FT['eps'], 2.0, None, 'flecha_ai')], nombre='fortune:episodios')),
                                (3.54, captura(f'{A}/cap/ft_eps.png', [(FT['eps_1'], 0.12, None, 'flecha_ad')], w0=1500, w1=1180, nombre='fortune:episodios'))]),
     lambda tl: 'ML' if tl < 3.54 else 'MR')
toma('20', 41.12, 44.92, G(g_podcasts, k=0.76), 'G')
_s = [v * 2 for v in SOM['results'][:4]]
toma('21', 44.92, 47.82, lienzo(SO, (0, 0, 1700), (0, 40, 1400), [('caja', tuple(_s), 0.9), ('flecha_ad', tuple(_s), 0.9)], nombre='biblioteca-texto:cabecera', dur_mov=0.8), 'ML')
_c5 = SOM['cards']['1516530687243066']
toma('22', 47.82, 49.62, tarjeta(CARD('1516530687243066'), [('caja', _c5['phr'][0], 0.5)]), 'PR')
toma('23', 49.62, 52.04, G(g_publicos, logo=True, k=0.86), 'G')
toma('24', 52.04, 53.92, Serie([(0, clip('1884119762755431', 7.5)), (0.62, clip('2448516895887382', 4.0)), (1.24, clip('2704233700026537', 2.0))]),
     lambda tl: 'PL' if tl < 0.62 else ('PR' if tl < 1.24 else 'PL'))
toma('25', 53.92, 55.98, G(g_guardar, k=0.84), 'G')
toma('26', 55.98, 59.00, PORTADA(), 'PL')
for _s in S: _s['gab'] = 'C'                                          # Gabriel fijo: abajo al centro en TODAS las tomas
SHOTS = S
REPETICION_PERMITIDA = {'portada': 'regla 10 de la guia de Gabriel: el cierre vuelve a la imagen del inicio',
                        'fortune:episodios': 'misma captura, la toma sigue: el recuadro pasa de 11.000 episodios a 700 podcasts'}

GUION = [
 'AG1 vende cerca de 600 *millones', 'de dólares al año',
 'y este es el sistema', 'de anuncios que hay detrás', 'para que lo uses con tu *marca',
 'primero, ahora mismo', 'tienen más de 1.500 *anuncios', 'activos en Meta', 'y más de 1.000 son *videos',
 'pero aquí viene lo *interesante', 'con ayuda de *Claude', 'revisé los 121', 'que más se están mostrando',
 'y 44 de ellos', 'dicen exactamente lo *mismo', 'palabra por palabra',
 'lo único que cambia', 'es quién lo *dice',
 'cada uno lo está publicando', 'un creador de contenido *distinto', 'desde su propia cuenta',
 'ya no están probando el *mensaje', 'están probando nuevas *caras',
 'y mira, cuando cambian', 'el anuncio lo hacen', 'según quien lo *ve',
 'si eres *militar', 'te ofrecen un descuento',
 'si viajas mucho', 'te muestran sus sobres de *viaje',
 'y si es tu primera compra', 'te regalan el kit de *bienvenida',
 'pero lo que más me *sorprendió', 'es que desde 2022', 'han patrocinado', 'más de 11.000 ~ *episodios', 'en más de 700 podcasts',
 'y dependiendo del podcast', 'desde el que llegues', 'te espera una *página', 'hecha solo para ti',
 'o sea, AG1 ya no está', 'buscando su próximo anuncio *ganador',
 'ya entendió exactamente', 'qué mensaje *vende', 'y ahora está buscando otros *públicos', 'con dolores parecidos',
 'para posicionarse', 'como la mejor *solución',
 'guarda este *video', 'para el día que tu anuncio', 'ganador se canse,', 'estoy seguro que', 'lo vas a *necesitar',
]
_pal = json.load(open(f'{A}/pal33.json'))[:-2]          # las dos ultimas "palabras" son ruido del transcriptor
SUBS = armar_tarjetas(_pal, GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
