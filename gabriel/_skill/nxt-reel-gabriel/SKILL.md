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

## Más videos que gráficos, hook dopamínico (Gabriel, feedback del 38, 39 y 40, 2026-11-23)

- **Hook (0–6 s): ráfaga de videos** de las marcas que se van a nombrar, ~1,5 s cada uno ("o si no alcanzan todas, las que alcancen"), con el título encima: "necesitamos que el hook sea lo más dopamínico posible siempre". No una imagen fija ni una cuadrícula.
- **No abusar del gráfico**: "del segundo 52 hasta casi el 1:10 solo se usa gráfico, no podemos abusar tanto… tenemos que irlo turnando con videos para que no perdamos la atención; tanto tiempo viendo solo letras la va a aburrir". Nunca más de ~4 s de gráfico seguido: intercalar con anuncios de la marca (Biblioteca de Anuncios) o videos de su web. Si una idea se puede contar con videos (estilo de vida, uso del producto), van videos con una etiqueta corta encima (`T_`), no un gráfico.
- **Al hablar de la marca, su publicidad**: "en especial cuando ya empezamos a hablar de la marca, meter vídeos de la publicidad de ellos".
- **Gráficos más visuales**: "que no quede simplemente tachar la palabra sino algo visualmente más llamativo o con figuras" (figuras, objetos que se transforman, personas, íconos), y "efecto de dinero" cuando hay plata en juego (`lluvia_billetes` en el 39 v02, `contador` en verde_ayudas).
- **Lo que se ve tiene que ser lo que se dice**: "esta representación no está alineada con lo que se dice" (40: "suplementos deportivos" → gente entrenando, no tarros grises; "dejar de inventar sabores" → video del trabajo detrás de un sabor, no vainilla/chocolate tachados). Para un oficio o una persona que se nombra (fisicoculturista, instructor de vuelo): una foto real (Wikimedia Commons sirve; no stock pago).
- **Gráficos grandes, sin huecos** (revisión del 41 y el 44): cada gráfico propio llena y≈170–730 con elementos grandes (figuras e íconos ≥ 200 px, textos ≥ 60 px), entrando por partes. Nunca pastillitas arriba con todo el blanco vacío debajo.
- **Notas de prensa y páginas como tarjeta**, nunca la página entera en letra chica ni una franja fina sobre blanco: zoom hasta que la frase marcada sea grande (alto de mayúscula ≥ ~45 px) y entre completa con margen (nunca cortada por un borde), dentro de una tarjeta (medio + titular arriba, el párrafo con la frase abajo) que llena y≈170–730 sobre un fondo real desenfocado (producto o anuncio de la marca).
- **Cada video o anuncio una sola vez**: si se reusa un clip, ponerle su nombre real de fuente para que `--control` lo detecte.
- Si la marca no tiene ningún video (Bio.me: sin anuncios activos ni videos en su sitio), se avisa en la entrega.

## Base para los próximos videos (Agus, 2026-11-23: "top, seguir así, el cliente va a renovar 30 videos más… quiero que sea una base")

El enfoque del 38, 39 y 40 es la base: todo lo de esta skill se aplica igual en cada video nuevo, y se va mejorando de a poco.

**Contador de dinero cuando dice una cifra de plata** ("cuando diga millones haya animaciones de contador de dinero"): cada vez que Gabriel dice millones, miles de dólares, ventas, facturación o una valuación, la cifra aparece como contador que sube de 0 al número y frena al llegar (con un rebote chico), sincronizado: arranca cuando empieza a decir la cifra y llega al número cuando termina de decirla.
- Dentro de un gráfico propio: `c = contador(400, t0, dur=0.9, sufijo=' M')` y en el gráfico `c(im, tl, 540, 430)`.
- Encima de una captura o un anuncio: `toma(..., texto=contador_toma(990, t0, cy=420, sufijo=' millones'))` (caja oscura detrás, número en verde).
- Formato latino (1.000.000; decimales con coma, `dec=1`). Prefijo `US$` por defecto; para pesos u otra moneda, `prefijo='$'` o `'€'`.
- Sonido: `bop(t0, CUENTA, ...)` al arrancar y `bop(t_fin, MONEDA, ...)` al llegar (del paquete de Naza).
- La cifra es la que dice Gabriel; si la fuente dice otra (estimado, "casi"), va en un texto chico debajo ("estimado", "Fuente: …").

## Antes de mandarle CUALQUIER video a Gabriel: lo que él siempre corrige

