#!/usr/bin/env python3
"""NXT · motor de gráficos estilo Amy (v0.1).
Uso: python3 -I amy_render.py proyecto.json
Dibuja subtítulos (Montserrat Light, corte seco), títulos Light+Black con glow y notas en cursiva
sobre un video 1080x1920. Con "limpiar_original": true borra (inpaint) el texto que ya trae el video:
solo para pruebas de recreación sobre una referencia ya editada."""
import sys, os, json, subprocess, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import amytext as T

VERSION = "0.2"
P = json.load(open(sys.argv[1]))
BASE = os.path.dirname(os.path.abspath(sys.argv[1]))
rp = lambda p: p if os.path.isabs(p) else os.path.join(BASE, p)
FONTS = {k: rp(v) for k, v in P["fuentes"].items()}
ST = P["estilo"]
W, H = 1080, 1920

def blur(a, sigma):
    return cv2.GaussianBlur(a, (0, 0), sigma) if sigma > 0 else a

class Elem:
    """Un bloque de texto ya rasterizado: alfa de texto, glow y sombra recortados a su caja."""
    def __init__(self, lines, style, f0, f1, anim="corte", dur=1, f_bloque=None):
        self.f0, self.f1, self.anim, self.dur = f0, f1, anim, dur
        self.col = np.float32(style.get("color", [255, 255, 255])[::-1])   # color del texto (RGB en el JSON)
        self.fb = f0 if f_bloque is None else f_bloque   # cuadro en que arranca la animación del bloque
        canvas = np.zeros((H, W), np.float32)
        sh = style.get("cursiva_falsa", 0)
        for ln in lines:
            c1 = np.zeros((H, W), np.float32)
            T.draw_line(c1, ln["texto"], FONTS[ln["fuente"]], ln["tam"], ln["tracking"], ln["x"], ln["base"], ln.get("alinear", "left"))
            if sh:  # cursiva falsa: inclina cada línea sobre su propia línea base
                c1 = cv2.warpAffine(c1, np.float32([[1, -sh, sh * ln["base"]], [0, 1, 0]]), (W, H), flags=cv2.INTER_LINEAR)
            canvas = np.maximum(canvas, c1)
        glow = np.clip(blur(canvas, style.get("glow_sigma", 0)) * style.get("glow_gan", 0), 0, 1) * style.get("glow_op", 0) if style.get("glow_op", 0) else None
        shadow = None
        if style.get("sombra_op", 0):
            s = blur(canvas, style["sombra_sigma"]); dy = int(style.get("sombra_dy", 0))
            if dy: s = np.roll(s, dy, axis=0)
            shadow = np.clip(s * style.get("sombra_gan", 1.6), 0, 1) * style["sombra_op"]
        tot = canvas.copy()
        for x in (glow, shadow):
            if x is not None: tot = np.maximum(tot, x)
        ys, xs = np.nonzero(tot > 0.004)
        y0, y1, x0, x1 = max(ys.min() - 2, 0), min(ys.max() + 3, H), max(xs.min() - 2, 0), min(xs.max() + 3, W)
        self.box = (y0, y1, x0, x1)
        self.a = canvas[y0:y1, x0:x1].copy()
        self.g = glow[y0:y1, x0:x1].copy() if glow is not None else None
        self.s = shadow[y0:y1, x0:x1].copy() if shadow is not None else None
        d = int(style.get("limpiar_dilat", 6))
        m = cv2.dilate((canvas > 0.04).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * d + 1, 2 * d + 1)))
        ys, xs = np.nonzero(m)
        self.mbox = (ys.min(), ys.max() + 1, xs.min(), xs.max() + 1)
        self.m = m[self.mbox[0]:self.mbox[1], self.mbox[2]:self.mbox[3]].copy()

    def dy(self, f):
        """Desplazamiento vertical (px) de la entrada "sube": medido en la referencia T2 V8."""
        if self.anim != "sube": return 0.0
        return max(0.0, 78.0 * 0.875 ** (f - self.fb) - 3.0)

    def op(self, f):
        if f < self.f0 or f >= self.f1: return 0.0
        if self.anim == "sube":
            i = f - self.fb
            return 0.05 if i <= 0 else 1 - (1 - min(i / 14.0, 1.0)) ** 2
        if self.anim == "fade":
            p = min((f - self.f0 + 1) / float(self.dur), 1.0); return 1 - (1 - p) ** 2.2
        return 1.0

    def _shift(self, arr, frac):
        return cv2.warpAffine(arr, np.float32([[1, 0, 0], [0, 1, frac]]), (arr.shape[1], arr.shape[0]), flags=cv2.INTER_LINEAR) if frac else arr

    def draw(self, img, f):
        o = self.op(f)
        if o <= 0: return
        d = self.dy(f); di = int(np.floor(d)); frac = d - di
        y0, y1, x0, x1 = self.box; y0 += di; y1 += di
        if y1 > H: return
        reg = img[y0:y1, x0:x1].astype(np.float32)
        if self.s is not None: reg *= (1 - self._shift(self.s, frac) * o)[..., None]
        if self.g is not None: reg += (self.col - reg) * (self._shift(self.g, frac) * o * o)[..., None]
        reg += (self.col - reg) * (self._shift(self.a, frac) * o)[..., None]
        img[y0:y1, x0:x1] = np.clip(reg, 0, 255).astype(np.uint8)

    def mask_at(self, f):
        d = int(round(self.dy(f))); a, b, c, e = self.mbox
        return (a + d, min(b + d, H), c, e), self.m[:min(b + d, H) - (a + d)]

