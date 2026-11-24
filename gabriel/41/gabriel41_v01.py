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


def borroso(i, ss, nombre, **k):
    usar(nombre); return ClipBorroso(ad(i, 'mp4'), ss, **k)


DAN = dict(recorte=(1920, 680, 0, 200), entero=270)                       # video corporativo de danone.com (16:9 con franjas negras)
dan = lambda ss, nombre: clip('danone_corp', ss, nombre='danone.com: video corporativo (' + nombre + ')', **DAN)


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


def g_plato(tl, T):                  # "si comes menos, cada comida tiene que valer por dos" (10.56-13.78)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    r = lerp(250, 165, ease((tl - 1.26) / 0.5)) * pop(tl, 0.05)
    if r > 0:
        d.ellipse([540 - r, 440 - r, 540 + r, 440 + r], fill=(255, 255, 255), outline=TINTA, width=8)
        d.ellipse([540 - r * .72, 440 - r * .72, 540 + r * .72, 440 + r * .72], outline=(210, 210, 206), width=5)
    if tl > 1.3: pegar(im, pastilla('Comes menos', 42, fondo=GRIS), 540, 205, pop(tl, 1.3))
    if tl > 1.9: pegar(im, pastilla('Proteína', 50, fondo=VERDE_OSC), 330, 600, lerp(0.7, 1.1, pop(tl, 1.9)))
    if tl > 2.2: pegar(im, pastilla('Nutrientes', 50, fondo=VERDE_OSC), 760, 600, lerp(0.7, 1.1, pop(tl, 2.2)))
    if tl > 2.96: pegar(im, _texto('x2', 150, ROJO), 540, 440, lerp(0.6, 1, pop(tl, 2.96)))
    return im


