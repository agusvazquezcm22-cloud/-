#!/usr/bin/env python3
"""Amy · Tanda 2 · video 1 (efecto rebote). Montaje base + proyecto de texto, estilo minimalista.
Uso: python3 -I video1_montaje.py <carpeta_trabajo> <kit> <version>"""
import sys, os, json, subprocess, numpy as np, cv2
S, KIT, VER = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, KIT); import amytext as T, amy_seguir as SEG_CARD
V = f"{S}/v1"; FPS = 30; W, H = 1080, 1920
FU = {"light": f"{KIT}/fuentes/Montserrat-Light.ttf", "semibold": f"{KIT}/fuentes/Montserrat-SemiBold.ttf"}
VERDE = [188, 205, 157]                      # verde de marca (tomado de la portada «MI MÉTODO»)
g = lambda t: round(t * FPS) / FPS           # todo a la grilla de cuadros: audio y video cortan igual
# Cortes: solo en silencios medidos (>= 0,25 s), dejando aire antes y después de la voz.
# Se salta 17,48 -> 21,12: fuera «ella se llama…» (frase que Amy deja cortada) y su pausa.
SEG = [(0.90, 1.66, "med", {}), (1.66, 5.42, "close", {}),
       (5.70, 11.72, "med", {}),
       (11.86, 13.72, "br_squat", {"in": 2.0}),
       (14.08, 15.42, "close", {}), (15.42, 17.48, "med", {}),
       (21.12, 25.20, "wide", {"foto": True}),
       (25.20, 26.80, "close", {}), (26.80, 28.15, "med", {}),
       (28.15, 29.85, "br_rdl", {"in": 2.6}), (29.85, 31.62, "br_crunch", {"in": 3.0}),
       (31.62, 33.20, "close", {})]
SEG = [(g(a), g(b), s, e) for a, b, s, e in SEG]
FIN = 10                                      # cola: 1/3 s sobre el último cuadro para que no termine en seco
T_SEGUIR = 31.80                              # la tarjeta Seguir entra mientras Amy dice la última frase
out0 = []; n = 0
for a, b, src, ex in SEG:
    k = int(round((b - a) * FPS)); out0.append((n, n + k)); n += k
NV = n; NF = NV + FIN
def tmap(t):
    for (a, b, _, _), (o0, o1) in zip(SEG, out0):
        if a - 1e-6 <= t <= b + 1e-6: return min(o0 + int(round((t - a) * FPS)), o1)
    for i in range(len(SEG) - 1):
        if SEG[i][1] < t < SEG[i + 1][0]: return out0[i][1]
    return 0 if t < SEG[0][0] else NV

# ---- tarjeta de la foto antes/después ----
CW = 780; CX, CY = 150, 105
ph = cv2.imread(f"{S}/t2raw/v1_antes_despues.png", cv2.IMREAD_UNCHANGED)[..., :3]
ph = cv2.resize(ph, (CW, CW), interpolation=cv2.INTER_AREA).astype(np.float32)
lab = np.zeros((CW, CW), np.float32)
for txt, cx in (("antes", CW * 0.25), ("después", CW * 0.75)): T.draw_line(lab, txt, FU["light"], 50, -0.07, cx, CW - 36, "center")
shd = np.clip(cv2.GaussianBlur(lab, (0, 0), 5) * 1.8, 0, 1) * 0.6
ph = ph * (1 - shd[..., None]); ph += (255 - ph) * lab[..., None]
mask = np.zeros((CW, CW), np.float32); cv2.rectangle(mask, (40, 0), (CW - 40, CW), 1, -1); cv2.rectangle(mask, (0, 40), (CW, CW - 40), 1, -1)
for cx, cy in ((40, 40), (CW - 40, 40), (40, CW - 40), (CW - 40, CW - 40)): cv2.circle(mask, (cx, cy), 40, 1, -1, cv2.LINE_AA)
mask = cv2.GaussianBlur(mask, (0, 0), 0.8); pad = 60
shadow = np.zeros((CW + 2 * pad, CW + 2 * pad), np.float32); shadow[pad:-pad, pad:-pad] = mask; shadow = cv2.GaussianBlur(shadow, (0, 0), 22) * 0.5
def put_card(img, k):
    p = min(k / 12.0, 1.0); o = 1 - (1 - p) ** 2; dy = int(round(60 * (1 - p) ** 2)); y, x = CY + dy, CX
    r = img[y - pad:y + CW + pad, x - pad:x + CW + pad].astype(np.float32); r *= (1 - shadow * o)[..., None]
    img[y - pad:y + CW + pad, x - pad:x + CW + pad] = r.astype(np.uint8)
    r = img[y:y + CW, x:x + CW].astype(np.float32); a = (mask * o)[..., None]
    img[y:y + CW, x:x + CW] = (r * (1 - a) + ph * a).astype(np.uint8)