Agus (2026-11-21): "el cliente suele pedir muchos detalles, así que cada vez que mandamos un video acordate que va a mandar una corrección". Cada entrega vuelve con algo. Antes de enviar, mirar el video como lo mira él y pasar esta lista (sale de sus correcciones reales); lo que no cumpla se arregla antes, no después:

1. **Primer cuadro / portada**: grande y llamativa. La imagen principal llena desde el título hasta la cabeza de Gabriel; nada chico "apretado arriba" con un hueco desenfocado debajo ("queda un espacio gigante aquí… se está perdiendo lo llamativo de la primera imagen"). Se ve la cara de la persona; el título no la tapa. En un VS con fundadores conocidos, van ellos (con el logo de su marca), no los productos.
2. **Ningún hueco grande** en ninguna toma: si entre el subtítulo y Gabriel queda una franja vacía o desenfocada de más de ~250 px, agrandar o bajar el visual.
3. **Nada repetido**: ninguna imagen dos veces, y la del inicio no vuelve ni a mitad ni al final.
4. **Video antes que imagen fija**: dos capturas seguidas no; grilla de la Biblioteca como fondo no, si existe el video. En los momentos fuertes y en el cierre, video.
5. **Cierre**: personas usando o tomando el producto, no el producto solo ni la portada. **Termina cuando termina su voz** (Gabriel, 2026-11-23: "está más largo el video que mi voz, porque se sigue moviendo cuando yo dejé de hablar"): sin cola, `DUR` = duración del crudo.
6. **Cada recuadro, flecha o subrayado** está sobre las palabras exactas que prueban la frase que suena (Agus, 2026-11-23: "cuando marcas algo en rojo, que sea lo que dice… hay veces que marcas las cosas erróneas… que no vuelva a pasar"). Reglas fijas:
   - **Nunca ubicar una marca a ojo.** Cada rectángulo sale medido del texto en la página: `frase.js` (notas), `pagina_entera.js` con `FRASES='[...]'` (páginas), `biblioteca_capturas*.js` con `{"id": ["frase 1", "frase 2"]}` (tarjetas de la Biblioteca → `cards[id].frases[frase]`). En el config se usan esos rectángulos directo, sin sumar ni estimar.
   - Para el nombre de un producto o un precio: recuadro, no subrayado (el subrayado cae sobre la línea de abajo).
   - **El rectángulo medido puede no coincidir con la captura** (39: en bio.me la página cambió de letra después de medir y el recuadro de "fiber supplements" cayó sobre "wellness"). Por eso la hoja de `revisar_marcas.py` se mira siempre. Si no coincide, se vuelve a capturar o se mide sobre la misma imagen por píxeles (columnas y filas de texto oscuro en la banda de la frase) y se anota en el config cómo se midió.
   - Imágenes sin texto medible por la página (fichas de producto en .webp, tablas en una foto): medir por píxeles la columna o la fila que se marca. Si la marca baja hasta la franja de subtítulos (y 735–1060), marcar solo la parte que entra (39: las 6 primeras dosis de la ficha de Blueprint), no achicar todo hasta que no se lea.
   - En videos de anuncios no va marca: el texto del video no se puede medir.
   - **Antes de renderizar: `python3 kit/revisar_marcas.py config.py hoja.jpg`.** Recorta cada marca en su segundo, con lo que dice el subtitulo debajo, y avisa si queda fuera de pantalla, bajo el título, en la franja de subtítulos o detrás de Gabriel. Mirar la hoja entera y leer cada recorte: tiene que decir lo mismo que el subtítulo. Cero avisos antes de renderizar.
7. **Cada visual** muestra lo que se está diciendo en ese segundo (si habla de podcasts, de lives, de TikTok: eso mismo, o lo más cercano que exista y avisar).
8. **Texto propio de los anuncios** fuera de la franja de subtítulos y no detrás de la cabeza de Gabriel.
9. **Logos**: uno solo por cuadro.
10. **Sonido**: sin el "angelical" (Botanical / Deep), efectos bajos que acompañan.

Y al entregar: decir en dos líneas qué se hizo con cada cosa que pidió, y avisar lo que no se pudo conseguir. Gabriel numera los videos distinto que las carpetas: identificar el video por lo que se ve en su captura.

## Al terminar cada video: subirlo a la web de revisión (SIEMPRE, sin que Agus lo pida)

Agus (2026-11-23). Le pasa al cliente un link propio de NXT donde ve sus videos y deja el feedback por segundo:
**https://nxt-revision.netlify.app/#gabriel**

