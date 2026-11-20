---
name: "nxt-reel-gabriel"
description: "Edita reels de NXT Media para Gabriel Monsalve (@gabriel.growthp, G Growth) con su estilo aprobado: pantalla verde estilo Chase Chappell (Gabriel recortado abajo sobre anuncios, capturas y gráficos de la marca, flecha y recuadro rojo) y subtítulos de línea blanca chica + palabra clave grande verde. Usala siempre que Agus hable de Gabriel, la sesión de Gabriel, su guía de edición, un video numerado de Gabriel (32, 33…), pantalla verde, mini charla con tele o correcciones de Gabriel, aunque no nombre la skill."
---

# Reels de Gabriel Monsalve (NXT Media · Agus)

**Estilo aprobado por Gabriel el 2026-11-20** sobre el video 32 (IM8): "de resto está brutal". Es la base de todos sus próximos reels. Agus edita y corrige; hablarle en español, corto y directo.

## Reglas fijas

- **Cada vez que termines (una versión entregada o una tanda de correcciones), actualizá esta skill** sin esperar a que lo pida: anotá lo nuevo en `historial.md`, pasá a este archivo y a `referencias/gabriel.md` cualquier regla o error nuevo, copiá el motor y la lista de tomas vigentes a `kit/`, empaquetá (`python -m scripts.package_skill <carpeta>` desde la skill skill-creator) y mandale el `.skill` a Agus con `SendUserFile` para que lo guarde. La carpeta instalada es de solo lectura: se trabaja sobre la copia del repo (`gabriel/_skill/nxt-reel-gabriel/`).
- Preguntar solo lo necesario y avanzar con lo que hay. Cada decisión de edición tiene un motivo (Agus descartó una edición "sin criterio").
- Cuando Gabriel manda correcciones y dice que el resto está bien, se toca **solo** lo pedido. Lo único que se suma es lo que exige el control de abajo.
- Entrega: `GABRIEL_<n>_vNN.mp4`, 1080×1920, por `SendUserFile`. Nunca pisar versiones. No subir nada a la carpeta de Drive del cliente ni publicar si Agus no lo pide.
- **Sonidos: solo los del paquete de Naza** (o los que ya trae esta skill). Nunca sonidos sintetizados ni "predeterminados": Agus lo pidió expreso. Ver la sección Sonido.
- Música: la pone Gabriel desde Instagram; no se baja de YouTube.
- Si un número en pantalla ya no coincide con lo que dice Gabriel, avisar antes de exportar (lo pide su guía).

## Las 6 reglas de Gabriel (2026-11-20) · valen para todos sus videos

1. **El título nunca tapa la cara de la persona de la portada.** El primer cuadro es la portada: la persona se ve entera y el título va arriba, por encima de ella, fijo desde el cuadro 0.
2. **No repetir el mismo logo o marca dos veces en un cuadro.** En gráficos propios el logo va una vez, arriba; si el gráfico ya muestra la marca, va sin logo (`G(fn, logo=False)`). El título no lleva logo si ya nombra la marca.
3. **Cada visual representa la frase que suena en ese momento.** Un gráfico genérico "no dice mucho": mejor un anuncio o video real de la marca que muestre eso mismo.
4. **No usar el mismo B-roll o captura más de una vez por video.** Tampoco dos tramos del mismo clip en momentos separados. Única excepción: el cierre vuelve a la imagen de la portada (regla 10 de su guía).
5. **El cierre también lleva apoyo visual**: imágenes o videos reales que representen lo que se ofrece, no capturas de texto.
6. **Subtítulos con tiempo de lectura**: ninguna tarjeta menos de 0,7 s; la palabra clave grande, al menos 0,8 s visible. Si no alcanza, se unen tarjetas; nunca se acorta el tiempo.

Las frases textuales de Gabriel y cómo se resolvió cada una están en `referencias/gabriel.md`, sección 0.k.

## Dónde está todo

