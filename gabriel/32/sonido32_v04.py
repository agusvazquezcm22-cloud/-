"""Video 32 (IM8) · v04 = imagen de la v03 + pista de efectos.

Sonidos: SOLO los del paquete de Naza (Drive, carpeta "sonidos"), el mismo que se uso en el video 31.
Motor y receta: `_kit/nxt_sonido.py`, tal cual el del 31 (niveles bajo el pico de la voz, graves siempre con
capa de aire, sin pitidos). Las capas de transicion, plano, golpe, glitch, foto, foco, bop y clic estan copiadas
del config aprobado del 31 (`gabriel31_v13.json`); lo nuevo usa archivos del mismo paquete.
Nada sintetizado.
"""
import os, sys, json, subprocess
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
import nxt_sonido as ns

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad')
SON = f'{A}/sonidos'
DUR = 76.5
VIDEO = sys.argv[1]; SALIDA = sys.argv[2]
W = os.path.dirname(SALIDA) or '.'

BOT, DEEP, MOMO, SLOW = 'Botanical Whoosh (1).wav', 'Deep, Mini, Whoosh (11).wav', 'Momo WOOSH 3.mp3', 'slow woosh.mp3'
AIRE_BOT = {'archivo': BOT, 'recorte': [2.3, 4.6], 'pasabajos': 2000, 'rel_db': -3}
AIRE_DEEP = {'archivo': DEEP, 'velocidad': 0.8, 'rel_db': -3}
def tr(t, grave, aire, nota): return {'t': t, 'tipo': 'transicion', 'capas': [{'archivo': grave}, aire], 'db_extra': -2, 'nota': nota}
PLANOS = [[{'archivo': BOT, 'recorte': [2.9, 3.8]}], [{'archivo': DEEP, 'velocidad': 1.2}], [{'archivo': BOT, 'recorte': [2.6, 3.6], 'pasabajos': 6000}],
          [{'archivo': BOT, 'recorte': [3.0, 3.9]}], [{'archivo': BOT, 'recorte': [3.1, 4.1], 'pasabajos': 5000}]]
_np = [0]
def plano(t, nota):
    c = PLANOS[_np[0] % len(PLANOS)]; _np[0] += 1
    return {'t': t, 'tipo': 'plano', 'capas': c, 'db_extra': -2, 'nota': nota}
def uno(t, tipo, archivo, nota, **k): return {'t': t, 'tipo': tipo, 'capas': [dict(archivo=archivo, **k)], 'db_extra': -2, 'nota': nota}
MG7, MG10, MG13 = 'Magnetic, Button (7).wav', 'Magnetic, Button (10).wav', 'Magnetic, Button (13).wav'
GR1, GR6, CUR = 'Granular, Button, Select (1).wav', 'Granular, Button, Select (6).wav', 'Button, Cursor, Select (5).wav'
L1, L2, O1, O2 = 'Mini list down _1.wav', 'Mini list down _2.wav', 'Mini list (one shot).wav', 'Mini list (one shot)_2.wav'
MONEDA, CUENTA = 'Coin Flip (Spin, Rotation) (1).wav', 'Countdown, List, Numbers (5).wav'
FOTO = {'recorte': [0.1, 0.75]}

T_CONTRARIO, T_BECKHAM = float(sys.argv[3]), float(sys.argv[4])    # cuando aparece cada palabra clave (del config de imagen)

