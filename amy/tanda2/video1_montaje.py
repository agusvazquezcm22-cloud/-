#!/usr/bin/env python3
"""Montaje base del video 1 de Amy (Tanda 2) + proyecto de texto para amy_render."""
import sys, os, json, subprocess, numpy as np, cv2
S = sys.argv[1]; KIT = sys.argv[2]; VER = sys.argv[3]
sys.path.insert(0, KIT); import amytext as T
V = f"{S}/v1"; FPS = 30; W, H = 1080, 1920
L = f"{KIT}/fuentes/Montserrat-Light.ttf"; B = f"{KIT}/fuentes/Montserrat-Black.ttf"
# (t0, t1, fuente, extra)  tiempos del crudo IMG_1732
SEG = [
 (0.95, 1.66, "med", {}), (1.66, 5.40, "close", {}),
 (5.75, 11.70, "med", {"bn": True}),
 (11.90, 13.70, "br_squat", {"in": 2.0}),
 (14.15, 15.42, "close", {}), (15.42, 17.45, "med", {}),
 (18.35, 20.00, "wide", {"foto": True}), (21.30, 25.20, "wide", {"foto": True}),
 (25.20, 26.75, "close", {}), (27.00, 28.15, "med", {}),
 (28.15, 29.85, "br_rdl", {"in": 2.6}), (29.85, 31.60, "br_crunch", {"in": 3.0}),
 (31.75, 33.12, "close", {}),
]
out0 = []; n = 0
for a, b, src, ex in SEG:
    k = int(round((b - a) * FPS)); out0.append((n, n + k)); n += k
NF = n
def tmap(t):
    for (a, b, _, _), (o0, o1) in zip(SEG, out0):
        if a - 1e-6 <= t <= b + 1e-6: return min(o0 + int(round((t - a) * FPS)), o1)
    for i in range(len(SEG) - 1):                # cae en un silencio cortado
        if SEG[i][1] < t < SEG[i + 1][0]: return out0[i][1]
    return 0 if t < SEG[0][0] else NF

# ---------- tarjeta de la foto ----------
CW = 780; CX, CY = 150, 105
ph = cv2.imread(f"{S}/t2raw/v1_antes_despues.png", cv2.IMREAD_UNCHANGED)[..., :3]
ph = cv2.resize(ph, (CW, CW), interpolation=cv2.INTER_AREA)
lab = np.zeros((CW, CW), np.float32)
for txt, cx in (("antes", CW * 0.25), ("después", CW * 0.75)):
    T.draw_line(lab, txt, L, 54, -0.07, cx, CW - 36, "center")
sh = np.clip(cv2.GaussianBlur(lab, (0, 0), 5) * 1.8, 0, 1) * 0.6
ph = ph.astype(np.float32) * (1 - sh[..., None]); ph += (255 - ph) * lab[..., None]
mask = np.zeros((CW, CW), np.float32); cv2.rectangle(mask, (40, 0), (CW - 40, CW), 1, -1); cv2.rectangle(mask, (0, 40), (CW, CW - 40), 1, -1)
for cx, cy in ((40, 40), (CW - 40, 40), (40, CW - 40), (CW - 40, CW - 40)): cv2.circle(mask, (cx, cy), 40, 1, -1, cv2.LINE_AA)
mask = cv2.GaussianBlur(mask, (0, 0), 0.8)
pad = 60; shadow = np.zeros((CW + 2 * pad, CW + 2 * pad), np.float32); shadow[pad:-pad, pad:-pad] = mask
shadow = cv2.GaussianBlur(shadow, (0, 0), 22) * 0.55
def put_card(img, k):
    """k = cuadros desde que entra la tarjeta: sube 60 px con fundido en 12 cuadros."""
    p = min(k / 12.0, 1.0); o = 1 - (1 - p) ** 2; dy = int(round(60 * (1 - p) ** 2))
    y, x = CY + dy, CX
    r = img[y - pad:y + CW + pad, x - pad:x + CW + pad].astype(np.float32); r *= (1 - shadow * o)[..., None]
    img[y - pad:y + CW + pad, x - pad:x + CW + pad] = r.astype(np.uint8)
    r = img[y:y + CW, x:x + CW].astype(np.float32); a = (mask * o)[..., None]
    img[y:y + CW, x:x + CW] = (r * (1 - a) + ph * a).astype(np.uint8)

