"""Render de texto con tracking (interletra) para el estilo Amy. Devuelve alfa float32 0..1."""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

SS = 3  # supermuestreo

@lru_cache(maxsize=64)
def _font(path, px):
    return ImageFont.truetype(path, px)

def line_alpha(text, font_path, size, tracking=0.0, ss=SS):
    """Alfa de una línea. Devuelve (alfa HxW, ancho_avance, ascent) en px finales.
    tracking en em (negativo = apretado). El origen (0, ascent) es el inicio de la línea base."""
    f = _font(font_path, int(round(size * ss)))
    asc, desc = f.getmetrics()
    xs = []; x = 0.0
    for i, ch in enumerate(text):
        xs.append(x)
        adv = f.getlength(ch)
        if i + 1 < len(text):
            pair = f.getlength(ch + text[i + 1])
            adv = pair - f.getlength(text[i + 1])  # incluye kerning
            adv += tracking * size * ss
        x += adv
    w = int(x + size * ss * 0.6) + 8; pad = int(size * ss * 0.3)
    im = Image.new("L", (w + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(im)
    for ch, cx in zip(text, xs):
        if ch != " ":
            d.text((pad + cx, pad), ch, font=f, fill=255)
    W = im.width // ss; H = im.height // ss
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255.0
    return a, x / ss, asc / ss, pad / ss

def paste_alpha(canvas, a, x, y):
    """Suma (max) el alfa `a` en canvas con esquina sup-izq en (x,y) (float -> entero)."""
    x = int(round(x)); y = int(round(y))
    H, W = canvas.shape; h, w = a.shape
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    canvas[y0:y1, x0:x1] = np.maximum(canvas[y0:y1, x0:x1], a[y0 - y:y1 - y, x0 - x:x1 - x])

def draw_line(canvas, text, font_path, size, tracking, x, baseline, align="left"):
    """Dibuja una línea en canvas (alfa). x = borde izq (o centro si align=center) del avance; baseline en px."""
    a, adv, asc, pad = line_alpha(text, font_path, size, tracking)
    if align == "center": x = x - adv / 2.0
    elif align == "right": x = x - adv
    paste_alpha(canvas, a, x - pad, baseline - asc - pad)
    return adv
