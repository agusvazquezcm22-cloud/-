"""Video 35 (Liquid I.V. vs Electrolit) · sonidos. Mismo paquete (Naza) y misma receta que el 31 al 34.
Uso: python3 sonido35_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v35')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 74.1
EVENTOS = [
    tr(1.96, SLOW, AIRE_BOT, 'entra la nota de Entrepreneur'),
    clic(3.26, MG13, 'recuadro en los 1.000 millones'),
    plano(4.64, 'grafico: ventas de Electrolit'),
    bop(5.39, MONEDA, 'aparece la cifra de 617 millones'),
    tr(7.94, MOMO, AIRE_DEEP, 'pantalla dividida: cada una le habla a otra persona'),
    tr(10.50, SLOW, AIRE_DEEP, 'ronda 1: sus anuncios'),
    clic(11.76, MG7, 'recuadro en los 200 anuncios de Liquid'),
    clic(13.36, GR1, 'recuadro en el boton Subscribe'),
    bop(14.22, O1, 'subrayado: cuando te suscribes'), bop(15.21, O2, 'subrayado: suscribete y ahorra'),
    plano(15.86, 'Biblioteca de Electrolit'),
    clic(17.36, MG10, 'recuadro en los 80 anuncios de Electrolit'),
    glitch(18.69, 'no hay boton de compra'),
    foto(20.04, 'rafaga: a quien patrocina'),
    bop(21.82, L2, 'Cruz Azul'), bop(22.48, L1, 'Pumas'), bop(23.22, O1, "Pato O'Ward"),
    tr(24.22, MOMO, AIRE_BOT, 'ronda 2: a donde te llevan'),
    plano(26.10, 'pagina de suscripcion de Liquid'),
    clic(26.84, MG13, 'recuadro: arma tu suscripcion'),
    clic(28.62, GR6, 'paso 1: para que la quieres'), clic(29.20, MG7, 'paso 2: el sabor'), clic(30.36, MG10, 'paso 3: cuantos sobres'),
    plano(31.70, 'beneficios de la suscripcion'),
    golpe(32.28, 'golpe clave 1 de 2: 30 % menos en cada pedido'),
    bop(34.16, O2, 'subrayado: muestras gratis'), bop(35.46, L2, 'subrayado: regalos sorpresa'),
    tr(36.36, SLOW, AIRE_BOT, 'Electrolit hace lo contrario'),
    plano(40.40, 'botella gigante en la cancha'),
    foto(42.28, 'en tu equipo, en las carreras'),
    bop(43.59, CUENTA, 'entran las cadenas donde se compra'),
    tr(44.98, MOMO, AIRE_DEEP, 'ronda 3: vuelve la pantalla dividida'),
    plano(48.16, 'sobre de Liquid'),
    clic(51.58, CUR, 'recuadro en las cuatro ocasiones'),
    bop(53.18, O1, 'fiesta'), bop(54.32, L2, 'gym'), bop(54.84, L1, 'avion'), bop(55.58, O2, 'calor'),
    foto(55.84, 'rafaga de creadores'),
    clic(58.72, GR1, 'recuadro en los microinfluencers'),
    tr(60.42, SLOW, AIRE_DEEP, 'Electrolit usa Meta como tele'),
    bop(60.62, O1, 'aparece la tele'),
    plano(62.56, 'anuncio con el equipo'),
    foto(66.92, 'rafaga alternando las dos marcas'),
    golpe(70.18, 'golpe clave 2 de 2: no compiten en precio'),
    plano(70.44, 'vuelve la pantalla dividida'),
    clic(73.56, MG7, 'aparece "comentarios"'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo35.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON)[-6:]))
