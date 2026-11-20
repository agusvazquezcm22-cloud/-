"""Video 33 (AG1) · sonidos. Mismo paquete (Naza) y misma receta que el 31 y el 32.
Uso: python3 sonido33_v01.py <video_sin_sonido.mp4> <salida.mp4>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))        # kit/
from sonido_verde import *

A = os.environ.get('GAB_ASSETS', '.')
SON = os.environ.get('GAB_SONIDOS', os.path.join(A, '..', 'sonidos'))
DUR = 58.1
EVENTOS = [
    tr(1.10, SLOW, AIRE_BOT, 'entra la nota de Fortune'),
    clic(1.40, MG13, 'recuadro en los 600 millones'),
    foto(2.54, 'rafaga de anuncios de creadores'),
    tr(5.50, MOMO, AIRE_BOT, 'capitulo: primero, sus anuncios'),
    clic(9.14, MG7, 'recuadro en el contador de videos'),
    tr(10.20, MOMO, AIRE_DEEP, 'capitulo: pero aqui viene lo interesante'),
    bop(11.98, O1, 'aparece Claude'),
    plano(12.90, 'grilla de los anuncios con el mismo texto'),
    plano(14.52, 'entra el mosaico de creadores'),
    bop(14.97, O2, 'subrayado 1'), bop(15.25, L2, 'subrayado 2'), bop(15.53, L1, 'subrayado 3'), bop(15.81, O1, 'subrayado 4'),
    golpe(16.17, 'golpe clave 1 de 2: exactamente lo mismo'),
    clic(18.16, GR1, 'nombre 1'), clic(18.46, MG10, 'nombre 2'), clic(18.76, GR6, 'nombre 3'), clic(19.06, MG13, 'nombre 4'),
    glitch(23.33, 'ya no estan probando el mensaje'),
    foto(24.14, 'rafaga de caras'),
    tr(25.54, SLOW, AIRE_DEEP, 'capitulo: cuando cambian el anuncio'),
    plano(28.18, 'anuncio para militares'),
    foco(32.16, 'foto del kit de bienvenida'),
    bop(33.38, L2, 'anuncio del kit gratis'),
    tr(34.84, MOMO, AIRE_BOT, 'capitulo: lo que mas me sorprendio'),
    golpe(38.18, 'golpe clave 2 de 2: recuadro en los 11.000 episodios'),
    clic(39.84, MG13, 'recuadro en los 700 podcasts'),
    plano(41.12, 'grafico: cada podcast, su pagina'),
    bop(41.40, CUENTA, 'entran los tres podcasts'),
    tr(44.92, SLOW, AIRE_BOT, 'capitulo: o sea'),
    clic(45.82, MG7, 'recuadro en los 920 anuncios con el mismo texto'),
    clic(48.32, CUR, 'recuadro en el mensaje'),
    bop(50.17, O2, 'publico 1'), bop(50.47, L2, 'publico 2'), bop(50.77, L1, 'publico 3'),
    foto(52.04, 'rafaga final de anuncios'),
    bop(53.97, O1, 'aparece el icono de guardar'),
    clic(54.34, MG10, 'se marca guardar'),
    plano(55.98, 'vuelve la portada'),
    clic(57.30, MG7, 'aparece "necesitar"'),
]
if __name__ == '__main__':
    print('\n'.join(montar(f'{A}/dl/crudo33.mp4', sys.argv[1], sys.argv[2], EVENTOS, DUR, SON)[-6:]))