EVENTOS = [
    tr(1.56, SLOW, AIRE_BOT, 'entra el comunicado (primera prueba)'),
    uno(2.06, 'clic', MG13, 'recuadro en los 23,7 M'),
    plano(4.06, 'grafico: linea de tiempo'),
    uno(8.29, 'bop', L1, 'aparece el sobre (16 -> 1)'),
    uno(8.88, 'foto', 'camera shutter sfx (1).mp3', 'rafaga de anuncios', **FOTO),
    tr(11.44, MOMO, AIRE_BOT, 'capitulo: Empecemos con sus anuncios'),
    uno(15.16, 'glitch', 'Fast Glitch 1.mp3', 'se tacha "Su producto"', recorte=[0.25, 0.66], pasabajos=9000),
    uno(15.74, 'bop', O1, 'lista: articulaciones'), uno(16.92, 'bop', O2, 'lista: cansancio'),
    uno(17.48, 'bop', L2, 'lista: digestion'), uno(17.92, 'bop', L1, 'lista: menopausia'),
    plano(18.40, 'tarjeta del anuncio para escepticos'),
    uno(20.80, 'clic', MG7, 'recuadro en el contador de la Biblioteca'),
    tr(23.86, MOMO, AIRE_DEEP, 'capitulo: Pero por que hacen esto'),
    uno(25.44, 'clic', CUR, 'flecha al boton Shop Now'),
    plano(28.14, 'entra la pagina'),
    uno(29.20, 'clic', GR1, 'recuadro: estudios'), uno(29.88, 'clic', MG10, 'recuadro: ingredientes'),
    uno(30.38, 'clic', GR6, 'recuadro: famosos'), uno(30.90, 'clic', MG13, 'recuadro: comparacion'),
    uno(32.40, 'clic', MG7, 'recuadro: garantia'),
    tr(36.24, SLOW, AIRE_DEEP, 'capitulo: Pero aqui viene lo interesante'),
    {'t': 38.70, 'tipo': 'golpe', 'db_extra': -3, 'nota': 'golpe clave 1 de 2: recuadro en los 285 dolares',
     'capas': [{'archivo': BOT, 'recorte': [2.36, 2.84], 'alinear': 'fin', 'rel_db': -4}, {'archivo': 'Hit Impact (No FX) (4).wav'}, {'archivo': MG13, 'rel_db': -6}]},
    uno(41.20, 'clic', MG10, 'recuadro: about six months'),
    uno(41.98, 'bop', CUENTA, 'se llenan los meses del calendario'),
    uno(44.32, 'bop', MONEDA, 'moneda en la primera compra'),
    {'t': T_CONTRARIO, 'tipo': 'golpe', 'db_extra': -3, 'nota': 'golpe clave 2 de 2: lo contrario',
     'capas': [{'archivo': DEEP, 'recorte': [0.3, 0.99], 'alinear': 'fin', 'rel_db': -4}, {'archivo': 'Hit Impact (No FX) (4).wav'}, {'archivo': MG7, 'rel_db': -6}]},
    tr(47.24, SLOW, AIRE_BOT, 'capitulo: mira como suben el ticket'),
    uno(48.52, 'bop', O1, 'lista: plan de 3 meses'), uno(49.96, 'bop', O2, 'lista: kit de regalo'),
    uno(50.64, 'bop', L2, 'lista: envio gratis'), uno(51.38, 'bop', L1, 'lista: garantia'),
    plano(51.94, 'entra la clienta con su pedido'),
    uno(56.16, 'clic', GR6, 'aparece "1 cliente"'),
    uno(58.70, 'bop', MONEDA, 'monedas: cobrarte cada 3 meses'),
    uno(62.02, 'clic', MG13, 'recuadro en 4.1x'),
    plano(64.10, 'entra el clip de la caja'),
    tr(67.90, SLOW, AIRE_DEEP, 'sube la flecha del costo'),
    tr(69.24, MOMO, AIRE_BOT, 'cierre: muro de anuncios'),
    uno(71.10, 'foto', 'camera shutter sfx (1).mp3', 'cierre: anuncios en video', **FOTO),
    uno(72.78, 'foco', 'Camera_Focusing_sound_effect_non_(getmp3.pro).mp3', 'cierre: su oferta', recorte=[0, 0.8]),
    uno(73.55, 'clic', CUR, 'recuadro: solo suscriptores'),
    uno(75.22, 'bop', L1, 'vuelve la portada'),
    uno(T_BECKHAM, 'clic', MG7, 'aparece BECKHAM'),
]

def medir(wav):
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', wav, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in r.split('\n') if ' I:' in l][-1].split('I:')[1].split('LUFS')[0])
    P = float([l for l in r.split('\n') if 'Peak:' in l][-1].split('Peak:')[1].split('dBFS')[0])
    return I, P

voz = f'{W}/_voz32.wav'; fx = f'{W}/_efectos32.wav'; mez = f'{W}/_mezcla32.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{A}/dl/crudo32.mp4', '-vn', '-af', 'highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', '-t', str(DUR), voz], check=True)
vI, vP = medir(voz)
informe, pico_fx, tonos = ns.armar_pista('ffmpeg', SON, EVENTOS, DUR, fx, pico_voz=vP, voz_lufs=vI)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voz, '-i', fx, '-filter_complex', '[0:a][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=false:attack=3:release=60', '-ar', '48000', mez], check=True)
mI, mP = medir(mez)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO, '-i', mez, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(DUR), '-movflags', '+faststart', SALIDA], check=True)
L = []
for e in informe:
    L.append('%6.2fs %-10s %4.1f dB bajo la voz (%6.1f dBFS)  %s | %s' % (e['t'], e['tipo'], e['bajo_voz_db'], e['pico_dbfs'], e['archivos'], e['nota']))
usos = {}
for e in EVENTOS:
    for c in e['capas']: usos[c['archivo']] = usos.get(c['archivo'], 0) + 1
L += ['', 'Sonidos: %d · archivos distintos: %d (todos del paquete de Naza)' % (len(informe), len(usos)),
      'Veces que se usa cada archivo: ' + ', '.join('%s x%d' % (k, v) for k, v in sorted(usos.items(), key=lambda x: -x[1])),
      'Voz: %.1f LUFS, pico %.1f dBFS' % (vI, vP),
      'Pico de toda la pista de efectos: %.1f dBFS (%.1f dB bajo el pico de la voz)' % (pico_fx, vP - pico_fx),
      'Mezcla final: %.1f LUFS, pico %.1f dBFS' % (mI, mP),
      'Tonos sostenidos (pitidos) entre 300 Hz y 6 kHz: ' + (', '.join('%.2fs %d Hz %.2fs' % t for t in tonos) if tonos else 'ninguno')]
open(SALIDA.replace('.mp4', '_sonidos.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L[-7:]))