- **Guía de edición de Gabriel** (Drive, Google Doc "Copy of Guia edición ", id `1Z2lnrdt8l47JapJRDTL_IfXKpdcrakfHOdmBtGiphEs`): una sección por video ("VIDEO 32", "VIDEO 33"…) con cómo quiere la edición, reglas, lista de tomas con tiempos y links. Es larga: leerla por sección.
- **Crudos**: carpeta de Drive con subcarpetas "32.", "33."… (id `1nqxxjwGmT2lTle6kBlNHOsp_jxVRtt22`), un mp4 por carpeta, compartidos por link. El conector de Drive no baja más de 10 MB: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
- **Estilo completo e historial de decisiones**: `referencias/gabriel.md` (copia en Drive junto a `gabriel_correcciones_IM8_2026-11-20.md`, carpeta `1Rsl2h2WprK5h64FkiY1nY-EHcqsYbE9D`; la versión anterior queda al lado como `gabriel_anterior_<fecha>.md`). El conector de Drive no edita el contenido de un archivo existente: se sube la versión nueva y se renombra la anterior.
- **Videos de podcasts u otro material de YouTube**: no se bajan. Se resuelve con la nota que da la cifra o con un gráfico, y se avisa.
- **Motor del formato mini charla (video 31)**: `render_gabriel.py` y `nxt_sonido.py` en Drive, carpeta `_kit` (id `1zEpDIFxFavnFl1AGCkzOQQ_pT-FTkl1O`).
- **Repo**: `agusvazquezcm22-cloud/-`, carpeta `gabriel/` (`_kit/`, `32/`, `_skill/`).
- **Entorno en la nube "gabriel-edicion"**: ya permite Drive, im8health.com, StockTitan, Meta (Biblioteca de Anuncios y sus servidores de imágenes) y el modelo de transcripción. Para otra marca hay que pedir sus hosts con `update_environment` cuando el proxy los rechace.

## Qué formato toca

- **Pantalla verde** (crudo con fondo verde; la guía dice que copia a Chase Chappell): todo lo de abajo. Es el formato de los videos 32 en adelante.
- **Mini charla con tele** (video 31): reglas en `referencias/gabriel.md`, secciones 0.a a 0.i. Comparte el juego de subtítulos.

## Pantalla verde: cómo es

- **Gabriel** recortado del verde, pegado al borde de abajo, siempre sobre imagen, video o gráfico a pantalla completa. Nunca sobre fondo vacío ni en pantalla dividida. Cinco lugares fijos: `G` grande (media pantalla) sobre capturas y gráficos; `ML`/`MR` medio; `PL`/`PR` pequeño en esquina sobre anuncios. Cambia de lugar en cada corte, nunca dentro de una toma.
- **Ritmo**: corte seco siempre, sin transiciones ni efectos. Imagen nueva cada 1–2 s; ráfagas de 0,5–1 s al enumerar. Lo que Gabriel nombra se ve en ese mismo segundo. El crudo ya viene sin pausas.
- **Material**: real de la marca y en la mejor calidad. Anuncios de la Biblioteca de Anuncios de Meta con su texto original; capturas de su página; la fuente de cada cifra (comunicado, nota) con el dato marcado. Nada de stock.
- **Marcas rojas**: flecha + recuadro sobre la cifra o frase; subrayado en frases cortas; zoom leve hacia el dato. Sobre fondo rojo el recuadro va blanco (`caja_b`). Nunca círculos, resaltador amarillo, stickers ni emojis animados.
- **Gráficos propios**: fondo claro punteado, logo de la marca arriba una sola vez, elementos simples que entran por partes, en la mitad de arriba (abajo está Gabriel y en el medio el subtítulo).
- **Subtítulos** (juego aprobado): línea blanca Inter Display SemiBold 86 px; palabra clave Inter Display ExtraBold 180 px en verde menta `#4DCB84`, debajo de la blanca y tocándola, siempre dibujada encima. La clave entra cuando se dice (fundido 0,07 s, escala 88 → 100 % en 0,11 s); las blancas por corte seco. Lugar fijo en todo el video: línea sola en y 850, clave en y 880. Una clave por frase como máximo; no terminar una tarjeta en conector ni cruzar una coma. Todo lo dicho aparece.
- **Portada**: foto oficial de la persona o marca, entera, con la cara entre el título y la franja de subtítulos. Título en caja oscura, Inter Display ExtraBold, con la cifra en verde. Si la portada es un anuncio con su propio titular arriba, va entero y más chico sobre su versión desenfocada (`clip(..., encaje=(0.68, 330))`) para que el título no lo pise.
- **Qué no se muestra**: cada guía trae su lista (en IM8: anuncios de peso o GLP-1, porcentajes de resultados del estudio clínico, antes y después, testimonios con nombre, avisos de Black Friday, precios resaltados). Se tapa en la captura (ocultar el elemento antes de capturar) o se elige otro material.
- **Audio**: voz a −14 LUFS, pico −1,5 dBFS.

