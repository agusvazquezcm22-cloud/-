"""Video 36 · "La estrategia del test de Aluné" · v01
Formato pantalla verde, una marca. El centro del video es el test de piel de quiz.alune.com.co: cada pantalla es una
captura real del recorrido (430x764 px CSS, 3 px por px = 9:16). Gabriel fijo abajo al centro en todas las tomas.
Tiempos de la transcripcion del crudo (84,5 s; se corta en 84,3: lo ultimo que dice es "comentarios").
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v36')
RAW = f'{A}/dl/crudo36.mp4'
DUR = 84.3
CABEZA = 620                 # fila del crudo donde esta el tope de su cabeza (medido: 592-670)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'                    # lugar fijo de Gabriel en todo el video
configurar(A, logo=None)

AD = dict(mujeres='1481277277303145', sintomas='1511613764113110', duermes='965685766307754', razon='1153283190517779', ruido='2650736035339728', bandeja='1799664991086053',
          medida='1532452245604460', cansada='2369136963629680', iceberg='1086499060885265', pastilla='1155603330479888')

# ------------------------------------------------------------ pantallas del test (capturas con sus textos medidos)
QM = json.load(open(f'{A}/cap/q_meta.json')); OM = json.load(open(f'{A}/cap/o_meta.json'))
META = {'q': QM, 'o': OM}
K = 1080 / 1290              # px de pantalla por px de captura


def _lona(pref, k):
    """La captura con una franja de su mismo fondo debajo, para poder correr la vista hacia abajo."""
    im = img(f'{A}/cap/{pref}_{k:02d}.png')[:2292]
    pie = np.tile(im[-8:-7], (1500, 1, 1))
    return np.concatenate([im, pie], 0)


def r_(pref, k, frag, mx=18, my=14, n=0):
    """Rectangulo (px de captura) del n-esimo texto de esa pantalla que contiene `frag`, con margen."""
    t = [x for x in META[pref][k]['t'] if frag in x[0]][n]
    return (t[1] * 3 - mx, t[2] * 3 - my, t[3] * 3 + 2 * mx, t[4] * 3 + 2 * my)


def pant(pref, k, marcas=(), foco=None, a=400, nombre=None, zoom=0.035):
    """Pantalla del test a todo el ancho. foco: texto que tiene que quedar a `a` px del borde de arriba (corre la vista)."""
    y0 = 0
    if foco: y0 = max(0, int(r_(pref, k, foco)[1] - a / K))
    return lienzo(_lona(pref, k), (0, y0, 1290), (1290 * zoom / 2, y0 + 12, 1290 * (1 - zoom)), marcas, nombre=nombre or f'test:{pref}{k:02d}')


# ------------------------------------------------------------ logo y piezas para los graficos
def _chip():
    lg = Image.fromarray(img(f'{A}/cap/q_19.png')[34:172, 30:340]); lg = lg.resize((int(lg.width * 100 / lg.height), 100), Image.LANCZOS)
    m = Image.new('L', lg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, lg.width - 1, lg.height - 1], radius=24, fill=255)
    c = Image.new('RGBA', lg.size, (0, 0, 0, 0)); c.paste(lg, (0, 0), m); return c
CHIP = _chip()


def G2(fn, chip=CHIP, y1=1100, k=0.86, y=196):
    usar('grafico:' + fn.__name__); base = _va._puntos(chip)
    def f(tl, T):
        g = fn(tl, T).crop((0, 290, W, y1)); g = g.resize((int(W * k), int((y1 - 290) * k)), Image.LANCZOS)
        im = base.copy(); im.paste(g, ((W - g.width) // 2, y)); return im
    return Grafico(f)


def _caja(s, w=300, h=150, col=(255, 255, 255), tam=54, txtcol=TINTA):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=col + (255,), outline=TINTA + (255,), width=7)
    d.text((w / 2, h / 2), s, font=font(tam), fill=txtcol + (255,), anchor='mm'); return c
C_AD = _caja('Anuncio', 330, 150, (250, 220, 120))
C_T = [_caja(f'Test {n}', 250, 140) for n in (1, 2, 3)]


def g_tests(tl, T):                  # "uno distinto para cada posible problema"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_AD, 540, 420, pop(tl, 0.05))
    for n, t0 in enumerate((1.25, 2.1, 2.9)):
        x = 220 + n * 320
        flecha_recta(d, (540 + (n - 1) * 90, 505), (x, 690), ease((tl - t0) / 0.22))
        pegar(im, C_T[n], x, 780, pop(tl, t0 + 0.16))
    return im


def _mini(pref, k, w=280):
    """Miniatura de la portada de un test (la parte de arriba: foto y titular), como un telefono."""
    t = Image.fromarray(img(f'{A}/cap/{pref}_{k:02d}.png')[:1500]).resize((w, int(1500 * w / 1290)), Image.LANCZOS)
    c = Image.new('RGBA', (w + 16, t.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], radius=30, fill=TINTA + (255,))
    m = Image.new('L', t.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, t.width - 1, t.height - 1], radius=24, fill=255); c.paste(t, (8, 8), m); return c
MINIS = [(_mini('n', 0), 'Sueño', 0.70), (_mini('q', 0), 'Piel', 1.32), (_mini('m', 0), 'Ánimo', 1.78)]
P_PORQUE = pastilla('¿Por qué?', 64, fondo=ROJO)


def g_tres(tl, T):                   # "para sueno, piel y animo" ... "pero por que hacen esto?"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n, (mi, nombre, t0) in enumerate(MINIS):
        x = 205 + n * 335; k = pop(tl, t0)
        if k > 0: pegar(im, mi, x, 640, lerp(0.86, 1, k))
        if k > 0.6: txt(d, (x, 860), nombre, 60, TINTA)
    if tl > 2.36: pegar(im, P_PORQUE, 540, 376, lerp(0.85, 1, pop(tl, 2.36)))
    return im


def g_dinero(tl, T):                 # "ya no te pregunta por tu piel, te pregunta por tu dinero"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    txt(d, (540, 520), 'Tu piel', 150, GRIS)
    p = ease((tl - 0.7) / 0.25); w = font(150).getlength('Tu piel')
    if p > 0: d.line([(540 - w / 2 - 20, 528), (540 - w / 2 - 20 + (w + 40) * p, 528)], fill=ROJO, width=16)
    k = pop(tl, 1.95)
    if k > 0:
        c = Image.new('RGBA', (900, 220), (0, 0, 0, 0)); ImageDraw.Draw(c).text((450, 110), 'Tu dinero', font=font(170), fill=VERDE_OSC + (255,), anchor='mm'); pegar(im, c, 540, 760, lerp(0.86, 1, k))
    return im


def _tarro(h=300):
    t = Image.open(ad(AD['sintomas'])).convert('RGB'); w0, h0 = t.size; t = t.crop((int(w0 * .33), int(h0 * .22), int(w0 * .67), int(h0 * .80))); t = t.resize((int(t.width * h / t.height), h), Image.LANCZOS)
    m = Image.new('L', t.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, t.width - 1, t.height - 1], radius=36, fill=255); c = Image.new('RGBA', t.size, (0, 0, 0, 0)); c.paste(t, (0, 0), m); return c
TARRO = _tarro()


def g_ticket(tl, T):                 # "subir el ticket promedio": un tarro y entran dos mas
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    for n, t0 in enumerate((0.05, 0.55, 0.95)):
        pegar(im, TARRO, 300 + n * 240, 560, pop(tl, t0))
    p = ease((tl - 1.5) / 0.3)
    if p > 0:
        txt(d, (470, 850), 'Ticket promedio', 70, TINTA)
        flecha_recta(d, (810, 900), (810, 900 - 110 * p), 1 if p > 0.6 else 0.01, color=VERDE_OSC, ancho=16)
    return im


def g_barras(tl, T):                 # "ese plan parece nada en comparacion con lo que has gastado": cifras de las capturas del test
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    p1 = ease((tl - 0.15) / 0.45); p2 = ease((tl - 1.9) / 0.3)
    if p1 > 0:
        d.rounded_rectangle([190, 880 - 470 * p1, 470, 880], radius=22, fill=ROJO)
        if p1 > 0.9: txt(d, (330, 370), '$2.880.000', 62, TINTA); txt(d, (330, 930), 'en cremas', 50, GRIS, 'SemiBold')
    if p2 > 0:
        d.rounded_rectangle([610, 880 - 54 * p2, 890, 880], radius=16, fill=VERDE_OSC)
        if p2 > 0.9: txt(d, (750, 786), '$329.900', 62, TINTA); txt(d, (750, 930), 'el plan', 50, GRIS, 'SemiBold')
    return im


def _marca(ok, tam=92):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c); d.ellipse([0, 0, tam - 1, tam - 1], fill=(VERDE_OSC if ok else ROJO) + (255,)); b = (255, 255, 255, 255)
    if ok: d.line([(tam * .26, tam * .52), (tam * .44, tam * .70), (tam * .76, tam * .32)], fill=b, width=12, joint='curve')
    else: d.line([(tam * .3, tam * .3), (tam * .7, tam * .7)], fill=b, width=12); d.line([(tam * .7, tam * .3), (tam * .3, tam * .7)], fill=b, width=12)
    return c
C_TEST, C_TIENDA, M_OK, M_NO = _caja('Test', 280, 150), _caja('Tienda', 280, 150), _marca(True), _marca(False)


def g_caminos(tl, T):                # "te mandan a un test y no a su tienda"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, C_AD, 540, 420, pop(tl, 0.05))
    flecha_recta(d, (470, 505), (310, 690), ease((tl - 0.55) / 0.22)); pegar(im, C_TEST, 300, 780, pop(tl, 0.7)); pegar(im, M_OK, 430, 705, pop(tl, 1.0))
    flecha_recta(d, (610, 505), (770, 690), ease((tl - 1.45) / 0.22), color=GRIS); pegar(im, C_TIENDA, 780, 780, pop(tl, 1.6)); pegar(im, M_NO, 910, 705, pop(tl, 1.9))
    return im


# ------------------------------------------------------------ Biblioteca y pagina
AM = json.load(open(f'{A}/cap/a_fbmeta.json')); ALM = json.load(open(f'{A}/cap/almeta.json'))
AG = img(f'{A}/cap/a_fbg0.png'); _ra = tuple(v * 2 for v in AM['results'][:4])


def _card_larga():
    """La tarjeta del anuncio a todo el ancho, con fondo debajo: la vista baja hasta el enlace (quiz.alune.com.co)."""
    c = Image.open(f'{A}/cap/a_card_1597328349075545.png').convert('RGB'); lona = Image.new('RGB', (c.width + 60, c.height + 1700), (240, 242, 245)); lona.paste(c, (30, 40)); return np.asarray(lona)
CARD = _card_larga()
_enl = (30 + 14, 40 + 1066, 250, 34)       # "QUIZ.ALUNE.COM.CO" en la tarjeta (px de la captura, 2 px por px CSS)

PORTADA = lambda: anuncio(AD['duermes'], 0.03, nombre='portada', encaje=(0.66, 330))

# ------------------------------------------------------------ tomas
toma('01', 0.00, 1.04, PORTADA(), GAB, T_(['La estrategia del', 'test de Aluné'], 196, 66, t0=-1.0, clave={'test'}, emo='🤯'))
toma('02', 1.04, 2.02, lienzo(AG, (0, 0, 1700), (0, 300, 1500), [('caja', _ra, 0.1), ('flecha_ad', _ra, 0.1)], nombre='biblioteca:cabecera', dur_mov=0.4), GAB)
toma('03', 2.02, 3.70, lienzo(CARD, (0, 0, 952), (0, 560, 952), [('sub', _enl, 0.75)], nombre='tarjeta:enlace al test', dur_mov=0.5), GAB)
toma('04', 3.70, 5.24, anuncio(AD['bandeja'], 0.04), GAB)
toma('05', 5.24, 8.76, Serie([(0, captura(f'{A}/cap/al_lema.png', [([[ALM['lema'][0][0], ALM['lema'][0][1], 300, 72]], 0.9, None, 'flecha_ad')], nombre='alune.com.co:lema')),
                              (2.20, anuncio(AD['cansada'], 0.03))]), GAB)
toma('06', 8.76, 10.66, Serie([(0, anuncio(AD['ruido'], 0)), (0.95, anuncio(AD['iceberg'], 0))]), GAB)
toma('07', 10.66, 13.10, Serie([(0, anuncio(AD['mujeres'], 0.03, [('caja', (0.10, 0.195, 0.80, 0.115), 0.5)])),
                                (1.56, pant('n', 0, nombre='test:portada noche'))]), GAB)
META['n'] = json.load(open(f'{A}/cap/n_meta.json'))
toma('08', 13.10, 17.28, G2(g_tests), GAB)
toma('09', 17.28, 20.52, G2(g_tres, k=0.84), GAB)
toma('10', 20.52, 22.02, pant('q', 0, [('caja', r_('q', 0, 'Test gratuito', 60, 22), 0.5)], nombre='test:portada piel'), GAB)
toma('11', 22.02, 24.12, pant('q', 6, [('caja', r_('q', 6, 'Cómo está tu ciclo'), 0.5)]), GAB)
toma('12', 24.12, 26.18, Serie([(0, pant('q', 1, [('sub', r_('q', 1, 'lo primero que notaste', 0, 6), 0.12)])),
                                (0.90, pant('q', 2, [('sub', r_('q', 2, 'por la mañana', 0, 6), 0.1)])),
                                (1.56, pant('q', 4, [('sub', r_('q', 4, 'tus noches', 0, 6), 0.08)]))]), GAB)
toma('13', 26.18, 28.68, pant('q', 13, [('caja', r_('q', 13, 'no me reconozco', 60, 30), 1.1), ('flecha_ad', r_('q', 13, 'no me reconozco', 60, 30), 1.1)]), GAB)
toma('14', 28.68, 31.98, pant('q', 12, [('sub', r_('q', 12, 'No envejeciste de golpe', 0, 6), 1.5)], foco='No envejeciste de golpe', a=470), GAB)
toma('15', 31.98, 34.24, pant('q', 8, [('caja', r_('q', 8, '8 de 11', 16, 12), 0.6), ('flecha_ai', r_('q', 8, '8 de 11', 16, 12), 0.6)], nombre='test:pregunta 8'), GAB)
toma('16', 34.24, 36.72, G2(g_dinero), GAB)
toma('17', 36.72, 39.64, pant('q', 9, [('caja', r_('q', 9, '$120.000', 30, 18), 0.6, 2.1), ('caja', r_('q', 9, 'Unos 2 años', 60, 30), 2.1)], foco='$120.000', a=430, nombre='test:pregunta 8'), GAB)
toma('18', 39.64, 43.40, pant('q', 14, [('caja', r_('q', 14, 'Al ritmo de hoy'), 1.2), ('flecha_ad', r_('q', 14, 'Al ritmo de hoy'), 1.2)]), GAB)
toma('19', 43.40, 47.36, Serie([(0, pant('q', 15)),
                                (1.86, pant('q', 17, [('caja', r_('q', 17, 'Brillo Apagado', 30, 20), 1.1), ('flecha_ad', r_('q', 17, 'Brillo Apagado', 30, 20), 1.1)], foco='Brillo Apagado', a=520))]), GAB)
toma('20', 47.36, 50.38, pant('o', 21, [('caja', r_('o', 21, 'Desbloqueaste por terminar', 70, 22), 0.9), ('caja', r_('o', 21, '−$120.100', 16, 14), 1.9)]), GAB)
toma('21', 50.38, 53.94, pant('o', 19, [('sub', r_('o', 19, 'Hoy, por terminar tu test', 0, 6), 1.2), ('caja', r_('o', 19, '$329.900', 10, 6), 2.2)], foco='Hoy, por terminar tu test', a=330), GAB)
toma('22', 53.94, 55.06, pant('q', 19, nombre='oferta:arriba'), GAB)
toma('23', 55.06, 59.38, pant('o', 20, [('caja', r_('o', 20, 'Recomendado para', 22, 14), 1.4), ('caja', r_('o', 20, '3 tarros · 90 noches', 14, 12), 2.5), ('flecha_ad', r_('o', 20, '3 tarros · 90 noches', 14, 12), 2.5)]), GAB)
toma('24', 59.38, 61.88, G2(g_ticket), GAB)
toma('25', 61.88, 66.06, G2(g_barras), GAB)
toma('26', 66.06, 68.38, G2(g_caminos), GAB)
toma('27', 68.38, 70.04, anuncio(AD['pastilla'], 0.04), GAB)
toma('28', 70.04, 74.40, Serie([(0, pant('q', 10)),
                                (1.92, pant('q', 9, [('caja', r_('q', 9, '$2.880.000', 30, 18), 0.9), ('flecha_ai', r_('q', 9, '$2.880.000', 30, 18), 0.9)], foco='$2.880.000', a=420, nombre='test:lo que lleva gastado'))]), GAB)
toma('29', 74.40, 78.90, pant('q', 7, [('caja', r_('q', 7, 'Esos 5 años no son tuyos', 20, 14), 2.9)], foco='Tienes 44', a=430), GAB)
toma('30', 78.90, 81.52, anuncio(AD['medida'], 0.04), GAB)
toma('31', 81.52, 84.30, PORTADA(), GAB, T_(['¿Funcionaría para', 'cualquier marca?'], 196, 66, t0=0.25, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {'portada': 'regla 10 de la guia de Gabriel: el cierre vuelve a la imagen del inicio',
                        'test:pregunta 8': 'la misma pregunta antes y despues de contestar (asi la pide la guia: tomas 17 y 19)'}

GUION = [
 'Esta marca tiene', 'unos 60 *anuncios', 'activos en Meta', 'y no te invita', 'a ver su tienda *online',
 'Aluné es una marca *colombiana', 'que promete ayudar', 'a las mujeres', 'en la *menopausia', 'a volver a dormir', 'la noche *entera',
 'Y aquí está', 'el sistema exacto', 'que hay detrás',
 'Lo que ellos hacen', 'con sus anuncios', 'es mandarte a un *test',
 'Pero no uno genérico,', 'tienen uno *distinto', 'para cada posible problema', 'de su cliente ideal',
 'En este caso para *sueño,', 'piel y *ánimo', 'Pero ¿por qué hacen esto?',
 'Para entenderlo,', 'miremos el de la *piel',
 'Primero te pregunta', 'como si tuvieras enfrente', 'a un *médico',
 'Qué notaste,', 'cómo amaneces,', 'cómo duermes',
 'Y como es de esperar,', 'te pone frases', 'con las que te *identificas',
 'Porque antes de venderte', 'cualquier cosa,', 'necesita que sientas', 'que te *entiende',
 'Pero en la pregunta', 'número *8', 'viene lo interesante',
 'Ya no te pregunta', 'por tu piel,', 'te pregunta por tu *dinero',
 'Te pregunta como cuánto', 'gastas al mes en *cremas,', 'desde hace cuánto',
 'Y ahí mismo', 'te hace la *cuenta', 'de lo que vas a seguir gastando', 'si no cambias nada',
 'Y al terminar este test,', 'todavía no te vende,', 'le pone *nombre', 'a lo que te pasa',
 'Y además por solo', 'hacer el test,', 'desbloqueas un descuento *especial',
 'De esta manera,', 'cuando por fin ves la oferta,', 'ya sientes que vas *ganando',
 'Y mira cómo suben el *ticket',
 'En vez de venderte', 'un solo tarro,', 'te arman un plan', 'de 90 *noches', 'según tu resultado',
 'Una de las mejores estrategias', 'para subir el ticket *promedio',
 'Y lo más importante,', 'ese plan ahora parece *nada', 'en comparación con', 'lo que has gastado antes',
 'Por esa razón ellos', 'te mandan a un *test', 'y no a su tienda',
 'No lo usan para', 'recomendar su producto',
 'Lo usan para que', 'antes que vea el precio,', 'la clienta sume sola', 'cuánta platica lleva *perdida',
 'Esta estrategia te da a entender', 'que basta con hacerle saber', 'a tu clienta', 'todo lo que le ha *costado', 'ese problema',
 'Y que con tu producto', 'lo habría resuelto', 'hace mucho *tiempo',
 '¿Crees que esto funcionaría', 'para cualquier *marca?', 'Te leo en los *comentarios',
]
_pal = [x for x in json.load(open(f'{A}/pal36.json')) if x['s'] < 84.2]
SUBS = armar_tarjetas(_pal, GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
