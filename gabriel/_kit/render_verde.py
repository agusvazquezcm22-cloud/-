"""Motor del formato "pantalla verde" de Gabriel (referencia: Chase Chappell).

Gabriel recortado del verde, pegado abajo, sobre imagen/video/grafico a pantalla
completa. Corte seco, marcas rojas, sin subtitulos propios.

Uso:  python3 render_verde.py <config.py> [--prev t1,t2,...] [--out archivo.mp4]
El config define RAW, DUR y SHOTS (ver gabriel/32/gabriel32_v01.py).
"""
import subprocess, sys, math, os, importlib.util
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

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
}


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
        a = a * ramp[None, :]
    y = ytop - int(round((CABEZA - Y0) * s))
    h = min(nh, H - y)
    rgb, a = rgb[:h], a[:h]
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

    def __init__(self, path, ss=0.0, ancla=0.5, vel=1.0):
        self.path, self.ss, self.ancla, self.vel = path, ss, ancla, vel
        self.p = None; self.n = -1; self.last = None

    def _cmd(self, ss, n=None):
        vf = f"setpts=PTS/{self.vel},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{self.ancla}"
        c = ['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', self.path, '-vf', vf, '-an']
        if n: c += ['-frames:v', str(n)]
        return c + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']

    def frame(self, tl, T, seq=True):
        k = int(round(tl * FPS))
        if not seq:
            raw = subprocess.run(self._cmd(self.ss + tl * self.vel, 1), capture_output=True).stdout
            return np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy(), None
        if self.p is None:
            self.p = subprocess.Popen(self._cmd(self.ss), stdout=subprocess.PIPE)
        while self.n < k:
            raw = self.p.stdout.read(W * H * 3)
            if len(raw) < W * H * 3: break
            self.last = np.frombuffer(raw, np.uint8).reshape(H, W, 3); self.n += 1
        return self.last.copy(), None

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
        fr, tr = act[1].frame(tl - act[0], t1 - act[0], **kw) if isinstance(act[1], Clip) else act[1].frame(tl - act[0], t1 - act[0])
        self.actual = act[1]; self.tl_act = tl - act[0]
        return fr, tr


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


# ---------------------------------------------------------------- render
def cargar(path):
    spec = importlib.util.spec_from_file_location('cfg', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def componer(cfg, shot, t, crudo, seq=True):
    tl = t - shot['t0']; T = shot['t1'] - shot['t0']
    src = shot['fondo']
    if isinstance(src, (Clip, Serie)):
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
    if shot.get('texto'):
        pil = Image.fromarray(fr); shot['texto'](pil, tl, T); fr = np.asarray(pil)
    return fr


def leer_crudo(raw, ss=None, n=None):
    c = ['ffmpeg', '-v', 'error']
    if ss is not None: c += ['-ss', f'{ss:.3f}']
    c += ['-i', raw, '-vf', f'fps={FPS},scale={W}:{H}', '-an']
    if n: c += ['-frames:v', str(n)]
    return c + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']


def main():
    cfg = cargar(sys.argv[1])
    shots = cfg.SHOTS
    for a, b in zip(shots, shots[1:]):
        assert abs(a['t1'] - b['t0']) < 1e-6, (a['id'], b['id'])
    if '--prev' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--prev') + 1].split(',')]
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'prev.jpg'
        cols = min(len(ts), 8); filas = (len(ts) + cols - 1) // cols
        tw, th = 270, 480
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
            for c in ([f] if isinstance(f, Clip) else [p[1] for p in f.partes if isinstance(p[1], Clip)] if isinstance(f, Serie) else []): c.cerrar()
            si += 1
        fr = componer(cfg, shots[si], t, crudo)
        wr.stdin.write(fr.tobytes())
        if k % 300 == 0: print(f'{t:5.1f}s', shots[si]['id'], flush=True)
    wr.stdin.close(); wr.wait(); rd.kill()
    print('listo', out)


if __name__ == '__main__':
    sys.modules['render_verde'] = sys.modules['__main__']   # el config importa este mismo modulo
    main()
