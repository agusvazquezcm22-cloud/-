#!/usr/bin/env python3
"""Amy · Tanda 2 · video 2 (rutina con banda): tarjeta Seguir sobre el cierre + proyecto de texto.
Uso: python3 -I video2_texto.py <base.mp4> <avatar.png> <kit> <salida_base.mp4> <proyecto.json> <salida_final.mp4>"""
import sys, json, subprocess, cv2, numpy as np
BASE, AVATAR, KIT, BASE2, PROY, SALIDA = sys.argv[1:7]
sys.path.insert(0, KIT); import amytext as T, amy_seguir as C
FU = {"light": f"{KIT}/fuentes/Montserrat-Light.ttf", "semibold": f"{KIT}/fuentes/Montserrat-SemiBold.ttf"}
VERDE = [188, 205, 157]; TR = -0.07; TS = 52.5; CIERRE = 540
cap = cv2.VideoCapture(BASE); av = cv2.imread(AVATAR)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-", "-i", BASE, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-c:a", "copy", BASE2], stdin=subprocess.PIPE)
f = 0
while True:
    ok, img = cap.read()
    if not ok: break
    if f >= CIERRE + 8: C.dibujar(img, f - CIERRE - 8, av)
    enc.stdin.write(img.tobytes()); f += 1
enc.stdin.close(); enc.wait()
adv = lambda t, fu, tam: T.line_alpha(t, FU[fu], tam, TR)[1]
subs, notas = [], []
def c(f0, f1, partes, base=1081):
    if isinstance(partes, str): subs.append({"f0": f0, "f1": f1, "texto": partes, "base": base}); return
    ws = [adv(t, "semibold" if k else "light", TS) for t, k in partes]; x = 540 - (sum(ws) + TR * TS * (len(partes) - 1)) / 2
    for (t, k), w in zip(partes, ws):
        notas.append({"f0": f0, "f1": f1, "estilo": "clave" if k else "sub_parte", "lineas": [dict(texto=t, fuente="semibold" if k else "light", tam=TS, tracking=TR, x=round(x, 1), base=base)]}); x += w + TR * TS
c(75, 135, "sin hacer esto antes"); c(135, 225, [("3 ejercicios ", 1), ("con banda", 0)]); c(225, 300, [("menos ", 0), ("lesiones", 1)])
c(300, 375, [("más ", 0), ("movilidad", 1)]); c(375, 465, [("y mejor ", 0), ("postura", 1)]); c(465, 540, "guárdalo para tu próximo entreno")
tam = 92; w = max(adv("no entrenes", "light", tam), adv("tren superior", "semibold", tam)); x = round(540 - w / 2, 1)
SH = {"sombra_op": 0.55, "sombra_sigma": 5, "sombra_dy": 2}; SH2 = {"sombra_op": 0.5, "sombra_sigma": 9, "sombra_dy": 2}
P = {"video": BASE2, "salida": SALIDA, "limpiar_original": False, "fuentes": FU,
     "estilo": {"subtitulo": {"fuente": "light", "tam": TS, "tracking": TR, "x_centro": 540, "base": 1081, **SH}, "sub_parte": SH, "clave": {"color": VERDE, **SH}, "titulo_fino": SH2, "titulo_clave": {"color": VERDE, **SH2}},
     "subtitulos": subs, "notas": notas,
     "titulos": [{"f0": 3, "f1": 75, "lineas": [dict(texto="no entrenes", fuente="light", tam=tam, tracking=TR, x=x, base=1090, estilo="titulo_fino"),
                                               dict(texto="tren superior", fuente="semibold", tam=tam, tracking=TR, x=x, base=1090 + round(0.9 * tam), estilo="titulo_clave", f_ver=20)]}]}
json.dump(P, open(PROY, "w"), ensure_ascii=False, indent=1); print("ok", f)