Regla de oro: la página NUNCA queda vacía ni pierde videos. Cada video nuevo se SUMA (Video 1, 2, 3…). Una corrección del mismo video reemplaza solo ese video y conserva su número.

Pasos (PC Windows de Agus, carpeta `NXT_CLIENTES\_REVISION\_local`; desde una sesión en la nube hay que pedir esa carpeta con `request_computer_folder`):
1. Agregar el video (usar la versión liviana `_celular` / `_para_subir` si existe):
   `python publicar.py agregar gabriel "<ruta al mp4>" --titulo "Video 32" --version v01 --nombre "Gabriel Monsalve"`
   - Mismo `--titulo` que uno anterior = corrección (reemplaza ese video y actualiza la versión).
   - `python publicar.py lista` muestra qué hay en cada página.
2. Armar el paquete con TODA la web (todas las entregas de todos los clientes, porque cada publicación reemplaza el sitio entero):
   `python publicar.py paquete --destino "<scratchpad de la sesión>\partes"`
   (nunca en el Escritorio: Google Drive sincroniza el Escritorio y la extensión de Chrome no sube esos archivos).
3. Publicar en Chrome (Claude in Chrome, cuenta de Google de Agus): app.netlify.com/projects/nxt-revision/deploys → con JS crear un `<input type=file>` por cada parte → subir cada parte con file_upload (UNA por llamada, máximo 10 MB) → unirlas con JS en un solo `File([...partes], 'nxt-revision.zip')` → ponerlo en `#dropzone-file-upload` y disparar `change`. Esperar a que diga "Published".
4. Verificar en vivo `nxt-revision.netlify.app/#gabriel`: que estén todos los videos (los viejos también) y que el nuevo cargue.
5. Pasarle a Agus el link, listo para mandar.

La página de Gabriel (`entregas/gabriel.json` del sitio) lista los videos en orden: `{ "n": 8, "titulo": "Video 38", "version": "final", "archivo": "videos/gabriel/video-38-final.mp4" }`. **`n` es la posición en la página** (1 = Video 31, 2 = Video 32 … 8 = Video 38, 9 = Video 39, 10 = Video 40) y el feedback se guarda con ese número: nunca renumerar. El video nuevo va al final con el `n` siguiente; una corrección reemplaza el archivo y conserva su `n`.
- Desde la nube no hay token de Netlify (Agus no lo pasa) ni la carpeta de la PC: Agus publica. Para pasarle videos, versiones livianas (`GABRIEL_NN_drive.mp4`, 720×1280, 2 pasadas a 760k, 7–9 MB). El conector de Drive no sube nada de más de ~3 MB por llamada. Si al subir al Drive le sale "file unreadable", el archivo está en una carpeta sincronizada (Escritorio) o no terminó de bajar: moverlo a Descargas.

**Feedback del cliente**: leerlo directo del Apps Script (devuelve JSON con video, segundo, versión, nombre, texto y tipo "nota" o "aprobado"):
`curl -sL "https://script.google.com/macros/s/AKfycbxy3y2s_HGwFCr2RdDcZnq3SPUQ2V1h5dhdoRyP3d3L686rPyvlN0GGX-1nIecDlDftEg/exec?entrega=gabriel"`
(hosts script.google.com y script.googleusercontent.com habilitados en el entorno). "video" es la posición en la página: Video NN = posición NN − 30. También queda en la planilla "Feedback NXT" (hoja "Feedback"). Cuando Agus pregunte "¿qué dijo Gabriel?", leerlo y corregir con el segundo exacto.

## Correcciones de Gabriel del 2026-11-21 (AG1 y Lemme vs IM8) · valen para todos

Dijo "de resto está brutal". Lo que pidió, textual, y la regla que deja:

- "En vez de poner dos seguidas del administrador, pondría la anterior que es un pantallazo de administrador y **el video de esa creadora, como tal el anuncio y no el pantallazo**, para que el corte sea más dopamínico." → nunca dos capturas de la Biblioteca seguidas: después de una captura va el anuncio real en video.
- "Aquí en vez de eso, pondría **contenido en video** que tienen en TikTok de fondo." / "Aquí se repite la imagen del comienzo, usaría mejor **videos de las dos marcas**." / "Y aquí al final nuevamente la misma imagen. También cambiarlo por algo de video." → **la portada no se repite** ni a mitad ni en el cierre (reemplaza la regla 10 de su guía): ahí van videos de la marca (en un VS, `Mitades` con un video de cada una). Siempre que haya video real, va video antes que grilla o captura.
- "En la foto de la comparación me gustaría que se vieran **los fundadores**." → en un VS de marcas con cara conocida, la portada son las dos personas (con el logo de su marca), no los productos.
- "Creo que no está alineado con lo que se viene hablando o se puso el cuadrado en un punto que no es." → el recuadro va exactamente sobre las palabras que prueban la frase (se dijo "ya no es de un mes, sino de 3" → recuadro en "Quarterly subscription"); ampliar y leer cada recuadro antes de renderizar.
- "Cuando hablamos de los podcast si podemos mostrar un cortico de algún podcast estaría top, solo si lo encuentran." → opcional; no se baja de YouTube.
- Sobre el 35 (Liquid I.V. vs Electrolit): "solo la última toma no me gusta porque es la misma del inicio, pondría algo más visual y **no solo el producto, alguien tomándolos**". → en el cierre van personas usando o tomando el producto. En `Mitades`, los clips se recortan en cuadrado sin su texto propio (`clip(id, ss, recorte=(720, 720, 0, y), entero=150)`) para que las dos mitades queden parejas y nada pise el subtítulo. Ejemplo: `kit/ejemplos/gabriel35_v02.py`.
- Dónde hay video de una marca además de la Biblioteca: su propio sitio. `node kit/web/imagenes_y_videos.js <url>` lista las imágenes grandes y los videos que carga cada página (en lemmelive.com: la portada y /pages/ambassador).
- Ojo con los números: Gabriel llamó "35" al de AG1 (el 33) y "38" al de Lemme vs IM8 (el 37). Identificar el video por lo que se ve en su captura, no por el número.

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
- **Recorrido de un test** (video 36, Aluné): las pantallas del test se capturan una por una con `kit/web/test_por_pasos.js` (viewport 430×764, que ya es 9:16; guarda la captura y el rectángulo de cada texto). En el config, `pant(prefijo, n, marcas, foco='texto')` muestra la pantalla a todo el ancho y corre la vista para que el dato quede arriba de los subtítulos; `r_(prefijo, n, 'texto')` da el rectángulo para el recuadro. Plantilla: `kit/ejemplos/gabriel36_v02.py`.
- **VS** (video 35, "Liquid I.V. vs Electrolit"): es el formato pantalla verde con dos marcas frente a frente. La primera marca del título va SIEMPRE a la izquierda y la otra a la derecha. Pantalla dividida solo para comparar las dos a la vez (portada, un momento a mitad y el cierre): `Mitades(fuente_izq, fuente_der)` para dos clips, o una imagen armada para la portada (los dos productos y un "VS"). El resto, una imagen a la vez, con la misma prueba para las dos (la misma vista de la Biblioteca). En los gráficos propios va arriba el logo de la marca de la que se habla (`G2(fn, CHIP_x)`), recortado de un anuncio suyo. Plantilla: `kit/ejemplos/gabriel35_v02.py` (y `gabriel37_v05.py`, hecho sin guía).

## Pantalla verde: cómo es

