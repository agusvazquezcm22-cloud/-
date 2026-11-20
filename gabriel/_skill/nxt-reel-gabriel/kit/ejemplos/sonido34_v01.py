"""Video 34 (The Everyday Lab) · sonidos. Mismo paquete (Naza) y misma receta que el 31, el 32 y el 33.
Uso: python3 sonido34_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v34')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 62.8
EVENTOS = [
    tr(2.06, SLOW, AIRE_BOT, 'entra el articulo de la marca'),
    clic(2.96, MG13, 'recuadro en las 11.000 mexicanas'),
    foto(4.50, 'rafaga de anuncios'),
    plano(5.92, 'anuncio: colageno sublingual'),
    tr(7.16, MOMO, AIRE_BOT, 'capitulo: sus anuncios en Meta'),
    clic(8.06, MG7, 'recuadro en el contador de anuncios'),
    bop(9.99, O1, 'subrayado: fecha 1'), bop(10.29, L2, 'subrayado: fecha 2'),
    foto(12.84, 'rafaga: la fundadora'),
    plano(14.46, 'anuncio en la calle'),
    plano(16.22, 'tarjeta de la Biblioteca'),
    bop(16.72, O2, 'subrayado en el texto del anuncio'),
    foco(17.94, 'frasco de polvo: absorcion 15-30 %'),
    glitch(20.23, 'ya no funciona como antes'),
    tr(21.48, MOMO, AIRE_DEEP, 'capitulo: la estrategia'),
    plano(22.93, 'fabrica'),
    bop(24.56, O1, 'aparece "Tienda"'), bop(25.26, O2, 'aparece "Articulo"'),
    plano(25.80, 'entra el articulo'),
    clic(28.68, GR1, 'recuadro en los combos'),
    golpe(30.64, 'golpe clave 1 de 2: publirreportaje'),
    tr(31.58, SLOW, AIRE_DEEP, 'capitulo: como suben el ticket'),
    bop(32.46, MONEDA, 'ticket'),
    clic(33.22, GR1, 'recuadro: 1 frasco'), clic(34.70, MG10, 'recuadro: 2 frascos'), clic(36.14, GR6, 'recuadro: 3 frascos'), clic(37.08, MG13, 'recuadro: 4 frascos'),
    plano(38.14, 'sube a la suscripcion'),
    clic(39.04, MG7, 'recuadro en la suscripcion'),
    plano(40.40, 'tabla de descuentos por frecuencia'),
    bop(40.65, O2, 'frecuencia 1'), bop(41.25, L2, 'frecuencia 2'), bop(41.85, L1, 'frecuencia 3'),
    tr(42.76, MOMO, AIRE_BOT, 'capitulo: cancelar la suscripcion'),
    plano(44.86, 'pagina de suscripciones'),
    clic(46.02, CUR, 'recuadro en "minimo 2 entregas"'),
    bop(48.02, L2, '1a entrega'), bop(48.47, L1, '2a entrega'),
    golpe(49.38, 'golpe clave 2 de 2: asegurada'),
    tr(49.86, SLOW, AIRE_BOT, 'capitulo: la conclusion'),
    clic(52.64, MG10, 'recuadro en la semana (el habito)'),
    foto(54.00, 'comentario y resenas de clientas'),
    clic(54.88, GR6, 'recuadro: el segundo bote'), clic(55.33, MG13, 'recuadro: el tercer insumo'),
    bop(56.23, O1, 'aparece el avion de enviar'),
    plano(57.98, 'frasco sobre la mesa'),
    plano(59.94, 'vuelve la portada'),
    clic(62.40, MG7, 'aparece "vez?"'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo34.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON)[-6:]))