## Sonido

Agus: "los sonidos, clave". Van siempre, con el estilo del video 31.

- **De dónde salen**: carpeta de Drive "sonidos" de Naza (id `1J3lIkZN-0oNCYm2UVprYrfAQUsbiLDVS`, dentro de "recursos"), 33 archivos. Es el mismo paquete del 31. Se bajan con `download_file_content` del conector de Drive, que deja el archivo en disco (hasta 10 MB cada uno). La carpeta es privada: no sirve `curl`.
- **Motor**: `kit/nxt_sonido.py`, el mismo del 31, sin cambios. Ejemplo completo: `kit/ejemplos/sonido32_v04.py` y su informe `GABRIEL_32_v04_sonidos.txt`. La pista de efectos se mezcla con la voz y se monta sobre el video ya renderizado sin volver a renderizar la imagen.
- **Receta** (de la skill `nxt-reel-agus`): cada efecto con el pico entre 12,5 y 18 dB por debajo del pico de la voz, nunca arriba; los graves (Momo WOOSH, slow woosh, Hit Impact) siempre con una capa de aire (Botanical Whoosh con pasa-bajos o Deep Mini Whoosh), porque solos no se oyen en el celular; nunca pitidos; nunca el mismo sonido muchas veces seguidas; sin risers.
- **Qué va dónde** (como quedó en el 32):
  - Cambio de capítulo → transición: `Momo WOOSH 3` o `slow woosh` + capa de aire, alternando las cuatro combinaciones.
  - Entrada de un gráfico, una tarjeta o un clip → whoosh suave solo (`Botanical` recortado o `Deep Mini`), no en todos los cortes.
  - Recuadro rojo sobre una cifra → clic (`Magnetic, Button` 7, 10, 13; `Granular, Button, Select`; `Button, Cursor, Select`), rotando archivos.
  - Enumeraciones (lista de anuncios, partes de la oferta) → un `Mini list` distinto por ítem.
  - Dos golpes clave por video, en las dos frases más fuertes → whoosh que termina en el golpe + `Hit Impact` + `Magnetic, Button`.
  - Tachado o negación → `Fast Glitch 1`. Ráfaga de anuncios → `camera shutter sfx`. Monedas → `Coin Flip`. Calendario → `Countdown, List, Numbers`.
- **Control**: el informe lista cada sonido con su tiempo y nivel, cuántas veces se usa cada archivo, el pico de la pista y si hay tonos sostenidos. Mezcla final a −14 LUFS, pico −1,5 dBFS.
- En el 31 la versión final llevó además la canción que pidió Gabriel, 19 dB bajo la voz. En el 32 no se pidió.

## Flujo

1. Leer la sección del video en la guía y, si hay, las correcciones pendientes. Elegir el entorno "gabriel-edicion".
2. Bajar el crudo. Transcribir: `python3 kit/transcribir.py crudo.mp4 pal.json "Marca, nombres"`. Revisar nombres propios (escribió "IMA" por IM8).
3. Juntar material:
   - Anuncios: `node kit/web/biblioteca_cosechar.js <id_pagina> bodies.txt palabra1,palabra2` y enseguida `python3 kit/bajar_anuncios.py bodies.txt ads/` (los enlaces vencen). Mirar `hoja_jpg.jpg` y `hoja_mp4.jpg` para elegir; para cada video sacar cuadros en varios momentos antes de usarlo.
   - Grilla y tarjetas de la Biblioteca: `node kit/web/biblioteca_capturas.js <id_pagina> cap '{"<library id>":"frase a subrayar"}'`.
   - Frase con cifra en una nota o comunicado: `node kit/web/frase.js <url> cap st '{"clave":"frase exacta"}'`.
   - Página de la marca: adaptar `kit/web/ejemplo_pagina_im8.js` y `ejemplo_faq_im8.js` (ocultan banners y lo prohibido antes de capturar, 3 px por px CSS).