- **Gabriel** recortado del verde, pegado al borde de abajo, siempre sobre imagen, video o gráfico a pantalla completa. Nunca sobre fondo vacío. Lugar: `C` (el único que se usa). `R` (abajo a la izquierda, como la referencia), `G`, `ML`/`MR` y `PL`/`PR` quedan en el motor por los videos viejos y no se usan.
- **Gabriel cambia de lugar a lo largo del video** (Gabriel, feedback del 38, 39 y 40, 2026-11-23: "me quedo solo en el medio, recuerda que tengo que ir moviéndome por la pantalla, en algunas tomas a la derecha, en otras a la izquierda, en otras en el medio"; "cambiar la ubicación de mi silueta a lo largo del vídeo para darle más dinamismo"). Mismo tamaño y altura de siempre (escala 0,74, tope de la cabeza en y 1300), pero el lugar cambia toma a toma: `CI` (cabeza en x 290), `CD` (x 790) y `C` (centro, x 540). En el config, al final: `LUGARES = ['CI', 'CD', 'C']` y `for k, sh in enumerate(S): sh['gab'] = LUGARES[k % 3]` (o elegir a mano por toma). Esto reemplaza la regla anterior de "fijo al centro" (Agus, 2026-11-20). `revisar_marcas.py` ya mira dónde está Gabriel en cada toma. En cada crudo medir `CABEZA` (fila del tope de su cabeza) y ponerla en el config.
- **Lo que se señala va arriba de la franja de subtítulos**: los subtítulos ocupan y 735–1060 (la línea blanca sube a 735 cuando hay palabra clave) y Gabriel ocupa abajo al centro (cabeza x 390–690 desde y 1300, hombros de lado a lado desde y 1600). El precio, la frase o el recuadro que se está nombrando tiene que quedar entre y 150 y 720; como mucho, algo chico entre y 1080 y 1280 o a los costados de su cabeza; si cae en la franja, se reencuadra la captura (en el 34 los subtítulos tapaban los precios de los paquetes).
- **Texto propio de los anuncios**: casi todos traen subtítulos quemados a media altura. Elegir el tramo del anuncio donde su texto no cae en la franja 800–1060 (o es una sola palabra chica), y nunca dejar un titular del anuncio justo detrás de nuestra línea. Si el anuncio es una imagen con mucho texto, va entera y más chica arriba: `anuncio(id, encaje=(0.62, 40))`.
- **Ritmo**: corte seco siempre, sin transiciones ni efectos. Imagen nueva cada 1–2 s; ráfagas de 0,5–1 s al enumerar. Lo que Gabriel nombra se ve en ese mismo segundo. El crudo ya viene sin pausas.
- **Material**: real de la marca y en la mejor calidad. Anuncios de la Biblioteca de Anuncios de Meta con su texto original; capturas de su página; la fuente de cada cifra (comunicado, nota) con el dato marcado. Nada de stock.
- **Marcas rojas**: flecha + recuadro sobre la cifra o frase; subrayado en frases cortas; zoom leve hacia el dato. Sobre fondo rojo el recuadro va blanco (`caja_b`). Nunca círculos, resaltador amarillo, stickers ni emojis animados.
- **Gráficos propios**: fondo claro punteado, logo de la marca arriba una sola vez, elementos simples que entran por partes, en la mitad de arriba (abajo está Gabriel y en el medio el subtítulo). Con Gabriel en `C` van más grandes que antes (`G(fn, k=0.76…0.92)`): el `k` más alto con el que el dibujo termina arriba de y 720.
- **Subtítulos** (juego aprobado): línea blanca Inter Display SemiBold 86 px; palabra clave Inter Display ExtraBold 180 px en verde menta `#4DCB84`, debajo de la blanca y tocándola, siempre dibujada encima. La clave entra cuando se dice (fundido 0,07 s, escala 88 → 100 % en 0,11 s); las blancas por corte seco. Lugar fijo en todo el video: línea sola en y 850, clave en y 880. Una clave por frase como máximo; no terminar una tarjeta en conector ni cruzar una coma. Todo lo dicho aparece.
- **Portada**: foto oficial de la persona o marca, entera, con la cara entre el título y la franja de subtítulos. Título en caja oscura, Inter Display ExtraBold, con la cifra en verde. Si la portada es un anuncio con su propio titular arriba, va entero y más chico sobre su versión desenfocada (`clip(..., encaje=(0.68, 330))`) para que el título no lo pise.
- **Qué no se muestra**: cada guía trae su lista (en IM8: anuncios de peso o GLP-1, porcentajes de resultados del estudio clínico, antes y después, testimonios con nombre, avisos de Black Friday, precios resaltados). Se tapa en la captura (ocultar el elemento antes de capturar) o se elige otro material.
- **Final con la voz** (reemplaza el "cierre con cola" del 36): Gabriel pidió que el video no siga cuando él dejó de hablar. `DUR` = duración del crudo (el crudo ya termina con la última palabra), sin sonido de cierre después de la voz y con un fundido corto del audio (`montar(..., fundido=0.12)`). El último subtítulo queda hasta el final (`armar_tarjetas(..., dur=DUR)`).
- **Audio**: voz a −14 LUFS, pico −1,5 dBFS.

## Sonido

Agus: "los sonidos, clave". Van siempre, con el estilo del video 31.

