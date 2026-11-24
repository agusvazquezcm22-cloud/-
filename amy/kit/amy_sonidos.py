#!/usr/bin/env python3
"""Mezcla de efectos de sonido para los reels de Amy.
Uso: python3 -I amy_sonidos.py <video_con_audio.mp4> <eventos.json> <carpeta_sonidos_wav> <salida.mp4>
eventos.json: {"fps": 30, "eventos": [{"f": cuadro, "tipo": "clave"}, ...]}
Cada tipo usa un sonido de la carpeta «sonidos» de NXT (convertido a WAV mono 48 kHz) y un pico fijo en dBFS."""
import sys, json, subprocess, wave, numpy as np
SR = 48000
# tipo -> (archivo, pico dBFS, adelanto en s para que el golpe caiga en el cuadro)
MAPA = {"clave":  ("Magnetic_Button_10.wav",      -10.0, 0.0),    # clic de 17 ms: cada palabra clave en verde
        "lista":  ("Mini_list_one_shot.wav",      -11.0, 0.0),    # tic de 11 ms: cada renglón de una lista
        "foto":   ("Deep_Mini_Whoosh_11.wav",     -15.0, 0.30),   # whoosh suave: entra la tarjeta de la foto
        "seguir": ("Button_Cursor_Select_5.wav",  -11.0, 0.0),    # entra la tarjeta Seguir
        "toque":  ("Magnetic_Button_7.wav",       -10.0, 0.0)}    # toque del botón Seguir
def sfx(path, pico):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    a = np.abs(x); act = np.nonzero(a > 0.03 * a.max())[0]; x = x[max(act[0] - 48, 0):]          # sin silencio inicial
    n = min(len(x), int(0.004 * SR)); x[-n:] *= np.linspace(1, 0, n)
    return x / np.abs(x).max() * 10 ** (pico / 20)
def main():
    vid, evj, carpeta, out = sys.argv[1:5]
    ev = json.load(open(evj)); fps = ev.get("fps", 30)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    mix = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); cache = {}
    for e in ev["eventos"]:
        arch, pico, adel = MAPA[e["tipo"]]
        s = cache.setdefault(e["tipo"], sfx(f"{carpeta}/{arch}", pico))
        i = max(int(round((e["f"] / fps - adel) * SR)), 0); j = min(i + len(s), len(mix))
        if j > i: mix[i:j] += s[:j - i, None]
    mix = np.clip(mix, -0.89, 0.89)                                                          # tope en -1 dBFS
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", vid, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-map", "0:v", "-map", "1:a",
                          "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    p.stdin.write(mix.astype(np.float32).tobytes()); p.stdin.close(); p.wait()
    print("sonidos:", len(ev["eventos"]), {t: sum(1 for e in ev["eventos"] if e["tipo"] == t) for t in MAPA})
if __name__ == "__main__": main()
