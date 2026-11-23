"""Video 40 («Lo prestado se devuelve», Ghost) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos) y cierre con cola.
Uso: python3 sonido40_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v40')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 84.53
EVENTOS = [
    foto(1.44, 'corte 2'), plano(2.88, 'galletas Oreo'),
    tr(5.34, SLOW, AIRE_BOT, 'capitulo: los fundadores'),
    bop(5.94, MONEDA, '2016'), bop(6.64, O1, '2 amigos'), foto(7.64, 'foto fisicoculturista'), foto(8.74, 'foto piloto'),
    plano(9.92, 'entrenando 1'), foto(10.48, 'corte 2'), foto(11.04, 'corte 3'), foto(11.60, 'corte 4'),
    tr(12.16, MOMO, AIRE_DEEP, 'el giro: los sabores'),
    plano(12.16, 'fabrica'), foto(13.70, 'I+D de un sabor'),
    foto(14.98, 'comiendo dulces'), foto(16.86, 'Sour Patch Kids'), foto(18.92, 'comiendo Oreo'), plano(20.52, 'anuncio Oreo'),
    plano(22.14, 'galleta en leche'),
    plano(25.32, 'grafico: x4'), bop(27.00, MONEDA, 'x4'),
    tr(28.32, SLOW, AIRE_BOT, 'capitulo: la venta'),
    clic(31.44, MG7, 'recuadro: US$990 M'), clic(33.48, GR1, 'recuadro: 60%'),
    golpe(34.94, 'golpe clave 1 de 2: les estoy hablando de Ghost'),
    plano(35.24, 'marcas de Mondelez'),
    tr(37.02, MOMO, AIRE_DEEP, 'capitulo: la licencia'),
    clic(37.98, MG10, 'recuadro: Oreo'),
    plano(39.68, 'grafico: la licencia'), bop(41.18, L2, 'KDP'), bop(41.88, O2, 'Mondelez'), glitch(42.58, 'no venia incluida'),
    plano(43.96, 'titular: demanda'), clic(44.62, GR6, 'subrayado: lawsuit'),
    plano(45.26, 'titular: fin de la alianza'), clic(46.28, CUR, 'subrayado: come to an end'),
    plano(47.04, 'anuncio de Ghost'),
    plano(49.00, 'Yahoo: otra marca'), clic(50.52, MG13, 'recuadro: Applied Nutrition'), clic(51.64, MG7, 'recuadro: colaboracion con Mondelez'),
    tr(52.42, SLOW, AIRE_BOT, 'la leccion'),
    plano(52.42, 'anuncio de Ghost'), plano(54.06, 'grafico: tu cliente'), golpe(57.30, 'golpe clave 2 de 2: no es tu cliente'),
    plano(57.60, 'grafico: tu tienda'),
    plano(60.56, 'anuncio de Ghost'), plano(62.72, 'grafico: prestado / tuyo'), bop(63.40, L1, 'vuelven a comprar'), bop(64.98, O2, 'tuyo'),
    tr(65.20, MOMO, AIRE_DEEP, 'Amazon y Mercado Libre'),
    bop(67.54, L2, 'Amazon'), bop(68.04, L1, 'Mercado Libre'),
    plano(68.54, 'anuncio de Ghost'), plano(70.30, 'grafico: datos'), bop(70.46, O1, 'sus datos'), bop(71.84, MONEDA, 'comision'),
    plano(72.24, 'anuncio de Ghost'), plano(74.30, 'grafico: tuyo'), clic(75.74, GR1, 'tuyo'),
    bop(76.36, O2, 'tienda'), bop(76.90, L1, 'WhatsApp'), bop(77.50, L2, 'correos'),
    foto(77.94, 'sabor propio de Ghost'),
    plano(80.16, 'clienta con Ghost'),
    clic(82.46, MG7, 'aparece la pregunta'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo40.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