- **De dónde salen**: carpeta de Drive "sonidos" de Naza (id `1J3lIkZN-0oNCYm2UVprYrfAQUsbiLDVS`, dentro de "recursos"), 33 archivos (20 bajados al principio + `Granular Combo (10)` y `(13)`, `approach_2`, `Fast B.Music Transition (1)` y `Enter & Back`, bajados el 2026-11-21). Es el mismo paquete del 31. Se bajan con `download_file_content` del conector de Drive, que deja el archivo en disco (hasta 10 MB cada uno). La carpeta es privada: no sirve `curl`.
- **Motor**: `kit/nxt_sonido.py`, el mismo del 31, sin cambios. Ejemplo completo: `kit/ejemplos/sonido32_v04.py` y su informe `GABRIEL_32_v04_sonidos.txt`. La pista de efectos se mezcla con la voz y se monta sobre el video ya renderizado sin volver a renderizar la imagen.
- **Receta 2** (pedido de Agus sobre el 37, 2026-11-21: "el sonido que se escucha como angelical, de fondo, sacalo, reemplazalo por otro mejor, y que los sonidos se escuchen un poco más bajitos, que acompañen"):
  - **No se usan más `Botanical Whoosh (1)` ni `Deep, Mini, Whoosh (11)`**: los dos tienen un tono sostenido de 624 Hz (el "angelical") y sonaban en cada transición y en cada entrada. Tampoco `approach_2` (tono de 1 kHz).
  - La capa de aire de las transiciones y las entradas es un tramo corto (0,35–0,55 s) de `Granular Combo (13)` con pasa-bajos: textura sin tono. Los graves (`Momo WOOSH 3`, `slow woosh`, `Hit Impact`) siguen yendo con esa capa, porque solos no se oyen en el celular.
  - **Todo 3 dB más bajo** que la receta del 31: cada efecto queda entre 19 y 23 dB por debajo del pico de la voz (`BAJAR = 3.0` en `sonido_verde.py`; `montar(..., bajar=0)` reproduce lo anterior).
  - Nunca pitidos; nunca el mismo sonido muchas veces seguidas; sin risers.
  - Para elegir un sonido nuevo del paquete, medirlo antes: si tiene un tono sostenido (planitud espectral ≈ 0 y más de 1 s), no va de fondo.
- **Qué va dónde** (como quedó en el 32):
  - Cambio de capítulo → transición: `Momo WOOSH 3` o `slow woosh` + capa de aire (`Granular Combo (13)`), alternando las cuatro combinaciones.
  - Entrada de un gráfico, una tarjeta o un clip → textura corta sola (`Granular Combo (13)`, cinco tramos que rotan), no en todos los cortes.
  - Recuadro rojo sobre una cifra → clic (`Magnetic, Button` 7, 10, 13; `Granular, Button, Select`; `Button, Cursor, Select`), rotando archivos.
  - Enumeraciones (lista de anuncios, partes de la oferta) → un `Mini list` distinto por ítem.
  - Dos golpes clave por video, en las dos frases más fuertes → `Hit Impact` + `Magnetic, Button`.
  - Tachado o negación → `Fast Glitch 1`. Ráfaga de anuncios → `camera shutter sfx`. Monedas → `Coin Flip`. Calendario → `Countdown, List, Numbers`.
- **Control**: el informe lista cada sonido con su tiempo y nivel, cuántas veces se usa cada archivo, el pico de la pista y si hay tonos sostenidos. Mezcla final a −14 LUFS, pico −1,5 dBFS.
- En el 31 la versión final llevó además la canción que pidió Gabriel, 19 dB bajo la voz. En el 32 no se pidió.

## Flujo

1. Leer la sección del video en la guía y, si hay, las correcciones pendientes. Elegir el entorno "gabriel-edicion".
2. Bajar el crudo. Transcribir: `python3 kit/transcribir.py crudo.mp4 pal.json "Marca, nombres"`. Revisar nombres propios (escribió "IMA" por IM8).
3. Juntar material:
   - Anuncios: `node kit/web/biblioteca_cosechar.js <id_pagina> bodies.txt palabra1,palabra2` y enseguida `python3 kit/bajar_anuncios.py bodies.txt ads/` (los enlaces vencen). Mirar `hoja_jpg.jpg` y `hoja_mp4.jpg` para elegir; para cada video sacar una hoja de contacto de un cuadro por segundo (`ffmpeg -i ad.mp4 -vf "fps=1,scale=180:320,tile=12x2" -frames:v 1 hoja.jpg`) y elegir el segundo exacto: sin texto del anuncio en la franja de subtítulos y que muestre lo que dice la frase.
   - Grilla y tarjetas de la Biblioteca: `node kit/web/biblioteca_capturas.js <id_pagina> cap '{"<library id>":"frase a subrayar"}'`.
   - Frase con cifra en una nota o comunicado: `node kit/web/frase.js <url> cap st '{"clave":"frase exacta"}'`.
   - Página larga entera (un artículo, para recorrerla): `node kit/web/pagina_larga.js <url> cap art` saca tramos solapados y se unen descartando la franja de arriba de cada tramo (ahí se repite el encabezado fijo).
   - Página de la marca: adaptar `kit/web/ejemplo_pagina_im8.js` y `ejemplo_faq_im8.js` (ocultan banners y lo prohibido antes de capturar, 3 px por px CSS).
