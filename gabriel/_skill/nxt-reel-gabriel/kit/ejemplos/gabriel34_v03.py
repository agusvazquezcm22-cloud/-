"""Video 34 · "La estrategia de recompra de The Everyday Lab" · v03 (= v01: Gabriel fijo abajo al centro, la ubicacion que Agus marco con su captura)
Formato pantalla verde aprobado. Novedad (pedido de Agus, 2026-11-20): Gabriel SIEMPRE en el mismo lugar
(abajo al centro, mismo tamano). Tiempos de la transcripcion del crudo (62,8 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v34')
RAW = f'{A}/dl/crudo34.mp4'
DUR = 62.8
CABEZA = 720                 # fila del crudo donde esta el tope de la cabeza de Gabriel (medido: 696-754)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'                    # lugar fijo de Gabriel en todo el video

# logo de la marca: encabezado de su sitio
_lg = Image.open(f'{A}/cap/prod_top.png').convert('RGB').crop((96, 138, 866, 262))
_chip = Image.new('RGBA', (_lg.width + 60, _lg.height + 36), (0, 0, 0, 0))
ImageDraw.Draw(_chip).rounded_rectangle([0, 0, _chip.width - 1, _chip.height - 1], radius=30, fill=(255, 255, 255, 255))
_chip.paste(_lg, (30, 18))
configurar(A, logo=_chip)

ART = json.load(open(f'{A}/cap/artmeta.json')); SUSM = json.load(open(f'{A}/cap/susmeta.json'))
PAGM = json.load(open(f'{A}/cap/pag_fbmeta.json')); PVM = json.load(open(f'{A}/cap/pv_fbmeta.json'))
PAG = np.concatenate([img(f'{A}/cap/pag_fbg{i}.png') for i in range(2)], 0)          # Biblioteca de Anuncios (2 px por px CSS)
ARTL = img(f'{A}/cap/artl_tira.png')                                                   # articulo entero ya unido (2 px por px CSS)
PROD = img(f'{A}/cap/prod_top.png')                                                    # pagina del producto (3 px por px CSS)
P3 = lambda r: tuple(v * 3 for v in r)
V_PACKS = (1230, 2160, 1230)                                                           # columna de compra con los paquetes ARRIBA de la franja de subtitulos
V_SUS = (1080, 1650, 1380)                                                             # idem con la caja de suscripcion arriba y margen para la flecha
PACK = {1: (452, 862, 80, 118), 2: (540, 846, 84, 134), 3: (632, 846, 84, 134), 4: (724, 846, 84, 134)}
SUSCRIP = (452, 658, 352, 112)


def _revista():
    """El articulo visto de lejos, como una pagina de revista (desde abajo del titulo: su guia pide no hacer zoom al titular)."""
    tira = Image.fromarray(ARTL[1040:1040 + 6400]).resize((580, 2263), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (236, 234, 228)); d = ImageDraw.Draw(c)
    d.rectangle([244, 84, 836, H], fill=(205, 203, 198)); c.paste(tira, (250, 90))
    return c
REVISTA = _revista()


# ------------------------------------------------------------ graficos propios
def _caja_txt(s, col=(255, 255, 255), txtcol=TINTA, w=360, h=230):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=col + (255,), outline=TINTA + (255,), width=8)
    d.text((w / 2, h / 2), s, font=font(66), fill=txtcol + (255,), anchor='mm'); return c
C_TIENDA, C_ART = _caja_txt('Tienda'), _caja_txt('Artículo', (250, 255, 0))


def g_tienda_articulo(tl, T):        # "ademas de su tienda en linea, tienen un articulo"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_TIENDA, 300, 640, pop(tl, 0.08))
    k = pop(tl, 0.78)
    if k > 0: txt(d, (540, 640), '+', 110, GRIS)
    pegar(im, C_ART, 780, 640, k)
    return im


def _paquete(tam=190):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, tam - 1, tam - 1], radius=22, fill=(196, 150, 96, 255), outline=TINTA + (255,), width=7)
    d.rectangle([tam * .44, 0, tam * .56, tam], fill=(160, 116, 66, 255)); d.line([(0, tam * .34), (tam, tam * .34)], fill=TINTA + (255,), width=5)
    return c
def _tilde(tam=96):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=VERDE_OSC + (255,))
    d.line([(tam * .26, tam * .52), (tam * .44, tam * .70), (tam * .76, tam * .32)], fill=(255, 255, 255, 255), width=12, joint='curve'); return c
PAQ, TILDE = _paquete(), _tilde()


def g_segunda(tl, T):                # "la segunda compra ya esta asegurada"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n, (x, s) in enumerate(((330, '1ª entrega'), (750, '2ª entrega'))):
        k = pop(tl, 0.08 + n * 0.45)
        pegar(im, PAQ, x, 600, k)
        if k > 0.6: txt(d, (x, 760), s, 50, GRIS, 'SemiBold')
    flecha_recta(d, (450, 600), (630, 600), ease((tl - 0.35) / 0.2))
    pegar(im, TILDE, 838, 512, pop(tl, 1.44))                 # el tilde entra con la palabra "asegurada" (49,38)
    return im


def g_enviar(tl, T):                 # "mandale este video al encargado"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    k = pop(tl, 0.05, 0.2); s = lerp(0.85, 1, k); cx, cy = 540 + 40 * (1 - k), 660
    pts = [(-190, -40), (190, -150), (40, 170), (-10, 30)]
    P = [(cx + x * s, cy + y * s) for x, y in pts]
    d.polygon(P, fill=TINTA); d.line([P[3], P[1]], fill=(250, 250, 248), width=10)
    return im


# ------------------------------------------------------------ tomas
PORTADA = lambda: clip('1897138358362815', 1.0, nombre='portada', encaje=(0.68, 330))    # anuncio real de la marca: el producto, entero, con el titulo arriba
_fe = [P3x for P3x in [tuple(v * 2 for v in f[:4]) for f in PAGM['fechas'][:3]]]
_r = tuple(v * 2 for v in PAGM['results'][:4])
_pv = PVM['cards']['1124013453681159']

toma('01', 0.00, 2.06, PORTADA(), GAB, T_(['La estrategia de recompra', 'de The Everyday Lab'], 208, 64, t0=-1.0, clave={'recompra'}, emo='🤯'))
toma('02', 2.06, 4.50, captura(f'{A}/cap/art_m11.png', [(ART['m11'], 0.9, None, 'flecha_ai')], nombre='articulo:11.000 mexicanas'), GAB)
toma('03', 4.50, 5.92, Serie([(0, clip('2247147509476476', 1.0)), (0.80, clip('1788719022212894', 1.0))]), GAB)
toma('04', 5.92, 7.16, clip('29772789222328669', 1.0), GAB)
toma('05', 7.16, 9.74, lienzo(PAG, (0, 0, 1700), (0, 300, 1500), [('caja', _r, 0.9), ('flecha_ad', _r, 0.9)], nombre='biblioteca:cabecera', dur_mov=0.7), GAB)
toma('06', 9.74, 12.84, Serie([(0, lienzo(PAG, (60, 380, 1560), (60, 440, 1500), [('sub', _fe[n], 0.25 + 0.3 * n) for n in range(2)], nombre='biblioteca:fechas')),
                               (1.42, lienzo(PAG, (60, 5300, 1900), (940, 5320, 1900), nombre='biblioteca:filas 4-6'))]), GAB)
toma('07', 12.84, 14.46, Serie([(0, clip('1444794981074414', 0.3)), (0.54, clip('28935788239456073', 1.0)), (1.08, clip('1665766688468142', 1.0))]), GAB)
toma('08', 14.46, 16.22, clip('1710450817266219', 1.0), GAB)
toma('09', 16.22, 21.48, Serie([(0, tarjeta(f'{A}/cap/pv_card_1124013453681159.png', [('sub', _pv['phr'][0], 0.5)], nombre='tarjeta:polvo')),   # "eso que mas te duele"
                                (1.72, clip('1947201419590680', 13.2)),                                                                   # el polvo de siempre: "absorcion 15-30 % maximo"
                                (3.28, clip('2390595551724057', 3.6))]), GAB)
toma('10', 21.48, 24.48, Serie([(0, anuncio('4559683627604264', 0.05)), (1.45, clip('1625851928922760', 3.3))]), GAB)
toma('11', 24.48, 25.80, G(g_tienda_articulo, k=0.92), GAB)
toma('12', 25.80, 27.68, lienzo(ARTL, (0, 1040, 1640), (0, 1500, 1640), nombre='articulo:inicio'), GAB)
_pq = (88, 13980, 1472, 464)
toma('13', 27.68, 30.06, lienzo(ARTL, (0, 13200, 1640), (0, 13300, 1640), [('caja', _pq, 1.0)], nombre='articulo:paquetes'), GAB)
toma('14', 30.06, 31.58, Lienzo(REVISTA, (0, 0, W), (0, 90, W)), GAB)
S[-1]['fuentes'] = ['articulo:de lejos']
toma('15', 31.58, 40.40, Serie([
    (0.00, Lienzo(PROD, (0, 0, 2460), V_PACKS, dur_mov=0.9)),                                                         # "mira como suben el ticket"
    (1.14, Lienzo(PROD, V_PACKS, None, [('caja', P3(PACK[1]), 0.5, 1.98), ('caja', P3(PACK[2]), 1.98, 3.42), ('caja', P3(PACK[3]), 3.42, 4.36), ('caja', P3(PACK[4]), 4.36, 5.42)])),
    (6.56, Lienzo(PROD, V_PACKS, V_SUS, [('caja', P3(SUSCRIP), 0.9), ('flecha_ai', P3(SUSCRIP), 0.9)])),   # "su estrategia de suscripcion"
]), GAB)
S[-1]['fuentes'] = ['tienda:columna de compra']
_f = lambda y: (20, y - 12, 380, 60)
toma('16', 40.40, 42.76, captura(f'{A}/cap/sus_frec.png', [([_f(520)], 0.25, 0.85, None), ([_f(423)], 0.85, 1.45, None), ([_f(326)], 1.45, None, None)], w0=2460, w1=2200, yrel=0.33, nombre='suscripciones:frecuencias'), GAB)
toma('17', 42.76, 47.94, Serie([(0, clip('2164872967459312', 1.0)),
                                (2.10, captura(f'{A}/cap/sus_min2.png', [(SUSM['min2'], 1.16, None, 'flecha_ai')], nombre='suscripciones:minimo 2'))]), GAB)
toma('18', 47.94, 49.86, G(g_segunda, k=0.92), GAB)
toma('19', 49.86, 52.34, anuncio('2252390632322718', 0.06), GAB)
toma('20', 52.34, 56.18, Serie([
    (0.00, anuncio('28935788239456073', 0.02, [('caja', (0.05, 0.535, 0.55, 0.09), 0.3)], encaje=(0.62, 40))),               # "el habito": GLOW todos los dias + la semana
    (0.96, clip('28751467064464376', 9.3)),                                                                                # "3 meses de usarlo y me siento otra"
    (1.66, anuncio('1049972658093063', 0)),                                                                                # comentario de una clienta
    (2.39, anuncio('1516075690337129', 0.02, [('caja', (0.465, 0.268, 0.478, 0.07), 0.15), ('caja', (0.534, 0.578, 0.44, 0.07), 0.6)])),   # "el segundo bote", "el tercer insumo"
]), GAB)
toma('21', 56.18, 57.98, G(g_enviar, k=0.92), GAB)
toma('22', 57.98, 59.94, clip('1630625931987533', 20.2), GAB)
toma('23', 59.94, 62.80, PORTADA(), GAB)
SHOTS = S
REPETICION_PERMITIDA = {'portada': 'regla 10 de la guia de Gabriel: el cierre vuelve a la imagen del inicio'}

GUION = [
 'The Everyday Lab es', 'una marca mexicana de *colágeno', 'que afirma que más de 11.000 ~ *mexicanas', 'ya la eligieron',
 'y este es el sistema exacto', 'que hay detrás', 'para que lo uses con tu *marca',
 'En este momento tienen', 'más de 70 *anuncios', 'activos en Meta',
 'Casi todos de las últimas *semanas,', 'lo que muestra que tienen', 'bastante *rotación',
 'y en muchos sale la *fundadora',
 'Y no te hablan de lo bueno', 'que es su colágeno,', 'prefieren mencionarte', 'eso que más te *duele',
 'porque entienden que', 'probablemente', 'el que estás tomando', 'ya no funciona como *antes',
 'y para esto está usando', 'una estrategia', 'que pocas marcas', 'en el sector usan',
 'Además de su tienda en línea,', 'tienen un *artículo', 'que parece de revista',
 'Y al final del artículo', 'te ofrecen sus *combos,', 'a esto se le llama *publirreportaje',
 'Y mira cómo suben el *ticket',
 'Un frasco cuesta', '899 *pesos,', 'si llevas 2 te dan el *5%,', 'si llevas 3 el *10%', 'y llevas 4 el *15%',
 'Y claro que no se puede', 'dejar al lado su estrategia', 'de *suscripción',
 'Mientras más', 'seguido lo pides,', 'más barato te *sale',
 'Y si creías que no eran', 'lo suficientemente *astutos', 'para cancelar la suscripción', 'tienes que recibir', 'mínimo 2 *entregas',
 'O sea, la segunda compra', 'ya está *asegurada',
 'The Everyday Lab no está', 'tratando de venderte su *colágeno',
 'Te está vendiendo el *hábito', 'de tomarlo', 'porque es lo único', 'que hace que la clienta *vuelva',
 'Mándale este video', 'al encargado de tu ~ ~ *tienda_en_línea', 'porque probablemente', 'se tenga que *preguntar',
 '¿Qué estamos haciendo', 'para que un cliente', 'nos compre una segunda *vez?',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal34.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
