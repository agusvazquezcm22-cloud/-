"""Video 45 («El bombero del cafe», Innerbloom) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos); termina con la voz.
Uso: python3 sonido45_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v45')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 79.233
EVENTOS = [
    foto(1.50, 'hook: segundo corte de bomberos'),
    plano(2.76, 'lista de tiendas'), bop(3.88, CUENTA, '+300 tiendas'), bop(4.38, MONEDA, 'llega a 300'),
    plano(4.72, 'incendio'),
    tr(7.56, SLOW, AIRE_BOT, 'capitulo: Ollie'), foto(8.40, 'bomberos de Nueva Zelanda'),
    plano(9.40, 'bombero equipandose'), foto(11.68, 'madrugadas'), foto(12.56, 'cafe'),
    tr(14.64, MOMO, AIRE_DEEP, 'el mar'), foto(16.40, 'piscina'), plano(18.26, 'tomando su cafe'),
    plano(21.26, 'Estados Unidos'), foto(23.36, 'cold brew'),
    plano(26.16, 'grafico: algo mas'), bop(26.86, O1, '+'), glitch(28.41, '?'),
    golpe(29.56, 'golpe clave 1 de 2: asi nacio Innerbloom'),
    clic(31.26, MG13, 'recuadro: 15,4 g'),
    tr(32.86, SLOW, AIRE_BOT, 'el mercado'),
    plano(34.86, 'Foodpreneur: 300 tiendas'), clic(36.10, MG7, 'recuadro: 300 tiendas'),
    tr(38.10, MOMO, AIRE_DEEP, 'el problema'),
    plano(40.88, 'grafico: la plata'), bop(41.84, L2, 'tiendas'), bop(42.92, O1, 'entra'), glitch(44.20, 'sale'),
    clic(45.38, GR1, 'recuadro: perdio tiendas'),
    plano(46.60, 'grafico: tiendas'), bop(47.38, L1, 'nuevas'), bop(48.46, O2, 'las que ya tenia'),
    plano(49.34, 'camion de bomberos'),
    clic(51.30, GR6, 'recuadro: dejo de ser bombero'), clic(52.26, CUR, 'recuadro: sin red, sin inversionistas'),
    plano(54.30, 'su marca'),
    tr(55.42, SLOW, AIRE_BOT, 'vender por internet'),
    clic(59.98, MG10, 'recuadro: US$1 M'), bop(59.98, CUENTA, 'contador'), bop(60.58, MONEDA, 'llega al millon'),
    plano(61.84, 'su anuncio'), clic(63.52, MG13, 'recuadro: olliepuddick'),
    plano(65.56, 'grafico: directo'), bop(66.30, L1, 'flecha'), bop(67.40, O1, 'control'),
    tr(68.20, MOMO, AIRE_DEEP, 'su historia'),
    golpe(72.76, 'golpe clave 2 de 2: autenticidad'),
    plano(73.62, 'Ollie a camara'), clic(77.48, MG7, 'sigueme'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo45.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