4. Escribir la lista de tomas copiando `kit/ejemplos/gabriel34_v03.py` (Gabriel fijo en `C` en todas las tomas) (usa `kit/verde_ayudas.py`, que ya trae anuncios, tarjetas, capturas con recuadro, gráficos y el registro de fuentes): cada `toma(id, t0, t1, fondo, lugar_de_Gabriel)` con los tiempos de la transcripción, y el `GUION` de subtítulos (una palabra del guion por cada palabra transcrita; `*` marca la clave; `~` oculta una palabra). El del 32 (`gabriel32_v03.py`) es anterior y trae sus ayudas adentro.
5. Hoja de cuadros: `python3 kit/render_verde.py config.py --prev t1,t2,… --cols 4 --ancho 540 --out hoja.jpg` (8 cuadros por hoja, grandes). Mirar todas las tomas, con el subtítulo puesto, antes de renderizar: en el 34 la primera pasada tenía seis choques de texto que el control no ve.
6. Control (abajo). Render: `python3 kit/render_verde.py config.py --out GABRIEL_<n>_vNN.mp4` (unos 8 minutos por 76 s; correrlo en segundo plano).
7. Sonidos: copiar `kit/ejemplos/sonido34_v01.py` (usa `kit/sonido_verde.py`: `tr`, `plano`, `clic`, `bop`, `foto`, `foco`, `glitch`, `golpe` y `montar`), poner cada evento en el tiempo del corte o de la marca, y correrlo sobre el mp4 renderizado.
8. Verificar el archivo (duración, LUFS, cuadros negros o congelados) y mirar una hoja de cuadros del mp4 final. Entregar y actualizar esta skill.

## Control antes de entregar

`python3 kit/render_verde.py config.py --control` revisa primero que **cada clip exista y alcance** para el tramo pedido (39 v01: un id de anuncio mal tipeado cortó el render a los 47 s y el video salió congelado desde ahí), y después informa la tarjeta más corta, cuánto se ve la clave que menos se ve, las líneas achicadas y los visuales repetidos; falla si hay alguno repetido que no esté declarado en `REPETICION_PERMITIDA`. Además, a ojo:

- **Portada**: sacar el cuadro 0 y mirarlo a tamaño completo. Cara visible, título arriba, sin logo repetido.
- **Logos duplicados**: revisar cada gráfico propio y el título.
- **Recuadros**: ampliar cada captura marcada y leer qué quedó adentro del recuadro.
- **Cada clip**: que lo que se ve sea lo que dice la frase y no tenga nada de la lista prohibida.
- Lo que el control no ve: dos fuentes distintas que se parecen (dos zonas de la misma página, dos tramos del mismo anuncio).

### Pasada final (antes de decir "listo para entregar")

Sacar una hoja con **un cuadro por segundo del mp4 final** (`ffmpeg -ss N -t 24 -i video.mp4 -vf "fps=1,scale=270:480,tile=8x3" -frames:v 1 hoja.jpg`, de a 24 s) y mirarla entera. Lo que apareció en la pasada final del 37 y el control no ve:

- **Pantalla dividida (`Mitades`)**: cada mitad ocupa y 170–1130, así que el texto propio de un anuncio (que suele ir al 60–70 % de su alto) cae justo en la franja de subtítulos. Para las mitades elegir videos sin texto en esa zona (tomas de producto) o revisar cuadro por cuadro.
- **Primer cuadro de cada clip**: si el `ss` cae 0,1 s antes de un corte interno del anuncio, entra un destello de otra escena. Ubicar el corte exacto (color medio cuadro a cuadro) y arrancar después.
- **Frases cortadas en una captura**: si la frase que prueba lo que se dice queda cortada por el borde, reencuadrar hasta que se lea entera.
- **Texto del anuncio detrás de la cabeza de Gabriel** (x 390–690, de y 1300 para abajo): subir el video (`entero=30`) o elegir otro tramo.

## Errores que ya pasaron