def g_complicado(tl, T):             # "sus planes de alimentacion eran demasiado complicados" (22.42-25.90)
    im = fondo_grafico(); d = ImageDraw.Draw(im); rnd = np.random.default_rng(3)
    for k in range(9):
        t0 = 0.05 + k * 0.16
        if tl < t0: continue
        x, y = 170 + (k % 3) * 370, 260 + (k // 3) * 150; ang = rnd.uniform(-14, 14)
        hoja = _caja(['Plan ' + str(k + 1)], 250, 110, (250, 236, 200) if k % 2 else (236, 236, 232), 36)
        pegar(im, hoja.rotate(ang, expand=True, resample=Image.BICUBIC), x, y, pop(tl, t0))
    if tl > 1.5:
        p = ease((tl - 1.5) / 0.6)
        for k in range(5):
            a = (150 + k * 190, 230); b = (930 - k * 170, 610)
            d.line([a, (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)], fill=ROJO, width=7)
    if tl > 2.86: pegar(im, pastilla('Demasiado complicado', 52, fondo=ROJO), 540, 700, lerp(0.8, 1, pop(tl, 2.86)))
    return im


TARROS = [_tarro(c) for c in ((236, 196, 120), (180, 210, 230), (214, 120, 110), (150, 200, 150))]
BOLSA = None


def _bolsa(w=260):
    c = Image.new('RGBA', (w, int(w * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); W_, H_ = c.size
    d.polygon([(W_ * .12, H_ * .1), (W_ * .88, H_ * .1), (W_ * .95, H_ * .98), (W_ * .05, H_ * .98)], fill=(17, 17, 20, 255))
    d.rectangle([W_ * .12, H_ * .02, W_ * .88, H_ * .12], fill=(40, 40, 44, 255))
    d.rounded_rectangle([W_ * .22, H_ * .42, W_ * .78, H_ * .62], radius=10, fill=(255, 255, 255, 255))
    d.text((W_ / 2, H_ * .52), 'Todo en 1', font=font(int(w * .11)), fill=TINTA + (255,), anchor='mm'); return c
BOLSA = _bolsa(380)


def g_uno(tl, T):                    # "todos los nutrientes en un solo producto" (27.40-29.72)
    im = fondo_grafico()
    p = ease((tl - 0.7) / 0.55)
    for k, t in enumerate(TARROS):
        x0, y0 = 170 + k * 247, 330
        if p < 1: pegar(im, t, lerp(x0, 540, p), lerp(y0, 440, p), pop(tl, 0.05 + k * 0.1) * lerp(1, 0.2, p))
    if tl > 1.1: pegar(im, BOLSA, 540, 440, lerp(0.6, 1, pop(tl, 1.1)))
    if tl > 1.6: pegar(im, pastilla('Un solo producto', 50, fondo=VERDE_OSC), 540, 700, pop(tl, 1.6))
    return im


def _pieza(txt, col, tam=(380, 200), lado='d'):
    w, h = tam; c = Image.new('RGBA', (w + 60, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    if lado == 'd':
        d.rounded_rectangle([0, 0, w, h - 1], radius=26, fill=col + (255,), outline=TINTA + (255,), width=6)
        d.ellipse([w - 34, h / 2 - 38, w + 42, h / 2 + 38], fill=col + (255,), outline=TINTA + (255,), width=6)
        d.rectangle([w - 40, h / 2 - 32, w - 3, h / 2 + 32], fill=col + (255,))
        d.text((w / 2, h / 2), txt, font=font(44), fill=TINTA + (255,), anchor='mm')
    else:
        d.rounded_rectangle([60, 0, w + 59, h - 1], radius=26, fill=col + (255,), outline=TINTA + (255,), width=6)
        d.ellipse([60 - 38, h / 2 - 38, 60 + 38, h / 2 + 38], fill=(250, 250, 248, 255), outline=TINTA + (255,), width=6)
        d.text((60 + w / 2 + 14, h / 2), txt, font=font(44), fill=TINTA + (255,), anchor='mm')
    return c
P_SUPER, P_DIRECTA = _pieza('Supermercados', (226, 236, 250)), _pieza('Venta directa', (212, 240, 224), lado='i')


def g_rompecabezas(tl, T):           # "Y era justo lo que le faltaba a Danone" (46.62-48.32)
    im = fondo_grafico(); p = ease((tl - 0.6) / 0.5)
    pegar(im, P_SUPER, lerp(250, 345, p), 440, pop(tl, 0.05)); pegar(im, P_DIRECTA, lerp(840, 735, p), 440, pop(tl, 0.2))
    pegar(im, pastilla('Danone', 40, fondo=(0, 84, 166)), 300, 290, pop(tl, 0.1)); pegar(im, pastilla('Huel', 40, fondo=TINTA), 790, 290, pop(tl, 0.25))
    if tl > 1.1: pegar(im, _texto('✓', 110, VERDE_OSC), 540, 640, pop(tl, 1.1))
    return im


ETIQ = None


def _etiqueta(w=300, h=150):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    for x in range(30, w - 30, 30): d.line([(x, h / 2), (x + 15, h / 2)], fill=(190, 190, 186, 255), width=5)
    return c
ETIQ = _etiqueta()


def g_cliente(tl, T):                # "nace un cliente nuevo que todavia no tiene una marca" + "la primera marca que lo identifica se lo lleva"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, PER, 300, 420, pop(tl, 0.05)); pegar(im, _texto('?', 120, ROJO), 300, 250, pop(tl, 0.3))
    pegar(im, ETIQ, 760, 420, pop(tl, 0.5))
    if tl < 2.6 and tl > 0.9: pegar(im, pastilla('Cliente nuevo, sin marca', 44, fondo=TINTA), 540, 680, pop(tl, 0.9))
    if tl > 3.24:                                                          # 54.28 "primera marca"
        pegar(im, hlogo(230), 760, 420, lerp(0.6, 1, pop(tl, 3.24)))
        pegar(im, pastilla('Se lo lleva', 50, fondo=VERDE_OSC), 540, 680, pop(tl, 3.6))
    return im


def g_pasos(tl, T):                  # "la marca que sepa leer esos cambios (63.96) y posicionar su producto a tiempo (65.72) ... la delantera (67.34)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pasos = [(['Cambia', 'el hábito'], 0.05, (236, 236, 232)), (['La marca', 'lo lee'], 1.34, (250, 236, 200)), (['Toma la', 'delantera'], 4.72, (212, 240, 224))]
    for i, (s, t0, col) in enumerate(pasos):
        if tl < t0: continue
        x = 190 + i * 350
        if i: flecha_recta(d, (x - 350 + 150, 440), (x - 160, 440), ease((tl - t0) / 0.18))
        pegar(im, _caja(s, 290, 160, col, 44), x, 440, lerp(0.86, 1, pop(tl, t0)))
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

# ------------------------------------------------------------ tomas
toma('01', 0.00, 2.04, Serie([(0.00, dan(27.0, 'gente comiendo')), (1.02, dan(28.3, 'desayuno'))]), GAB)              # "millones de personas empezaban a comer menos"
toma('02', 2.04, 3.58, lienzo(OZ, (0, 0, W), (120, 210, W - 240), nombre='commons.wikimedia.org: Ozempic (foto)'), GAB)  # "por medicamentos como Ozempic"
toma('03', 3.58, 4.54, dan(0.4, 'heladera con yogures Danone'), GAB)                                                     # "Danone, la de los yogures"
toma('04', 4.54, 7.18, borroso('1780988933101495', 0.4, 'anuncio-video:1780988933101495 (Huel, desenfocado)'), GAB,     # "buscaba una marca que tuviera..."
     T_(['¿Cuál?'], 300, 90, t0=0.5))
toma('05', 7.18, 10.56, lienzo(RTE, (0, 40, 1640), (40, 60, 1560), [('caja', F_BILLION, 1.90)], nombre='rte.ie: Danone compra por casi €1.000 M (Huel tapado)'), GAB,
     contador_toma(1000, 1.98, cy=640, prefijo='Casi €', sufijo=' M', tam=110))                                         # "acordo pagar mil millones de euros"
toma('06', 10.56, 13.78, Grafico(g_plato), GAB)
toma('07', 13.78, 15.00, dan(53.0, 'linea de produccion'), GAB)                                                         # "Su director general tenia claro..."
toma('08', 15.00, 18.44, lienzo(FD, (120, 4180, 1360), (150, 4200, 1300), [('sub', r, 0.66) for r in F_GLP], nombre='fooddive.com: consumidores de GLP-1 (Huel tapado)'), GAB)
toma('09', 18.44, 20.38, borroso('1595225641819088', 1.0, 'anuncio-video:1595225641819088 (Huel, desenfocado)'), GAB)  # "no es una marca que salio de la nada"
usar('anuncio-video:2143082343178303 (fundador de Huel; rotulo tapado)')
toma('10', 20.38, 22.42, ClipZona(ad('2143082343178303', 'mp4'), 5.8, zona=(0, 860, 860, 420)), GAB,                   # "su fundador ya habia perdido 80 mil libras"
     varios(contador_toma(80000, 1.08, cy=470, prefijo='-£', tam=110), entre(1.1, 9, lambda pil, tl, T: pegar(pil, pastilla('Fuente: The Grocer', 34, fondo=(236, 236, 232), color=GRIS, pad=(30, 16)), 540, 600))))
toma('11', 22.42, 25.90, Grafico(g_complicado), GAB)
toma('12', 25.90, 27.40, borroso('897943063070733', 22.0, 'anuncio-video:897943063070733 (Huel, desenfocado)'), GAB)    # "esta segunda vez se arriesgo por lo simple"
toma('13', 27.40, 29.72, Grafico(g_uno), GAB)
toma('14', 29.72, 30.62, Grafico(lambda tl, T: (lambda im: (pegar(im, hlogo(int(lerp(620, 700, ease(tl / 0.4)))), 540, 430, 1.0), im)[1])(fondo_grafico())), GAB)
S[-1]['fuentes'] = ['logo de huel.com']
toma('15', 30.62, 32.74, clip('2143082343178303', 8.7, nombre='anuncio-video:2143082343178303 (s8.7: Black Edition en polvo)'), GAB)     # "comidas completas en polvo"
toma('16', 32.74, 34.92, clip('3000851350254150', 21.2, nombre='anuncio-video:3000851350254150 (40 g de proteina)'), GAB)  # "con 40 gramos de proteina"
toma('17', 34.92, 37.90, dan(17.2, 'Activia y Aqua en la planta'), GAB)            # "la estrategia de Danone iba mas alla"
toma('18', 37.90, 40.88, Serie([(0.00, dan(53.8, 'cajas en la cinta')), (1.40, dan(14.3, 'vasos de yogur en la linea'))]), GAB)                # "Danone vende sobre todo en supermercados"
toma('19', 40.88, 42.40, clip('1139302692155017', 25.4, nombre='anuncio-video:1139302692155017 (s25: "Huel shipped directly to your door")'), GAB)
toma('20', 42.40, 43.76, lienzo(DANP, (400, 7050, 1240), (480, 7090, 1160), [('sub', F_DTC, 0.30)], nombre='danone.com: venta directa por internet'), GAB)   # "venta directa por internet"
toma('21', 43.76, 46.62, lienzo(BLK, (640, 120, 1000), (700, 150, 940), [('caja', F_4M, 1.70)], nombre='uk.huel.com: 4.000.000 de clientes'), GAB,
     contador_toma(4, 1.74, cy=640, prefijo='+', sufijo=' millones de clientes', tam=80))                              # "mas de 4 millones de clientes"
toma('22', 46.62, 48.32, Grafico(g_rompecabezas), GAB)
toma('23', 48.32, 51.54, Serie([(0.00, dan(58.0, 'gente')), (1.74, dan(27.6, 'comer')), (2.28, dan(0.0, 'de noche')), (2.82, clip('1780988933101495', 3.8, nombre='anuncio-video:1780988933101495 (cuidarse)'))]), GAB,
     varios(entre(1.74, 2.28, T_(['Come'], 200, 64)), entre(2.28, 2.82, T_(['Duerme'], 200, 64)), entre(2.82, 9, T_(['Se cuida'], 200, 64))))  # come 50.06 / duerme 50.60 / se cuida 51.14
toma('24', 51.54, 53.64, Grafico(g_cliente), GAB)
toma('25', 53.64, 54.70, clip('1318473731360637', 1.0, nombre='anuncio-video:1318473731360637 (clienta con su shaker)'), GAB)
toma('26', 54.70, 56.14, desfase(g_cliente, 3.16), GAB)
toma('27', 56.14, 57.72, clip('1780988933101495', 16.0, nombre='anuncio-video:1780988933101495 (s16: el producto)'), GAB)  # "Huel no tuvo que cambiar su producto"
toma('28', 57.72, 60.14, clip('1318473731360637', 9.0, nombre='anuncio-video:1318473731360637 (s9: su forma de comer)'), GAB)
toma('29', 60.14, 62.62, Serie([(0.00, clip('1595225641819088', 30.0, nombre='anuncio-video:1595225641819088 (s30)')), (0.62, dan(29.4, 'tomando agua')),
                                (1.24, clip('897943063070733', 1.0, nombre='anuncio-video:897943063070733 (s1)')), (1.86, dan(28.9, 'desayuno con cafe'))]), GAB)   # rafaga de habitos
toma('30', 62.62, 65.00, Grafico(g_pasos), GAB)
toma('31', 65.00, 66.30, clip('1139302692155017', 12.4, nombre='anuncio-video:1139302692155017 (s12: la bolsa)'), GAB)
toma('32', 66.30, 67.68, desfase(g_pasos, 3.68), GAB)
toma('33', 67.68, 69.62, clip('1780988933101495', 10.0, nombre='anuncio-video:1780988933101495 (s10: tomando Huel)'), GAB)  # "Mandaselo a esa persona..."
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
