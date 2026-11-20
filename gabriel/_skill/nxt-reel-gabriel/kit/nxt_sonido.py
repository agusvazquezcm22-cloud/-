"""NXT · pista de efectos con la receta de sonido de Agus.

Fuente de la receta: skill nxt-reel-agus, sección 1 ("Los sonidos están muy bien"):
  - efectos suaves, sincronizados y variados; pico entre 12,5 y 18 dB POR DEBAJO de la voz, nunca arriba;
  - los graves solos (Momo WOOSH, slow woosh, Hit Impact) no se oyen en el celular: siempre con una
    capa de aire (Botanical Whoosh con pasa-bajos, o Deep Mini Whoosh);
  - niveles por tipo de momento (tabla NIVELES);
  - no en cada palabra, nunca pitidos, nunca el mismo sonido muchas veces.

Arma UNA pista de efectos (wav) para mezclar con la voz, y devuelve un informe con el nivel real
de cada sonido y un control de tonos sostenidos (pitidos).
"""
import math
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
# dB por debajo del PICO de la voz
NIVELES = {"golpe": 13.0, "glitch": 14.7, "clic": 15.2, "foto": 15.2, "foco": 16.7,
           "plano": 17.0, "subida": 17.0, "bop": 17.7}
RANGO = (12.5, 18.0)      # todo efecto termina con el pico dentro de este rango bajo la voz
TRANSICION_LU = 14.0      # transiciones: sonoridad 14 dB bajo la de la voz


