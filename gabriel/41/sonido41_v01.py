"""Video 41 («El cliente que todavia no tiene marca», Huel) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos),
final con la voz (sin cola ni sonido de cierre despues de la ultima palabra).
Uso: python3 sonido41_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v41')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 71.03
EVENTOS = [
    foto(1.02, 'corte 2'), plano(2.04, 'Ozempic'), foto(3.58, 'yogures Danone'),
    glitch(4.54, 'marca desenfocada'), bop(5.04, O1, '¿Cual?'),
    tr(7.18, SLOW, AIRE_BOT, 'capitulo: la compra'),
    clic(9.10, MG13, 'recuadro: close to 1 billion'), bop(9.16, CUENTA, 'contador'), bop(10.20, MONEDA, 'llega a 1.000 M'),
    plano(10.56, 'grafico: el plato'), bop(11.86, O2, 'comes menos'), bop(12.46, L2, 'proteina'), bop(12.76, L1, 'nutrientes'), golpe(13.52, 'golpe clave 1 de 2: x2'),
    plano(13.78, 'linea de produccion'), plano(15.00, 'Food Dive'), clic(15.66, MG7, 'subrayado: GLP-1'),
    tr(18.44, MOMO, AIRE_DEEP, 'capitulo: el fundador'),
    plano(20.38, 'fundador'), bop(21.46, CUENTA, 'contador -80.000'), bop(22.40, MONEDA, 'llega'),
    plano(22.42, 'grafico: planes'), glitch(24.20, 'se cruzan'), bop(25.28, O1, 'demasiado complicado'),
    plano(25.90, 'por lo simple'), plano(27.40, 'grafico: todo en uno'), bop(28.50, L2, 'la bolsa'),
    golpe(29.72, 'golpe clave 2 de 2: Huel'),
    plano(30.62, 'polvo'), foto(32.74, '40 g de proteina'),
    tr(34.92, SLOW, AIRE_BOT, 'capitulo: la estrategia de Danone'),
    foto(36.42, 'Activia'), plano(37.90, 'supermercados'), foto(39.30, 'corte'),
    plano(40.88, 'venta directa'), clic(42.70, CUR, 'subrayado: direct-to-consumer'),
    clic(45.46, GR1, 'recuadro: 4.000.000'), bop(45.50, CUENTA, 'contador clientes'),
    plano(46.62, 'grafico: rompecabezas'), bop(47.22, O2, 'encajan'), bop(47.72, MONEDA, 'check'),
    tr(48.32, MOMO, AIRE_DEEP, 'capitulo: la leccion'),
    bop(50.06, L1, 'come'), bop(50.60, L2, 'duerme'), bop(51.14, O1, 'se cuida'),
    plano(51.54, 'grafico: cliente sin marca'), plano(53.64, 'clienta'), clic(54.28, GR6, 'entra el logo'),
    plano(56.14, 'el producto'), plano(57.72, 'forma de comer'),
    foto(60.14, 'rafaga de habitos'), foto(60.76, 'r2'), foto(61.38, 'r3'), foto(62.00, 'r4'),
    plano(62.62, 'grafico: pasos'), bop(63.96, L1, 'la marca lo lee'), plano(65.00, 'la bolsa'), bop(67.34, O2, 'toma la delantera'),
    plano(67.68, 'tomando Huel'), clic(69.86, MG7, 'recuadro: Seguir'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo41.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
