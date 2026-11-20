# Kit del formato pantalla verde

- `render_verde.py`: motor. `python3 render_verde.py <config.py> --prev t1,t2 --cols 4 --ancho 540 --out hoja.jpg`
  (hoja de cuadros grande), `--control` (tiempo de lectura y visuales repetidos), `--out video.mp4` (render).
- `verde_ayudas.py`: constructores comunes para la lista de tomas (desde el 33). `sonido_verde.py`: recetas de sonido y montaje.
- `ejemplos/gabriel34_v01.py` y `sonido34_v01.py`: video 34 (The Everyday Lab). Plantilla para los siguientes:
  Gabriel fijo abajo al centro (`GAB = 'C'`), lo señalado arriba de la franja de subtítulos.
- `ejemplos/gabriel33_v01.py` y `sonido33_v01.py`: video 33 (AG1), con Gabriel cambiando de lado en cada corte.
- `ejemplos/gabriel32_v03.py`: lista de tomas aprobada del video 32 (IM8), con sus ayudas adentro.
  Espera una carpeta de trabajo (variable `GAB_ASSETS`) con `dl/` (crudo, logo, foto de portada), `cap/` (capturas),
  `ads/` (anuncios) y `pal32.json` (transcripción). Ese material no viene en la skill: se vuelve a bajar.
- `nxt_sonido.py`: motor de la pista de efectos (el del video 31). `ejemplos/sonido32_v04.py`: los sonidos del 32.
  Los archivos de sonido no vienen en la skill: se bajan de la carpeta de Naza en Drive a `<GAB_ASSETS>/sonidos/`.
- `transcribir.py`, `bajar_anuncios.py`, `web/*.js`: ver el flujo en SKILL.md. `web/pagina_larga.js` captura una página
  entera en tramos solapados; `web/ejemplo_producto_tel.js` captura la página de un producto sin esconder la columna de compra.

Necesita: ffmpeg, Python con numpy, opencv-python-headless, pillow y openai-whisper; Node con Playwright;
fuentes Inter Display y Noto Color Emoji.