# ---------- video base ----------
base = f"{V}/base_{VER}.mp4"; aud = f"{V}/audio_{VER}.m4a"
if "--solo-json" not in sys.argv:
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", base], stdin=subprocess.PIPE)
    caps = {}; foto0 = None
    for (a, b, src, ex), (o0, o1) in zip(SEG, out0):
        c = caps.setdefault(src, cv2.VideoCapture(f"{V}/{src}.mp4"))
        c.set(cv2.CAP_PROP_POS_FRAMES, int(round((ex["in"] if "in" in ex else a) * FPS)))
        if ex.get("foto") and foto0 is None: foto0 = o0
        for f in range(o0, o1):
            ok, img = c.read()
            if ex.get("bn"):
                g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
                g = np.clip((g - 128) * 1.08 + 124, 0, 255).astype(np.uint8); img = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
            if ex.get("foto"): put_card(img, f - foto0)
            enc.stdin.write(img.tobytes())
    enc.stdin.close(); enc.wait()
    # audio: mismos cortes, fundidos de 8 ms en cada unión, -14 LUFS
    parts = []; fc = ""; i = 0
    j = 0
    while j < len(SEG):                           # une segmentos contiguos
        a, b = SEG[j][0], SEG[j][1]
        while j + 1 < len(SEG) and abs(SEG[j + 1][0] - b) < 1e-6: j += 1; b = SEG[j][1]
        d = b - a
        fc += f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.3f}:d=0.008[a{i}];"; parts.append(f"[a{i}]"); i += 1; j += 1
    fc += "".join(parts) + f"concat=n={i}:v=0:a=1,highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{S}/t2raw/v1_IMG_1732.MOV", "-filter_complex", fc, "-map", "[o]", "-ar", "48000", "-c:a", "aac", "-b:a", "256k", aud], check=True)
    mux = f"{V}/basea_{VER}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", aud, "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", mux], check=True)

# ---------- proyecto de texto ----------
def block(lines, first_base, step=0.66):
    """lines: [(texto, fuente, tam, tracking, t_ver)] -> líneas alineadas a la izquierda, bloque centrado."""
    ws = [T.line_alpha(t, L if fu == "light" else B, tam, tr)[1] for t, fu, tam, tr, _ in lines]
    x = 540 - max(ws) / 2.0; out = []; base_y = first_base
    for i, (t, fu, tam, tr, tv) in enumerate(lines):
        if i: base_y += step * tam * (1.12 if fu == "black" and lines[i - 1][1] == "light" and tam > lines[i - 1][2] * 1.2 else 1.0)
        d = dict(texto=t, fuente=fu, tam=tam, tracking=tr, x=round(x, 1), base=round(base_y))
        if tv is not None: d["f_ver"] = tmap(tv)
        out.append(d)
    return out