def leer(ffmpeg, ruta, recorte=None, velocidad=1.0, pasabajos=None, pasaaltos=None):
    af = ["aresample=48000"]
    if abs(velocidad - 1.0) > 1e-3:
        af += [f"asetrate={int(SR * velocidad)}", "aresample=48000"]
    if pasabajos:
        af.append(f"lowpass=f={pasabajos}")
    if pasaaltos:
        af.append(f"highpass=f={pasaaltos}")
    cmd = [ffmpeg, "-v", "error"]
    if recorte:
        cmd += ["-ss", str(recorte[0]), "-t", str(round(recorte[1] - recorte[0], 3))]
    cmd += ["-i", str(ruta), "-af", ",".join(af), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    # fundidos cortos: un recorte nunca deja un clic
    n_in, n_out = min(len(x), int(0.004 * SR)), min(len(x), int(0.06 * SR))
    if n_in:
        x[:n_in] *= np.linspace(0, 1, n_in, dtype=np.float32)[:, None]
    if n_out:
        x[-n_out:] *= np.linspace(1, 0, n_out, dtype=np.float32)[:, None]
    return x


def _db(v):
    return 20 * math.log10(max(1e-9, float(v)))


def pico_db(x):
    return _db(np.abs(x).max()) if len(x) else -180.0


def rms_ventana_db(x, seg=0.4):
    m = x.mean(axis=1).astype(np.float64)
    n = min(len(m), int(seg * SR))
    if n <= 0:
        return -180.0
    c = np.cumsum(np.insert(m ** 2, 0, 0.0))
    return _db(math.sqrt(float(np.max((c[n:] - c[:-n]) / n))))


def _punto_fuerte(x, ms=10):
    m = np.abs(x).max(axis=1).astype(np.float64)
    n = max(1, int(SR * ms / 1000))
    if len(m) <= n:
        return int(np.argmax(m))
    c = np.cumsum(np.insert(m ** 2, 0, 0.0))
    return int(np.argmax(c[n:] - c[:-n])) + n // 2


def armar_evento(ffmpeg, carpeta, ev, pico_voz, voz_lufs):
    capas = []
    for c in ev["capas"]:
        x = leer(ffmpeg, Path(carpeta) / c["archivo"], c.get("recorte"), c.get("velocidad", 1.0),
                 c.get("pasabajos"), c.get("pasaaltos"))
        p = float(np.abs(x).max()) if len(x) else 0.0
        if p <= 0:
            raise SystemExit(f"Sonido vacío: {c['archivo']}")
        x = x / p * (10 ** (c.get("rel_db", 0) / 20))
        alin = c.get("alinear", "pico")
        ancla = len(x) if alin == "fin" else 0 if alin == "inicio" else _punto_fuerte(x)
        ancla -= int(c.get("desfase", 0) * SR)   # desfase > 0: esa capa suena más tarde
        capas.append((x, ancla))
    pre = max(a for _, a in capas)
    largo = max(len(x) - a for x, a in capas) + pre
    buf = np.zeros((largo, 2), np.float32)
    for x, a in capas:
        buf[pre - a: pre - a + len(x)] += x
    tipo = ev["tipo"]
    if tipo == "transicion":
        g = (voz_lufs - TRANSICION_LU) - rms_ventana_db(buf)
    else:
        g = (pico_voz - NIVELES[tipo]) - pico_db(buf)
    pk = pico_db(buf) + g
    pk = min(max(pk, pico_voz - RANGO[1]), pico_voz - RANGO[0])
    g = pk - pico_db(buf) + ev.get("db_extra", 0)
    buf *= 10 ** (g / 20)
    return buf, pre


def tonos_sostenidos(pista, min_dur=0.25):
    """Busca notas sostenidas (pitidos) entre 300 Hz y 6 kHz en la pista de efectos."""
    m = pista.mean(axis=1).astype(np.float64)
    N, H = 2048, 512
    if len(m) < N:
        return []
    win = np.hanning(N)
    k0, k1 = int(300 * N / SR), int(6000 * N / SR)
    marcas = []
    for i in range(1 + (len(m) - N) // H):
        seg = m[i * H: i * H + N]
        if math.sqrt(float(np.mean(seg ** 2))) < 10 ** (-62 / 20):
            marcas.append(None)
            continue
        sp = np.abs(np.fft.rfft(seg * win)) ** 2
        k = int(np.argmax(sp[k0:k1])) + k0
        conc = float(sp[max(0, k - 2): k + 3].sum() / (sp.sum() + 1e-20))
        marcas.append(k if conc > 0.55 else None)
    tonos, i = [], 0
    while i < len(marcas):
        if marcas[i] is None:
            i += 1
            continue
        j = i
        while j + 1 < len(marcas) and marcas[j + 1] is not None and abs(marcas[j + 1] - marcas[j]) <= 1:
            j += 1
        dur = (j - i + 1) * H / SR
        if dur >= min_dur:
            tonos.append((round(i * H / SR, 2), round(marcas[i] * SR / N), round(dur, 2)))
        i = j + 1
    return tonos


def armar_pista(ffmpeg, carpeta, eventos, dur, salida_wav, pico_voz=-1.5, voz_lufs=-14.0):
    """eventos: [{"t": seg, "tipo": ..., "capas": [...], "nota": ...}] con el tiempo ya resuelto."""
    pista = np.zeros((int(dur * SR) + SR, 2), np.float32)
    informe = []
    for ev in sorted(eventos, key=lambda e: e["t"]):
        buf, pre = armar_evento(ffmpeg, carpeta, ev, pico_voz, voz_lufs)
        ini = int(round(ev["t"] * SR)) - pre
        a, b = max(0, ini), min(len(pista), ini + len(buf))
        if b <= a:
            continue
        pista[a:b] += buf[a - ini: b - ini]
        pk = pico_db(buf[a - ini: b - ini])
        informe.append({"t": ev["t"], "tipo": ev["tipo"], "archivos": " + ".join(c["archivo"] for c in ev["capas"]),
                        "pico_dbfs": round(pk, 1), "bajo_voz_db": round(pico_voz - pk, 1),
                        "desde": round(max(0, ini) / SR, 2), "hasta": round(b / SR, 2), "nota": ev.get("nota", "")})
    pista = pista[: int(dur * SR)]
    total = pico_db(pista)
    with wave.open(str(salida_wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(pista, -1, 1) * 32767).astype("<i2").tobytes())
    return informe, round(total, 1), tonos_sostenidos(pista)
