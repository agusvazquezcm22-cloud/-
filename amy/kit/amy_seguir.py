"""Tarjeta «Seguir» de cierre para Amy (@amyfitcoach_): blanca, minimalista, botón verde de marca.
dibujar(img, k, avatar) pinta la tarjeta sobre un cuadro BGR 1080x1920; k = cuadros desde que entra."""
import os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
_D = os.path.dirname(os.path.abspath(__file__))
VERDE = (188, 205, 157); OSCURO = (30, 36, 28)
CW, CH, SS = 800, 176, 2
TAP = 34          # cuadro en que se "toca" el botón

def _card(usuario, sub, avatar_bgr, siguiendo):
    im = Image.new("RGBA", (CW * SS, CH * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, CW * SS - 1, CH * SS - 1], radius=CH * SS // 2, fill=(255, 255, 255, 246))
    f1 = ImageFont.truetype(f"{_D}/fuentes/Montserrat-SemiBold.ttf", 40 * SS); f2 = ImageFont.truetype(f"{_D}/fuentes/Montserrat-Light.ttf", 28 * SS)
    fb = ImageFont.truetype(f"{_D}/fuentes/Montserrat-SemiBold.ttf", 32 * SS)
    av = 132 * SS; ax, ay = 22 * SS, (CH * SS - av) // 2
    a = cv2.cvtColor(cv2.resize(avatar_bgr, (av, av), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)
    m = Image.new("L", (av, av), 0); ImageDraw.Draw(m).ellipse([0, 0, av - 1, av - 1], fill=255)
    im.paste(Image.fromarray(a), (ax, ay), m)
    tx = ax + av + 26 * SS
    d.text((tx, 46 * SS), usuario, font=f1, fill=OSCURO + (255,))
    d.text((tx, 100 * SS), sub, font=f2, fill=(110, 116, 108, 255))
    bw, bh = 214 * SS, 76 * SS; bx, by = CW * SS - bw - 28 * SS, (CH * SS - bh) // 2
    txt = "Siguiendo" if siguiendo else "Seguir"
    if siguiendo: d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=(255, 255, 255, 255), outline=VERDE + (255,), width=3 * SS)
    else: d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=VERDE + (255,))
    w = d.textlength(txt, font=fb); d.text((bx + (bw - w) / 2, by + 16 * SS), txt, font=fb, fill=OSCURO + (255,))
    return np.asarray(im.resize((CW, CH), Image.LANCZOS), np.float32)

_cache = {}
def dibujar(img, k, avatar_bgr, usuario="amyfitcoach_", sub="Vida Fit", cy=1010):
    if k < 0: return
    key = (usuario, sub)
    if key not in _cache: _cache[key] = (_card(usuario, sub, avatar_bgr, False), _card(usuario, sub, avatar_bgr, True))
    c = _cache[key][1 if k >= TAP + 3 else 0]
    p = min(k / 12.0, 1.0); o = 1 - (1 - p) ** 2; dy = int(round(50 * (1 - p) ** 2))
    s = 0.95 if TAP <= k < TAP + 3 else 1.0      # el toque: la tarjeta se achica un instante
    if s != 1.0: c = cv2.resize(c, (int(CW * s), int(CH * s)), interpolation=cv2.INTER_AREA)
    h, w = c.shape[:2]; x = (1080 - w) // 2; y = cy - h // 2 + dy
    sh = np.zeros((h + 80, w + 80), np.float32); sh[40:-40, 40:-40] = c[..., 3] / 255.0
    sh = cv2.GaussianBlur(sh, (0, 0), 16) * 0.35 * o
    r = img[y - 40 + 8:y + h + 40 + 8, x - 40:x + w + 40].astype(np.float32); r *= (1 - sh)[..., None]
    img[y - 40 + 8:y + h + 40 + 8, x - 40:x + w + 40] = r.astype(np.uint8)
    a = (c[..., 3:4] / 255.0) * o; r = img[y:y + h, x:x + w].astype(np.float32)
    img[y:y + h, x:x + w] = (r * (1 - a) + c[..., 2::-1] * a).astype(np.uint8)
