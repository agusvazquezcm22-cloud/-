"""Video 37 (Lemme vs IM8) · sonidos. Mismo paquete (Naza) y misma receta que el 31 al 36.
v04: pasada final (mismos sonidos). v03: correcciones de Gabriel (mismos sonidos, tres ajustados a los cortes nuevos). v02: receta 2 (sin el sonido 'angelical', 3 dB mas bajo) y cierre con cola.
Uso: python3 sonido37_v05.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v37')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 72.15
EVENTOS = [
    tr(3.84, SLOW, AIRE_BOT, 'ronda 1: los anuncios de Lemme'),
    clic(4.64, MG13, 'recuadro en los 580 anuncios de Lemme'),
    bop(6.80, O1, 'productos'), bop(7.44, L2, 'beneficios'), bop(8.20, L1, 'descuentos'),
    plano(8.66, 'Biblioteca de IM8'),
    clic(9.82, MG7, 'recuadro en los 1.900 anuncios de IM8'),
    foto(11.86, 'rafaga: creadores, estudios, Beckham'),
    plano(14.28, 'anuncio que arranca con el problema'),
    tr(17.70, MOMO, AIRE_DEEP, 'ronda 2: a donde te llevan'),
    plano(19.06, 'grafico: una pagina por producto'),
    bop(19.66, O2, 'pagina 1'), bop(20.16, L2, 'pagina 2'), bop(20.61, L1, 'pagina 3'),
    plano(21.50, 'anuncio de Debloat'),
    plano(23.00, 'pagina de Debloat'),
    clic(24.95, GR1, 'recuadro en los jeans apretados'),
    tr(26.40, SLOW, AIRE_DEEP, 'IM8 hace lo contrario'),
    plano(29.20, 'pagina de IM8'),
    clic(31.72, MG10, 'recuadro en el plan de 3 meses'),
    golpe(34.18, 'golpe clave 1 de 2: te regala el kit de bienvenida'),
    plano(35.24, 'anuncio del kit'),
    clic(36.56, GR6, 'recuadro: suscripcion trimestral'),
    tr(37.52, MOMO, AIRE_BOT, 'ronda 3: los creadores'),
    plano(38.74, 'grafico: TikTok Shop'),
    bop(39.56, MONEDA, 'aparecen los 13 millones'),
    bop(42.12, CUENTA, 'entran los creadores'),
    clic(43.46, CUR, 'comision por venta'),
    plano(44.66, 'video de una creadora de Lemme'),
    foto(47.62, 'otra creadora'),
    glitch(49.38, 'contenido sin usar'),
    tr(49.76, SLOW, AIRE_BOT, 'IM8 va por otro camino'),
    foto(51.18, 'Giannis'), bop(51.98, O1, 'Sabalenka'), bop(53.00, O2, 'Inter de Miami'),
    plano(54.48, 'grafico: si la marca crece'),
    bop(56.20, L2, 'ellos tambien ganan'),
    tr(57.00, MOMO, AIRE_DEEP, 'cierre: vuelve la pantalla dividida'),
    plano(60.52, 'grafico: de TikTok Shop a Meta'),
    clic(62.08, MG13, 'aparece Meta'),
    plano(62.82, 'grafico: una pagina por avatar'),
    bop(63.87, L1, 'pagina 1'), bop(64.37, L2, 'pagina 2'), bop(64.87, O1, 'pagina 3'),
    golpe(66.36, 'golpe clave 2 de 2: la pregunta final'),
    plano(68.68, 'cambian los dos videos'),
    clic(70.66, MG7, 'aparece "comentarios"'),
    tr(71.25, SLOW, AIRE_DEEP, 'cierre: sale con el ultimo cuadro'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo37.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.35)[-6:]))