4. Escribir la lista de tomas copiando `kit/ejemplos/gabriel33_v01.py` (usa `kit/verde_ayudas.py`, que ya trae anuncios, tarjetas, capturas con recuadro, gráficos y el registro de fuentes): cada `toma(id, t0, t1, fondo, lugar_de_Gabriel)` con los tiempos de la transcripción, y el `GUION` de subtítulos (una palabra del guion por cada palabra transcrita; `*` marca la clave; `~` oculta una palabra). El del 32 (`gabriel32_v03.py`) es anterior y trae sus ayudas adentro.
5. Hoja de cuadros: `python3 kit/render_verde.py config.py --prev t1,t2,… --out hoja.jpg`. Mirar todas las tomas antes de renderizar.
6. Control (abajo). Render: `python3 kit/render_verde.py config.py --out GABRIEL_<n>_vNN.mp4` (unos 8 minutos por 76 s; correrlo en segundo plano).
7. Sonidos: copiar `kit/ejemplos/sonido33_v01.py` (usa `kit/sonido_verde.py`: `tr`, `plano`, `clic`, `bop`, `foto`, `foco`, `glitch`, `golpe` y `montar`), poner cada evento en el tiempo del corte o de la marca, y correrlo sobre el mp4 renderizado.
8. Verificar el archivo (duración, LUFS, cuadros negros o congelados) y mirar una hoja de cuadros del mp4 final. Entregar y actualizar esta skill.

## Control antes de entregar

`python3 kit/render_verde.py config.py --control` informa la tarjeta más corta, cuánto se ve la clave que menos se ve, las líneas achicadas y los visuales repetidos; falla si hay alguno repetido que no esté declarado en `REPETICION_PERMITIDA`. Además, a ojo:

- **Portada**: sacar el cuadro 0 y mirarlo a tamaño completo. Cara visible, título arriba, sin logo repetido.
- **Logos duplicados**: revisar cada gráfico propio y el título.
- **Recuadros**: ampliar cada captura marcada y leer qué quedó adentro del recuadro.
- **Cada clip**: que lo que se ve sea lo que dice la frase y no tenga nada de la lista prohibida.
- Lo que el control no ve: dos fuentes distintas que se parecen (dos zonas de la misma página, dos tramos del mismo anuncio).

## Errores que ya pasaron

- El recuadro rojo cayó sobre otra frase: la página repetía el texto en un bloque oculto. `frase.js` ya exige que esté visible, pero igual se amplía y se lee.
- Un clip elegido por la miniatura resultó ser un primer plano que no tenía nada que ver. Siempre sacar cuadros del tramo exacto.
- La barra de búsqueda de la Biblioteca es fija y se repite en las capturas 2 a 4; la grilla real termina antes de lo que parece.
- La Biblioteca a veces responde "No ads match" aunque haya anuncios (en AG1 la vista general falló todo el día y solo cargaron el filtro de video y la búsqueda por texto). `biblioteca_capturas.js` reintenta solo; si sigue vacía, usar otro filtro y avisar que ese número no se pudo capturar.
- Sitios con verificación anti-bots (drinkag1.com): no se intenta saltarla. Se pide la captura a Agus o se dibuja un gráfico propio.
- Una nota con muro de pago (Glossy) no muestra la cifra: buscar la misma cifra en otra fuente de la guía.
- Las ayudas usan `fondo_grafico()` para dibujar gráficos; `BASE` importado con `*` queda vacío.
- Recuadro rojo sobre fondo rojo: no se ve.
- El texto propio de un anuncio quedó detrás de Gabriel: usar `Clip(..., subir=px)` o cambiar el lugar de Gabriel.
- Una pregunta sobre Black Friday quedó visible en una lista de preguntas frecuentes: revisar también el texto chico de las capturas.
- El conector de Drive no baja archivos de más de 10 MB ni edita el contenido de archivos existentes. Los de hasta 10 MB los guarda en disco.
- La v03 del 32 se entregó sin sonidos y Agus los tuvo que pedir: los sonidos van desde la primera versión.

## Historial y pendientes

Ver `historial.md`: qué se hizo en cada video, qué quedó pendiente con Gabriel y qué videos faltan.
