"""Video 40 («Lo prestado se devuelve», Ghost) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos) y cierre con cola.
Uso: python3 sonido40_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v40')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 85.43
EVENTOS = [
    plano(2.88, 'lata de Sour Patch Kids'),
    tr(5.34, SLOW, AIRE_BOT, 'capitulo: los fundadores'),
    bop(5.94, MONEDA, '2016'), bop(6.64, O1, '2 amigos'), bop(7.86, L2, 'fisicoculturista'), bop(9.04, L1, 'instructor de vuelo'),
    plano(9.92, 'grafico: una marca mas'),
    tr(12.16, MOMO, AIRE_DEEP, 'el giro: los sabores'),
    glitch(13.88, 'se tacha vainilla'), glitch(14.26, 'se tacha chocolate'),
    foto(14.98, 'gomitas'), foto(16.86, 'Sour Patch Kids'), foto(18.92, 'Oreo'),
    clic(21.92, MG13, 'recuadro: OREO'),
    plano(22.14, 'galleta'),
    plano(25.32, 'grafico: x4'), bop(27.00, MONEDA, 'x4'),
    tr(28.32, SLOW, AIRE_BOT, 'capitulo: la venta'),
    clic(31.44, MG7, 'recuadro: US$990 M'), clic(33.48, GR1, 'recuadro: 60%'),
    golpe(34.94, 'golpe clave 1 de 2: les estoy hablando de Ghost'),
    plano(35.24, 'tarro Sour Patch Kids nitido'),
    tr(37.02, MOMO, AIRE_DEEP, 'capitulo: la licencia'),
    clic(37.98, MG10, 'recuadro: Oreo'),
    plano(39.68, 'grafico: la licencia'), bop(41.18, L2, 'KDP'), bop(41.88, O2, 'Mondelez'), glitch(42.58, 'no venia incluida'),
    plano(43.96, 'titular: demanda'), clic(44.62, GR6, 'subrayado: lawsuit'),
    plano(45.26, 'titular: fin de la alianza'), clic(46.28, CUR, 'subrayado: come to an end'),
    plano(47.04, 'sin sus sabores'),
    plano(49.00, 'Yahoo: otra marca'), clic(50.52, MG13, 'recuadro: Applied Nutrition'), clic(51.64, MG7, 'recuadro: colaboracion con Mondelez'),
    tr(52.42, SLOW, AIRE_BOT, 'la leccion'),
    bop(54.12, O1, 'tu marca'), bop(54.42, L2, 'el dulce'), golpe(57.30, 'golpe clave 2 de 2: no es tu cliente'),
    plano(57.60, 'grafico: tu tienda'),
    plano(60.56, 'grafico: prestado / tuyo'), bop(62.36, L1, 'prestado'), bop(64.98, O2, 'tuyo'),
    tr(65.20, MOMO, AIRE_DEEP, 'Amazon y Mercado Libre'),
    bop(67.54, L2, 'Amazon'), bop(68.04, L1, 'Mercado Libre'),
    plano(68.54, 'grafico: datos'), bop(70.44, O1, 'sus datos'), bop(71.84, MONEDA, 'comision'),
    plano(72.24, 'grafico: tuyo'), bop(73.72, L2, 'te conocen'), clic(75.74, GR1, 'tuyo'),
    bop(76.36, O2, 'tienda'), bop(76.90, L1, 'WhatsApp'), bop(77.50, L2, 'correos'),
    foto(77.94, 'sabor propio de Ghost'),
    plano(80.16, 'clienta con Ghost'),
    clic(82.46, MG7, 'aparece la pregunta'),
    tr(84.60, SLOW, AIRE_DEEP, 'cierre: sale con el ultimo cuadro'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo40.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.35)[-6:]))
