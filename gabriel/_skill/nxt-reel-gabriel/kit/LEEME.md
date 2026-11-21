# Kit del formato pantalla verde

- `render_verde.py`: motor. `python3 render_verde.py <config.py> --prev t1,t2 --cols 4 --ancho 540 --out hoja.jpg`
  (hoja de cuadros grande), `--control` (tiempo de lectura y visuales repetidos), `--out video.mp4` (render).
- `verde_ayudas.py`: constructores comunes para la lista de tomas (desde el 33). `sonido_verde.py`: recetas de sonido y montaje.
- `ejemplos/gabriel36_v02.py` y `sonido36_v02.py`: video 36, recorrido de un test (pantallas con `pant` y `r_`).
- `ejemplos/gabriel37_v04.py` y `sonido37_v04.py`: video 37, otro VS (usa además material de IM8 del 32: variable `GAB_IM8`).
- `ejemplos/gabriel35_v01.py` y `sonido35_v01.py`: video 35, formato VS (pantalla dividida con `Mitades`, logos por marca con `G2`).
- `ejemplos/gabriel34_v03.py` y `sonido34_v01.py`: video 34 (The Everyday Lab). PLANTILLA para los siguientes:
  Gabriel fijo abajo al centro (`GAB = 'C'`) en todas las tomas; lo señalado arriba de los subtítulos.
- `ejemplos/gabriel33_v04.py`: el 33 pasado al lugar fijo (sobre-escribe el lugar de todas las tomas al final de la lista).
- `ejemplos/gabriel33_v01.py` y `sonido33_v01.py`: video 33 (AG1) como se hizo primero, con Gabriel cambiando de lado (ya no se hace así).
- `ejemplos/gabriel32_v03.py`: lista de tomas aprobada del video 32 (IM8), con sus ayudas adentro.
  Espera una carpeta de trabajo (variable `GAB_ASSETS`) con `dl/` (crudo, logo, foto de portada), `cap/` (capturas),
  `ads/` (anuncios) y `pal32.json` (transcripción). Ese material no viene en la skill: se vuelve a bajar.
- `nxt_sonido.py`: motor de la pista de efectos (el del video 31). `ejemplos/sonido32_v04.py`: los sonidos del 32.
  Los archivos de sonido no vienen en la skill: se bajan de la carpeta de Naza en Drive a `<GAB_ASSETS>/sonidos/`.
- `transcribir.py`, `bajar_anuncios.py`, `web/*.js`: ver el flujo en SKILL.md. `web/pagina_larga.js` captura una página
  entera en tramos solapados; `web/test_por_pasos.js` recorre un test y captura cada pantalla con sus textos; `web/ejemplo_pasos_liquid.js` mide y captura un armador por pasos; `web/buscar_pagina.js` encuentra el id de la página de una marca en la Biblioteca; `web/reel_referencia.js` abre un reel de referencia de Instagram para estudiarlo; `web/ejemplo_producto_tel.js` captura la página de un producto sin esconder la columna de compra.

Necesita: ffmpeg, Python con numpy, opencv-python-headless, pillow y openai-whisper; Node con Playwright;
fuentes Inter Display y Noto Color Emoji.
