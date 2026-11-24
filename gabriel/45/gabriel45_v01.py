"""Video 45 · "El bombero del cafe" (Innerbloom, Ollie Puddick) · v01
Formato pantalla verde, historia del fundador (guia de Gabriel, VIDEO 45, linea 4065) + todo lo que Gabriel fue corrigiendo:
- Gabriel cambia de lugar toma a toma (CI / CD / C); termina con la voz (DUR = crudo, sin cola).
- Hook con dos cortes de VIDEO reales en los primeros 3 s; mas videos que graficos; cada fuente de video se usa una sola vez.
- Persona u oficio nombrado = foto o video real: Ollie (fotos de innerbloomcoffee.com.au y Our Place Magazine, su anuncio
  en la Biblioteca de Anuncios), bomberos de Nueva Zelanda y videos de bomberos y surf de Wikimedia Commons (sin stock pago).
- La marca se revela en "Asi nacio Innerbloom" (28,90 s): antes, el logo de Innerbloom no se lee (latas desenfocadas por zonas).
- Marcas rojas solo sobre rectangulos medidos (frase330.js / adcard.js) o medidos por pixeles; capturas como tarjeta grande
  sobre un fondo real desenfocado.
Lo que no se muestra (regla 12): promesas de salud del cafe (energia sin bajon, "facil para el estomago"), datos de ventas que no
esten en las fuentes. No hay foto de Ollie de uniforme: van fotos y videos reales de bomberos, sin decir que es el.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v45')
RAW = f'{A}/dl/crudo45.mp4'
DUR = 79.233                 # termina con la voz (el crudo termina con la ultima palabra)
CABEZA = 735
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (120, 120, 118)
CAFE = (90, 60, 40)


def foto(path, crop=None, blur=()):
    """Foto real; blur = rectangulos (x, y, w, h) en px de la foto que se desenfocan (logo de Innerbloom antes de la revelacion)."""
    im = Image.open(path).convert('RGB')
    for x, y, w, h in blur:
        im.paste(im.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(28)), (x, y))
    return im.crop(crop) if crop else im


def panel(im, y=170, ancho=W, alto_max=820):
    """La foto grande arriba (desde y 170), sobre su version desenfocada a pantalla completa."""
    k = min(ancho / im.width, alto_max / im.height); f = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(40))
    c = Image.blend(c, Image.new('RGB', c.size, (0, 0, 0)), 0.25); c.paste(f, ((W - f.width) // 2, y)); return c


def foto_toma(path, crop=None, blur=(), nombre=None, y=170, zoom=0.04, **k):
    c = panel(foto(path, crop, blur), y=y, **k)
    return lienzo(c, (0, 0, W), (W * zoom / 2, H * zoom * 0.2, W * (1 - zoom)), nombre=nombre)


def tarjeta(png, y0, y1, grupos, fondo, nombre, escala=3, top=170, ancho=1064, x0=0, x1=None, zoom=0.03):
    """Captura como tarjeta blanca grande (y 170-730) sobre un fondo real desenfocado.
    grupos: [(rects_css, t0, t1)] -> recuadro rojo en cada rect (rectangulos MEDIDOS por frase330.js / adcard.js)."""
    usar(nombre)
    im = Image.open(png).convert('RGB'); x1 = x1 if x1 is not None else im.width / escala
    g = np.asarray(im.convert('L')).astype(int)
    def _blanca(y, paso):                                  # corre el corte hasta una fila sin texto (no cortar lineas a la mitad)
        y = int(y)
        for _ in range(40):
            if 0 <= y < g.shape[0] and g[y, :].min() > 200: return y
            y += paso
        return y
    ya, yb = _blanca(y0 * escala, -1), _blanca(y1 * escala, 1); y0 = ya / escala
    card = im.crop((int(x0 * escala), ya, int(x1 * escala), yb))
    k = ancho / card.width; card = card.resize((ancho, int(card.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(fondo)).filter(ImageFilter.GaussianBlur(36)); c = Image.blend(c, Image.new('RGB', c.size, (0, 0, 0)), 0.3)
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=28, fill=255)
    xo = (W - ancho) // 2; c.paste(card, (xo, top), m)
    ms = []
    for rects, t0, t1 in grupos:
        for r in rects:
            ms.append(('caja', (xo + (r[0] - x0) * escala * k, top + (r[1] - y0) * escala * k, r[2] * escala * k, r[3] * escala * k), t0, t1))
    return Lienzo(c, (0, 0, W), (W * zoom / 2, H * zoom * 0.2, W * (1 - zoom)), ms)


# ------------------------------------------------------------ material
S_ = lambda f: f'{A}/site/{f}'
FN = json.load(open(f'{A}/cap/fmmeta.json'))                                     # Foodpreneur a 330 px CSS (frase330.js, 3 px por px CSS)
FN_PNG = lambda k: f'{A}/cap/fm_{k}.png'
ADC = json.load(open(f'{A}/cap/adcard.json'))                                   # tarjeta del anuncio 985135284619460 (adcard.js, 3 px por px CSS)
LOGO = Image.open(S_('Innerbloom_Brandmark-02.png')).convert('RGBA')            # logo blanco de innerbloomcoffee.com.au
LOGO_OSC = Image.open(S_('Innerbloom_Brandmark-03.png')).convert('RGBA')
FONDO_LATAS = Image.open(S_('Innerbloom6pk.jpg')).convert('RGB')
FONDO_CAFE = Image.open(S_('InnerbloomMay26-1661.jpg')).convert('RGB')
# logos de Innerbloom en las latas (medidos sobre la foto, cuadricula de 100 px): se desenfocan antes de la revelacion
BLUR_MAY26 = [(1030, 1230, 180, 300)]
BLUR_CINNY = [(1140, 740, 210, 260)]
BLUR_510B = [(500, 530, 200, 160)]


def logo(w, oscuro=False):
    lg = LOGO_OSC if oscuro else LOGO; lg = lg.crop(lg.getbbox()); return lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)


# ------------------------------------------------------------ graficos propios (llenan y 170-730, elementos grandes)
def _texto(s, tam, col=TINTA):
    f = font(tam); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _vaso(tam=300):
    """Vaso de cafe con hielo (dibujo simple)."""
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.polygon([(w * .12, h * .06), (w * .88, h * .06), (w * .78, h * .96), (w * .22, h * .96)], fill=(255, 255, 255, 255), outline=TINTA + (255,))
    d.polygon([(w * .17, h * .30), (w * .83, h * .30), (w * .78, h * .94), (w * .22, h * .94)], fill=(150, 100, 62, 255))
    for x, y in ((.33, .38), (.55, .45), (.42, .58)): d.rounded_rectangle([w * x, h * y, w * x + w * .17, h * y + w * .17], radius=8, fill=(225, 238, 244, 230))
    d.line([(w * .12, h * .06), (w * .22, h * .96), (w * .78, h * .96), (w * .88, h * .06)], fill=TINTA + (255,), width=8)
    return c
VASO = _vaso()


def g_idea(tl, T):                   # "Y si el cafe (26.54) ademas de despertarte (27.38) te diera algo mas (28.48)?"
    im = fondo_grafico()
    pegar(im, VASO, 330, 430, lerp(0.86, 1, pop(tl, 0.05)))
    if tl > 0.70: pegar(im, _texto('+', 220, VERDE_OSC), 640, 420, pop(tl, 0.70))
    if tl > 2.25: pegar(im, _texto('?', 300, ROJO), 860, 420, lerp(0.7, 1, pop(tl, 2.25)))
    if tl > 1.20: pegar(im, pastilla('¿Algo más?', 64, fondo=TINTA), 540, 690, pop(tl, 1.20))
    return im


def _tienda(tam=200, col=(214, 120, 60), gris=False):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); s = tam
    col = (190, 190, 186) if gris else col; borde = (160, 160, 156) if gris else TINTA
    d.rectangle([s * .12, s * .40, s * .88, s * .95], fill=(255, 255, 255, 255), outline=borde + (255,), width=7)
    for i in range(4):
        d.pieslice([s * (.08 + i * .21), s * .18, s * (.08 + (i + 1) * .21), s * .46], 0, 180, fill=(col if i % 2 == 0 else (255, 255, 255)) + (255,), outline=borde + (255,), width=5)
    d.rectangle([s * .08, s * .10, s * .92, s * .32], fill=col + (255,), outline=borde + (255,), width=7)
    d.rectangle([s * .40, s * .62, s * .60, s * .95], fill=borde + (255,))
    return c
TIENDA, TIENDA_G, TIENDA_N = _tienda(), _tienda(gris=True), _tienda(col=(30, 150, 90))


def _flecha_gruesa(d, x0, y, x1, col, grosor, p):
    if p <= 0: return
    xe = x0 + (x1 - x0) * p
    if xe - grosor * 0.9 > x0: d.rectangle([x0, y - grosor / 2, xe - grosor * 0.9, y + grosor / 2], fill=col)
    d.polygon([(xe, y), (xe - grosor * 1.4, y - grosor * 1.1), (xe - grosor * 1.4, y + grosor * 1.1)], fill=col)


def g_plata(tl, T):                  # "Vendian muchisimas tiendas (41.84) pero la plata le entraba (42.92) mucho mas lento de lo que salia (44.20)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for i in range(4): pegar(im, TIENDA.resize((220, 220)), 165 + i * 250, 290, pop(tl, 0.05 + i * 0.12))
    pe = ease((tl - 2.04) / 1.6)                                                      # la que entra: finita y lenta
    if tl > 2.04:
        pegar(im, _texto('Entra', 80, VERDE_OSC), 160, 500, pop(tl, 2.04)); _flecha_gruesa(d, 320, 500, 1000, VERDE_OSC, 24, pe * 0.55)
    ps = ease((tl - 3.32) / 0.25)                                                     # la que sale: gruesa y rapida
    if tl > 3.32:
        pegar(im, _texto('Sale', 80, ROJO), 160, 660, pop(tl, 3.32)); _flecha_gruesa(d, 320, 660, 1020, ROJO, 80, ps)
    return im


def g_tiendas(tl, T):                # "por estar buscando tiendas nuevas (47.38) en vez de cuidarlas que ya tenia (48.46)"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    gris = tl > 1.86
    for i in range(3):
        pegar(im, (TIENDA_G if gris and i != 1 else TIENDA).resize((220, 220)), 200, 210 + 0 + i * 0, 1.0) if False else None
    for i, (x, y) in enumerate(((180, 300), (180, 560))):
        pegar(im, TIENDA_G.resize((220, 220)) if gris else TIENDA.resize((220, 220)), x, y, pop(tl, 0.05 + i * 0.1))
    if tl > 0.05: pegar(im, _texto('Las de antes', 60, GRIS if gris else TINTA), 200, 720, 1.0)
    for i, (x, y) in enumerate(((620, 300), (880, 300), (620, 560), (880, 560))):
        if tl > 0.78 + i * 0.18: pegar(im, TIENDA_N.resize((220, 220)), x, y, pop(tl, 0.78 + i * 0.18))
    if tl > 0.78: pegar(im, _texto('Nuevas', 60, VERDE_OSC), 750, 700, pop(tl, 0.78))
    return im


def _persona(col=TINTA, tam=280):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([tam * .32, tam * .02, tam * .68, tam * .38], fill=col + (255,)); d.pieslice([tam * .1, tam * .44, tam * .9, tam * 1.28], 180, 360, fill=col + (255,)); return c
PERSONA = _persona()


def g_directo(tl, T):                # "Vender directo por internet le devolvio el control (67.40) de su negocio"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, logo(560, oscuro=True), 540, 230, pop(tl, 0.05))
    pegar(im, PERSONA.resize((300, 300)), 820, 520, pop(tl, 0.25))
    pegar(im, _texto('Cliente', 66, TINTA), 820, 700, pop(tl, 0.25))
    p = ease((tl - 0.40) / 0.5)
    if p > 0:
        pegar(im, TIENDA_G.resize((220, 220)), 300, 520, 1 - ease((tl - 0.40) / 0.45))   # la tienda del medio se va
        _flecha_gruesa(d, 160, 520, 640, VERDE_OSC, 60, p)
    if tl > 1.84: pegar(im, pastilla('Control', 76, fondo=VERDE_OSC), 330, 690, lerp(0.86, 1, pop(tl, 1.84)))
    return im


def g_revela(tl, T):                 # "Asi nacio Innerbloom" (29.56): el logo nitido por primera vez sobre las latas
    im = panel(Image.open(S_('Innerbloom3pk.jpg')).convert('RGB').crop((0, 450, 2000, 2350)), y=170, alto_max=800)
    pegar(im, logo(int(lerp(760, 820, ease(tl / 0.4)))), 540, 260, pop(tl, 0.55))
    return im


def oscurece(path, t0, dur, crop=None):
    base = np.asarray(panel(foto(path, crop))).astype(np.float32)
    return Grafico(lambda tl, T: Image.fromarray((base * lerp(1.0, 0.35, ease((tl - t0) / dur))).astype(np.uint8)))


# ------------------------------------------------------------ tomas
NUT = (416, 1473, 217, 162)          # "15.4g Protein" medido por pixeles en mixed-pack-all-protein_3.jpg (pixeles blancos > 230, x 416-633, y 1473-1635)


def _nutricion():
    X0, Y0 = 200, 1330; im = Image.open(f'{A}/prod/mixed-pack-all-protein_3.jpg').convert('RGB').crop((X0, Y0, 1400, 1930))
    k = W / im.width; f = im.resize((W, int(im.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(im)).filter(ImageFilter.GaussianBlur(40)); c.paste(f, (0, 170))
    return c, ((NUT[0] - X0) * k, 170 + (NUT[1] - Y0) * k, NUT[2] * k, NUT[3] * k)
NUTC, NUTR = _nutricion()

toma('01', 0.00, 2.76, Serie([(0.00, clip('cfa', 21.0, nombre='commons: CFA, bomberos apagando un incendio')),          # "apagando incendios"
                              (1.50, clip('mwss', 27.0, nombre='commons: bomberos frente al fuego (MWSS 172)'))]), GAB)
S[-1]['fuentes'] = ['commons.wikimedia.org: Mobile firefighting training prop (CFA, Australia)', 'commons.wikimedia.org: MWSS 172 Firefighting Training']
toma('02', 2.76, 4.72, foto_toma(f'{A}/cap/stores_map.png', (90, 700, 760, 1000), nombre='innerbloomcoffee.com.au: lista de tiendas (sin el titulo con la marca)', y=235, alto_max=490), GAB,
     contador_toma(300, 1.12, cy=140, prefijo='+', sufijo=' tiendas', dur=0.5, tam=110))                                 # "300" (3.88)
toma('03', 4.72, 7.56, clip('usaf', 33.5, nombre='commons: incendio de entrenamiento (31 CE)'), GAB)                       # "casi lo pierde todo"
toma('04', 7.56, 9.40, Serie([(0.00, foto_toma(f'{A}/cap/story.png', (0, 400, 820, 2580), nombre='innerbloomcoffee.com.au/our-story: Ollie Puddick', alto_max=760)),
                              (0.84, foto_toma(f'{A}/commons/bomberos1.jpg', nombre='commons: bomberos de Nueva Zelanda (Palmerston North, 2019)'))]), GAB,
     varios(entre(0.0, 0.84, T_(['Ollie Puddick'], 110, 70)), entre(0.84, 9, T_(['Bombero profesional'], 110, 66))))
toma('05', 9.40, 11.68, clip('afn', 21.0, nombre='commons: bombero equipandose (AFN)'), GAB)                             # "turnos largos"
toma('06', 11.68, 12.56, foto_toma(S_('Untitled_Studio_Innerbloom_Jan25-4353.jpg'), nombre='innerbloomcoffee.com.au: corredores al amanecer'), GAB)   # "madrugadas"
toma('07', 12.56, 14.64, foto_toma(S_('InnerbloomMay26-1661.jpg'), (0, 300, 2000, 2700), BLUR_MAY26, nombre='innerbloomcoffee.com.au: cafe servido (logo desenfocado)'), GAB)   # "cafe, pero mucho cafe"
toma('08', 14.64, 16.40, clip('surf2', 3.4, nombre='commons: surf en Oahu'), GAB)                                        # "vivia en el mar, era surfista"
toma('09', 16.40, 18.26, foto_toma(S_('Colouring_Ollie.00_03_06_05.Still040.jpg'), nombre='innerbloomcoffee.com.au: Ollie en la piscina'), GAB)   # "competia en deportes acuaticos"
toma('10', 18.26, 21.26, foto_toma(S_('510B4819.jpg'), None, BLUR_510B, nombre='innerbloomcoffee.com.au: Ollie tomando su cafe en la playa'), GAB)   # "necesitaba rendir"
toma('11', 21.26, 23.36, foto_toma(S_('A8C5C506-9F0D-4083-95DE-EC38781C9D3F.jpg'), nombre='innerbloomcoffee.com.au: Ollie con palmeras'), GAB,
     T_(['En Estados Unidos'], 110, 64, t0=0.8))
toma('12', 23.36, 26.16, foto_toma(S_('Innerbloom_Cinny_Bun-1367.jpg'), (0, 0, 2000, 2501), BLUR_CINNY, nombre='innerbloomcoffee.com.au: cafe frio sobre hielo (logo desenfocado)'), GAB,
     T_(['Cold brew'], 110, 72, t0=0.18))                                                                                  # "cafe cold brew" (23.36)
toma('13', 26.16, 28.90, Grafico(g_idea), GAB)
toma('14', 28.90, 32.86, Serie([(0.00, Grafico(g_revela)),
                              (1.20, lienzo(NUTC, (0, 0, W), (20, 30, W - 40), [('caja', NUTR, 1.16)], nombre='innerbloomcoffee.com.au: 15,4 g de proteina'))]), GAB)
S[-1]['fuentes'] = ['innerbloomcoffee.com.au: logo y latas', 'innerbloomcoffee.com.au: 15,4 g de proteina']
toma('15', 32.86, 34.86, foto_toma(S_('ourplace_ollie.jpg'), nombre='ourplacemagazine.co.nz: Ollie en su puesto del mercado'), GAB,
     varios(T_(['Mercados de agricultores'], 110, 60, t0=0.9), lambda pil, tl, T: pegar(pil, pastilla('Foto: Our Place Magazine', 34, fondo=(236, 236, 232), color=GRIS, pad=(28, 14)), 540, 145)))
toma('16', 34.86, 38.10, tarjeta(FN_PNG('tiendas'), 459.9, 620.9, [(FN['tiendas'], 1.24, None)], FONDO_LATAS, 'buzzsprout.com (Foodpreneur): 300 tiendas'), GAB)
toma('17', 38.10, 40.88, oscurece(S_('UntitledStudio-Innerbloom-Sep25-9479.jpg'), 0.6, 1.6), GAB)
S[-1]['fuentes'] = ['innerbloomcoffee.com.au: latas en la mano']
toma('18', 40.88, 44.50, Grafico(g_plata), GAB)
toma('19', 44.50, 46.60, tarjeta(FN_PNG('perdio'), 459.9, 620.9, [(FN['perdio'], 0.88, None)], FONDO_CAFE, 'buzzsprout.com (Foodpreneur): perdio tiendas'), GAB)
toma('20', 46.60, 49.34, Grafico(g_tiendas), GAB)
toma('21', 49.34, 50.90, clip('helsinki', 7.0, nombre='commons: camion de bomberos que sale'), GAB)                       # "dejo su trabajo de bombero"
toma('22', 50.90, 54.30, tarjeta(FN_PNG('bombero'), 459.9, 620.9, [(FN['bombero'], 0.40, 1.36), (FN['bombero_1'], 1.36, None)],
                                 Image.open(f'{A}/commons/bomberos2.jpg').convert('RGB'), 'buzzsprout.com (Foodpreneur): dejo de ser bombero'), GAB)
toma('23', 54.30, 55.42, foto_toma(S_('UntitledStudio-Innerbloom-Sep25-9474.jpg'), nombre='innerbloomcoffee.com.au: lata en la mano'), GAB)   # "dedicarse solo a su marca"
toma('24', 55.42, 58.04, lienzo(img(f'{A}/cap/prodpage.png'), (0, 330, 1640), (860, 1520, 760), dur_mov=1.8,
                                 nombre='innerbloomcoffee.com.au: tienda online'), GAB)                                                     # "vender por internet"
toma('25', 58.04, 61.84, tarjeta(FN_PNG('millon'), 499.9, 580.9, [(FN['millon'], 1.94, None)], FONDO_LATAS, 'buzzsprout.com (Foodpreneur): US$1 M online', top=380), GAB,
     contador_toma(1000000, 1.94, cy=230, prefijo='US$', dur=0.6, tam=110))                                                # "millon de dolares" (59.98)
def _anuncio_tarjeta():
    """Tarjeta del anuncio en la Biblioteca (adcard.png, 3 px por px CSS) sobre fondo desenfocado; recuadro en "olliepuddick",
    medido con adcard.js (rango de texto dentro de la tarjeta)."""
    im = Image.open(f'{A}/cap/adcard.png').convert('RGB').crop((0, 0, 1464, 1260)); k = 1000 / im.width
    card = im.resize((1000, int(im.height * k)), Image.LANCZOS)
    bg = Image.blend(Image.fromarray(cubrir(FONDO_LATAS)).filter(ImageFilter.GaussianBlur(36)), Image.new('RGB', (W, H)), 0.3)
    xo, top = (W - 1000) // 2, 170; bg.paste(card, (xo, top))
    fx, fy, fw, fh = ADC['frase']
    return bg, (xo + fx * 3 * k, top + fy * 3 * k, fw * 3 * k, fh * 3 * k)
ADCARD, ADBOX = _anuncio_tarjeta()
toma('26', 61.84, 65.56, Lienzo(ADCARD, (0, 0, W), (ADBOX[0] + ADBOX[2] / 2 - 225, ADBOX[1] - 420 * 450 / W, 450), [('caja', ADBOX, 1.68)], dur_mov=0.9), GAB)   # "sale el mismo" (63.52)
S[-1]['fuentes'] = ['facebook.com/ads/library: anuncio 985135284619460 (InnerBloom with olliepuddick)']
toma('27', 65.56, 68.20, Grafico(g_directo), GAB)
toma('28', 68.20, 71.00, lienzo(panel(Image.open(f'{A}/cap/story.png').convert('RGB').crop((880, 880, 1620, 1275)), y=200, alto_max=560), (0, 0, W), (20, 30, W - 40),
                                 nombre='innerbloomcoffee.com.au/our-story: su historia'), GAB)                                            # "contando su historia"
toma('29', 71.00, 73.62, foto_toma(S_('Coffee.jpg'), nombre='innerbloomcoffee.com.au: dos latas'), GAB,
     T_(['AUTENTICIDAD'], 110, 100, t0=1.76, clave={'AUTENTICIDAD'}))                                                       # "La autenticidad" (72.76)
toma('30', 73.62, 79.233, Serie([(0.00, clip('985135284619460', 21.9, nombre='anuncio-video:985135284619460 (Ollie a camara)')),
                                 (3.86, foto_toma(S_('Innerbloom6pk.jpg'), (0, 300, 2000, 2400), nombre='innerbloomcoffee.com.au: latas'))]), GAB,
     entre(3.86, 9, T_(['Sígueme para más historias'], 110, 60, emo='👇')))
# Gabriel cambia de lugar toma a toma (izquierda / derecha / centro)
LUGARES = ['CI', 'CD', 'C']
for _k, _sh in enumerate(S): _sh['gab'] = LUGARES[_k % 3]
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'Este hombre pasaba los turnos', 'apagando *incendios', 'y terminó creando un *café', 'que hoy está en más de 300 *tiendas',
 'Pero casi lo pierde *todo', 'justo cuando mejor le estaba *yendo',
 'Ollie *Puddick', 'era bombero *profesional', 'y por supuesto su vida', 'se basaba en turnos *largos,', '*madrugadas', 'y para aguantar *café,', 'pero mucho *café',
 'En su tiempo libre', 'vivía en el *mar,', 'era *surfista', 'y competía en deportes *acuáticos',
 'Así que no le bastaba', 'con estar *despierto,', 'necesitaba *rendir',
 'Cuando vivía en Estados *Unidos', 'descubrió el café *cold_brew', 'y le llegó una idea', 'que no le salía de la *cabeza',
 'Y si el café', 'además de *despertarte', 'te diera algo *más',
 'Así nació *Innerbloom,', 'café listo para tomar', 'con 15 gramos de *proteína', 'en cada *lata',
 'Empezó vendiendo los mercados', 'de *agricultores', 'y en pocos años ya estaban', 'más de 300 *tiendas', 'en Australia y Nueva *Zelanda',
 'Y cuando estaba en su mejor *momento', 'llegó algo que casi lo *hunde',
 'Vendían muchísimas *tiendas', 'pero la plata le entraba', 'mucho más *lento', 'de lo que *salía',
 'Y además empezó a perder *algunas', 'sin darse *cuenta', 'por estar buscando tiendas *nuevas', 'en vez de cuidarlas que ya *tenía',
 'Entonces tomó una decisión *difícil,', 'dejó su trabajo de *bombero', 'sin *inversionistas,', 'sin red de *seguridad', 'para dedicarse solo a su *marca',
 'Y lo que lo sacó de esta *incertidumbre', 'fue vender por *internet',
 'Hoy él mismo se puso una meta', 'de llegar al millón de *dólares', 'en ventas en un *año',
 'Y en muchos de sus *anuncios', 'sale él *mismo', 'contando qué hay en cada *lata',
 'Vender directo por internet', 'le devolvió el *control', 'de su *negocio',
 'Y salir él mismo en *cámara', 'contando su *historia', 'le dio algo que ninguna otra', 'marca de café le podría *copiar', 'La *autenticidad',
 'Mándaselo a ese amigo *fundador', 'que no quiere salir en *cámara', 'para que entienda', 'lo que se está *perdiendo',
 'Y sígueme para más *historias', 'como esta',
]
# la transcripcion repite dos veces "Mandaselo a ese amigo fundador..." despues del final (error de Whisper): se descartan esas 22 palabras
SUBS = armar_tarjetas(json.load(open(f'{A}/pal45.json'))[:-22], GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
