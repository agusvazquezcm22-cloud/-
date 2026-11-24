"""Video 42 · "La trampa del descuento" (Huel y Extra Life) · v01
Formato pantalla verde, tema general con dos marcas como prueba (guia de Gabriel, "LA TRAMPA DEL DESCUENTO") + todo lo que
Gabriel fue corrigiendo en el 38, 39 y 40:
- Hook 0-3,94 s: rafaga de VIDEOS de las dos marcas (dos cortes en los primeros 3 s), con el titulo encima.
- Gabriel cambia de lugar toma a toma (CI / CD / C), mismo tamano.
- Mas videos que graficos: ningun tramo de grafico propio de mas de ~3,8 s; entre graficos van anuncios reales de Huel y Extra Life
  (Biblioteca de Anuncios) y videos de extra-life.cl. Graficos con figuras (etiqueta, cabeza, calendario, regalo, boton).
- La portada no vuelve al final: el cierre es una persona usando Huel en su dia.
- Termina con la voz (DUR = duracion del crudo, sin cola).
- Marcas rojas solo sobre rectangulos medidos (tarjeta de la Biblioteca con FRASES; texto del creativo de Huel medido por pixeles).
Lo que no se muestra (regla 12): promesas de salud o de peso (se descartaron anuncios con "lose a few pounds", "32-inch waist",
"body fat", GLP-1, "sin caña", y la columna de nutrientes del creativo de Huel), ni precios en grande (la tarjeta de Extra Life
va recortada arriba del creativo, que tiene el precio).
Cambios respecto de la guia: la pagina try.huel.com/uk/trial-box ya no ofrece el shaker gratis (ahora dice "save 10%"): el
shaker gratis se prueba con el anuncio en video de Huel "Free shaker with your first order*" y con el creativo del anuncio
1766309524036309 ("Free T-shirt and shaker"). La tarjeta de ese anuncio no carga en la Biblioteca (la pagina de Huel responde
vacia): se usa su imagen original.
Tiempos de la transcripcion del crudo (58,5 s).
"""
import os, sys, json, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v42')
RAW = f'{A}/dl/crudo42.mp4'
DUR = 58.5                   # termina con el crudo (su voz termina en ~58,0)
CABEZA = 715                 # fila del crudo donde esta el tope de su cabeza (medido: 704-732)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
configurar(A, logo=None)
GRIS = (150, 150, 146)
ROJO_ = (227, 38, 46)


# ------------------------------------------------------------ figuras (contenido entre y 180 y 720: abajo van subtitulos y Gabriel)
def _texto(s, tam, col=TINTA, peso='ExtraBold'):
    f = font(tam, peso); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _etiqueta(texto, w=560, h=220, col=ROJO_, tam=82, apagada=False):
    """Etiqueta de precio con agujero (figura de descuento)."""
    col = GRIS if apagada else col
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.polygon([(0, h / 2), (h * 0.42, 0), (w - 1, 0), (w - 1, h - 1), (h * 0.42, h - 1)], fill=col + (255,))
    d.ellipse([h * 0.26 - 16, h / 2 - 16, h * 0.26 + 16, h / 2 + 16], fill=(250, 250, 248, 255))
    d.text(((h * 0.42 + w) / 2, h / 2), texto, font=font(tam), fill=(255, 255, 255, 255), anchor='mm'); return c


def _regalo(tam=230, col=(30, 150, 90), apagado=False):
    col = GRIS if apagado else col
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle([tam * .08, tam * .38, tam * .92, tam * .98], fill=col + (255,), outline=TINTA + (255,), width=6)
    d.rectangle([0, tam * .24, tam - 1, tam * .42], fill=col + (255,), outline=TINTA + (255,), width=6)
    d.rectangle([tam * .44, tam * .24, tam * .56, tam * .98], fill=(250, 220, 120, 255))
    d.ellipse([tam * .22, tam * .04, tam * .50, tam * .26], outline=(250, 220, 120, 255), width=12)
    d.ellipse([tam * .50, tam * .04, tam * .78, tam * .26], outline=(250, 220, 120, 255), width=12); return c


def _persona(tam=200, col=TINTA):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .08, tam * .44, tam * .92, tam * 1.3], 180, 360, fill=col + (255,)); return c


