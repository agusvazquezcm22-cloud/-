"""Video 39 («¿Compras el producto o el marketing?») · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos) y cierre con cola.
Uso: python3 sonido39_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v39')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 84.53
EVENTOS = [
    foto(1.47, 'hook: Create'), foto(2.94, 'hook: Blueprint'), foto(4.41, 'hook: Goli'),
    tr(5.88, SLOW, AIRE_BOT, 'marca 1: Bio.me'),
    clic(7.58, MG13, 'veredicto: marketing'),
    clic(9.22, MG7, 'recuadro: fiber supplements'),
    plano(10.92, 'tienda de Bio.me'),
    clic(13.53, GR1, 'recuadro: Kids'), clic(14.31, GR6, 'recuadro: GLP-1'), clic(16.33, MG10, 'recuadro: Lemonade'), bop(16.94, O1, 'subrayado: electrolitos'),
    plano(17.44, 'grafico: fibra'),
    bop(18.54, L2, 'ninos'), bop(18.84, L1, 'GLP-1'), bop(19.14, O2, 'electrolitos'),
    tr(20.64, MOMO, AIRE_DEEP, 'marca 2: Grüns'),
    golpe(22.62, 'golpe clave 1 de 2: aqui compras el producto'),
    plano(22.92, 'pagina de Grüns'),
    clic(23.76, MG13, 'recuadro: vegetales'), clic(24.30, MG7, 'recuadro: vitaminas'), clic(24.84, GR1, 'recuadro: fibra'),
    plano(25.10, 'clienta comiendo'),
    clic(29.90, CUR, 'recuadro: suscripcion'),
    plano(30.72, 'grafico: Unilever'), bop(31.34, O1, 'subrayado: Unilever'), bop(31.82, CUENTA, 'lluvia de billetes'), bop(32.16, MONEDA, 'compro Grüns'),
    tr(32.64, SLOW, AIRE_BOT, 'marca 3: Create'),
    clic(34.44, MG10, 'veredicto: marketing'),
    clic(35.38, GR6, 'recuadro: gomitas'),
    foto(35.98, 'colores'), bop(36.64, L2, 'creador 1'), bop(37.20, L1, 'creador 2'), bop(37.76, O2, 'creador 3'),
    plano(40.20, 'grafico: creatina'), bop(41.42, O1, 'como se ve'), bop(42.12, L2, 'quien te la muestra'),
    tr(42.78, MOMO, AIRE_DEEP, 'marca 4: Blueprint'),
    clic(45.42, MG13, 'veredicto: producto'),
    foto(45.72, 'rafaga: anuncios con Bryan'), bop(46.52, L1, 'anuncio 2'), bop(47.32, O2, 'anuncio 3'),
    clic(48.66, MG7, 'recuadro: dosis'),
    clic(49.49, GR1, 'recuadro: certificados'), clic(50.30, CUR, 'recuadro: 3rd party'), clic(50.90, MG10, 'recuadro: reporte'),
    plano(51.38, 'grafico: mirar / confiar'), bop(52.76, L2, 'certificado'), bop(53.88, O1, 'te hace confiar'),
    tr(54.20, SLOW, AIRE_BOT, 'marca 5: Goli'),
    clic(55.56, GR6, 'veredicto: marketing'),
    foto(55.88, 'rafaga: virales'), bop(56.58, L1, 'viral 2'), bop(57.28, O2, 'viral 3'),
    plano(58.02, 'grafico: 400 millones'), bop(59.58, MONEDA, '+US$400 M'),
    glitch(62.02, 'fallo de NAD'), clic(62.40, MG13, 'subrayado: promesas'),
    plano(63.80, 'titular: acquired'), clic(65.28, MG7, 'subrayado: acquired'),
    tr(67.82, MOMO, AIRE_DEEP, 'el patron'),
    bop(67.87, O1, 'v1'), bop(68.17, L2, 'v2'), bop(68.47, L1, 'v3'), bop(68.77, O2, 'v4'), bop(69.07, L2, 'v5'),
    plano(69.96, 'video estilo de vida'), bop(71.12, O1, 'estilo de vida -> marketing'), plano(72.00, 'Goli'),
    plano(74.16, 'video producto'), bop(74.96, L1, 'resuelve un problema -> producto'), plano(76.00, 'Blueprint'),
    foto(77.92, 'rafaga: un producto de cada marca'),
    golpe(80.76, 'golpe clave 2 de 2: la pregunta final'),
    plano(83.10, 'clienta comiendo'),
    clic(82.80, MG7, 'aparece el titulo'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo39.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