- **Render cortado sin aviso** (39 v01): el error quedó escondido detrás de `| tail` y la mezcla de sonido rellenó el resto con el último cuadro. Renderizar siempre con `set -o pipefail`, el log completo a un archivo (`> salida/render.log 2>&1 || { tail -20 salida/render.log; exit 1; }`) y comprobar con `ffprobe` que la pista de video dure `DUR` antes de mezclar.
- Un producto que la marca ya no vende (Ghost × Sour Patch Kids / Oreo, 40) no está en su tienda ni en su `products.json`: las fotos oficiales siguen en las notas de Stack3d (`https://www.stack3d.com/post-sitemap.xml` … `post-sitemap5.xml`, filtrar por marca y sabor; la imagen es el `og:image` de cada nota) y en el blog de la marca (`sitemap_articles_1.xml`). Amazon responde 503 a los bots y el archivo web (web.archive.org) no se pudo habilitar.
- En una página con beneficios al lado del producto (Bio.me, Grüns, Blueprint), la captura entera muestra promesas de salud prohibidas por la guía: armar un panel (foto + título + precio, el resto tapado en blanco) o una ficha solo con las columnas que se necesitan, y revisar el texto chico.
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
- Se interpretó la referencia de Agus al pie de la letra (persona abajo a la izquierda) y él quería a Gabriel al centro como ya estaba en el 34 v01: ante un cambio de encuadre, mandar un cuadro de muestra antes de renderizar todo.
- Al cambiar a Gabriel de lugar, lo que estaba pensado para ese rincón quedó detrás de él (una etiqueta, el cuarto ítem de una lista): revisar todas las tomas después de cambiar el lugar, y si una lista no entra, que la captura baje por ella.
- El 36 v01 terminaba 0,2 s antes de que acabara la última palabra (se puso `DUR` en el final de la transcripción): el final se mide en el crudo, no en la transcripción, y lleva cola.
- La Biblioteca de Anuncios a veces responde "No ads match" para todos los países y sí muestra todo con el país de la marca: `PAIS=CO node kit/web/biblioteca_cosechar_pais.js <id> bodies.txt` y `PAIS=CO node kit/web/biblioteca_capturas_pais.js …` (pasó con Mumu).
- Una página con un producto prohibido en la grilla o fotos de antes y después: `kit/web/pagina_entera.js <url> salida.png "palabra prohibida"` saca la tarjeta que la contiene, `OCULTAR_IMG="y0-y1"` esconde las imágenes de esa banda y `FRASES='[...]'` devuelve el rectángulo exacto de cada frase.
- Si la guía no trae el video (pasó con el 37), se hace igual con el formato que corresponde y se avisa arriba de todo en la entrega; antes se vuelve a leer el documento por si lo completaron.
- Un anuncio elegido por la miniatura ("The Ultimate Test") hablaba de otra cosa (Fórmula 1, no estudios clínicos): leer el texto del anuncio en grande antes de usarlo.
- Un sitio reparte variantes distintas de la misma página (el test de Aluné tiene dos portadas y dos páginas de oferta): reintentar con contexto nuevo hasta que salga la que describe la guía, y capturar todo el recorrido en una misma corrida.
- Cuando un script de exploración imprime cada pantalla, limitar la salida (pocos caracteres por paso): una corrida larga llenó la conversación.
- Los recuadros de una página cayeron 30–40 px corridos: se midieron los elementos y después se hizo scroll y la página se acomodó. Medir en el mismo momento de la captura (`kit/web/ejemplo_pasos_liquid.js`).
- Videos de anuncios que no son 9:16 (cuadrados, 4:5, apaisados): al llenarlos a pantalla se les corta el texto de los costados. Van enteros con `clip(id, ss, entero=150)`; si traen franjas negras o interesa una zona, `recorte=(w, h, x, y)`.
- Un sitio con verificación anti-bots (bevnet.com) no dejó capturar la cifra: va un gráfico propio con la cifra de la guía y "Fuente: …", y se avisa.
- Una palabra que la transcripción no entiende ("De las que Electrolit…"): no se inventa; se oculta con `~` y se avisa.
- La v03 del 32 se entregó sin sonidos y Agus los tuvo que pedir: los sonidos van desde la primera versión.
- La columna de compra de una tienda (Shopify) es `position: sticky`: si la captura oculta todo lo fijo y lo pegajoso, desaparece. En esa página ocultar solo lo `fixed`.
- Una flecha quedó cortada contra el borde porque el recuadro ocupaba todo el ancho: sin margen, va el recuadro solo o se abre el encuadre.
- Dos anuncios con el mismo id pueden ser piezas distintas (un video y una imagen del mismo anuncio): mirar las dos antes de descartar una por repetida.

## Historial y pendientes

Ver `historial.md`: qué se hizo en cada video, qué quedó pendiente con Gabriel y qué videos faltan.
