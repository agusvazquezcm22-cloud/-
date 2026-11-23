"""Video 39 · "¿Compras el producto o el marketing?" · v01
Formato pantalla verde, video de veredictos: cinco marcas (Bio.me, Grüns, Create, Blueprint, Goli), un juicio para cada una
(guia de Gabriel, VIDEO 39) + todo lo que Gabriel y Agus fueron corrigiendo en los videos anteriores:
- Gabriel fijo abajo al centro en todas las tomas (layout C).
- Portada grande y llamativa (cuadricula con los cinco productos), sin hueco; la portada NO vuelve a mitad ni al final
  (la guia pedia repetir la cuadricula en las tomas 25 y 29: en su lugar van los veredictos en fila y un cierre con personas
  tomando / comiendo los productos, como pidio Gabriel).
- Video antes que imagen fija; nunca dos capturas iguales seguidas.
- Marcas rojas SOLO sobre rectangulos medidos (pagina_entera.js FRASES, frase.js) o medidos por pixeles (columna de dosis),
  y revisadas con revisar_marcas.py. En los videos de anuncios no va marca (no hay como medir el texto del video).
- Veredicto de cada marca: su logo + "MARKETING" / "PRODUCTO", mismo tamano y color para las cinco. Nada deja mal a una marca.
Lo que no se muestra (regla 12 de la guia): promesas de salud (bajar de peso, grasa, detox, hinchazon, glucosa), el
"Reduces body fat" de Bio.me, plumas o cajas de Ozempic, antes y despues, notas negativas de Create. Por eso las paginas de
producto de Bio.me van como panel (titulo + precio, sin la lista de beneficios) y la ficha de Blueprint solo con nombre y dosis.
Tiempos de la transcripcion del crudo (84,53 s).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from verde_ayudas import *
import verde_ayudas as _va

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v39')
RAW = f'{A}/dl/crudo39.mp4'
DUR = 85.43                  # 84,53 del crudo + 0,9 de cola
CABEZA = 735                 # fila del crudo donde esta el tope de su cabeza (medido: 624-746)
AUDIO_FILTRO = 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'
GAB = 'C'
configurar(A, logo=None)
GRIS = (120, 120, 118)

# ------------------------------------------------------------ logos y veredictos
LG = {n: Image.open(f'{A}/logos/{n}_t.png').convert('RGBA') for n in ('bio', 'gruns', 'create', 'blueprint', 'goli')}
FONDO_LG = {'gruns': (44, 112, 62)}                      # el logo de Grüns es blanco: va sobre su verde


def chip_logo(n, w=440, h=150, alto=86):
    """Logo de la marca en una tarjeta del mismo tamano para las cinco."""
    lg = LG[n]; k = min(alto / lg.height, (w - 80) / lg.width); lg = lg.resize((int(lg.width * k), int(lg.height * k)), Image.LANCZOS)
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=FONDO_LG.get(n, (255, 255, 255)) + (255,), outline=(226, 226, 222, 255), width=3)
    c.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2)); return c


def chip_veredicto(palabra, w=440, h=110, tam=66):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=TINTA + (255,))
    d.text((w / 2, h / 2), palabra, font=font(tam), fill=(255, 255, 255, 255), anchor='mm'); return c
VMK, VPR = chip_veredicto('MARKETING'), chip_veredicto('PRODUCTO')
CH = {n: chip_logo(n) for n in LG}


def VER(n, palabra, t_logo, t_pal, cy=290):
    """Al decir el nombre: su logo arriba; al decir el veredicto, debajo, MARKETING o PRODUCTO (igual para las cinco)."""
    ch, vd = CH[n], (VMK if palabra == 'MARKETING' else VPR)
    def f(pil, tl, T):
        if tl >= t_logo: pegar(pil, ch, 540, cy, lerp(0.86, 1, pop(tl, t_logo)))
        if tl >= t_pal: pegar(pil, vd, 540, cy + 142, lerp(0.86, 1, pop(tl, t_pal)))
    f.caja_titulo = (540 - 220, cy - 75, 540 + 220, cy + 142 + 55)
    return f


# ------------------------------------------------------------ portada: los cinco productos en cuadricula
def _tile(src, caja, w=340, h=425, fondo=(255, 255, 255)):
    im = Image.open(src).convert('RGB').crop(caja); t = Image.fromarray(cubrir(im, w, h))
    c = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w + 11, h + 11], radius=34, fill=(255, 255, 255, 255), outline=(222, 222, 218, 255), width=3)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=255)
    c.paste(t, (6, 6), m); return c
PRODUCTOS = dict(
    bio=(f'{A}/cap/bio_shop.png', (120, 1600, 720, 2400)),                 # Daily Prebiotic Fiber (tienda de bio.me)
    gruns=(f'{A}/cap/gruns_prod.png', (80, 300, 1080, 1540)),              # bolsa de Grüns (sin el panel de beneficios)
    create=(f'{A}/cap/create_prod.png', (32, 224, 540, 744)),              # Creatine Monohydrate Gummies
    blueprint=(f'{A}/bp/Blood_Orange_3_pack.webp', (240, 200, 960, 1100)),  # Longevity Mix
    goli=(f'{A}/cap/goli_ancho.png', (1900, 420, 2880, 1645)),             # frasco de ACV (goli.com)
)


def _portada():
    c = fondo_grafico(); orden = ['bio', 'gruns', 'create', 'blueprint', 'goli']
    pos = [(184, 500), (540, 500), (896, 500), (184, 955), (896, 955)]
    for n, (cx, cy) in zip(orden, pos):
        t = _tile(*PRODUCTOS[n]); c.paste(t, (cx - t.width // 2, cy - t.height // 2), t)
        ch = CH[n].resize((220, 75), Image.LANCZOS); c.paste(ch, (cx - 110, cy + 178), ch)
    return c
PORT = _portada()


# ------------------------------------------------------------ graficos propios (contenido entre y 180 y 730: abajo van subtitulos y Gabriel)
def _texto(s, tam, col=TINTA, peso='ExtraBold'):
    f = font(tam, peso); w = int(f.getlength(s)) + 30; c = Image.new('RGBA', (w, int(tam * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((w / 2, c.height / 2), s, font=f, fill=col + (255,), anchor='mm'); return c


def _caja(lineas, w=300, h=150, col=(255, 255, 255), tam=46, tinta=TINTA):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=col + (255,), outline=TINTA + (255,), width=6)
    lh = tam * 1.12; y0 = h / 2 - lh * (len(lineas) - 1) / 2
    for i, s in enumerate(lineas): d.text((w / 2, y0 + i * lh), s, font=font(tam), fill=tinta + (255,), anchor='mm')
    return c


def g_logos(tl, T):                  # "Lo vemos con 5 marcas de suplementos": rafaga de logos
    im = fondo_grafico(); orden = ['bio', 'gruns', 'create', 'blueprint', 'goli']
    n = min(4, int(tl / (T / 5))); ch = CH[orden[n]].resize((660, 225), Image.LANCZOS)
    pegar(im, ch, 540, 440, 1.0); return im


def g_fibra(tl, T):                  # "Casi todos parten de la fibra; lo que cambia es para quien esta hecha la etiqueta"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    k = pop(tl, 0.05)
    if k > 0:
        r = 125 * lerp(0.85, 1, k); d.ellipse([540 - r, 330 - r, 540 + r, 330 + r], fill=VERDE_OSC, outline=TINTA, width=7)
        d.text((540, 330), 'Fibra', font=font(64), fill=(255, 255, 255), anchor='mm')
    for i, (s, x, t0) in enumerate((('Niños', 190, 1.05), ('GLP-1', 540, 1.35), ('Electrolitos', 890, 1.65))):
        p = ease((tl - t0) / 0.2)
        if p <= 0: continue
        a = (540 + (x - 540) * 0.32, 452); b = (x, 560)
        flecha_recta(d, a, b, p)
        if p > 0.6: pegar(im, _caja([s], 300 if i == 2 else 240, 104, tam=44), x, 632, pop(tl, t0 + 0.12))
    return im


UNI = _texto('Unilever', 130)


def g_unilever(tl, T):               # "Pero por algo Unilever termino comprandola" (Beauty Independent no se puede capturar)
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, UNI, 540, 300, pop(tl, 0.45))
    p = ease((tl - 0.62) / 0.22); w = UNI.width - 60
    if p > 0: d.line([(540 - w / 2, 384), (540 - w / 2 + w * p, 384)], fill=ROJO, width=12)       # subrayado sobre "Unilever"
    if tl > 1.0: flecha_recta(d, (540, 420), (540, 490), ease((tl - 1.0) / 0.18))
    if tl > 1.1: pegar(im, CH['gruns'], 540, 580, lerp(0.86, 1, pop(tl, 1.1)))
    if tl > 1.44: pegar(im, pastilla('compró Grüns', 50, fondo=VERDE_OSC), 830, 470, pop(tl, 1.44))
    if tl > 0.45: pegar(im, pastilla('Fuente: Beauty Independent', 34, fondo=(236, 236, 232), color=GRIS, pad=(30, 16)), 540, 705)
    return im


def g_creatina(tl, T):               # "lo nuevo no es la creatina: es como se ve y quien te la muestra"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    pegar(im, _caja(['Creatina'], 360, 120, (236, 236, 232), 54, GRIS), 540, 270, pop(tl, 0.1))
    if tl > 0.74: pegar(im, _texto('+', 90, GRIS), 540, 382, pop(tl, 0.74))
    if tl > 1.22: pegar(im, _caja(['Cómo se ve'], 520, 116, ROJO, 56, (255, 255, 255)), 540, 490, lerp(0.86, 1, pop(tl, 1.22)))
    if tl > 1.92: pegar(im, _caja(['Quién te la muestra'], 640, 116, ROJO, 56, (255, 255, 255)), 540, 640, lerp(0.86, 1, pop(tl, 1.92)))
    return im


def _cara():
    im = Image.open(f'{A}/bp/Blueprint_Bryan_1_2.jpg').convert('RGB').crop((330, 5, 520, 195)).resize((280, 280), Image.LANCZOS)
    m = Image.new('L', (280, 280), 0); ImageDraw.Draw(m).ellipse([0, 0, 279, 279], fill=255)
    c = Image.new('RGBA', (292, 292), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse([0, 0, 291, 291], fill=TINTA + (255,)); c.paste(im, (6, 6), m); return c


def _certificado():
    c = Image.new('RGBA', (240, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, 239, 299], radius=20, fill=(255, 255, 255, 255), outline=TINTA + (255,), width=6)
    for i in range(5): d.rounded_rectangle([34, 46 + i * 34, 206 - (40 if i % 2 else 0), 58 + i * 34], radius=6, fill=(205, 205, 200, 255))
    d.ellipse([140, 200, 214, 274], fill=VERDE_OSC + (255,))
    d.line([(158, 238), (172, 252), (198, 222)], fill=(255, 255, 255, 255), width=8, joint='curve'); return c
CARA, CERT = _cara(), _certificado()


def g_mirar_confiar(tl, T):          # "Bryan te lleva mucha gente, pero son los datos lo que te hacen confiar"
    im = fondo_grafico()
    pegar(im, CARA, 290, 360, pop(tl, 0.05)); pegar(im, pastilla('Te hace mirar', 46, fondo=TINTA), 290, 600, pop(tl, 0.3))
    if tl > 1.38: pegar(im, CERT, 790, 360, pop(tl, 1.38))
    if tl > 2.5: pegar(im, pastilla('Te hace confiar', 46, fondo=VERDE_OSC), 790, 600, pop(tl, 2.5))
    return im


def g_400(tl, T):                    # "segun estimaciones llegaron a mas de 400 millones de dolares en un solo ano"
    im = fondo_grafico()
    pegar(im, CH['goli'], 540, 250, pop(tl, 0.05))
    if tl > 1.56: pegar(im, _texto('+US$400 M', 150, VERDE_OSC), 540, 430, lerp(0.86, 1, pop(tl, 1.56)))
    if tl > 3.38: pegar(im, _texto('en un año (estimado)', 58), 540, 565, pop(tl, 3.38))
    if tl > 0.3: pegar(im, pastilla('Fuente: Fast Company', 34, fondo=(236, 236, 232), color=GRIS, pad=(30, 16)), 540, 680)
    return im


def g_veredictos(tl, T):             # "Aqui tienes el patron del que casi nadie habla": los cinco veredictos en fila (no es la portada)
    im = fondo_grafico()
    for i, (n, v) in enumerate((('bio', VMK), ('gruns', VPR), ('create', VMK), ('blueprint', VPR), ('goli', VMK))):
        t0 = 0.05 + i * 0.3; y = 200 + i * 112
        if tl < t0: continue
        k = pop(tl, t0); pegar(im, CH[n].resize((300, 102), Image.LANCZOS), 360, y, k); pegar(im, v.resize((330, 82), Image.LANCZOS), 720, y, k)
    return im


def g_patron(tl, T):                 # "mientras mas atado esta el estilo de vida ... marketing ... compres / mas problemas resuelve ... producto ... decision"
    im = fondo_grafico(); d = ImageDraw.Draw(im)
    filas = [(260, [(['Estilo', 'de vida'], 1.16), (['Marketing'], 3.00), (['La compra'], 3.86)], ['bio', 'create', 'goli'], 3.0, (250, 236, 200)),
             (540, [(['Resuelve', 'problemas'], 5.00), (['Producto'], 6.48), (['Decisión'], 7.60)], ['gruns', 'blueprint'], 6.48, (212, 240, 224))]
    for y, cajas, logos, tl_logos, col in filas:
        for i, (s, t0) in enumerate(cajas):
            if tl < t0: continue
            x = 190 + i * 350
            if i > 0: flecha_recta(d, (x - 350 + 150, y), (x - 160, y), ease((tl - t0) / 0.18))
            pegar(im, _caja(s, 290, 140, col if i == 1 else (255, 255, 255), 44), x, y, lerp(0.86, 1, pop(tl, t0)))
        if tl >= tl_logos:
            for j, n in enumerate(logos):
                x = 540 + (j - (len(logos) - 1) / 2) * 230; pegar(im, CH[n].resize((200, 68), Image.LANCZOS), x, y + 122, pop(tl, tl_logos + j * 0.1))
    return im


# ------------------------------------------------------------ capturas (2 px por px CSS; prensa: 3 px por px CSS)
P2 = lambda r, k=2: tuple(v * k for v in r)
def _une(*rs):
    x0 = min(r[0] for r in rs); y0 = min(r[1] for r in rs); x1 = max(r[0] + r[2] for r in rs); y1 = max(r[1] + r[3] for r in rs)
    return (x0, y0, x1 - x0, y1 - y0)
J = lambda n: json.load(open(f'{A}/cap/{n}.json'))
BH = img(f'{A}/cap/bio_home2.png')
# "fiber supplements" MEDIDO por pixeles en bio_home2.png (palabras en x 783-858 y 872-1095, filas 947-983): el json de esa captura
# quedo 32 px CSS mas abajo (la pagina movio el texto despues de medir), revisar_marcas.py lo mostro sobre "wellness".
F_FIBER = (783, 945, 313, 40)
BS = img(f'{A}/cap/bio_shop.png')
GH, GHJ = img(f'{A}/cap/gruns_home.png'), J('gruns_home')
GP, GPJ = img(f'{A}/cap/gruns_prod.png'), J('gruns_prod')
CP, CPJ = img(f'{A}/cap/create_prod.png'), J('create_prod')
CHM = img(f'{A}/cap/create_home.png')
COA, COAJ = img(f'{A}/cap/bp_coas.png'), J('bp_coas')
BPH = img(f'{A}/cap/bp_home.png')


def _bp_hero():
    """Foto principal de blueprint.bryanjohnson.com (bolsas + bebida), a todo el ancho sobre su version desenfocada.
    Solo la foto: debajo la pagina tiene pestanas con beneficios ("Energy & Stress Support")."""
    h = Image.fromarray(BPH).crop((820, 228, 1610, 620)); k = W / h.width; h = h.resize((W, int(h.height * k)), Image.LANCZOS)
    c = Image.fromarray(cubrir(h)).filter(ImageFilter.GaussianBlur(40)); c.paste(h, (0, 200)); return c
NAD, NADJ = img(f'{A}/cap/nad_titulo.png'), J('nadmeta')
NUT, NUTJ = img(f'{A}/cap/nut_titulo.png'), J('nutmeta')
OY = 300


def _panel_bio(n):
    """Pagina de producto de Bio.me como panel: foto + titulo + precio. Se tapa (blanco) la columna derecha debajo del precio,
    donde estan las promesas de salud (regla 12)."""
    im = Image.open(f'{A}/cap/{n}.png').convert('RGB').crop((0, 0, 1640, 1000)); ImageDraw.Draw(im).rectangle([824, 520, 1640, 1000], fill=(255, 255, 255))
    c = Image.new('RGB', (1640, 2916), (255, 255, 255)); c.paste(im, (0, OY)); return np.asarray(c)
enP = lambda r: (r[0] * 2, r[1] * 2 + OY, r[2] * 2, r[3] * 2)                       # rect CSS de la pagina -> panel
KIDS, GLP, LEM = _panel_bio('bio_kids2'), _panel_bio('bio_glp2'), _panel_bio('bio_lem2')
F_KIDS = enP(J('bio_kids2')['frases']['Kids Daily Prebiotic Fiber'][0])
F_GLP = enP(J('bio_glp2')['frases']['GLP-1 Support'][0])
F_LEM = enP(_une(*J('bio_lem2')['frases']['Daily Prebiotic Fiber Lemonade']))
F_ELEC = enP(J('bio_lem2')['frases']['Prebiotic and Electrolytes'][0])


def _ficha_bp():
    """Ficha de Blueprint (Longevity Mix): solo la columna de nombres y la de dosis (sin la del medio, que trae beneficios)."""
    b = Image.open(f'{A}/bp/BloodOrange_6.webp').convert('RGB')
    izq = b.crop((79, 120, 345, 900)); der = b.crop((815, 120, 925, 900))
    c = Image.new('RGB', (420, 830), (255, 255, 255)); c.paste(izq, (14, 30)); c.paste(der, (296, 30))
    k = 2.4; c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    lona = Image.new('RGB', (1640, 2916), (250, 250, 248)); lona.paste(c, ((1640 - c.width) // 2, 140))
    # columna de dosis MEDIDA por pixeles en BloodOrange_6.webp: x 842-902; filas 204-216, 262-274, ... 492-504 (las 6 primeras dosis;
    # la columna entera bajaba hasta la franja de subtitulos) -> en la lona
    x0 = (1640 - c.width) // 2 + (296 + 842 - 815) * k; y0 = 140 + (30 + 204 - 120) * k
    return np.asarray(lona), (x0, y0, 60 * k, (504 - 204) * k)
FICHA, F_DOSIS = _ficha_bp()


def _goli_frasco():
    """Frasco de ACV de Goli (goli.com) entero sobre su rojo, para pantalla completa."""
    b = Image.open(f'{A}/cap/goli_ancho.png').convert('RGB'); col = b.getpixel((1700, 1000))
    j = b.crop((1560, 300, 2880, 1760)); k = 1080 / j.width; j = j.resize((1080, int(j.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), col); c.paste(j, (0, 360)); return c
GOLI_F6 = Image.open(f'{A}/cap/goli_f6.png').convert('RGB')                          # cuadro del anuncio 1436992817881401 (s6)

# ------------------------------------------------------------ tomas
toma('01', 0.00, 1.92, lienzo(PORT, (0, 0, W), (16, 20, W - 32), nombre='portada'), GAB,
     T_(['¿Producto o marketing?'], 180, 74, t0=-1.0, clave={'Producto', 'marketing'}, emo='🤔'))
toma('02', 1.92, 3.60, Grafico(g_logos), GAB)
S[-1]['fuentes'] = ['logos de bio.me, gruns.co, trycreate.co, blueprint.bryanjohnson.com, goli.com']
toma('03', 3.60, 5.88, lienzo(np.asarray(Image.fromarray(cubrir(GOLI_F6)).filter(ImageFilter.GaussianBlur(28))), (0, 0, W), (30, 50, W - 60),
                              nombre='anuncio:1436992817881401 desenfocado'), GAB, T_(['La última…'], 300, 80, t0=0.1))
toma('04', 5.88, 8.60, lienzo(BH, (0, 0, 1640), (60, 40, 1520), nombre='bio.me:inicio'), GAB, VER('bio', 'MARKETING', 0.74, 1.70))
toma('05', 8.60, 10.92, lienzo(BH, (0, 300, 1640), (440, 595, 1000), [('caja', F_FIBER, 0.62)],
                               nombre='bio.me:fiber supplements', dur_mov=0.5), GAB)
toma('06', 10.92, 13.48, lienzo(BS, (0, 1150, 1640), (0, 2250, 1640), nombre='bio.me:tienda'), GAB)
toma('07', 13.48, 17.44, Serie([
    (0.00, lienzo(KIDS, (0, 180, 1640), None, [('caja', F_KIDS, 0.05)], nombre='bio.me:kids')),                       # "uno para ninos"
    (0.78, lienzo(GLP, (0, 180, 1640), None, [('caja', F_GLP, 0.05)], nombre='bio.me:glp-1 support')),               # "otro para quienes usan medicamentos..."
    (2.80, lienzo(LEM, (0, 180, 1640), None, [('caja', F_LEM, 0.05, 0.62), ('sub', F_ELEC, 0.66)], nombre='bio.me:lemonade')),   # "y otros con electrolitos"
]), GAB)
toma('08', 17.44, 20.64, Grafico(g_fibra), GAB)
toma('09', 20.64, 22.92, clip('1634957604749546', 1.0, nombre='anuncio-video:1634957604749546 (bolsas de Grüns)'), GAB, VER('gruns', 'PRODUCTO', 0.56, 1.98))
toma('10', 22.92, 25.10, lienzo(GH, (0, 1500, 1640), (306, 1672, 1000), [
    ('caja', P2(_une(*GHJ['frases']['Including whole fruits and veggies'])), 0.84, 1.38),
    ('caja', P2(_une(*GHJ['frases']['Vitamins & Minerals'])), 1.38, 1.92),
    ('caja', P2(GHJ['frases']['of Fiber'][0]), 1.92)], nombre='gruns.co:60 ingredientes', dur_mov=0.5), GAB)
toma('11', 25.10, 27.54, clip('1628525708786841', 9.6, nombre='anuncio-video:1628525708786841 (comiendo Grüns)'), GAB)
toma('12', 27.54, 30.72, lienzo(GP, (0, 3250, 1300), (0, 3405, 1000), [
    ('caja', P2(_une(GPJ['frases']['Subscribe & Save'][0], GPJ['frases']['28 packs each 4 weeks'][0])), 2.36), ('flecha_ad', P2(_une(GPJ['frases']['Subscribe & Save'][0], GPJ['frases']['28 packs each 4 weeks'][0])), 2.36)],
    nombre='gruns.co:suscripcion', dur_mov=0.6), GAB)
toma('13', 30.72, 32.64, Grafico(g_unilever), GAB)
toma('14', 32.64, 34.76, clip('c4', 0.5, nombre='trycreate.co:video c4'), GAB, VER('create', 'MARKETING', 0.72, 1.80))
toma('15', 34.76, 38.40, Serie([
    (0.00, lienzo(CP, (0, 300, 1640), None, [('caja', P2(CPJ['frases']['Creatine Monohydrate Gummies'][0]), 0.62)], nombre='trycreate.co:gomitas')),   # "creatina en gomitas"
    (1.22, lienzo(CHM, (0, 700, 1640), (60, 760, 1520), nombre='trycreate.co:colores')),                                                     # "y de colores"
    (1.88, clip('c3', 0.5, nombre='trycreate.co:video c3')), (2.44, clip('c10', 1.0, nombre='trycreate.co:video c10')),                      # "y con creadores..."
    (3.00, clip('c14', 1.0, nombre='trycreate.co:video c14')),
]), GAB)
toma('16', 38.40, 40.20, clip('c16', 0.3, nombre='trycreate.co:video c16'), GAB)
toma('17', 40.20, 42.78, Grafico(g_creatina), GAB)
toma('18', 42.78, 45.72, clip('2735339296860660', 1.2, nombre='anuncio-video:2735339296860660 (Bryan)'), GAB, VER('blueprint', 'PRODUCTO', 0.64, 2.64))
toma('19', 45.72, 48.16, Serie([
    (0.00, clip('1164776219427548', 0.2, nombre='anuncio-video:1164776219427548')),
    (0.80, clip('1465665538843736', 0.3, nombre='anuncio-video:1465665538843736')),
    (1.60, clip('1482981607056502', 4.0, nombre='anuncio-video:1482981607056502 ("Bryan Johnson is saying")')),
]), GAB)
toma('20', 48.16, 51.38, Serie([
    (0.00, lienzo(FICHA, (0, 40, 1720), (0, 100, 1640), [('caja', F_DOSIS, 0.50)], nombre='blueprint:ficha longevity mix (nombres y dosis)')),   # "dosis exactas"
    (1.28, lienzo(COA, (300, 1150, 1000), None, [('caja', P2(COAJ['frases']['CERTIFICATES OF ANALYSIS'][0]), 0.05), ('flecha_ad', P2(COAJ['frases']['CERTIFICATES OF ANALYSIS'][0]), 0.05)],
                  nombre='blueprint:certificados')),                                                                                             # "y certificados"
    (2.00, Lienzo(COA, (300, 1150, 1000), (0, 1519, 1350), [('caja', P2(COAJ['frases']['3rd Party Tested'][0]), 0.10, 0.74),
                                                             ('caja', P2(_une(*COAJ['frases']['Download Full Report'])), 0.74)], dur_mov=0.3)),   # "con laboratorios publicados"
]), GAB)
toma('21', 51.38, 54.20, Grafico(g_mirar_confiar), GAB)
S[-1]['fuentes'] = ['foto de Bryan Johnson de blueprint.bryanjohnson.com']
toma('22', 54.20, 55.88, clip('1436992817881401', 6.0, nombre='anuncio-video:1436992817881401 (nitido)'), GAB, VER('goli', 'MARKETING', 0.60, 1.36))
toma('23', 55.88, 58.02, Serie([
    (0.00, lienzo(_goli_frasco(), (0, 0, W), (40, 70, W - 80), nombre='goli.com:frasco acv')),
    (0.70, clip('1790366458882820', 1.0, nombre='anuncio-video:1790366458882820')),
    (1.40, clip('2509446156197561', 15.0, nombre='anuncio-video:2509446156197561')),
]), GAB)
toma('24', 58.02, 62.02, Grafico(g_400), GAB)
toma('25', 62.02, 63.80, lienzo(NAD, (270, 0, 2100), (300, 30, 2040), [('sub', P2(NADJ['titulo'][0], 3), 0.38), ('sub', P2(NADJ['titulo'][1], 3), 0.38)],
                                nombre='bbbprograms.org:fallo de NAD'), GAB)
toma('26', 63.80, 67.82, lienzo(NUT, (0, 1040, 1000), (0, 1100, 980), [('sub', P2(NUTJ['acq'][0], 3), 1.48)], nombre='nutraingredients-usa.com:goli acquired'), GAB)
toma('27', 67.82, 69.96, Grafico(g_veredictos), GAB)
toma('28', 69.96, 77.92, Grafico(g_patron), GAB)
toma('29', 77.92, 80.76, Serie([
    (0.00, lienzo(LEM, (0, 200, 1100), None, nombre='bio.me:bolsa lemonade')),
    (0.57, clip('1118292457497837', 1.0, nombre='anuncio-video:1118292457497837')),
    (1.14, clip('c8', 1.0, nombre='trycreate.co:video c8')),
    (1.71, lienzo(_bp_hero(), (0, 0, W), (20, 36, W - 40), nombre='blueprint:longevity mix (inicio)')),                # (el anuncio del senor decia "mental energy": promesa de salud)
    (2.28, clip('1001099186032292', 2.0, nombre='anuncio-video:1001099186032292')),
]), GAB)
toma('30', 80.76, 85.43, Serie([
    (0.00, clip('2735339296860660', 15.5, nombre='anuncio-video:2735339296860660 (s15: tomando el Longevity Mix)')),
    (2.34, clip('1893971481604723', 44.0, nombre='anuncio-video:1893971481604723 (comiendo Grüns)')),
]), GAB, T_(['¿Producto o marketing?'], 180, 74, t0=2.0, clave={'Producto', 'marketing'}, emo='👇'))
SHOTS = S
REPETICION_PERMITIDA = {}

GUION = [
 '¿Estás comprando el *marketing', 'o el *producto?',
 'Lo vemos con 5 marcas', 'de *suplementos', 'y la última tuvo que', 'cambiar de *dueño', 'para no *quebrar',
 'Empecemos con *Bio.me,', 'compras el *marketing', 'pero del *bueno',
 'Lo que vende es *fibra,', 'pero en vez de tener', 'un solo *producto', 'saca uno para cada cosa', 'que la gente está buscando *hoy',
 'Uno para *niños,', 'otro para quienes usan', 'medicamentos como ~ *Ozempic', 'y otros con *electrolitos',
 'Casi todos parten de la *fibra,', 'lo que cambia es para quién', 'está hecha la *etiqueta',
 'Sigamos con *Grüns,', 'aquí compras el *producto',
 'Son gomitas con *vegetales,', 'vitaminas y *fibra', 'para la gente que no', 'se quiere tomar el batido *verde', 'todos los *días',
 'Y su negocio no es sostenible', 'con solo la primera *compra,', 'vive de que *vuelvas',
 'Pero por algo *Unilever', 'terminó *comprándola',
 'Ahora pasamos con *Create,', 'le compras el *marketing',
 'Creatina en *gomitas', 'y de *colores', 'y con *creadores', 'de contenido por todas partes',
 'Se ve muy *divertida', 'y fácil de *tomar,', 'pero lo nuevo', 'no es la *creatina,', 'es cómo se *ve', 'y quiénes te lo *muestran',
 'Ahora vamos con *Blueprint,', 'aunque no lo creas,', 'compras el *producto',
 'Yo sé que casi todos', 'sus anuncios arrancan', 'con Bryan *Johnson,', 'pero detrás hay dosis *exactas', 'y certificados con', 'laboratorios *publicados',
 'Bryan te lleva mucha *gente,', 'pero son los datos', 'lo que te hacen *confiar',
 'Continuamos con *Goli,', 'compras el *marketing',
 'Sus gomitas de vinagre de *manzana', 'se hicieron *virales', 'y según estimaciones', 'llegaron a más de', '400 millones de *dólares', 'en un solo *año',
 'Pero sus promesas', 'terminaron en *demandas', 'y en 2024 terminó *vendida', 'a un grupo de *inversionistas', 'para evitar la *quiebra',
 'Aquí tienes el *patrón', 'del que casi nadie *habla',
 'Mientras más atado está', 'el estilo de *vida', 'a una marca,', 'más pesa el *marketing', 'para que la *compres',
 'Pero mientras más problemas *resuelve,', 'más pesa el *producto', 'para que tomes la *decisión',
 'Así que cuando revises los *anuncios,', 'hazte una sola *pregunta',
 '¿Me están comprando', 'por lo que hace mi *producto', 'o por el *marketing', 'que lo *rodea?',
]
SUBS = armar_tarjetas(json.load(open(f'{A}/pal39.json')), GUION, dur=DUR, min_tarjeta=0.7, min_clave=0.8)