mux = f"{V}/basea_{VER}.mp4"
if "--solo-json" not in sys.argv:
    base = f"{V}/base_{VER}.mp4"; aud = f"{V}/audio_{VER}.m4a"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", base], stdin=subprocess.PIPE)
    caps = {}; foto0 = None; avatar = cv2.imread(f"{V}/avatar.png"); f_seg = tmap(T_SEGUIR)
    for (a, b, src, ex), (o0, o1) in zip(SEG, out0):
        c = caps.setdefault(src, cv2.VideoCapture(f"{V}/{src}.mp4"))
        c.set(cv2.CAP_PROP_POS_FRAMES, int(round((ex["in"] if "in" in ex else a) * FPS)))
        if ex.get("foto") and foto0 is None: foto0 = o0
        for f in range(o0, o1):
            ok, img = c.read()
            if not ok: img = last.copy()          # el crudo termina justo al final de la voz
            last = img.copy()
            if ex.get("foto"): put_card(img, f - foto0)
            if f >= f_seg: SEG_CARD.dibujar(img, f - f_seg, avatar, cy=1330)
            enc.stdin.write(img.tobytes())
    for k in range(FIN):                           # cola sobre el último cuadro, con la tarjeta ya en «Siguiendo»
        img = last.copy(); SEG_CARD.dibujar(img, NV + k - f_seg, avatar, cy=1330)
        enc.stdin.write(img.tobytes())
    enc.stdin.close(); enc.wait()
    # audio: mismas uniones que el video; 8 ms de fundido en cada una; cola de ambiente que se apaga
    pieces = []; j = 0
    while j < len(SEG):
        a, b = SEG[j][0], SEG[j][1]
        while j + 1 < len(SEG) and abs(SEG[j + 1][0] - b) < 1e-6: j += 1; b = SEG[j][1]
        pieces.append((a, b)); j += 1
    fc = ""; lab_ = []
    for i, (a, b) in enumerate(pieces):
        d = b - a; fc += f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.4f}:d=0.008,apad=whole_dur={d:.4f}[a{i}];"; lab_.append(f"[a{i}]")
    fd = FIN / FPS
    fc += f"[0:a]atrim=19.50:20.00,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=0.05:d=0.27,atrim=0:{fd:.4f},apad=whole_dur={fd:.4f}[tail];"
    fc += "".join(lab_) + f"[tail]concat=n={len(pieces) + 1}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[o]"
    # ruido de gimnasio: reductor de voz (RNNoise, modelo bd) al 80 %: baja el fondo ~12 dB y la voz casi no cambia
    limpia = f"{V}/voz_limpia.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{S}/t2raw/v1_IMG_1732.MOV", "-vn", "-ac", "1", "-ar", "48000", "-af", f"highpass=f=80,arnndn=m={S}/nr/bd.rnnn:mix=0.8", limpia], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", limpia, "-filter_complex", fc, "-map", "[o]", "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "256k", aud], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", aud, "-map", "0:v", "-map", "1:a", "-c", "copy", mux], check=True)
    json.dump({"piezas_audio": pieces, "segmentos": [(s[0], s[1], s[2], o) for s, o in zip(SEG, out0)]}, open(f"{V}/cortes_{VER}.json", "w"))

# ---- texto ----
TR = -0.07; TS = 52.5
def adv(txt, fu, tam): return T.line_alpha(txt, FU[fu], tam, TR)[1]
subs, notas = [], []
def cap(t0, t1, partes, base=1081):
    """partes: texto simple o lista [(texto, clave?)]. Las claves van en SemiBold verde dentro de la misma línea."""
    f0, f1 = tmap(t0), tmap(t1)
    if f1 <= f0: return
    if isinstance(partes, str): subs.append({"f0": f0, "f1": f1, "texto": partes, "base": base}); return
    ws = [adv(t, "semibold" if k else "light", TS) for t, k in partes]; tot = sum(ws) + TR * TS * (len(partes) - 1); x = 540 - tot / 2
    for (t, k), w in zip(partes, ws):
        notas.append({"f0": f0, "f1": f1, "estilo": "clave" if k else "sub_parte", "lineas": [dict(texto=t, fuente="semibold" if k else "light", tam=TS, tracking=TR, x=round(x, 1), base=base)]})
        x += w + TR * TS