TR = -0.07
titulos = [
 {"f0": tmap(0.95), "f1": tmap(1.66), "lineas": block([("Déjame", "light", 170, TR, None), ("adivinar", "black", 170, -0.09, 1.24)], 1130)},
 {"f0": tmap(4.34), "f1": tmap(5.40), "lineas": block([("efecto", "light", 170, TR, None), ("rebote", "black", 184, -0.09, 4.84)], 1130)},
 {"f0": tmap(5.85), "f1": tmap(10.40), "lineas": [dict(texto=t, fuente="light", tam=76, tracking=TR, x=120, base=1036 + 88 * i, f_ver=tmap(tv)) for i, (t, tv) in enumerate((("dieta cetogénica", 6.02), ("dieta keto", 7.24), ("eliminar carbohidratos", 8.12), ("ayuno intermitente", 9.40)))]},
 {"f0": tmap(14.15), "f1": tmap(15.42), "lineas": block([("el problema", "light", 128, TR, None), ("no lo tienes", "light", 128, TR, 14.52), ("tú", "black", 176, -0.1, 15.00)], 1090)},
 {"f0": tmap(15.44), "f1": tmap(16.50), "lineas": block([("el problema es", "light", 108, TR, None), ("el método", "black", 164, -0.09, 15.96)], 1100)},
 {"f0": tmap(27.00), "f1": tmap(28.15), "lineas": block([("comenta", "light", 130, TR, None), dict_ := ("REBOTE", "black", 186, -0.07, 27.48)], 1105)},
 {"f0": tmap(28.68), "f1": tmap(29.70), "lineas": block([("una guía", "light", 118, TR, None), ("gratuita", "black", 164, -0.09, 29.06)], 1110)},
]
titulos[5]["lineas"][1]["estilo"] = "titulo_verde"
caps = [(1.68, 2.02, "ya llevas"), (2.02, 2.92, "más de 3 dietas"), (2.92, 3.38, "este año"), (3.38, 3.86, "y todas"), (3.86, 4.34, "han terminado en"),
        (10.40, 10.94, "de todo"), (10.94, 11.70, "has probado"), (11.90, 12.82, "y siempre vuelves"), (12.82, 13.70, "al mismo punto"),
        (16.50, 17.45, "que estás siguiendo"),
        (18.40, 19.06, "ella se llama", 1470),
        (21.30, 21.76, "si quieres saber", 1470), (21.76, 22.58, "qué fue lo que hizo", 1470), (22.58, 23.32, "mi clienta", 1470), (23.32, 24.28, "para poder conseguir", 1470), (24.28, 25.20, "estos cambios", 1470),
        (25.20, 25.60, "sin tener"), (25.60, 26.28, "un efecto rebote"), (26.28, 26.75, "luego"),
        (28.15, 28.68, "y te voy a enviar"), (29.70, 30.28, "para que tú también"), (30.28, 30.86, "puedas tener"), (30.86, 31.60, "este cambio"),
        (31.75, 32.40, "y no sufrir"), (32.40, 33.12, "lo mismo de nuevo")]
subs = []
for c in caps:
    d = {"f0": tmap(c[0]), "f1": tmap(c[1]), "texto": c[2]}
    if len(c) > 3: d["base"] = c[3]
    if d["f1"] > d["f0"]: subs.append(d)
P = {"video": f"{V}/basea_{VER}.mp4", "salida": f"{S}/out/AMY_T2_video1_{VER}.mp4", "limpiar_original": False,
     "fuentes": {"light": f"{KIT}/fuentes/Montserrat-Light.ttf", "black": f"{KIT}/fuentes/Montserrat-Black.ttf"},
     "estilo": {
      "subtitulo": {"fuente": "light", "tam": 52.5, "tracking": -0.07, "x_centro": 540, "base": 1081, "sombra_op": 0.55, "sombra_sigma": 5, "sombra_dy": 2},
      "titulo_fino": {"glow_op": 0.28, "glow_sigma": 9, "glow_gan": 1.5, "sombra_op": 0.3, "sombra_sigma": 12},
      "titulo_fuerte": {"glow_op": 0.32, "glow_sigma": 9, "glow_gan": 1.4, "sombra_op": 0.3, "sombra_sigma": 14},
      "titulo_verde": {"color": [62, 237, 28], "glow_op": 0.45, "glow_sigma": 12, "glow_gan": 1.5, "sombra_op": 0.35, "sombra_sigma": 14}},
     "subtitulos": subs, "titulos": titulos, "notas": []}
json.dump(P, open(f"{V}/proyecto_{VER}.json", "w"), ensure_ascii=False, indent=1)
print("cuadros", NF, "= %.2f s" % (NF / FPS)); print([(s[2], o) for s, o in zip(SEG, out0)])