elems = []
cs = ST["subtitulo"]
for c in P.get("subtitulos", []):
    ln = [{"texto": c["texto"], "fuente": cs["fuente"], "tam": cs["tam"], "tracking": cs["tracking"], "x": cs["x_centro"], "base": c.get("base", cs["base"]), "alinear": "center"}]
    elems.append(Elem(ln, cs, c["f0"], c["f1"]))
for t in P.get("titulos", []):
    for ln in t["lineas"]:
        st = ST[ln.get("estilo", "titulo_fuerte" if ln["fuente"] == "black" else "titulo_fino")]
        anim = ln.get("anim", t.get("anim", "sube"))
        elems.append(Elem([ln], st, ln.get("f_ver", t["f0"]), t["f1"], anim, f_bloque=t.get("f0")))
for n in P.get("notas", []):
    st = ST[n.get("estilo", "nota")]
    elems.append(Elem(n["lineas"], st, n["f0"], n["f1"], n.get("anim", "corte"), n.get("dur", 6)))

src = rp(P["video"]); out = rp(P["salida"])
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:.3f}", "-i", "-",
                        "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
limpiar = P.get("limpiar_original", False); solo_limpio = os.environ.get("SOLO_LIMPIO") == "1"
f = 0
while True:
    ok, img = cap.read()
    if not ok: break
    if img.shape[:2] != (H, W): img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    act = [e for e in elems if e.f0 <= f < e.f1]
    if limpiar and act:
        ms = [e.mask_at(f) for e in act]
        y0 = min(b[0] for b, _ in ms); y1 = max(b[1] for b, _ in ms); x0 = min(b[2] for b, _ in ms); x1 = max(b[3] for b, _ in ms)
        pad = 14; y0, x0 = max(y0 - pad, 0), max(x0 - pad, 0); y1, x1 = min(y1 + pad, H), min(x1 + pad, W)
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        for (a, b, c, d), mm in ms: m[a - y0:b - y0, c - x0:d - x0] |= mm
        img[y0:y1, x0:x1] = cv2.inpaint(img[y0:y1, x0:x1], m, 5, cv2.INPAINT_TELEA)
    if not solo_limpio:
        for e in act: e.draw(img, f)
    enc.stdin.write(img.tobytes()); f += 1
    if f % 150 == 0: print(f"{f}/{n}", flush=True)
enc.stdin.close(); enc.wait()
print("OK", out, f, "cuadros")
