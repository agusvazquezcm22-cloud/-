"""Video 38 · "La estrategia del «No lo compres» de Mumu" · v02
Formato pantalla verde, una marca (guia de Gabriel, VIDEO 38) + todo lo que Gabriel y Agus fueron corrigiendo:
Gabriel fijo abajo al centro en todas las tomas; portada grande; nada repetido (ni la imagen del inicio a mitad o al final);
video antes que imagen fija; cierre con personas tomando el producto; recuadros sobre las palabras exactas; cierre con cola.
Lo que no se muestra (regla 12 de la guia): kit "Desinflama y Fluye" ni la palabra "desinflama", testimonios de peso o tallas,
antes y despues, numero de clientas, prensa, el termo de regalo y el "envio gratis hoy" de los anuncios.
Tiempos de la transcripcion del crudo (67,4 s).
v02 (pedido de Agus: "cuando marcas algo en rojo, que sea lo que dice"): todas las marcas de las tarjetas salen de rectangulos MEDIDOS
(m2_fbmeta.json); el 15 % ya no queda tapado por el texto; en los kits va recuadro sobre el nombre.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v38')
RAW = f'{A}/dl/crudo38.mp4'
DUR = 68.3                   # 67,4 del crudo + 0,9 de cola
CABEZA = 692                 # fila del crudo donde esta el tope de su cabeza (medido: 679-712)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)

V = dict(no_lo_compres='1791861635431898', almuerzo='1149407634403392', pesadez='1636598021292250', glow_card='1735834964147494',
         glow_mesa='2326256071471933', tres_momentos='1134974522415500', comer_bien='1680241720780182', vinagre='1061055703650708',
         contabilidad='1427907056178921', hinchada='1422055726679395', rutina='3700633420089593',
         ingredientes='1110511728434081', manana='2129258181289185', toma_vaso='1337613895072452', vaso_verde='1750946557034216', constante='2092539741385400')
MORADO = (58, 43, 158)

# ------------------------------------------------------------ logo de Mumu (amarillo, de su sitio) en pastilla morada
def _chip():
    lg = Image.open(f'{A}/cap/logo_amarillo.png').convert('RGBA'); lg = lg.resize((int(lg.width * 64 / lg.height), 64), Image.LANCZOS)
    c = Image.new('RGBA', (lg.width + 64, 104), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, 103], radius=30, fill=MORADO + (255,))
    c.paste(lg, (32, 20), lg); return c
CHIP = _chip()


def G2(fn, chip=CHIP, y1=1100, k=0.86, y=196):
    """Grafico propio sobre fondo de puntos. chip=None antes de la toma 5 (la marca todavia no se nombra)."""
    usar('grafico:' + fn.__name__); base = _va._puntos(chip)
    def f(tl, T):
        g = fn(tl, T).crop((0, 290, W, y1)); g = g.resize((int(W * k), int((y1 - 290) * k)), Image.LANCZOS)
        im = base.copy(); im.paste(g, ((W - g.width) // 2, y)); return im
    return Grafico(f)


# ------------------------------------------------------------ graficos propios
def _tarro(col, tam=230):
    """Tarro simple sin marca (antes de la toma 5 no se ve el logo)."""
    c = Image.new('RGBA', (tam, int(tam * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(c); w, h = c.size
    d.rounded_rectangle([w * .1, h * .08, w * .9, h * .98], radius=28, fill=col + (255,), outline=TINTA + (255,), width=7)
    d.rounded_rectangle([w * .06, 0, w * .94, h * .16], radius=18, fill=(250, 250, 248, 255), outline=TINTA + (255,), width=7)
    d.rounded_rectangle([w * .24, h * .42, w * .76, h * .66], radius=14, fill=(255, 255, 255, 255)); return c
TARROS = [_tarro((60, 170, 80)), _tarro((236, 72, 150)), _tarro((214, 48, 49))]


def g_tres(tl, T):                   # "logra que te lleves tres productos en vez de uno"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n, t0 in enumerate((0.05, 1.10, 1.40)):
        pegar(im, TARROS[n], 260 + n * 280, 600, pop(tl, t0))
    if tl > 2.05: pegar(im, pastilla('3 en vez de 1', 60, fondo=VERDE_OSC), 540, 905, lerp(0.85, 1, pop(tl, 2.05)))
    return im


def _palabra(s, tam=150, col=TINTA):
    f = font(tam); w = int(f.getlength(s)) + 40; c = Image.new('RGBA', (w, int(tam * 1.4)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _silueta(tam=150):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); n = VERDE_OSC + (255,)
    d.ellipse([tam * .32, tam * .04, tam * .68, tam * .40], fill=n); d.pieslice([tam * .1, tam * .46, tam * .9, tam * 1.3], 180, 360, fill=n); return c
ESPANTAR, CALIFICAR, SIL = _palabra('Espantar'), _palabra('Calificar', col=VERDE_OSC), _silueta()


def g_calificar(tl, T):              # "no te esta espantando, sino calificando ... a su cliente ideal"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, ESPANTAR, 540, 470, pop(tl, 0.05))
    p = ease((tl - 0.42) / 0.25); w = ESPANTAR.width - 40
    if p > 0: d.line([(540 - w / 2, 480), (540 - w / 2 + w * p, 480)], fill=ROJO, width=18)
    k = pop(tl, 1.30)
    if k > 0: pegar(im, CALIFICAR, 500, 640, lerp(0.86, 1, k)); pegar(im, _va_tilde, 890, 620, k)
    if tl > 2.0: pegar(im, SIL, 300, 790, pop(tl, 2.0)); pegar(im, pastilla('su cliente ideal', 52, fondo=VERDE_OSC), 640, 790, pop(tl, 2.1))
    return im


def _tilde(tam=110):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.ellipse([0, 0, tam - 1, tam - 1], fill=VERDE_OSC + (255,))
    d.line([(tam * .26, tam * .52), (tam * .44, tam * .70), (tam * .76, tam * .32)], fill=(255, 255, 255, 255), width=13, joint='curve'); return c
_va_tilde = _tilde()


def _caja(s, w=330, h=150, col=(255, 255, 255), tam=54):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=col + (255,), outline=TINTA + (255,), width=7)
    d.text((w / 2, h / 2), s, font=font(tam), fill=TINTA + (255,), anchor='mm'); return c
C_AD, C_SUELTO, C_KIT = _caja('Anuncio', 320, 150, (250, 220, 120)), _caja('Batido suelto', 400), _caja('Kit', 260, 150, (212, 240, 224))


def g_suelto(tl, T):                 # "la gran mayoria no te mandan a un batido suelto"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_AD, 230, 600, pop(tl, 0.05)); flecha_recta(d, (400, 600), (560, 600), ease((tl - 0.4) / 0.2))
    pegar(im, C_SUELTO, 790, 600, pop(tl, 0.55))
    p = ease((tl - 1.05) / 0.22)
    if p > 0: d.line([(600, 600), (600 + 380 * p, 600)], fill=ROJO, width=16)
    return im


QUE_TOMAR, QUE_MEJORAR = _palabra('¿Qué tomar?', 130), _palabra('¿Qué mejorar?', 130, VERDE_OSC)


def g_mejorar(tl, T):                # "no estas decidiendo que tomar, sino que mejorar"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, QUE_TOMAR, 540, 500, pop(tl, 0.1))
    p = ease((tl - 1.52) / 0.25); w = QUE_TOMAR.width - 40
    if p > 0: d.line([(540 - w / 2, 508), (540 - w / 2 + w * p, 508)], fill=ROJO, width=16)
    k = pop(tl, 2.40)
    if k > 0: pegar(im, QUE_MEJORAR, 540, 760, lerp(0.86, 1, k))
    return im


def g_logo(tl, T):                   # "Se llama Mumu": el logo grande sobre el morado de la marca
    im = Image.new('RGB', (W, H), MORADO); lg = Image.open(f'{A}/cap/logo_amarillo.png').convert('RGBA')
    k = lerp(0.9, 1.0, ease(tl / 0.25)); lg = lg.resize((int(820 * k), int(820 * k * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, ((W - lg.width) // 2, 470 - lg.height // 2), lg); return im


def _mejores_amigos():
    """Una lista de "Mejores amigos" al estilo de Instagram, SIN nombres ni fotos de personas reales (la guia pide eso)."""
    c = Image.new('RGBA', (760, 860), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, 759, 859], radius=44, fill=(255, 255, 255, 255), outline=(225, 225, 222, 255), width=4)
    d.ellipse([300, 40, 460, 200], fill=(31, 192, 84, 255)); s = 52
    pts = [(380 + s * math.cos(math.radians(-90 + 36 * i)) * (1 if i % 2 == 0 else 0.42), 120 + s * math.sin(math.radians(-90 + 36 * i)) * (1 if i % 2 == 0 else 0.42)) for i in range(10)]
    d.polygon(pts, fill=(255, 255, 255, 255)); d.text((380, 250), 'Mejores amigos', font=font(50), fill=TINTA + (255,), anchor='mm')
    for n in range(4):
        y = 360 + n * 120
        if n == 1:
            ch = CHIP.resize((int(CHIP.width * 70 / CHIP.height), 70), Image.LANCZOS); c.paste(ch, (60, y - 35), ch)
            d.rounded_rectangle([560, y - 34, 700, y + 34], radius=34, fill=(31, 192, 84, 255)); d.text((630, y), 'Agregado', font=font(26), fill=(255, 255, 255, 255), anchor='mm')
        else:
            d.ellipse([60, y - 40, 140, y + 40], fill=(222, 222, 220, 255)); d.rounded_rectangle([170, y - 14, 470, y + 14], radius=14, fill=(232, 232, 230, 255))
            d.rounded_rectangle([560, y - 34, 700, y + 34], radius=34, outline=(200, 200, 198, 255), width=4)
    return c
MA = _mejores_amigos()


def g_mejores_amigos(tl, T):         # "como si te agregaran en Instagram"
    im = fondo_grafico(); pegar(im, MA, 540, 720, lerp(0.9, 1, pop(tl, 0.0, 0.2))); return im


# ------------------------------------------------------------ capturas
def _card(png):
    """Tarjeta de la Biblioteca (2 px por px CSS) sobre el gris de la Biblioteca, como lona para zoom: (np, factor css->lona)."""
    card = Image.open(png).convert('RGB'); k = 980 / card.width; card = card.resize((980, int(card.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, max(H, card.height + 400)), (240, 242, 245)); c.paste(card, (50, 110)); return np.asarray(c), 2 * k
M2 = json.load(open(f'{A}/cap/m2_fbmeta.json'))['cards']
FR = lambda i, f, k=0: M2[V[i]]['frases'][f][k]                                    # rectangulo MEDIDO de la frase en la tarjeta (px CSS)
NLC, fN = _card(f'{A}/cap/m2_card_{V["no_lo_compres"]}.png')
cN = lambda x, y, w, h: (50 + x * fN, 110 + y * fN, w * fN, h * fN)
PES, fP = _card(f'{A}/cap/m2_card_{V["pesadez"]}.png')
cP = lambda x, y, w, h: (50 + x * fP, 110 + y * fP, w * fP, h * fP)
GLW, fG = _card(f'{A}/cap/m2_card_{V["glow_card"]}.png')
cG = lambda x, y, w, h: (50 + x * fG, 110 + y * fG, w * fG, h * fG)
MM = json.load(open(f'{A}/cap/m_fbmeta.json'))
FBG = np.concatenate([img(f'{A}/cap/m_fbg{i}.png') for i in range(2)], 0)       # Biblioteca de Mumu (2 px por px CSS, pais: Colombia)
_rf = tuple(v * 2 for v in MM['results'][:4])
KITS, GLOW, DETOX, RENUEVA, SUS = (img(f'{A}/cap/{n}.png') for n in ('kits', 'glow', 'detox', 'renueva', 'sus'))
KJ, SJ = json.load(open(f'{A}/cap/kits.json')), json.load(open(f'{A}/cap/sus.json'))


def _suscripcion():
    """La pagina de suscripcion sin el bloque de fotos de clientas (antes y despues): arriba el texto (Close Friends, mensual,
    15 % / envio / regalo), al medio los iconos de beneficios, abajo la foto principal de la pagina."""
    sp = Image.fromarray(SUS); txt = sp.crop((0, 2160, 1640, 2530)); ico = sp.crop((0, 5200, 1640, 5520)); hero = sp.crop((0, 100, 1640, 2070))
    hh = 2920 - 690; k = hh / hero.height; hero = hero.resize((int(1640 * k), hh), Image.LANCZOS); hero = hero.crop(((hero.width - 1640) // 2, 0, (hero.width - 1640) // 2 + 1640, hh))
    c = Image.new('RGB', (1640, 2920), (255, 255, 255)); c.paste(txt, (0, 0)); c.paste(ico, (0, 370)); c.paste(hero, (0, 690)); return np.asarray(c)
P2 = lambda r, mx=10, my=8: (r[0] * 2 - mx, r[1] * 2 - my, r[2] * 2 + 2 * mx, r[3] * 2 + 2 * my)
kf = lambda f: P2(KJ['frases'][f][0], 14, 10)
sf = lambda f: P2(SJ['frases'][f][0], 10, 6)
SUSC = _suscripcion()
st = lambda f: (lambda r: (r[0], r[1] - 2160, r[2], r[3]))(sf(f))                                   # texto -> lona
si = lambda x, y, w, h: (x * 2, 370 + y * 2 - 5200, w * 2, h * 2)                                      # iconos (px CSS) -> lona
CAB = img(f'{A}/cap/cabecera.png')                                                  # cabecera de mumucol.com (3 px por px CSS)

# ------------------------------------------------------------ tomas
PORTADA = lambda: clip(V['no_lo_compres'], 1.0, nombre='portada')
toma('01', 0.00, 2.10, PORTADA(), GAB, T_(['La estrategia del', '«No lo compres»'], 196, 66, t0=-1.0, clave={'«No', 'lo', 'compres»'}, emo='🤯'))
toma('02', 2.10, 3.66, Serie([(0, clip(V['ingredientes'], 3.0)), (0.80, clip(V['vinagre'], 20.2))]), GAB)                          # batido verde, suplementos
toma('03', 3.66, 6.08, Serie([(0, clip(V['manana'], 31.0)), (1.20, clip(V['toma_vaso'], 23.0))]), GAB,
     T_(['1 minuto al día'], 196, 64, t0=0.3))
toma('04', 6.08, 8.76, G2(g_tres, None), GAB)
toma('05', 8.76, 9.42, Grafico(g_logo), GAB)
S[-1]['fuentes'] = ['logo de mumucol.com']
toma('06', 9.42, 11.74, clip(V['glow_mesa'], 0.3), GAB)
toma('07', 11.74, 16.90, Serie([
    (0.00, lienzo(NLC, (0, 0, W), (20, 20, W - 40), nombre='tarjeta:no lo compres')),                                          # "todo empieza con ese mismo anuncio"
    (1.38, Lienzo(NLC, (20, 20, W - 40), (60, 300, 760), [('sub', cN(*FR('no_lo_compres', 'No lo compres si lo que buscas es una dieta')), 2.35)], dur_mov=0.45)),                 # "...dice no lo compres si lo que buscas..."
]), GAB)
toma('08', 16.90, 20.52, G2(g_calificar), GAB)
toma('09', 20.52, 25.36, Serie([
    (0.00, lienzo(FBG, (0, 2400, 1900), (0, 300, 1700), nombre='biblioteca:grilla', dur_mov=3.0)),                               # "el resto de la pauta"
    (3.42, Lienzo(FBG, (0, 300, 1700), (0, 300, 1500), [('caja', _rf, 0.05), ('flecha_ad', _rf, 0.05)], dur_mov=0.4)),           # "mas de 50 anuncios activos"
]), GAB)
toma('10', 25.36, 27.56, tarjeta(f'{A}/cap/m2_card_{V["almuerzo"]}.png', [('sub', tuple(FR('almuerzo', 'El almuerzo estuvo rico')), 0.3)], nombre='tarjeta:almuerzo'), GAB)
toma('11', 27.56, 29.76, lienzo(PES, (0, 0, W), (30, 200, W - 60), [('sub', cP(*FR('pesadez', 'Esa pesadez de las tres')), 0.1, 1.1), ('sub', cP(*FR('pesadez', 'el botón del jean que aprieta')), 1.1)],
                               nombre='tarjeta:pesadez', dur_mov=0.4), GAB)
toma('12', 29.76, 31.62, G2(g_suelto), GAB)
toma('13', 31.62, 33.64, lienzo(KITS, (0, 2000, 1640), (0, 2600, 1640), nombre='mumucol.com:kits', dur_mov=2.0), GAB)
_nom = lambda j, n: P2(json.load(open(f'{A}/cap/{j}.json'))['textos'][[t[0] for t in json.load(open(f'{A}/cap/{j}.json'))['textos']].index(n)][1:], 12, 8)
toma('14', 33.64, 35.22, Serie([(0.00, lienzo(GLOW, (0, 1340, 1640), None, [('caja', _nom('glow', 'Kit Glow Up'), 0.05)], nombre='mumucol.com:kit glow up')),
                                (0.66, lienzo(DETOX, (0, 1340, 1640), None, [('caja', _nom('detox', 'Kit Detox'), 0.05)], nombre='mumucol.com:kit detox')),
                                (1.20, lienzo(RENUEVA, (0, 1340, 1640), None, [('caja', _nom('renueva', 'Kit Renueva'), 0.05)], nombre='mumucol.com:kit renueva'))]), GAB)
toma('15', 35.22, 37.94, G2(g_mejorar), GAB)
toma('16', 37.94, 40.28, clip(V['glow_card'], 9.5), GAB)                                                                          # los tres juntos en la mesa                                                                          # los tres juntos en la mesa
toma('17', 40.28, 44.26, lienzo(GLW, (0, 0, W), (20, 430, 760), [('caja', cG(*FR('glow_card', 'batido verde en la mañana')), 1.30, 2.20), ('caja', cG(*FR('glow_card', 'gomitas de manzana en el día')), 2.20, 3.28),
                                                                ('caja', cG(*FR('glow_card', 'colágeno en la noche')), 3.28)], nombre='tarjeta:glow up tres momentos', dur_mov=0.6), GAB)
toma('18', 44.26, 46.80, clip(V['vaso_verde'], 1.0), GAB, T_(['1 minuto cada uno'], 196, 64, t0=0.6))
toma('19', 46.80, 48.82, Serie([(0.00, lienzo(KITS, (0, 1900, 1300), None, [('caja', kf('AHORRA 15%'), 0.1)], nombre='mumucol.com:kits descuentos')),
                                (0.68, Lienzo(KITS, (340, 2980, 1300), None, [('caja', kf('AHORRA 18%'), 0.05)])),
                                (1.36, Lienzo(KITS, (0, 6378, 1000), None, [('caja', kf('AHORRA 25%'), 0.05)]))]), GAB,
     T_(['2 = 15% · 3 = 18% · 4 = 25%'], 140, 56, t0=0.1))
toma('20', 48.82, 52.00, lienzo(SUSC, (0, 0, 1640), (440, 0, 1200), [('caja', st('débito automático mensual'), 1.45, 1.95), ('sub', st('Close Friends para que tu Mumu'), 2.0)],
                               nombre='mumucol.com:suscripcion', dur_mov=0.5), GAB)
toma('21', 52.00, 53.34, G2(g_mejores_amigos, k=0.8), GAB)
toma('22', 53.34, 55.32, lienzo(SUSC, (318, 300, 1000), None, [('caja', si(188, 2643, 104, 98), 0.05, 0.84), ('caja', si(366, 2643, 98, 98), 0.84, 1.40),
                                                             ('caja', si(532, 2643, 98, 98), 1.40)], nombre='mumucol.com:beneficios close friends'), GAB)
toma('23', 55.32, 59.18, Serie([(0, clip(V['tres_momentos'], 18.0)), (1.90, clip(V['toma_vaso'], 37.0, nombre='anuncio-video:1337613895072452 (s37: la clienta con su vaso)'))]), GAB)
toma('24', 59.18, 62.90, Serie([(0.00, clip(V['hinchada'], 37.0)), (0.93, clip(V['contabilidad'], 0.5)), (1.86, clip(V['almuerzo'], 13.0)),
                                (2.79, clip(V['pesadez'], 25.0))]), GAB)
toma('25', 62.90, 68.30, Serie([(0, clip(V['comer_bien'], 28.3)), (3.52, clip(V['rutina'], 4.0))]), GAB,
     T_(['¿Te atreverías?'], 196, 70, t0=0.25, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 'Esta es la *invitación', 'que hace una marca *colombiana', 'que vende batidos verdes', 'y *suplementos',
 'para que cuidarte te tome', 'tan solo un minuto al *día',
 'Y aun así logra que te lleves', 'tres productos en vez de *uno',
 'Se llama *Mumu', 'y te muestro cómo lo hacen', 'para que lo pruebes con tu *marca',
 'Todo empieza con ese mismo *anuncio,', 'cuando miramos el mensaje completo', 'dice «No lo *compres»', 'si lo que buscas es hacer *dieta»',
 'No te está *espantando', 'sino *calificando', 'de una manera increíble', 'a su cliente *ideal',
 'Y eso lo puedes identificar', 'muy fácilmente', 'cuando nos ponemos a ver', 'el resto de la pauta', 'más de 50 *anuncios', 'activos',
 'Muchos arrancan con cosas', 'que sientes después de *almorzar', 'como la pesadez de la *tarde', 'o el jean que les *aprieta',
 'La gran mayoría no te mandan', 'a un batido *suelto', 'sino un kit con el nombre', 'del resultado que *deseas',
 'Glow Up, Detox o *Renueva',
 'De esta manera no estás decidiendo', 'qué tomar sino qué *mejorar',
 'Por esta razón terminas', 'con tres productos y no con *uno',
 'Por ejemplo con Glow Up te llevas', 'batido en la *mañana,', 'gomitas a *mediodía', 'y colágeno en la *noche',
 'No te demoras ni un minuto', 'tomando cada uno', 'y sin hacer *dieta',
 'Y mientras más sumas', 'más descuento te *dan',
 'Pero lo más curioso es que', 'si la quieres cada *mes', 'entras a su lista de Close *Friends',
 '~ como si te agregaran en *Instagram', 'precio especial, envío *gratis', 'y un *regalo',
 'Con eso te das cuenta que', 'la invitación a no comprar', 'no aleja a nadie', 'que realmente le *sirva',
 'Porque le está dejando claro', 'que con ellos no vas a *sufrir', 'y así es mucho más fácil', 'que te *elija',
 '¿Te atreverías a decirle', 'a alguien que no te compre', 'así sea por pura *estrategia?', 'Cuéntame en los *comentarios',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal38.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
