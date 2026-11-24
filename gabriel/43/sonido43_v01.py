"""Video 43 (VS Dirtea vs Let Loose) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos); termina con la voz.
Uso: python3 sonido43_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v43')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 71.93
EVENTOS = [
    foto(1.28, 'hook: caja DIRTEA'), foto(2.40, 'hook: DIRTEA en polvo'),
    tr(3.38, SLOW, AIRE_BOT, 'DIRTEA'),
    bop(4.78, O1, 'chai'), bop(5.20, L2, 'cacao'), bop(5.66, L1, 'gomitas'),
    plano(6.04, 'grafico x3'), bop(7.32, MONEDA, 'x3'),
    tr(8.72, MOMO, AIRE_DEEP, 'Let Loose'),
    plano(11.20, 'grafico 2 M'), bop(11.54, CUENTA, 'contador'), bop(12.54, MONEDA, 'US$2 M'),
    plano(13.84, 'pantalla dividida'), glitch(14.04, 'signo de pregunta'),
    tr(17.66, SLOW, AIRE_BOT, 'capitulo: las ofertas de DIRTEA'),
    foto(19.04, 'Black Friday'),
    clic(22.32, MG13, 'recuadro: 40% off & free gifts'),
    plano(23.70, 'grafico 50%'), bop(24.78, CUENTA, '40 a 50'),
    foto(26.36, 'otra mas'),
    plano(28.68, 'clienta'),
    plano(31.74, 'grafico: cuando comprar'), bop(31.98, O1, '40'), bop(32.76, L2, '50'), bop(33.62, L1, 'la siguiente'),
    tr(34.96, MOMO, AIRE_DEEP, 'capitulo: Let Loose'),
    plano(37.46, 'una historia'),
    plano(39.98, 'fundadora'),
    plano(41.74, 'bandeja de entrada'),
    golpe(44.28, 'golpe clave 1 de 2: el correo'),
    plano(44.66, 'correos de DIRTEA'), bop(45.38, CUENTA, '32 correos'), bop(46.70, MONEDA, 'en 30 dias'),
    plano(49.28, 'bienvenida de Let Loose'), bop(51.64, CUENTA, '9 correos'),
    bop(52.46, O1, 'sobres'),
    foto(53.36, 'una sola cosa'), foto(55.28, 'quien la creo'), foto(56.16, 'por que funciona'), foto(56.94, 'en que se diferencia'), foto(57.78, 'que dicen sus clientes'),
    plano(58.78, 'correo de la fundadora'), clic(59.80, GR1, 'recuadro: Founder'),
    tr(62.06, SLOW, AIRE_BOT, 'cierre: las dos marcas'),
    golpe(66.10, 'golpe clave 2 de 2: la pregunta final'),
    clic(71.00, MG7, 'aparece comentarios'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo43.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
