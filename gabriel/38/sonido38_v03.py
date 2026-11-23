"""Video 38 (Mumu, «No lo compres») · sonidos. Receta 2 (sin el sonido "angelical", efectos bajos) y cierre con cola.
Uso: python3 sonido38_v02.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v38')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 67.4
EVENTOS = [
    plano(2.10, 'ingredientes del batido'),
    foto(3.66, 'gente tomando el batido'),
    plano(6.08, 'grafico: tres productos'),
    bop(7.18, L2, 'entra el segundo'), bop(7.48, L1, 'entra el tercero'),
    golpe(8.90, 'golpe clave 1 de 2: se llama Mumu (aparece la marca)'),
    tr(11.74, SLOW, AIRE_BOT, 'capitulo: el anuncio'),
    clic(15.50, MG13, 'subrayado: no lo compres si lo que buscas es una dieta'),
    plano(16.90, 'grafico: espantar'),
    glitch(17.32, 'se tacha espantar'),
    bop(18.20, O1, 'aparece calificar'), bop(18.90, O2, 'la clienta ideal'),
    tr(20.52, MOMO, AIRE_DEEP, 'capitulo: el resto de la pauta'),
    clic(24.00, MG7, 'recuadro en los anuncios activos'),
    plano(25.36, 'anuncio del almuerzo'),
    bop(25.66, O1, 'subrayado almuerzo'),
    clic(27.66, GR1, 'subrayado: la pesadez de las tres'), clic(28.76, GR6, 'subrayado: el jean que aprieta'),
    tr(29.76, SLOW, AIRE_DEEP, 'capitulo: no un batido suelto'),
    glitch(30.80, 'se tacha batido suelto'),
    plano(31.62, 'coleccion de kits'),
    bop(33.64, O2, 'Glow Up'), bop(34.30, L2, 'Detox'), bop(34.84, L1, 'Renueva'),
    plano(35.22, 'grafico: que tomar / que mejorar'),
    glitch(36.74, 'se tacha que tomar'), bop(37.62, O1, 'aparece que mejorar'),
    plano(37.94, 'los tres productos en la mesa'),
    clic(41.58, MG10, 'recuadro: batido en la manana'), clic(42.48, MG13, 'recuadro: gomitas'), clic(43.56, MG7, 'recuadro: colageno en la noche'),
    plano(44.26, 'batido listo en un minuto'),
    bop(46.90, MONEDA, 'descuento 15'), clic(47.48, GR1, 'descuento 18'), clic(48.16, GR6, 'descuento 25'),
    tr(48.82, MOMO, AIRE_BOT, 'capitulo: la suscripcion'),
    clic(50.27, CUR, 'recuadro: debito mensual'),
    bop(50.82, O2, 'subrayado: Close Friends'),
    bop(52.00, CUENTA, 'lista de mejores amigos'),
    clic(53.39, MG10, 'recuadro: 15% off'), clic(54.18, MG13, 'recuadro: envio gratis'), clic(54.74, MG7, 'recuadro: regalo'),
    tr(55.32, SLOW, AIRE_BOT, 'capitulo: la conclusion'),
    foto(59.18, 'rafaga de anuncios'),
    golpe(60.70, 'golpe clave 2 de 2: no vas a sufrir'),
    plano(62.90, 'clienta tomando su batido'),
    clic(66.92, MG7, 'aparece comentarios'),
    ]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo38.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.12)[-6:]))
