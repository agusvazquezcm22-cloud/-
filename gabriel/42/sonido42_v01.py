"""Video 42 («La trampa del descuento») · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos), final con la voz.
Uso: python3 sonido42_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v42')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 58.5
EVENTOS = [
    foto(1.28, 'hook: Extra Life'), foto(2.80, 'hook: Huel'),
    tr(3.94, SLOW, AIRE_BOT, 'anuncio de Huel: welcome kit'),
    clic(5.25, MG13, 'subrayado: lleva una botella gratis'),
    golpe(6.10, 'golpe clave 1 de 2: 20% OFF'),
    bop(7.15, O1, 'la etiqueta se corre'), bop(7.35, L2, 'entra el regalo'),
    plano(8.12, 'Extra Life'),
    plano(9.40, 'grafico: la cabeza'), bop(10.50, MONEDA, 'la etiqueta en la cabeza'),
    plano(10.98, 'clientes de Extra Life'),
    plano(13.72, 'grafico: vale menos'), bop(13.84, O2, 'etiqueta'), glitch(16.02, 'se achica: vale menos'),
    foto(16.80, 'Huel'),
    plano(17.68, 'grafico: calendario'), bop(18.13, L1, 'descuento 1'), bop(18.45, L2, 'descuento 2'), bop(18.77, O1, 'descuento 3'), bop(19.09, O2, 'descuento 4'),
    tr(19.60, MOMO, AIRE_DEEP, 'lo que hace que destaquen'),
    foto(21.62, 'Extra Life'),
    plano(23.50, 'grafico: facil hacerlo mal'), glitch(24.00, 'signo !'),
    tr(25.74, SLOW, AIRE_BOT, 'relacionado con tu producto'),
    foto(28.76, 'lo que tu cliente necesita'),
    plano(31.68, 'grafico: llavero y cupon'), bop(32.78, L1, 'llavero'), bop(33.28, L2, 'cupon'), glitch(33.73, 'se apagan'),
    golpe(34.12, 'golpe clave 2 de 2: te regala un shaker'),
    plano(37.04, 'Extra Life en la farmacia'),
    plano(39.14, 'grafico: las ventas'), bop(39.70, O1, 'se frenan'), bop(40.12, CUENTA, 'aparece el boton'), clic(41.52, MG7, 'zoom al boton'), clic(42.04, GR1, 'boton apretado'),
    plano(42.94, 'Extra Life'),
    tr(44.88, MOMO, AIRE_BOT, 'Huel lo entendio'), clic(47.84, MG10, 'recuadro: free t-shirt and shaker'),
    plano(49.92, 'experiencia del cliente'),
    foto(52.72, 'mandaselo'), foto(54.22, 'Huel'),
    plano(55.88, 'cierre: Huel en su dia'), clic(56.08, GR6, 'aparece el texto final'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo42.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
