"""Video 36 (el test de Aluné) · sonidos. Mismo paquete (Naza) y misma receta que el 31 al 35.
v02: mismo listado; el audio sigue hasta que termina el ultimo sonido y se apaga en 0,35 s.
Uso: python3 sonido36_v02.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_kit'))
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '/tmp/claude-0/-home-user--/5179dee2-39cd-5dce-b326-2d7a39fe506b/scratchpad/v36')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 85.4
EVENTOS = [
    plano(1.04, 'Biblioteca de Anuncios'),
    clic(1.16, MG13, 'recuadro en los 58 anuncios'),
    bop(2.80, O1, 'subrayado en el enlace al test'),
    tr(3.70, SLOW, AIRE_BOT, 'presentacion de la marca'),
    clic(6.14, MG7, 'recuadro en el lema de la pagina'),
    foto(8.76, 'rafaga de anuncios'),
    tr(10.66, MOMO, AIRE_DEEP, 'capitulo: te mandan a un test'),
    clic(11.16, GR1, 'recuadro: test gratis'),
    plano(12.22, 'portada del test'),
    plano(13.10, 'grafico: un test por problema'),
    bop(14.35, L2, 'test 1'), bop(15.20, L1, 'test 2'), bop(16.00, O1, 'test 3'),
    bop(17.98, O2, 'sueno'), bop(18.60, L2, 'piel'), bop(19.06, L1, 'animo'),
    glitch(19.64, 'por que hacen esto'),
    tr(20.52, SLOW, AIRE_DEEP, 'capitulo: el test de piel'),
    clic(21.02, MG10, 'recuadro en test gratuito'),
    clic(22.52, GR6, 'recuadro en la pregunta del ciclo'),
    foto(24.12, 'rafaga de preguntas'),
    clic(27.28, CUR, 'recuadro en la frase'),
    bop(30.18, O1, 'subrayado: no envejeciste de golpe'),
    tr(31.98, MOMO, AIRE_BOT, 'capitulo: la pregunta 8'),
    clic(32.58, MG13, 'recuadro en 8 de 11'),
    plano(34.24, 'grafico: tu piel / tu dinero'),
    golpe(36.19, 'golpe clave 1 de 2: te pregunta por tu dinero'),
    clic(37.32, MG7, 'recuadro en los 120.000 al mes'), clic(38.82, GR1, 'recuadro en unos 2 anos'),
    plano(39.64, 'pregunta 11'),
    bop(40.84, MONEDA, 'recuadro en la cuenta de 1.440.000'),
    tr(43.40, SLOW, AIRE_BOT, 'capitulo: el resultado'),
    clic(46.36, MG10, 'recuadro en Brillo Apagado'),
    plano(47.36, 'bono por terminar el test'),
    clic(48.26, GR6, 'recuadro: desbloqueaste'), clic(49.26, MG13, 'recuadro en el descuento'),
    plano(50.38, 'la oferta'),
    bop(51.58, O2, 'subrayado: hoy, por terminar tu test'), clic(52.58, MG7, 'recuadro en el precio'),
    tr(53.94, MOMO, AIRE_DEEP, 'capitulo: como suben el ticket'),
    clic(56.46, CUR, 'recuadro: recomendado para tu resultado'), clic(57.56, MG10, 'recuadro: 3 tarros, 90 noches'),
    plano(59.38, 'grafico: tres tarros'),
    bop(59.93, L2, 'tarro 2'), bop(60.33, L1, 'tarro 3'),
    plano(61.88, 'grafico: lo gastado contra el plan'),
    bop(63.78, CUENTA, 'entra la barra del plan'),
    tr(66.06, SLOW, AIRE_DEEP, 'capitulo: por que un test y no la tienda'),
    bop(67.06, O1, 'test si'), glitch(67.96, 'tienda no'),
    foto(70.04, 'pregunta de los gastos'),
    golpe(72.86, 'golpe clave 2 de 2: recuadro en los 2.880.000'),
    plano(74.40, 'la edad del espejo'),
    clic(77.30, GR1, 'recuadro: esos 5 anos no son tuyos'),
    plano(78.90, 'anuncio del producto'),
    plano(81.52, 'vuelve la portada'),
    clic(83.96, MG7, 'aparece "comentarios"'),
    tr(84.50, SLOW, AIRE_DEEP, 'cierre: sale con el ultimo cuadro'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo36.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON, fundido=0.35)[-6:]))
