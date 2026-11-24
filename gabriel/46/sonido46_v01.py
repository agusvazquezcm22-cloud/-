"""Video 46 («Creadores que se quedan», Liquid I.V. + Bloom) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos);
termina con la voz (sin cola ni sonido de cierre despues).
Uso: python3 sonido46_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v46')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 77.9
EVENTOS = [
    foto(1.05, 'hook: creadora de Bloom'),
    plano(2.10, 'tarjeta de la Biblioteca'), clic(2.35, MG13, 'recuadro: Edward Digges with Liquid I.V.'), bop(3.05, O1, 'subrayado: #LiquidIVPartner'),
    foto(3.86, 'rafaga 1'), foto(4.63, 'rafaga 2'), foto(5.40, 'rafaga 3'), foto(6.17, 'rafaga 4'),
    tr(6.94, SLOW, AIRE_BOT, 'marca 1: Liquid I.V.'),
    plano(8.70, 'Entrepreneur'), clic(9.75, MG7, 'recuadro: over $1 billion'), bop(9.72, CUENTA, 'contador arranca'), bop(10.62, MONEDA, 'US$1.000 M'),
    plano(11.26, 'creador de Liquid I.V.'), plano(12.92, 'creadora'),
    clic(15.12, GR1, 'recuadro: one-to-one'), clic(15.73, GR6, 'recuadro: sharing ideas'), clic(17.29, CUR, 'recuadro: on our minds'),
    clic(19.98, MG10, 'recuadro: most powerful insights'), clic(20.72, MG13, 'recuadro: connections to marketing'),
    plano(20.98, 'grafico: ideas'), bop(21.43, L2, 'foco'),
    tr(22.08, MOMO, AIRE_DEEP, 'marca 2: Bloom'),
    foto(23.42, 'latas'), foto(24.40, 'proteina'), foto(24.78, 'gomitas'), foto(25.16, 'para mujeres'), foto(25.60, 'a lo grande'),
    plano(27.10, 'grafico: muestras'), bop(27.25, CUENTA, 'contador de muestras'), bop(29.05, MONEDA, '20.000'),
    plano(29.32, 'creadora'), foto(30.42, 'rafaga creadoras 1'), foto(30.94, 'rafaga 2'), foto(31.46, 'rafaga 3'),
    plano(31.98, 'grafico: se apagan'), glitch(33.03, '1 video y chao'),
    tr(33.96, SLOW, AIRE_BOT, 'el grupo'), bop(35.78, O1, 'llamada cada semana'),
    plano(36.96, 'video que vende'), bop(37.86, L1, 'este vende'),
    plano(39.20, 'grafico: el ejemplo'), bop(39.60, O2, 'flechas'),
    foto(40.70, 'repiten 1'), foto(41.39, 'repiten 2'), foto(42.08, 'repiten 3'),
    golpe(46.08, 'golpe clave 1 de 2: la estan construyendo con ellas'),
    tr(47.84, MOMO, AIRE_DEEP, 'los 4 consejos'),
    bop(47.94, L2, '1'), bop(48.09, L1, '2'), bop(48.24, O1, '3'), bop(48.39, O2, '4'), bop(50.84, MONEDA, 'billetes'),
    clic(51.80, GR1, 'consejo 1'), plano(54.94, 'clienta'), plano(57.30, 'grafico: perfiles'), bop(58.10, L2, 'el chico gana'),
    clic(59.02, GR6, 'consejo 2'), plano(60.80, 'mosaico'), bop(61.74, O1, 'check'),
    clic(63.18, CUR, 'consejo 3'), plano(66.30, 'grafico: ideas'), bop(66.75, L1, 'foco'),
    clic(68.56, MG10, 'consejo 4'), plano(70.40, 'grafico: razon'), bop(70.55, MONEDA, '$ por venta'), bop(72.16, O2, 'cada mes'),
    golpe(73.56, 'golpe clave 2 de 2: guardalo'),
    plano(76.26, 'cierre: creadora brindando'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo46.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
