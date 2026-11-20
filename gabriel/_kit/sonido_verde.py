"""Sonidos del formato pantalla verde: recetas de capas y montaje sobre el video ya renderizado.

Solo archivos del paquete de Naza (Drive, carpeta "sonidos"). Motor: `nxt_sonido.py` (el del video 31).
Las capas son las del config aprobado del 31; nada sintetizado.

Uso (ver `33/sonido33_v01.py`):
    from sonido_verde import *
    EVENTOS = [tr(1.10, SLOW, AIRE_BOT, 'entra la nota'), clic(1.40, MG13, 'recuadro'), ...]
    montar(crudo, video_sin_sonido, salida, EVENTOS, dur, carpeta_sonidos)
"""
import os, subprocess
import nxt_sonido as ns

BOT, DEEP, MOMO, SLOW = 'Botanical Whoosh (1).wav', 'Deep, Mini, Whoosh (11).wav', 'Momo WOOSH 3.mp3', 'slow woosh.mp3'
AIRE_BOT = {'archivo': BOT, 'recorte': [2.3, 4.6], 'pasabajos': 2000, 'rel_db': -3}
AIRE_DEEP = {'archivo': DEEP, 'velocidad': 0.8, 'rel_db': -3}
MG7, MG10, MG13 = 'Magnetic, Button (7).wav', 'Magnetic, Button (10).wav', 'Magnetic, Button (13).wav'
GR1, GR6, CUR = 'Granular, Button, Select (1).wav', 'Granular, Button, Select (6).wav', 'Button, Cursor, Select (5).wav'
L1, L2, O1, O2 = 'Mini list down _1.wav', 'Mini list down _2.wav', 'Mini list (one shot).wav', 'Mini list (one shot)_2.wav'
MONEDA, CUENTA = 'Coin Flip (Spin, Rotation) (1).wav', 'Countdown, List, Numbers (5).wav'
HIT = 'Hit Impact (No FX) (4).wav'
_PLANOS = [[{'archivo': BOT, 'recorte': [2.9, 3.8]}], [{'archivo': DEEP, 'velocidad': 1.2}], [{'archivo': BOT, 'recorte': [2.6, 3.6], 'pasabajos': 6000}],
           [{'archivo': BOT, 'recorte': [3.0, 3.9]}], [{'archivo': BOT, 'recorte': [3.1, 4.1], 'pasabajos': 5000}]]
_n = [0, 0]


def tr(t, grave, aire, nota):
    """Cambio de capitulo: grave (MOMO o SLOW) + capa de aire (AIRE_BOT o AIRE_DEEP). Alternar las cuatro combinaciones."""
    return {'t': t, 'tipo': 'transicion', 'capas': [{'archivo': grave}, aire], 'db_extra': -2, 'nota': nota}


def plano(t, nota):
    """Entrada de un grafico, una tarjeta o un clip: whoosh suave solo. Rota entre cinco variantes."""
    c = _PLANOS[_n[0] % len(_PLANOS)]; _n[0] += 1
    return {'t': t, 'tipo': 'plano', 'capas': c, 'db_extra': -2, 'nota': nota}


def uno(t, tipo, archivo, nota, **k): return {'t': t, 'tipo': tipo, 'capas': [dict(archivo=archivo, **k)], 'db_extra': -2, 'nota': nota}
def clic(t, archivo, nota): return uno(t, 'clic', archivo, nota)
def bop(t, archivo, nota): return uno(t, 'bop', archivo, nota)
def foto(t, nota): return uno(t, 'foto', 'camera shutter sfx (1).mp3', nota, recorte=[0.1, 0.75])
def foco(t, nota): return uno(t, 'foco', 'Camera_Focusing_sound_effect_non_(getmp3.pro).mp3', nota, recorte=[0, 0.8])
def glitch(t, nota): return uno(t, 'glitch', 'Fast Glitch 1.mp3', nota, recorte=[0.25, 0.66], pasabajos=9000)


def golpe(t, nota):
    """Golpe clave (dos por video como mucho): whoosh que termina en el golpe + Hit Impact + boton."""
    a = _n[1] % 2; _n[1] += 1
    w = {'archivo': BOT, 'recorte': [2.36, 2.84], 'alinear': 'fin', 'rel_db': -4} if a == 0 else {'archivo': DEEP, 'recorte': [0.3, 0.99], 'alinear': 'fin', 'rel_db': -4}
    return {'t': t, 'tipo': 'golpe', 'db_extra': -3, 'nota': nota, 'capas': [w, {'archivo': HIT}, {'archivo': MG13 if a == 0 else MG7, 'rel_db': -6}]}


def _medir(wav):
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', wav, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in r.split('\n') if ' I:' in l][-1].split('I:')[1].split('LUFS')[0])
    P = float([l for l in r.split('\n') if 'Peak:' in l][-1].split('Peak:')[1].split('dBFS')[0])
    return I, P


def montar(crudo, video, salida, eventos, dur, sonidos, filtro_voz='highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11'):
    """Voz del crudo (mismo filtro que el render) + pista de efectos -> mezcla con limitador -> se monta sobre `video`
    sin tocar la imagen. Escribe <salida>_sonidos.txt con cada sonido, su tiempo y su nivel."""
    w = os.path.dirname(salida) or '.'
    voz, fx, mez = f'{w}/_voz.wav', f'{w}/_efectos.wav', f'{w}/_mezcla.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', crudo, '-vn', '-af', filtro_voz, '-ar', '48000', '-ac', '2', '-t', str(dur), voz], check=True)
    vI, vP = _medir(voz)
    informe, pico_fx, tonos = ns.armar_pista('ffmpeg', sonidos, eventos, dur, fx, pico_voz=vP, voz_lufs=vI)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voz, '-i', fx, '-filter_complex', '[0:a][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=false:attack=3:release=60', '-ar', '48000', mez], check=True)
    mI, mP = _medir(mez)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', mez, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(dur), '-movflags', '+faststart', salida], check=True)
    L = ['%6.2fs %-10s %4.1f dB bajo la voz (%6.1f dBFS)  %s | %s' % (e['t'], e['tipo'], e['bajo_voz_db'], e['pico_dbfs'], e['archivos'], e['nota']) for e in informe]
    usos = {}
    for e in eventos:
        for c in e['capas']: usos[c['archivo']] = usos.get(c['archivo'], 0) + 1
    L += ['', 'Sonidos: %d en %.1f s · archivos distintos: %d (todos del paquete de Naza)' % (len(informe), dur, len(usos)),
          'Veces que se usa cada archivo: ' + ', '.join('%s x%d' % (k, v) for k, v in sorted(usos.items(), key=lambda x: -x[1])),
          'Voz: %.1f LUFS, pico %.1f dBFS' % (vI, vP),
          'Pico de toda la pista de efectos: %.1f dBFS (%.1f dB bajo el pico de la voz)' % (pico_fx, vP - pico_fx),
          'Mezcla final: %.1f LUFS, pico %.1f dBFS' % (mI, mP),
          'Tonos sostenidos (pitidos) entre 300 Hz y 6 kHz: ' + (', '.join('%.2fs %d Hz %.2fs' % t for t in tonos) if tonos else 'ninguno')]
    open(salida.replace('.mp4', '_sonidos.txt'), 'w').write('\n'.join(L) + '\n')
    for f in (voz, fx, mez): os.remove(f)
    return L