def titulo(t0, t1, l1, l2, tv2, tam=92, base=1090):
    w = max(adv(l1, "light", tam), adv(l2, "semibold", tam)); x = round(540 - w / 2, 1)
    return {"f0": tmap(t0), "f1": tmap(t1), "lineas": [dict(texto=l1, fuente="light", tam=tam, tracking=TR, x=x, base=base, estilo="titulo_fino"),
                                                      dict(texto=l2, fuente="semibold", tam=tam, tracking=TR, x=x, base=base + round(0.9 * tam), estilo="titulo_clave", f_ver=tmap(tv2))]}
titulos = [titulo(0.90, 1.66, "Déjame", "adivinar", 1.30),
           titulo(4.56, 5.42, "efecto", "rebote", 5.00),
           {"f0": tmap(5.86), "f1": tmap(10.60), "lineas": [dict(texto=t, fuente="light", tam=60, tracking=TR, x=150, base=1030 + 74 * i, estilo="titulo_fino", f_ver=tmap(tv)) for i, (t, tv) in enumerate((("dieta cetogénica", 6.10), ("dieta keto", 7.28), ("eliminar carbohidratos", 8.22), ("ayuno intermitente", 9.54)))]},
           titulo(15.46, 16.56, "el problema es", "el método", 16.04),
           titulo(26.98, 28.15, "comenta", "REBOTE", 27.66)]
cap(1.70, 2.14, "ya llevas"); cap(2.14, 2.96, [("más de ", 0), ("3 dietas", 1)]); cap(2.96, 3.44, "este año"); cap(3.44, 3.76, "y todas"); cap(3.76, 4.56, "han terminado en")
cap(10.66, 11.02, "de todo"); cap(11.02, 11.72, "has probado"); cap(11.86, 12.92, "y siempre vuelves"); cap(12.92, 13.72, [("al ", 0), ("mismo punto", 1)])
cap(14.08, 14.64, "el problema"); cap(14.64, 15.42, [("no lo tienes ", 0), ("tú", 1)]); cap(16.56, 17.48, "que estás siguiendo")
B2 = 1470
cap(21.12, 21.84, "si quieres saber", B2); cap(21.84, 22.68, "qué fue lo que hizo", B2); cap(22.68, 23.40, "mi clienta", B2); cap(23.40, 24.42, "para poder conseguir", B2); cap(24.42, 25.20, [("estos ", 0), ("cambios", 1)], B2)
cap(25.20, 25.74, "sin tener"); cap(25.74, 26.38, [("un ", 0), ("efecto rebote", 1)]); cap(26.38, 26.80, "luego")
cap(28.15, 28.78, "y te voy a enviar"); cap(28.78, 29.68, [("una ", 0), ("guía gratuita", 1)]); cap(29.68, 30.46, "para que tú también"); cap(30.46, 30.92, "puedas tener"); cap(30.92, 31.62, "este cambio")
cap(31.62, 32.46, "y no sufrir"); cap(32.46, 33.20, "lo mismo de nuevo")
SH = {"sombra_op": 0.55, "sombra_sigma": 5, "sombra_dy": 2}; SH2 = {"sombra_op": 0.5, "sombra_sigma": 9, "sombra_dy": 2}
P = {"video": mux, "salida": f"{S}/out/AMY_T2_video1_{VER}_master.mp4", "limpiar_original": False, "fuentes": FU,
     "estilo": {"subtitulo": {"fuente": "light", "tam": TS, "tracking": TR, "x_centro": 540, "base": 1081, **SH}, "sub_parte": SH, "clave": {"color": VERDE, **SH},
                "titulo_fino": SH2, "titulo_clave": {"color": VERDE, **SH2}},
     "subtitulos": subs, "titulos": titulos, "notas": notas}
json.dump(P, open(f"{V}/proyecto_{VER}.json", "w"), ensure_ascii=False, indent=1)
ev = [{"f": n_["f0"], "tipo": "clave"} for n_ in notas if n_["estilo"] == "clave"]
for t_ in titulos:
    for ln in t_["lineas"]:
        if ln.get("estilo") == "titulo_clave": ev.append({"f": ln["f_ver"], "tipo": "clave"})
        elif ln["tam"] == 60: ev.append({"f": ln["f_ver"], "tipo": "lista"})
ev += [{"f": [o for s_, o in zip(SEG, out0) if s_[3].get("foto")][0][0], "tipo": "foto"}, {"f": tmap(T_SEGUIR), "tipo": "seguir"}, {"f": tmap(T_SEGUIR) + SEG_CARD.TAP, "tipo": "toque"}]
json.dump({"fps": FPS, "eventos": sorted(ev, key=lambda e: e["f"])}, open(f"{V}/eventos_{VER}.json", "w"))
print("cuadros", NF, "= %.2f s" % (NF / FPS), "| sonidos", len(ev))
