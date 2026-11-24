"""Video 44 («Veinte y no cien», Bloom Life) · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos), final con la voz.
Uso: python3 sonido44_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v44')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 67.97
EVENTOS = [
    foto(0.84, 'hook: corte 2'),
    plano(1.68, 'grilla de 100'), bop(1.70, CUENTA, 'se llenan los perfiles'), glitch(2.98, 'quedan 20'),
    plano(4.28, 'Forbes'), clic(5.22, MG13, 'recuadro: crecen 15%'), bop(5.24, MONEDA, '+15% cada mes'),
    plano(6.36, 'los fundadores'), bop(7.58, CUENTA, 'contador US$20.000'), bop(8.30, MONEDA, 'llega a 20.000'),
    plano(8.56, 'el frasco'),
    tr(10.24, SLOW, AIRE_BOT, 'capitulo: nacio en Estados Unidos'), bop(11.14, O1, 'Argentina'),
    plano(13.58, 'frasco en la mano'), foto(15.36, 'la influencer'),
    plano(16.46, 'historia de Instagram'), bop(17.00, L2, 'corazones'),
    clic(17.75, MG7, 'recuadro: la respuesta fue inmediata'),
    plano(20.16, 'la flecha llega a Argentina'), bop(20.80, O2, 'hay mercado'),
    tr(21.48, MOMO, AIRE_DEEP, 'la revelacion'),
    golpe(22.52, 'golpe clave 1 de 2: Bloom Life'),
    foto(23.46, 'gomitas'), foto(23.86, 'capsulas'), foto(24.60, 'melena de leon'), foto(26.10, 'ashwagandha'),
    plano(26.78, 'creadora'), plano(28.54, 'grilla: todas'), bop(28.60, CUENTA, 'se llenan'),
    plano(30.54, 'muy selectivos'), glitch(31.10, 'se apagan'),
    plano(32.30, 'Forbes: embajadoras'), clic(32.90, GR1, 'recuadro: Florencia Raggi'), clic(33.76, GR6, 'recuadro: Pia Slapka'), clic(34.60, CUR, 'recuadro: mas de 20 embajadoras'),
    tr(36.78, SLOW, AIRE_BOT, 'capitulo: quien les compra'),
    plano(38.94, 'grafico: 95%'), bop(39.10, CUENTA, 'contador 95%'),
    foto(42.04, 'la creadora'), plano(43.40, 'grafico: embajadora'), bop(44.20, L1, 'confian'),
    plano(45.20, 'gomitas'), plano(46.80, 'iProfesional: la frase'), clic(48.62, MG10, 'recuadro: preferimos vender menos'),
    plano(51.36, 'frasco'), plano(53.00, 'iProfesional: 50%'), clic(54.10, MG13, 'recuadro: hasta un 50%'), bop(54.48, MONEDA, 'contador 50%'),
    tr(55.74, MOMO, AIRE_DEEP, 'capitulo: la leccion'),
    foto(56.64, 'rafaga 2'), foto(57.54, 'rafaga 3'), foto(58.44, 'rafaga 4'),
    plano(59.36, 'grafico: unas pocas'), plano(61.00, 'creadora'),
    golpe(62.92, 'golpe clave 2 de 2: puede jugar en tu contra'),
    plano(65.00, 'cierre: clientas con sus frascos'), clic(65.20, MG7, 'aparece mandaselo'), foto(66.40, 'ultimo corte'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo44.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
