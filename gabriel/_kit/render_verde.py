"""Motor del formato "pantalla verde" de Gabriel (referencia: Chase Chappell).

Gabriel recortado del verde, pegado abajo, sobre imagen/video/grafico a pantalla
completa. Corte seco, marcas rojas, sin subtitulos propios.

Uso:  python3 render_verde.py <config.py> [--prev t1,t2,... [--cols 4 --ancho 540]] [--out archivo.mp4]
El config define RAW, DUR y SHOTS (ver gabriel/32/gabriel32_v01.py).
"""
import subprocess, sys, math, os, importlib.util
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
ROJO = (227, 38, 46)
VERDE = (77, 203, 132)          # color de palabra clave aprobado por Gabriel
TINTA = (17, 17, 20)
FD = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
_fc = {}


def font(sz, peso='ExtraBold'):
    k = (sz, peso)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD % peso, sz)
    return _fc[k]


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def lerp(a, b, x):
    return a + (b - a) * x


# ---------------------------------------------------------------- Gabriel
Y0 = 470          # fila del crudo donde empieza el recorte (arriba solo hay verde)
CABEZA = 600      # fila del crudo donde esta el tope de la cabeza

# nombre: (escala, x izquierda, y pantalla del tope de la cabeza, lado interno a difuminar)
LAYOUT = {
    'G':  (1.00, 0, 985, None),       # grande, media pantalla
    'ML': (0.76, 0, 1150, 'r'),       # medio, izquierda
    'MR': (0.76, W - int(W * 0.76), 1150, 'l'),
    'PL': (0.50, 0, 1400, 'r'),       # pequeno, esquina izquierda
    'PR': (0.50, W - W // 2, 1400, 'l'),
    'C':  (0.74, (W - int(W * 0.74)) // 2, 1300, 'ambos'),   # mas grande, abajo al centro (cierre y momentos puntuales)
    'CI': (0.74, None, 1300, 'ambos'),  # mismo tamano que C, corrido a la izquierda (Gabriel 2026-11-23: "tengo que ir moviendome
    'CD': (0.74, None, 1300, 'ambos'),  # por la pantalla, en algunas tomas a la derecha, en otras a la izquierda, en otras en el medio")
    'R':  (0.60, None, 1200, 'r'),    # EL FIJO (referencia de Agus, reel de Chase Chappell): abajo a la izquierda, tope de la cabeza
}                                     # al 62 % del alto y centro de la cabeza al 25 % del ancho, en todo el video
CX = {'R': 270, 'CI': 290, 'CD': 790}                       # lugares que se ubican por el centro de la cabeza (px de pantalla)
CENTRO = 540                          # columna del crudo donde esta el centro de la cabeza (el config puede pisarla)


def recortar(fr):
    """fr: cuadro crudo RGB uint8 -> (rgb sin derrame verde, alfa float32)."""
    f = fr[Y0:].astype(np.int16)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(r, b)
    ex = (g - mx).astype(np.float32)
    a = 1.0 - np.clip((ex - 16.0) / 44.0, 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 1.1)
    a = np.clip((a - 0.42) / 0.50, 0, 1)
    g2 = np.minimum(g, mx + 4)
    out = np.stack([r, g2, b], -1).astype(np.uint8)
    return out, a


def poner_gabriel(dst, fr, lay):
    s, x0, ytop, lado = LAYOUT[lay]
    rgb, a = recortar(fr)
    if s != 1.0:
        nw, nh = int(W * s), int(round(rgb.shape[0] * s))
        rgb = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
        a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)
    nh, nw = a.shape
    if lado:
        ramp = np.clip(np.arange(nw, dtype=np.float32) / 46.0, 0, 1)
        if lado == 'r':
            ramp = ramp[::-1]
        elif lado == 'ambos':
            ramp = np.minimum(ramp, ramp[::-1])
        a = a * ramp[None, :]
    if x0 is None: x0 = int(round(CX[lay] - CENTRO * s))
    y = max(ytop - int(round((CABEZA - Y0) * s)), H - nh)      # nunca queda un hueco entre su cuerpo y el borde de abajo
    h = min(nh, H - y)
    c0 = max(0, -x0); c1 = min(nw, W - x0)                     # lo que cae fuera de la pantalla se descarta
    rgb, a = rgb[:h, c0:c1], a[:h, c0:c1]; x0 += c0; nw = c1 - c0
    # sombra suave para despegarlo de fondos claros
    sh = cv2.GaussianBlur(a, (0, 0), 14) * 0.38
    reg = dst[y:y + h, x0:x0 + nw].astype(np.float32)
    reg *= (1 - sh[..., None])
    reg = reg * (1 - a[..., None]) + rgb.astype(np.float32) * a[..., None]
    dst[y:y + h, x0:x0 + nw] = reg.astype(np.uint8)


# ---------------------------------------------------------------- fuentes de imagen
def cubrir(im, w=W, h=H, ancla=(0.5, 0.5)):
    """PIL -> np 'cover' w x h."""
    iw, ih = im.size
    s = max(w / iw, h / ih)
    im = im.resize((max(w, int(round(iw * s))), max(h, int(round(ih * s)))), Image.LANCZOS)
    x = int((im.width - w) * ancla[0]); y = int((im.height - h) * ancla[1])
    return np.asarray(im.crop((x, y, x + w, y + h)).convert('RGB'))


class Lienzo:
    """Imagen grande con 'vista' animada (zoom / paneo) y marcas rojas en coordenadas del lienzo."""

    def __init__(self, img, v0, v1=None, marcas=(), dur_mov=None):
        self.im = np.asarray(img.convert('RGB')) if isinstance(img, Image.Image) else img
        self.v0 = v0; self.v1 = v1 or v0; self.marcas = list(marcas); self.dur_mov = dur_mov

    def vista(self, tl, T):
        x = ease(tl / (self.dur_mov or T)) if self.dur_mov else tl / max(T, 1e-6)
        return [lerp(a, b, x) for a, b in zip(self.v0, self.v1)]   # x, y, ancho

    def frame(self, tl, T):
        vx, vy, vw = self.vista(tl, T)
        s = W / vw
        M = np.float32([[s, 0, -vx * s], [0, s, -vy * s]])
        interp = cv2.INTER_AREA if s < 0.6 else cv2.INTER_CUBIC
        if s < 0.6:   # reducir primero para no generar muare
            k = max(1, int(1 / s / 1.2))
            if not hasattr(self, '_red'): self._red = {}
            if k not in self._red:
                self._red[k] = cv2.resize(self.im, (self.im.shape[1] // k, self.im.shape[0] // k), interpolation=cv2.INTER_AREA) if k > 1 else self.im
            M = np.float32([[s * k, 0, -vx * s], [0, s * k, -vy * s]])
            out = cv2.warpAffine(self._red[k], M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        else:
            out = cv2.warpAffine(self.im, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)
        return out, (vx, vy, s)

    def a_pantalla(self, rect, tr):
        vx, vy, s = tr
        x, y, w, h = rect
        return ((x - vx) * s, (y - vy) * s, w * s, h * s)


class Clip:
    """Video a pantalla completa (cover), lectura secuencial."""

    def __init__(self, path, ss=0.0, ancla=0.5, vel=1.0, subir=0, encaje=None, entero=None, recorte=None):
        # subir=px: corre el video hacia arriba (su texto queda sobre Gabriel).  encaje=(escala, y): el video entero, mas chico,
        # sobre su propia version desenfocada (portada: deja lugar arriba para el titulo sin tapar el anuncio).
        # entero=y: el video ENTERO a todo el ancho (no 9:16: cuadrado, 4:5, apaisado) desde y px, sobre su version desenfocada,
        # para no cortarle el texto de los costados.  recorte=(w, h, x, y): recorta el original antes (franjas negras, una zona).
        self.path, self.ss, self.ancla, self.vel, self.subir, self.encaje = path, ss, ancla, vel, subir, encaje
        self.entero, self.recorte = entero, recorte
        self.p = None; self.n = -1; self.last = None

    def _cmd(self, ss, n=None):
        pre = "crop=%d:%d:%d:%d," % tuple(self.recorte) if self.recorte else ""
        vf = f"{pre}setpts=PTS/{self.vel},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{self.ancla}"
        if self.entero is not None:
            vf = (f"{pre}setpts=PTS/{self.vel},fps={FPS},split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"gblur=sigma=34,eq=brightness=-0.14[bg];[b]scale={W}:-2[fg];[bg][fg]overlay=0:{int(self.entero)}")
        c = ['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', self.path, '-vf', vf, '-an']
        if n: c += ['-frames:v', str(n)]
        return c + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']

    def frame(self, tl, T, seq=True):
        k = int(round(tl * FPS))
        if not seq:
            raw = subprocess.run(self._cmd(self.ss + tl * self.vel, 1), capture_output=True).stdout
            return self._subido(np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()), None
        if self.p is None:
            self.p = subprocess.Popen(self._cmd(self.ss), stdout=subprocess.PIPE)
        while self.n < k:
            raw = self.p.stdout.read(W * H * 3)
            if len(raw) < W * H * 3: break
            self.last = np.frombuffer(raw, np.uint8).reshape(H, W, 3); self.n += 1
        return self._subido(self.last.copy()), None

    def _subido(self, fr):
        if self.encaje:
            k, y = self.encaje; w, h = int(W * k), int(H * k)
            ch = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA)
            fondo = (cv2.GaussianBlur(fr, (0, 0), 42).astype(np.float32) * 0.62).astype(np.uint8)
            x = (W - w) // 2; h2 = min(h, H - y); fondo[y:y + h2, x:x + w] = ch[:h2]
            return fondo
        if not self.subir: return fr
        g = cv2.copyMakeBorder(fr, 0, self.subir, 0, 0, cv2.BORDER_REFLECT)[self.subir:self.subir + H]
        g[H - self.subir:] = cv2.GaussianBlur(g[H - self.subir:], (0, 0), 28)
        return np.ascontiguousarray(g)

    def cerrar(self):
        if self.p: self.p.kill(); self.p = None


class Grafico:
    """Grafico propio: fn(tl, T) -> PIL RGB 1080x1920."""

    def __init__(self, fn): self.fn = fn
    def frame(self, tl, T): return np.asarray(self.fn(tl, T)), None


class Serie:
    """Varias fuentes seguidas dentro de una misma toma: [(t_inicio_local, fuente), ...]."""

    def __init__(self, partes): self.partes = partes
    def frame(self, tl, T, **kw):
        act = [(t0, f) for t0, f in self.partes if tl >= t0 - 1e-6][-1]
        i = self.partes.index(act)
        t1 = self.partes[i + 1][0] if i + 1 < len(self.partes) else T
        fr, tr = act[1].frame(tl - act[0], t1 - act[0], **kw) if isinstance(act[1], (Clip, Mitades)) else act[1].frame(tl - act[0], t1 - act[0])
        self.actual = act[1]; self.tl_act = tl - act[0]
        return fr, tr


class Mitades:
    """Pantalla dividida (formato VS): dos fuentes lado a lado, la primera a la IZQUIERDA. Cada una se ve entera, a medio
    ancho, sobre su propia version desenfocada; linea blanca al medio. y = donde empieza cada mitad (px)."""

    def __init__(self, izq, der, y=170, linea=True):
        self.izq, self.der, self.y, self.linea = izq, der, y, linea

    def frame(self, tl, T, seq=True):
        out = np.zeros((H, W, 3), np.uint8); m = W // 2
        for n, f in enumerate((self.izq, self.der)):
            fr, _ = f.frame(tl, T, seq=seq) if isinstance(f, (Clip, Serie)) else f.frame(tl, T)
            fr = np.asarray(fr)
            bg = (cv2.GaussianBlur(fr[:, W // 4: W // 4 + m], (0, 0), 30).astype(np.float32) * 0.5).astype(np.uint8)
            ch = cv2.resize(fr, (m, H // 2), interpolation=cv2.INTER_AREA)
            bg[self.y:self.y + H // 2] = ch
            out[:, n * m:(n + 1) * m] = bg
        if self.linea: out[:, m - 3:m + 3] = 255
        return out, None


# ---------------------------------------------------------------- marcas rojas
def _perimetro(d, box, prog, ancho=9, punteado=False, ROJO=ROJO):
    x, y, w, h = box
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    total = 2 * (w + h); rest = total * prog
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        if rest <= 0: break
        f = min(1, rest / L)
        ex, ey = ax + (bx - ax) * f, ay + (by - ay) * f
        if punteado:
            n = max(1, int(L * f / 34))
            for i in range(n):
                p0 = i / n; p1 = p0 + 0.55 / n
                d.line([(ax + (ex - ax) * p0, ay + (ey - ay) * p0), (ax + (ex - ax) * p1, ay + (ey - ay) * p1)], fill=ROJO, width=ancho)
        else:
            d.line([(ax, ay), (ex, ey)], fill=ROJO, width=ancho)
            r = ancho / 2 - 0.5
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=ROJO); d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=ROJO)
        rest -= L


def _flecha(d, punta, cola, prog, ancho=13):
    px, py = punta; cx, cy = cola
    ex, ey = cx + (px - cx) * prog, cy + (py - cy) * prog
    d.line([(cx, cy), (ex, ey)], fill=ROJO, width=ancho)
    r = ancho / 2 - 0.5; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ROJO)
    if prog > 0.55:
        ang = math.atan2(py - cy, px - cx); L = 46
        for da in (2.55, -2.55):
            d.line([(ex, ey), (ex + L * math.cos(ang + da), ey + L * math.sin(ang + da))], fill=ROJO, width=ancho)
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=ROJO)


def dibujar_marcas(pil, marcas, tl, conv):
    d = ImageDraw.Draw(pil)
    for m in marcas:
        tipo, rect, t0 = m[0], m[1], m[2]
        t1 = m[3] if len(m) > 3 and m[3] is not None else 1e9
        if not (t0 <= tl < t1): continue
        x, y, w, h = conv(rect)
        pad = 14
        if tipo in ('caja', 'caja_p', 'caja_b'):   # caja_b: blanca, para fondos rojos
            _perimetro(d, (x - pad, y - pad, w + 2 * pad, h + 2 * pad), ease((tl - t0) / 0.22), punteado=(tipo == 'caja_p'), ROJO=(255, 255, 255) if tipo == 'caja_b' else ROJO)
        elif tipo == 'sub':
            p = ease((tl - t0) / 0.22)
            d.line([(x, y + h + 10), (x + w * p, y + h + 10)], fill=ROJO, width=9)
        elif tipo.startswith('flecha'):
            # flecha_ai: entra desde abajo-izquierda; flecha_ad: abajo-derecha; flecha_arr: desde arriba
            p = ease((tl - t0 - 0.08) / 0.22)
            if p <= 0: continue
            if tipo == 'flecha_ad':
                punta = (x + w + pad + 16, y + h / 2); cola = (punta[0] + 190, punta[1] + 150)
            elif tipo == 'flecha_arr':
                punta = (x + w / 2, y - pad - 16); cola = (punta[0] + 120, punta[1] - 190)
            else:
                punta = (x - pad - 16, y + h / 2); cola = (punta[0] - 190, punta[1] + 150)
            _flecha(d, punta, cola, p)


# ---------------------------------------------------------------- textos
_emoji_cache = {}


def emoji(ch, sz):
    k = (ch, sz)
    if k not in _emoji_cache:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((2, 4), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox())
        _emoji_cache[k] = im.resize((int(im.width * sz / im.height), sz), Image.LANCZOS)
    return _emoji_cache[k]


def etiqueta(pil, lineas, cy, tam=74, tl=1.0, clave=None, fondo=TINTA, color=(255, 255, 255), emo=None, logo=None):
    """Caja oscura redondeada con texto (una o mas lineas). clave: palabras que van en verde."""
    p = ease(tl / 0.16)
    if p <= 0: return
    f = font(tam)
    esp = f.getlength(' ')
    medidas = []
    for ln in lineas:
        ws = ln.split(' ')
        wpx = sum(f.getlength(w) for w in ws) + esp * (len(ws) - 1)
        medidas.append((ws, wpx))
    extra = (tam + 14) if emo else 0
    aw = max(m[1] for m in medidas)
    lh = int(tam * 1.16)
    bw = int(max(aw, medidas[-1][1] + extra) + 76); bh = lh * len(lineas) + 50
    capa = Image.new('RGBA', (bw, bh + (90 if logo is not None else 0)), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    oy = 90 if logo is not None else 0
    d.rounded_rectangle([0, oy, bw - 1, oy + bh - 1], radius=26, fill=fondo + (255,))
    for i, (ws, wpx) in enumerate(medidas):
        tot = wpx + (extra if (emo and i == len(medidas) - 1) else 0)
        x = (bw - tot) / 2; y = oy + 22 + i * lh
        for w in ws:
            lim = w.strip('.,!?¡¿"“”')
            d.text((x, y), w, font=f, fill=(VERDE if clave and lim in clave else color) + (255,))
            x += f.getlength(w) + esp
        if emo and i == len(medidas) - 1:
            e = emoji(emo, tam); capa.alpha_composite(e, (int(x + 2), int(y + tam * 0.12)))
    if logo is not None:
        lg = logo.resize((int(logo.width * 62 / logo.height), 62), Image.LANCZOS)
        chip = Image.new('RGBA', (lg.width + 44, 78), (0, 0, 0, 0))
        ImageDraw.Draw(chip).rounded_rectangle([0, 0, chip.width - 1, 77], radius=20, fill=(255, 255, 255, 255))
        chip.alpha_composite(lg, (22, 8)); capa.alpha_composite(chip, ((bw - chip.width) // 2, 0))
    if p < 1:
        k = lerp(0.9, 1.0, p)
        capa = capa.resize((int(capa.width * k), int(capa.height * k)), Image.LANCZOS)
        capa.putalpha(capa.getchannel('A').point(lambda v: int(v * p)))
    pil.paste(capa, (int((W - capa.width) / 2), int(cy - capa.height / 2)), capa)


# ---------------------------------------------------------------- subtitulos (juego aprobado en el video 31)
# Palabra simple: Inter Display SemiBold blanca. Palabra clave: ExtraBold verde menta, mas grande,
# debajo y tocandose con la blanca, siempre encima. Lugar fijo. La clave entra cuando se dice.
SUB = dict(tam=86, tam_clave=180, y_sola=850, y_clave=880, ancho=940, solape=8)
_sub_cache = {}


def _capa_texto(s, f, color):
    bb = f.getbbox(s); w = bb[2] - bb[0] + 120; h = bb[3] - bb[1] + 120
    t = Image.new('L', (w, h), 0); ImageDraw.Draw(t).text((60 - bb[0], 60 - bb[1]), s, font=f, fill=255)
    halo = t.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(min(255, v * 1.8) * 0.7))
    corta = t.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(min(255, v * 2.2) * 0.9))
    capa = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    capa.paste((0, 0, 0), (0, 0), halo); capa.paste((0, 0, 0), (0, 3), corta); capa.paste(color, (0, 0), t)
    return capa, bb[3] - bb[1]


def _ajustada(s, tam, peso, color):
    k = (s, tam, peso)
    if k not in _sub_cache:
        f = font(tam, peso)
        while f.getlength(s) > SUB['ancho'] and tam > 40:
            tam -= 4; f = font(tam, peso)
        _sub_cache[k] = _capa_texto(s, f, color)
    return _sub_cache[k]


def armar_tarjetas(palabras, guion, dur=None, min_tarjeta=0.7, min_clave=0.8, max_prestamo=0.30):
    """guion: lista de tarjetas; cada palabra corresponde a una de la transcripcion ('~' = no se muestra,
    '*' delante = palabra clave, que tiene que ser la ultima de la tarjeta).

    Tiempo de lectura (regla aprobada por Gabriel): ninguna tarjeta dura menos de min_tarjeta y la clave se ve
    al menos min_clave. Si una tarjeta queda corta se le presta tiempo de las vecinas moviendo el corte entre
    tarjetas (como mucho max_prestamo); si ni asi alcanza, falla: hay que unir tarjetas en el guion."""
    out = []; i = 0
    for tj in guion:
        toks = tj.split(' ')
        ws = palabras[i:i + len(toks)]; i += len(toks)
        clave = toks[-1][1:].replace('_', ' ') if toks[-1].startswith('*') else None      # '_' = espacio dentro de una misma palabra del guion
        simples = ' '.join(x for x in (toks[:-1] if clave else toks) if x != '~').replace('_', ' ')
        out.append(dict(t0=ws[0]['s'], fin=ws[-1]['e'], simples=simples, clave=clave, t_clave=ws[-1]['s'],
                        minimo=min_clave if clave else min_tarjeta))
    assert i == len(palabras), (i, len(palabras))
    out[0]['t0'] = 0.0
    for a, b in zip(out, out[1:]):
        a['pegada'] = b['t0'] - a['fin'] < 0.45
        a['t1'] = b['t0'] if a['pegada'] else a['fin'] + 0.12
    out[-1]['pegada'] = False
    out[-1]['t1'] = dur if dur else out[-1]['fin'] + 0.3       # con `dur`, la ultima tarjeta queda en pantalla hasta el final (cierre con cola)
    nat = [c['t1'] for c in out]
    falta = lambda c: max(0.0, c['minimo'] - (c['t1'] - c['t0']))
    for _ in range(4000):                       # relajacion: el corte se corre hacia la tarjeta a la que le sobra
        mov = 0.0
        for k in range(len(out) - 1):
            a, b = out[k], out[k + 1]
            if not a['pegada']: continue
            paso = 0.5 * (falta(a) - falta(b))
            nuevo = min(max(a['t1'] + paso, nat[k] - max_prestamo), nat[k] + max_prestamo)
            mov = max(mov, abs(nuevo - a['t1'])); a['t1'] = nuevo; b['t0'] = nuevo
        if mov < 1e-5: break
    for k, c in enumerate(out):                 # a cuadros enteros
        c['t0'] = round(c['t0'] * FPS) / FPS; c['t1'] = round(c['t1'] * FPS) / FPS
        c['corrida'] = round(c['t1'] - nat[k], 3)
    cortas = [(round(c['t1'] - c['t0'], 2), c['simples'], c['clave']) for c in out if c['t1'] - c['t0'] < c['minimo'] - 0.02]
    assert not cortas, ('tarjetas sin tiempo de lectura; unirlas en el guion', cortas)
    for c in out:
        c['min_clave'] = min_clave
    return out


def subtitulos(pil, t, tarjetas):
    for c in tarjetas:
        if not (c['t0'] <= t < c['t1']): continue
        if c['clave']:
            kc, hk = _ajustada(c['clave'], SUB['tam_clave'], 'ExtraBold', VERDE)
            top_clave = SUB['y_clave'] - hk / 2
            if c['simples']:
                sc, hs = _ajustada(c['simples'], SUB['tam'], 'SemiBold', (255, 255, 255))
                cy = top_clave + SUB['solape'] - hs / 2
                pil.paste(sc, (int((W - sc.width) / 2), int(cy - sc.height / 2)), sc)
            tk = min(c['t_clave'], c['t1'] - c.get('min_clave', 0.8))      # la clave se ve al menos 0,8 s
            tk = max(tk, c['t0'])
            if t >= tk:
                a = min(1.0, (t - tk) / 0.07); e = lerp(0.88, 1.0, ease((t - tk) / 0.11))
                capa = kc
                if e < 0.999: capa = kc.resize((int(kc.width * e), int(kc.height * e)), Image.LANCZOS)
                if a < 1: capa = capa.copy(); capa.putalpha(capa.getchannel('A').point(lambda v: int(v * a)))
                pil.paste(capa, (int((W - capa.width) / 2), int(SUB['y_clave'] - capa.height / 2)), capa)
        else:
            sc, hs = _ajustada(c['simples'], SUB['tam'], 'SemiBold', (255, 255, 255))
            pil.paste(sc, (int((W - sc.width) / 2), int(SUB['y_sola'] - sc.height / 2)), sc)
        return


# ---------------------------------------------------------------- render
def cargar(path):
    spec = importlib.util.spec_from_file_location('cfg', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _clips(f):
    """Todos los Clip que hay dentro de una fuente (para cerrar sus lectores al terminar la toma)."""
    if isinstance(f, Clip): return [f]
    if isinstance(f, Serie): return [c for _, g in f.partes for c in _clips(g)]
    if isinstance(f, Mitades): return _clips(f.izq) + _clips(f.der)
    return []


def componer(cfg, shot, t, crudo, seq=True):
    tl = t - shot['t0']; T = shot['t1'] - shot['t0']
    src = shot['fondo']
    if isinstance(src, (Clip, Serie, Mitades)):
        fr, tr = src.frame(tl, T, seq=seq)
    else:
        fr, tr = src.frame(tl, T)
    fr = np.array(fr, copy=True)
    base = src
    if isinstance(src, Serie):
        base, tl_m = src.actual, src.tl_act
    else:
        tl_m = tl
    marcas = getattr(base, 'marcas', None)
    if marcas or shot.get('antes'):
        pil = Image.fromarray(fr)
        if marcas: dibujar_marcas(pil, marcas, tl_m, lambda r: base.a_pantalla(r, tr))
        if shot.get('antes'): shot['antes'](pil, tl, T)
        fr = np.asarray(pil).copy()
    lay = shot['gab'](tl) if callable(shot['gab']) else shot['gab']
    if lay: poner_gabriel(fr, crudo, lay)
    subs = getattr(cfg, 'SUBS', None)
    if shot.get('texto') or subs:
        pil = Image.fromarray(fr)
        if shot.get('texto'): shot['texto'](pil, tl, T)
        if subs: subtitulos(pil, t, subs)
        fr = np.asarray(pil)
    return fr


def control(cfg):
    """Control antes de entregar: clips que existen y alcanzan, tiempo de lectura, visuales repetidos, tamanos de letra."""
    # 39 v01: un id de anuncio mal tipeado (el archivo no existia) corto el render a los 47 s sin que se viera el error.
    faltan = []
    for sh in cfg.SHOTS:
        f = sh['fondo']; partes = f.partes if isinstance(f, Serie) else [(0.0, f)]
        for n, (p0, g) in enumerate(partes):
            p1 = partes[n + 1][0] if n + 1 < len(partes) else sh['t1'] - sh['t0']
            for c in _clips(g):
                if not os.path.exists(c.path): faltan.append(f"{sh['id']}: NO EXISTE {c.path}"); continue
                dur = float(subprocess.run(['ffprobe', '-v', '0', '-show_entries', 'format=duration', '-of', 'csv=p=0', c.path], capture_output=True, text=True).stdout.strip() or 0)
                if c.ss + (p1 - p0) * c.vel > dur + 0.05: faltan.append(f"{sh['id']}: {os.path.basename(c.path)} dura {dur:.1f} s y se pide hasta {c.ss + (p1 - p0) * c.vel:.1f} s")
    print('CLIPS:', 'todos existen y alcanzan' if not faltan else '\n  ' + '\n  '.join(faltan))
    subs = getattr(cfg, 'SUBS', [])
    if subs:
        d = sorted((round(c['t1'] - c['t0'], 2), c['simples'], c['clave'] or '') for c in subs)
        print('TARJETA MAS CORTA: %.2f s  "%s %s"' % d[0]); print('  las 5 mas cortas:', [x[0] for x in d[:5]])
        kv = sorted((round(c['t1'] - max(c['t0'], min(c['t_clave'], c['t1'] - c.get('min_clave', 0.8))), 2), c['clave']) for c in subs if c['clave'])
        print('CLAVE QUE MENOS SE VE: %.2f s  "%s"   (claves: %d)' % (kv[0][0], kv[0][1], len(kv)))
        print('CORTE MAS CORRIDO respecto de la voz: %.2f s' % max(abs(c['corrida']) for c in subs))
        ch = []
        for c in subs:
            if not c['simples']: continue
            f = font(SUB['tam'], 'SemiBold'); w = f.getlength(c['simples'])
            if w > SUB['ancho']: ch.append((int(SUB['tam'] * SUB['ancho'] / w), c['simples']))
        print('LINEAS ACHICADAS (px de %d):' % SUB['tam'], sorted(ch)[:12])
    usos = {}
    for sh in cfg.SHOTS:
        for f in set(sh.get('fuentes', [])): usos.setdefault(f, []).append(sh['id'])
    perm = getattr(cfg, 'REPETICION_PERMITIDA', {})
    rep = {f: t for f, t in usos.items() if len(t) > 1 and f not in perm}
    print('VISUALES REPETIDOS:', rep or 'ninguno')
    for f, t in usos.items():
        if len(t) > 1 and f in perm: print('  repeticion permitida:', f, t, '-', perm[f])
    print('fuentes distintas:', len(usos), ' tomas:', len(cfg.SHOTS))
    return not rep and not faltan


def leer_crudo(raw, ss=None, n=None):
    c = ['ffmpeg', '-v', 'error']
    if ss is not None: c += ['-ss', f'{ss:.3f}']
    c += ['-i', raw, '-vf', f'fps={FPS},scale={W}:{H}', '-an']
    if n: c += ['-frames:v', str(n)]
    return c + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']


def main():
    cfg = cargar(sys.argv[1])
    for k in ('CABEZA', 'Y0', 'CENTRO'):            # cada crudo tiene a Gabriel a otra altura: el config puede fijar la fila de su cabeza
        if hasattr(cfg, k): globals()[k] = getattr(cfg, k)
    shots = cfg.SHOTS
    for a, b in zip(shots, shots[1:]):
        assert abs(a['t1'] - b['t0']) < 1e-6, (a['id'], b['id'])
    if '--control' in sys.argv:
        sys.exit(0 if control(cfg) else 1)
    if '--prev' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--prev') + 1].split(',')]
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'prev.jpg'
        arg = lambda k, d: int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
        cols = min(len(ts), arg('--cols', 8)); filas = (len(ts) + cols - 1) // cols
        tw = arg('--ancho', 270); th = tw * 16 // 9          # --cols 4 --ancho 540: hoja grande para revisar de cerca
        hoja = Image.new('RGB', (cols * tw, filas * th))
        for i, t in enumerate(ts):
            sh = [s for s in shots if s['t0'] <= t < s['t1']][0]
            raw = subprocess.run(leer_crudo(cfg.RAW, t, 1), capture_output=True).stdout
            crudo = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
            fr = componer(cfg, sh, t, crudo, seq=False)
            im = Image.fromarray(fr)
            if len(ts) == 1: im.save(out, quality=92); return
            im = im.resize((tw, th), Image.LANCZOS)
            ImageDraw.Draw(im).text((6, 4), f"{sh['id']} {t:.2f}", fill=(255, 0, 255))
            hoja.paste(im, ((i % cols) * tw, (i // cols) * th))
        hoja.save(out, quality=88); return
    out = sys.argv[sys.argv.index('--out') + 1]
    N = int(round(cfg.DUR * FPS))
    rd = subprocess.Popen(leer_crudo(cfg.RAW), stdout=subprocess.PIPE)
    af = getattr(cfg, 'AUDIO_FILTRO', 'anull')
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', cfg.RAW, '-map', '0:v', '-map', '1:a', '-af', af, '-t', f'{cfg.DUR:.3f}',
                           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                           '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    si = 0; crudo = None
    for k in range(N):
        t = k / FPS
        raw = rd.stdout.read(W * H * 3)
        if len(raw) == W * H * 3: crudo = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
        while si + 1 < len(shots) and t >= shots[si]['t1'] - 1e-6:
            f = shots[si]['fondo']
            for c in _clips(f): c.cerrar()
            si += 1
        fr = componer(cfg, shots[si], t, crudo)
        wr.stdin.write(fr.tobytes())
        if k % 300 == 0: print(f'{t:5.1f}s', shots[si]['id'], flush=True)
    wr.stdin.close(); wr.wait(); rd.kill()
    print('listo', out)


if __name__ == '__main__':
    sys.modules['render_verde'] = sys.modules['__main__']   # el config importa este mismo modulo
    main()