def _cabeza(w=460, h=460):
    """Cabeza de perfil (silueta) mirando a la derecha."""
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c); n = (60, 60, 66, 255)
    d.ellipse([w * .12, h * .02, w * .86, h * .74], fill=n)                       # craneo
    d.polygon([(w * .80, h * .40), (w * .95, h * .55), (w * .80, h * .60)], fill=n)  # nariz
    d.rectangle([w * .30, h * .60, w * .66, h * .98], fill=n)                       # cuello y mandibula
    d.polygon([(w * .66, h * .60), (w * .84, h * .62), (w * .78, h * .78), (w * .66, h * .80)], fill=n)
    return c


def _calendario(mes, tam=180, tag=False):
    c = Image.new('RGBA', (tam, int(tam * 1.1)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([0, h * .1, w - 1, h - 1], radius=18, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([0, h * .1, w - 1, h * .34], radius=18, fill=(70, 70, 78, 255))
    d.text((w / 2, h * .22), mes, font=font(int(tam * .2)), fill=(255, 255, 255, 255), anchor='mm')
    for i in range(3):
        for j in range(4): d.rounded_rectangle([w * .12 + j * w * .2, h * .44 + i * h * .17, w * .24 + j * w * .2, h * .54 + i * h * .17], radius=4, fill=(215, 215, 210, 255))
    return c


def _boton(apretado=0.0, apagado=False):
    w, h = 560, 200; c = Image.new('RGBA', (w, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    col = GRIS if apagado else ROJO_; dy = int(18 * apretado)
    d.rounded_rectangle([0, 30, w - 1, h + 29], radius=48, fill=(120, 20, 26, 255) if not apagado else (110, 110, 106, 255))
    d.rounded_rectangle([0, dy, w - 1, h - 1 + dy], radius=48, fill=col + (255,))
    d.text((w / 2, h / 2 + dy), 'BAJAR PRECIO', font=font(62), fill=(255, 255, 255, 255), anchor='mm'); return c


def _tarro(col=(200, 200, 196), tam=230):
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([w * .1, h * .08, w * .9, h * .98], radius=26, fill=col + (255,), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .06, 0, w * .94, h * .16], radius=16, fill=(250, 250, 248, 255), outline=TINTA + (255,), width=6)
    d.rounded_rectangle([w * .22, h * .42, w * .78, h * .66], radius=12, fill=(255, 255, 255, 255)); return c


def _llavero(tam=200, apagado=False):
    col = (150, 150, 146) if apagado else (210, 160, 40)
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .05, tam * .05, tam * .45, tam * .45], outline=col + (255,), width=12)
    d.rounded_rectangle([tam * .35, tam * .35, tam * .95, tam * .70], radius=14, fill=col + (255,))
    for k in range(3): d.rectangle([tam * (.55 + k * .12), tam * .70, tam * (.61 + k * .12), tam * .86], fill=col + (255,))
    return c


def _cupon(apagado=False):
    w, h = 300, 160; c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    col = (150, 150, 146) if apagado else (245, 190, 60)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill=col + (255,), outline=TINTA + (255,), width=5)
    for y in range(12, h - 10, 22): d.ellipse([w * .7 - 4, y, w * .7 + 4, y + 8], fill=(250, 250, 248, 255))
    d.text((w * .36, h / 2), 'CUPÓN', font=font(44), fill=TINTA + (255,), anchor='mm'); return c


ETQ, ETQ_GRIS = _etiqueta('20% OFF'), _etiqueta('20% OFF', apagada=True)
REGALO, PER, CAB = _regalo(300), _persona(230), _cabeza(560, 560)
TARRO = _tarro()


def g_descuento(tl, T):              # "...darte el descuento que quieran (6.10). Pero prefieren hacer otra cosa (7.02)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    p = ease((tl - 0.92) / 0.35)                                                       # la etiqueta se corre y se achica
    k = lerp(0.6, 1.0, pop(tl, 0.0, 0.14)) * lerp(1.0, 0.62, p)
    pegar(im, ETQ, lerp(540, 250, p), lerp(420, 430, p), k * lerp(1.0, 0.9, p))
    if p < 0.3:                                                                         # contador 0 -> 20 % dentro de la etiqueta
        pass
    if tl > 1.05: pegar(im, _texto('+', 150, TINTA), 540, 430, pop(tl, 1.05))
    if tl > 1.25: pegar(im, REGALO, 830, 400, lerp(0.7, 1.0, pop(tl, 1.25, 0.22)))
    if tl > 1.45: pegar(im, pastilla('Un regalo', 50, fondo=VERDE_OSC), 830, 640, pop(tl, 1.45))
    return im


def g_cabeza(tl, T):                 # "...lo que pasa en la cabeza (9.50) de su cliente cuando ve uno (10.58)"
    im = fondo_grafico()
    pegar(im, CAB, 540, 440, lerp(0.9, 1, pop(tl, 0.0, 0.2)))
    if tl > 1.10: pegar(im, ETQ.resize((330, 130), Image.LANCZOS), 520, 330, lerp(0.5, 1, pop(tl, 1.10, 0.15)))
    return im


def g_valemenos(tl, T):              # "...es un descuento (13.84). Solo le estas diciendo que tu producto realmente vale menos (16.22)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, TARRO, 320, 450, pop(tl, 0.0) * 1.2)
    pegar(im, ETQ.resize((340, 134), Image.LANCZOS), 320, 230, pop(tl, 0.12))
    k = lerp(1.0, 0.45, ease((tl - 2.3) / 0.6))                                          # el tarro "vale menos": se achica
    if tl > 1.0:
        pegar(im, TARRO, 780, 450 + (1 - k) * 140, pop(tl, 1.0) * k * 1.2)
        flecha_recta(d, (960, 260), (960, 600), ease((tl - 2.3) / 0.3))
    if tl > 2.5: pegar(im, pastilla('Vale menos', 54, fondo=ROJO_), 790, 680, pop(tl, 2.5))
    return im


MESES = ['ENE', 'FEB', 'MAR', 'ABR']
CALS = [_calendario(m, 210) for m in MESES]


def g_calendario(tl, T):             # "siempre va a esperar (18.30) a que vuelvas a bajar el precio (19.08)"
    im = fondo_grafico()
    for i, c in enumerate(CALS):
        x = 160 + i * 253; pegar(im, c, x, 340, pop(tl, 0.0 + i * 0.12))
        t0 = 0.45 + i * 0.32
        if tl > t0: pegar(im, ETQ.resize((200, 80), Image.LANCZOS), x + 20, 250, pop(tl, t0, 0.14))
    pegar(im, PER, 260, 610, pop(tl, 0.3))
    if tl > 0.65: pegar(im, pastilla('Esperando el próximo…', 48, fondo=TINTA), 650, 640, pop(tl, 0.65))
    return im


def g_mal(tl, T):                    # "El problema es que es muy facil hacerlo mal"
    im = fondo_grafico()
    pegar(im, _regalo(340, (214, 48, 49)), 540, 410, lerp(0.85, 1, pop(tl, 0.0)))
    if tl > 0.5: pegar(im, _texto('!', 260, ROJO_), 800, 280, lerp(0.6, 1, pop(tl, 0.5, 0.14)))
    if tl > 1.2: pegar(im, pastilla('Fácil hacerlo mal', 56, fondo=TINTA), 540, 650, pop(tl, 1.2))
    return im


def g_llavero(tl, T):                # "Mira Huel no te regala un llavero (32.84) ni un cupon (33.32) para otra compra"
    im = fondo_grafico()
    gris = tl > 2.05
    if tl > 1.10: pegar(im, _llavero(320, gris), 300, 420, pop(tl, 1.10))
    if tl > 1.60: pegar(im, _cupon(gris).resize((420, 224), Image.LANCZOS), 760, 430, pop(tl, 1.60))
    if tl > 2.05: pegar(im, pastilla('No suma nada', 50, fondo=(120, 120, 116)), 540, 660, pop(tl, 2.05))
    if tl < 1.10: pegar(im, _texto('¿Qué regala Huel?', 70, TINTA), 540, 400, pop(tl, 0.0))
    return im


def g_ventas(tl, T):                 # "el dia que las ventas se frenan (39.70) la tentacion (40.12) ... Bajar el precio (41.52)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pts = [(120, 640), (260, 560), (400, 470), (520, 420), (640, 410), (760, 408), (900, 406)]
    p = min(1, tl / 0.9); n = 1 + p * (len(pts) - 1)
    seg = [pts[int(i)] if i == int(i) else pts[int(i)] for i in range(int(n))]
    for a, b in zip(pts[:int(n)], pts[1:int(n) + 1]): d.line([a, b], fill=VERDE_OSC if a[0] < 500 else (200, 120, 40), width=14)
    d.line([(100, 660), (940, 660)], fill=TINTA, width=5); d.line([(100, 660), (100, 300)], fill=TINTA, width=5)
    if 0.56 < tl < 0.98: pegar(im, pastilla('Las ventas se frenan', 44, fondo=(200, 120, 40)), 700, 330, pop(tl, 0.56))
    if tl > 0.98:
        z = ease((tl - 2.38) / 0.4)                                                    # zoom al boton en "Bajar el precio"
        ap = 1.0 if 2.9 < tl < 3.2 else 0.0
        pegar(im, _boton(ap), lerp(540, 540, z), lerp(480, 470, z), lerp(0.7, 1.25, z) * pop(tl, 0.98, 0.2))
    return im


# ------------------------------------------------------------ capturas
def _card_top(png):
    """Tarjeta de la Biblioteca (2 px por px CSS) recortada arriba del creativo, sobre el gris de la Biblioteca."""
    card = Image.open(png).convert('RGB'); k = 980 / card.width; card = card.resize((980, int(card.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), (240, 242, 245)); c.paste(card, (50, 300)); return np.asarray(c), 2 * k
ELC, fE = _card_top(f'{A}/cap/el_card_top.png')
ELJ = json.load(open(f'{A}/cap/el_fbmeta.json'))['cards']['1571246460604433']['frases']
cE = lambda r: (50 + r[0] * fE, 300 + r[1] * fE, r[2] * fE, r[3] * fE)

HU = Image.open(f'{A}/cap/hu_ad_limpio.jpg').convert('RGB')                         # creativo del anuncio 1766309524036309 (1200 px)
HUC = Image.new('RGB', (W, H), (246, 246, 246)); _h = HU.resize((W, W), Image.LANCZOS); HUC.paste(_h, (0, 150)); HUC = np.asarray(HUC)
kh = W / 1200
# "Free T-shirt / and shaker" MEDIDO por pixeles en hu_ad_img.jpg: filas 953-985 y 1013-1045, columnas 62-298
F_SHAKER = (62 * kh, 150 + 953 * kh, (298 - 62) * kh, (1045 - 953) * kh)

# ------------------------------------------------------------ tomas
toma('01', 0.00, 3.94, Serie([
    (0.00, clip('1556341659546393', 8.0, nombre='anuncio-video:1556341659546393 (Huel, hook)')),
    (1.28, clip('1571246460604433', 6.0, nombre='anuncio-video:1571246460604433 (Extra Life, hook)')),
    (2.80, clip('1780988933101495', 0.3, nombre='anuncio-video:1780988933101495 (Huel, hook)')),
]), 'C', T_(['La trampa del descuento'], 190, 72, t0=-1.0, clave={'descuento'}, emo='🔥'))
toma('02', 3.94, 5.10, clip('1139302692155017', 8.8, nombre='anuncio-video:1139302692155017 (Huel: free welcome kit)'), 'CI')   # "Fijate en sus anuncios"
toma('03', 5.10, 6.10, lienzo(ELC, (0, 200, W), (40, 500, 640), [('sub', cE(ELJ['¡LLEVA UNA BOTELLA GRATIS!'][0]), 0.15)],
                              nombre='tarjeta:extra life botella gratis', dur_mov=0.5), 'CD')
toma('04', 6.10, 8.12, Grafico(g_descuento), 'C')
toma('05', 8.12, 9.40, clip('1032986392494613', 2.0, nombre='anuncio-video:1032986392494613 (Extra Life)'), 'CI')
toma('06', 9.40, 10.98, Grafico(g_cabeza), 'CD')
toma('07', 10.98, 13.72, clip('1215670467235858', 0.3, nombre='anuncio-video:1215670467235858 (Extra Life)'), 'C')
toma('08', 13.72, 16.80, Grafico(g_valemenos), 'CI')
toma('09', 16.80, 17.68, clip('1318473731360637', 0.3, nombre='anuncio-video:1318473731360637 (Huel)'), 'CD')
toma('10', 17.68, 19.60, Grafico(g_calendario), 'C')
toma('11', 19.60, 21.62, clip('988073447054924', 10.4, nombre='anuncio-video:988073447054924 (Huel)'), 'CI')
toma('12', 21.62, 23.50, clip('w5', 0.5, nombre='extra-life.cl: video w5'), 'CD')
toma('13', 23.50, 25.74, Grafico(g_mal), 'C')
toma('14', 25.74, 28.76, clip('1214119060794363', 15.0, nombre='anuncio-video:1214119060794363 (Huel con su shaker)'), 'CI',
     T_(['Relacionado con tu producto'], 190, 60, t0=0.3))
toma('15', 28.76, 31.68, clip('w1', 0.5, nombre='extra-life.cl: video w1 (sachet en su botella)'), 'CD',
     T_(['O con lo que tu cliente necesita'], 190, 56, t0=0.3))
toma('16', 31.68, 34.12, Grafico(g_llavero), 'C')
toma('17', 34.12, 37.04, clip('1815601653082584', 17.3, nombre='anuncio-video:1815601653082584 (Huel: free shaker with your first order)'), 'CI')
toma('18', 37.04, 39.14, clip('3878492702464195', 0.5, nombre='anuncio-video:3878492702464195 (Extra Life en la farmacia)'), 'CD')
toma('19', 39.14, 42.94, Grafico(g_ventas), 'C')
toma('20', 42.94, 44.88, clip('1166900458589155', 0.3, nombre='anuncio-video:1166900458589155 (Extra Life)'), 'CI')
toma('21', 44.88, 49.92, lienzo(HUC, (0, 0, W), (0, 600, 760), [('caja', F_SHAKER, 2.96)], nombre='anuncio:1766309524036309 (creativo Huel: free T-shirt and shaker)', dur_mov=2.8), 'CD')
toma('22', 49.92, 52.72, clip('1295471681923871', 20.0, nombre='anuncio-video:1295471681923871 (Extra Life)'), 'C')
toma('23', 52.72, 55.88, Serie([(0.00, clip('687165790307897', 8.0, nombre='anuncio-video:687165790307897 (Extra Life)')),
                                (1.50, clip('3000851350254150', 0.0, nombre='anuncio-video:3000851350254150 (Huel)'))]), 'CI')
toma('24', 55.88, 58.50, clip('1562772322216568', 44.0, nombre='anuncio-video:1562772322216568 (Huel en su dia)'), 'C',
     T_(['Mándaselo antes de su próxima promo'], 190, 54, t0=0.2, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 '¿Por qué marcas como *Huel', 'o Extra *Life', 'prefieren *regalarte', 'algo antes de bajar el *precio?',
 'Fíjate en sus *anuncios,', 'son marcas que podrían', 'darte el *descuento', 'que *quieran',
 'Pero prefieren hacer otra *cosa', 'porque entienden lo que pasa', 'en la *cabeza', 'de su cliente cuando ve *uno',
 'Si lo primero que le muestras', 'a tu cliente cuando quieres', 'vender más es un *descuento', 'Solo le estás diciendo',
 'que tu producto realmente', 'vale *menos', 'Y de ahí en adelante', 'siempre va a *esperar', 'a que vuelvas a bajar el *precio',
 'Lo que hace que estas marcas', '*destaquen', 'es hacerle sentir al cliente', 'que está ganando en todo *momento',
 'El problema es que es', 'muy fácil hacerlo *mal', 'Lo que regalas tiene que estar', 'directamente *relacionado', 'con tu *producto',
 'O con algo que tu cliente *ideal', 'probablemente también *necesita',
 'Mira Huel no te regala', 'un llavero ~ ~ ni un *cupón', 'para otra *compra', 'Te regala un *shaker', 'donde vas a preparar',
 'tu batido todos los *días', 'Y esto es más importante_de', 'lo que *parece', 'porque el día que las ventas', 'se *frenan',
 'la tentación siempre es la *misma', 'Bajar el precio es', 'la decisión más *fácil', 'pero no siempre es la que',
 'le conviene a tu *marca', 'Y Huel lo entendió', '*perfectamente', 'Prefiere que su cliente sienta', 'que se lleva algo',
 'que le sea *útil', 'aunque pague lo *mismo', 'Porque esto va a mejorar mucho', 'la *experiencia', 'de tu cliente con tus *productos',
 'Mándaselo a esa *persona', 'que lo necesita escuchar', 'antes de sacar su próxima *promoción', 'Y *malacostumbrar',
 'a sus clientes a esperar *descuentos',
]
# las 5 ultimas palabras de la transcripcion ("Gracias por ver el video", en 0,06 s) son un error de la transcripcion: se descartan
SUBS = armar_tarjetas(json.load(open(f'{A}/pal42.json'))[:-5], GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
