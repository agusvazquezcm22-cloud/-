"""Video 35 · "Liquid I.V. vs Electrolit: ¿quién lo hace mejor?" · v01
Formato VS (guia de Gabriel): dos marcas frente a frente, Liquid I.V. SIEMPRE a la izquierda y Electrolit a la derecha.
Pantalla dividida solo para comparar; fuera de eso, una imagen a la vez. Gabriel fijo en un solo lugar (pedido de Agus):
aca al centro, porque es el arbitro entre las dos mitades. Tiempos de la transcripcion del crudo (74,2 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v35')
RAW = f'{A}/dl/crudo35.mp4'
DUR = 74.1
CABEZA = 722                 # fila del crudo donde esta el tope de su cabeza (medido: 712-739)
CENTRO = 535                 # columna del centro de su cabeza (medido: 520-552)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'                    # lugar fijo de Gabriel en todo el video
configurar(A, logo=None)

# ------------------------------------------------------------ anuncios (Biblioteca de Anuncios de Meta)
L = dict(sobre='1061262113579933', amazon1='1933810037584691', variety='2027745281964723', bolsa='2178902119690568', ahorra30='1828405711682374',
         reco='2616181155474182', suscribe='2019305582089395',
         v_prime='1061262113579933', v_fiestas='1418322423102928', v_papa='979279478106524', v_cocina='1492782046029620', v_meta='1570533914202443',
         v_reponer='2616181155474182', v_ciencia='1089803047221823', v_manager='1806890497201184', v_polvo='2674952882955592')
E = dict(cruz='1794007652027945', beis='1111732004707536', botella='1408576487771223', cruz3='1554390252795810', pato350='1736261994559830',
         tenis='2128630834526561', pato6='1104996202058394', alsuper='2356798645128410', heb='2428210091043851', maraton='1395028259081947',
         benavides='1844187423519556', soriana='1453093860257523', patocita='1849260372735718', basquet='2850894288626349', padel='1531191821953342',
         v_sentado='1864427274427457', v_nombres='902795142853541', v_beis='951402061351963', v_campeones='1912404793069353', v_ritual='2718856935175881',
         v_juego='1644664610569228', v_inflable='4672245759672517', v_pumas='1007811685000357')


def _chip(path, caja, alto=104):
    """Logo real de la marca recortado de uno de sus anuncios, en pastilla redondeada."""
    lg = Image.open(path).convert('RGB').crop(caja); lg = lg.resize((int(lg.width * alto / lg.height), alto), Image.LANCZOS)
    m = Image.new('L', lg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, lg.width - 1, lg.height - 1], radius=26, fill=255)
    c = Image.new('RGBA', lg.size, (0, 0, 0, 0)); c.paste(lg, (0, 0), m); return c
CHIP_L = _chip(ad(L['ahorra30']), (36, 232, 548, 362))          # "LIQUID I.V." sobre su azul
CHIP_E = _chip(ad(E['alsuper']), (716, 44, 1046, 186))          # "Electrolit" sobre su azul


def G2(fn, chip=None, y1=1100, k=0.86, y=196):
    """Grafico propio con el logo de UNA de las dos marcas arriba (o ninguno si el dibujo ya la muestra)."""
    usar('grafico:' + fn.__name__); base = _va._puntos(chip)
    def f(tl, T):
        g = fn(tl, T).crop((0, 290, W, y1)); g = g.resize((int(W * k), int((y1 - 290) * k)), Image.LANCZOS)
        im = base.copy(); im.paste(g, ((W - g.width) // 2, y)); return im
    return Grafico(f)


# ------------------------------------------------------------ pantalla dividida de la portada (productos)
def _producto(path, caja, alto):
    im = Image.open(path).convert('RGB'); fondo = Image.fromarray(cubrir(im, W // 2, H)).filter(ImageFilter.GaussianBlur(46))
    p = im.crop(caja); p = p.resize((int(p.width * alto / p.height), alto), Image.LANCZOS)
    m = Image.new('L', p.size, 0); ImageDraw.Draw(m).rounded_rectangle([14, 14, p.width - 15, p.height - 15], radius=40, fill=255); m = m.filter(ImageFilter.GaussianBlur(12))
    fondo.paste(p, ((W // 2 - p.width) // 2, 312), m); return fondo


def _vs():
    c = Image.new('RGB', (W, H)); c.paste(_producto(ad(L['bolsa']), (430, 150, 1830, 2010), 468), (0, 0)); c.paste(_producto(ad(E['botella']), (380, 250, 980, 1520), 468), (W // 2, 0))
    d = ImageDraw.Draw(c); d.rectangle([W // 2 - 3, 0, W // 2 + 2, H], fill=(255, 255, 255))
    d.ellipse([W // 2 - 62, 484, W // 2 + 62, 608], fill=TINTA, outline=(255, 255, 255), width=6); d.text((W // 2, 546), 'VS', font=font(60), fill=(255, 255, 255), anchor='mm')
    return c
VS = _vs()
PORTADA = lambda: lienzo(VS, (0, 0, W), (16, 20, W - 32), nombre='portada')


# ------------------------------------------------------------ graficos propios
def g_617(tl, T):                    # "Electrolit vende mas de 600 millones solo en Estados Unidos" (BevNET: US$617,4 M)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    k = pop(tl, 0.75, 0.2)
    if k > 0:
        c = Image.new('RGBA', (980, 250), (0, 0, 0, 0)); ImageDraw.Draw(c).text((490, 125), 'US$617 M', font=font(196), fill=TINTA + (255,), anchor='mm'); pegar(im, c, 540, 560, lerp(0.86, 1, k))
    if tl > 1.25: txt(d, (540, 745), 'en ventas, solo en Estados Unidos', 54, GRIS, 'SemiBold')
    if tl > 1.7: pegar(im, pastilla('Fuente: BevNET', 40, fondo=(236, 236, 232), color=GRIS, pad=(34, 18)), 540, 850)
    return im


def _icono(dibujo, tam=210):
    c = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, tam - 1, tam - 1], radius=44, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=8); dibujo(d, tam); return c
def _copa(d, t):
    n = TINTA + (255,); d.polygon([(t * .26, t * .26), (t * .74, t * .26), (t * .5, t * .56)], fill=n); d.line([(t * .5, t * .54), (t * .5, t * .76)], fill=n, width=12); d.line([(t * .34, t * .78), (t * .66, t * .78)], fill=n, width=12)
    d.ellipse([t * .60, t * .16, t * .72, t * .28], fill=(250, 255, 0, 255), outline=n, width=5)
def _pesa(d, t):
    n = TINTA + (255,); d.rounded_rectangle([t * .30, t * .46, t * .70, t * .54], radius=6, fill=n)
    for x0, x1 in ((.16, .24), (.26, .34), (.66, .74), (.76, .84)):
        h = .20 if x0 in (.26, .66) else .13; d.rounded_rectangle([t * x0, t * (.5 - h), t * x1, t * (.5 + h)], radius=8, fill=n)
def _avion(d, t):
    n = TINTA + (255,); d.polygon([(t * .18, t * .56), (t * .84, t * .22), (t * .60, t * .82), (t * .50, t * .58)], fill=n); d.line([(t * .50, t * .58), (t * .84, t * .22)], fill=(255, 255, 255, 255), width=7)
def _sol(d, t):
    n = TINTA + (255,); d.ellipse([t * .34, t * .34, t * .66, t * .66], fill=(250, 255, 0, 255), outline=n, width=8)
    for a in range(8):
        ca, sa = math.cos(a * math.pi / 4), math.sin(a * math.pi / 4); d.line([(t * (.5 + .23 * ca), t * (.5 + .23 * sa)), (t * (.5 + .34 * ca), t * (.5 + .34 * sa))], fill=n, width=10)
ICONOS = [(_icono(_copa), 'Fiesta', 0.22), (_icono(_pesa), 'Gym', 1.36), (_icono(_avion), 'Avión', 1.88), (_icono(_sol), 'Calor', 2.62)]


def g_momentos(tl, T):               # "la noche de fiesta, el gym, el avion y el calor": entran con cada palabra
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    txt(d, (540, 400), '4 momentos', 64, GRIS, 'SemiBold')
    for n, (ic, nombre, t0) in enumerate(ICONOS):
        x = 165 + n * 250; k = pop(tl, t0)
        pegar(im, ic, x, 610, lerp(0.8, 1, k) if k > 0 else 0)
        if k > 0.6: txt(d, (x, 775), nombre, 52, TINTA)
    return im


def _tele():
    """Una tele simple con un anuncio real de Electrolit adentro."""
    c = Image.new('RGBA', (900, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, 899, 540], radius=34, fill=TINTA + (255,)); d.rectangle([410, 540, 490, 600], fill=TINTA + (255,)); d.rounded_rectangle([280, 596, 620, 626], radius=14, fill=TINTA + (255,))
    an = Image.open(ad(E['tenis'])).convert('RGB'); p = Image.fromarray(cubrir(an, 848, 488, (0.5, 0.66))); c.paste(p, (26, 26)); return c
TELE = _tele()


def g_tele(tl, T):                   # "usa Meta como si fuera television"
    im = fondo_grafico(); k = pop(tl, 0.1, 0.22); pegar(im, TELE, 540, 640, lerp(0.88, 1, k) if k > 0 else 0); return im


def _tienda(i):
    """De cada promo real: el renglon "DISPONIBLE EN" con el logo de la cadena (sin el precio)."""
    t = Image.open(ad(E[i])).convert('RGB').crop((560, 580, 1060, 800)); c = Image.new('RGBA', (t.width + 16, t.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], radius=30, fill=(255, 255, 255, 255)); m = Image.new('L', t.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, t.width - 1, t.height - 1], radius=24, fill=255)
    c.paste(t, (8, 8), m); return c
TIENDAS = [_tienda(i) for i in ('alsuper', 'heb', 'benavides', 'soriana')]


def g_tiendas(tl, T):                # "que lo compres donde tu prefieras": las cadenas de sus propias promos
    im = fondo_grafico()
    for n, t in enumerate(TIENDAS):
        k = pop(tl, 0.05 + 0.2 * n, 0.16); pegar(im, t, 285 + (n % 2) * 510, 520 + (n // 2) * 262, lerp(0.85, 0.95, k) if k > 0 else 0)
    return im


# ------------------------------------------------------------ capturas
ENT = json.load(open(f'{A}/cap/entmeta.json')); LQ = json.load(open(f'{A}/cap/lqmeta.json'))
LM = json.load(open(f'{A}/cap/l_fbmeta.json')); EM = json.load(open(f'{A}/cap/e_fbmeta.json'))
LG, EG = img(f'{A}/cap/l_fbg0.png'), img(f'{A}/cap/e_fbg0.png')                 # Biblioteca de cada marca, misma vista (2 px por px CSS)
_rl = tuple(v * 2 for v in LM['results'][:4]); _re = tuple(v * 2 for v in EM['results'][:4])
ARMA = img(f'{A}/cap/liqb_0.png')                                               # "Build your subscription" (3 px por px CSS)
SABOR = img(f'{A}/cap/liqb_1.png')                                              # el mismo armador con el paso de sabores abierto
P3 = lambda r: tuple(v * 3 for v in r)
PERKS = img(f'{A}/cap/lq_perks.png')

# ------------------------------------------------------------ tomas
toma('01', 0.00, 1.96, PORTADA(), GAB, T_(['Liquid I.V. vs Electrolit:', '¿quién lo hace mejor?'], 196, 62, t0=-1.0, clave={'vs'}, emo='🤯'))
toma('02', 1.96, 4.64, captura(f'{A}/cap/ent_mil.png', [(ENT['mil'], 1.3, None, 'flecha_ai')], nombre='entrepreneur:1.000 millones'), GAB)
toma('03', 4.64, 7.94, G2(g_617, CHIP_E), GAB)
toma('04', 7.94, 10.50, Mitades(clip(L['v_cocina'], 2.0), clip(E['v_sentado'], 4.0)), GAB)
toma('05', 10.50, 13.06, Serie([(0, clip(L['v_ciencia'], 0.1)),
                                (0.66, lienzo(LG, (0, 0, 1700), (0, 300, 1500), [('caja', _rl, 0.6), ('flecha_ad', _rl, 0.6)], nombre='biblioteca Liquid:cabecera', dur_mov=0.6))]), GAB)
toma('06', 13.06, 15.86, Serie([(0, tarjeta(f'{A}/cap/l_card_1061262113579933.png', [('caja', (341, 488, 97, 38), 0.3)], nombre='tarjeta Liquid:boton Subscribe')),
                                (0.96, anuncio(L['ahorra30'], 0.03, [('sub', (0.08, 0.345, 0.84, 0.05), 0.2)])),
                                (1.90, anuncio(L['suscribe'], 0.03, [('sub', (0.08, 0.30, 0.78, 0.06), 0.25)]))]), GAB)
toma('07', 15.86, 18.34, lienzo(EG, (0, 0, 1700), (0, 300, 1500), [('caja', _re, 1.5), ('flecha_ad', _re, 1.5)], nombre='biblioteca Electrolit:cabecera', dur_mov=0.7), GAB)
toma('08', 18.34, 20.04, tarjeta(f'{A}/cap/e_card_1794007652027945.png', [('caja_p', (334, 444, 98, 36), 0.35), ('flecha_ai', (334, 444, 98, 36), 0.35)], nombre='tarjeta Electrolit:sin boton'), GAB)
toma('09', 20.04, 21.82, Serie([(0, anuncio(E['beis'], 0.03)), (0.90, anuncio(E['basquet'], 0.03))]), GAB)
toma('10', 21.82, 24.22, Serie([(0, anuncio(E['cruz3'], 0.03)), (0.66, clip(E['v_pumas'], 64.6, recorte=(540, 590, 370, 80), entero=-120)), (1.40, anuncio(E['pato350'], 0.04))]), GAB)
toma('11', 24.22, 26.10, clip(L['v_meta'], 3.3), GAB)
_v = lambda y: (210, y, 2250)                                                    # columna del armador + la foto del producto (1,44 px por px CSS)
toma('12', 26.10, 31.70, Serie([
    (0.00, lienzo(ARMA, (0, 0, 2460), _v(0), [('caja', P3((436, 36, 358, 104)), 0.74)], nombre='liquid-iv.com:arma tu suscripcion', dur_mov=0.5)),   # "te arma tu suscripcion"
    (2.22, Lienzo(ARMA, _v(0), _v(465), [('caja', P3((436, 285, 358, 380)), 0.3)], dur_mov=0.25)),                                               # "para que la quieres"
    (3.00, lienzo(SABOR, (0, 2480, 2460), None, [('caja', P3((40, 944, 740, 232)), 0.1)], nombre='liquid-iv.com:sabores')),                       # "el sabor"
    (3.98, Lienzo(ARMA, _v(465), _v(1758), [('caja', P3((436, 684, 358, 428)), 0.28)], dur_mov=0.25)),                                           # "cuantos sobres" ... "te empuja a comprar mas"
]), GAB)
toma('13', 31.70, 36.36, Serie([
    (0.00, captura(f'{A}/cap/lq_perks.png', [(LQ['perks'], 0.5, None, 'flecha_ad')], nombre='liquid-iv.com:beneficios')),                          # "un 30 % menos en cada pedido"
    (2.36, Lienzo(PERKS, (430, 1690, 1530), None, [('sub', P3(LQ['perks_1'][0]), 0.1), ('sub', P3(LQ['perks_2'][0]), 1.4)])),                        # muestras gratis, regalos sorpresa
]), GAB)
toma('14', 36.36, 40.40, Serie([(0, clip(E['v_campeones'], 0.4)), (1.76, clip(E['v_ritual'], 0.2, entero=150))]), GAB)
toma('15', 40.40, 44.98, Serie([(0, clip(E['v_inflable'], 17.2)), (1.88, clip(E['v_nombres'], 6.6)), (2.54, anuncio(E['pato6'], 0.03)), (3.14, G2(g_tiendas, CHIP_E))]), GAB)
toma('16', 44.98, 48.16, PORTADA(), GAB)
toma('17', 48.16, 50.68, clip(L['v_polvo'], 5.6), GAB)
toma('18', 50.68, 52.96, captura(f'{A}/cap/ent_ocas.png', [(ENT['ocas'], 0.9, None, 'flecha_ad')], nombre='entrepreneur:cuatro ocasiones'), GAB)
toma('19', 52.96, 55.84, G2(g_momentos, CHIP_L), GAB)
toma('20', 55.84, 60.42, Serie([(0, clip(L['v_fiestas'], 2.8)), (0.66, clip(L['v_papa'], 1.0)), (1.36, clip(L['v_reponer'], 0.5, entero=150)), (2.02, clip(L['v_manager'], 6.0)),
                                (2.68, captura(f'{A}/cap/ent_micro.png', [(ENT['micro'], 0.2, None, 'flecha_ai')], nombre='entrepreneur:microinfluencers'))]), GAB)
toma('21', 60.42, 62.56, G2(g_tele, CHIP_E, k=0.9), GAB)
toma('22', 62.56, 66.92, Serie([(0, clip(E['v_juego'], 24.0)), (1.44, clip(E['v_beis'], 5.2))]), GAB)
toma('23', 66.92, 70.44, Serie([(0, anuncio(L['amazon1'], 0)), (0.58, anuncio(E['padel'], 0)), (1.16, anuncio(L['variety'], 0)), (1.74, anuncio(E['maraton'], 0)),
                                (2.32, anuncio(L['reco'], 0)), (2.90, anuncio(E['patocita'], 0))]), GAB)
toma('24', 70.44, 74.10, PORTADA(), GAB, T_(['¿Quién lo hace mejor?'], 196, 70, t0=0.25, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {'portada': 'regla 10 de la guia de Gabriel: la pantalla dividida del inicio vuelve en la toma 16 y en el cierre'}

GUION = [
 '¿Quién lo hace mejor?', 'Liquid o *Electrolit?',
 'Liquid dice que ya pasa', 'los mil *millones', 'de dólares en ventas', 'y Electrolit vende', 'más de 600 *millones', 'solo en Estados Unidos',
 'Pero cada una le habla', 'a una persona', 'completamente *distinta',
 'En sus anuncios', 'Liquid tiene unos *200', 'activos en Meta', 'y muchos te empujan', 'a una sola cosa,', 'a *suscribirte',
 'Por el otro lado', 'Electrolit en México', 'tiene unos *80', 'y ninguno te lleva', 'a una *tienda,', 'casi todos muestran', 'a quién *patrocina',
 'A Cruz Azul,', 'a los Pumas', "o al piloto Pato O'Ward ~",
 'Ahora lo más *curioso,', 'mira a dónde te llevan',
 'Mientras Liquid te arma', 'tu *suscripción', 'en pocos pasos,', 'eliges para qué la quieres,', 'el *sabor,', 'cuántos sobres',
 'Y aparte te empuja', 'a comprar más', 'dándote un ~ *30%', 'menos en cada pedido,', 'muestras *gratis', 'de sabores nuevos', 'y regalos *sorpresa',
 'Pero Electrolit hace', 'totalmente lo *contrario,', 'no intenta venderte', 'absolutamente nada por *internet',
 'Lo que busca es que lo veas', 'en todas *partes,', 'en tu equipo, en las carreras', 'y que lo compres donde tú *prefieras',
 'Pero si analizamos', 'detalladamente,', 'ninguno de los dos', 'vende lo que *crees',
 'Liquid no le vende', 'a gente que simplemente', 'quiere *hidratarse',
 'Su CEO cuenta que', 'encontraron cuatro *momentos', 'La noche de *fiesta,', 'el gym, el avión', 'y el *calor',
 'Y con eso arrancaron', 'a crear contenido', 'con un ejército', 'de ~ *microinfluencers', 'que eran clientes *reales',
 '~ ~ ~ Electrolit usa Meta', 'como si fuera *televisión',
 'No paga para que', 'le des *clic,', 'paga para que lo veas', 'en algo con lo que', 'te sientes *identificado',
 'Y por esta razón,', 'por más que vendan', 'lo mismo,', 'no compiten en *precio',
 '¿Y tú? ¿Quién crees que', 'lo hace *mejor?', '¿Liquid o Electrolit?', 'Te leo en los *comentarios',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal35.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
