# Kit del formato pantalla verde

- `render_verde.py`: motor. `python3 render_verde.py <config.py> --prev t1,t2 --out hoja.jpg` (hoja de cuadros),
  `--control` (tiempo de lectura y visuales repetidos), `--out video.mp4` (render).
- `ejemplos/gabriel32_v03.py`: lista de tomas aprobada del video 32 (IM8). Plantilla para los siguientes.
  Espera una carpeta de trabajo (variable `GAB_ASSETS`) con `dl/` (crudo, logo, foto de portada), `cap/` (capturas),
  `ads/` (anuncios) y `pal32.json` (transcripción). Ese material no viene en la skill: se vuelve a bajar.
- `transcribir.py`, `bajar_anuncios.py`, `web/*.js`: ver el flujo en SKILL.md.

Necesita: ffmpeg, Python con numpy, opencv-python-headless, pillow y openai-whisper; Node con Playwright;
fuentes Inter Display y Noto Color Emoji.
