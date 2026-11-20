# Estilo · Gabriel Monsalve (@gabriel.growthp)

**Estado: BORRADOR v01 (2026-11-15). Nada aprobado por Agus todavía.**

**Actualización 2026-11-20: el formato pantalla verde con subtítulos (video 32, IM8) quedó APROBADO por Gabriel como base de sus próximos videos. Ver 0.j y 0.k. Desde el 34, Gabriel va fijo abajo a la izquierda: ver 0.l.**

Cómo leer las marcas:
- **[M]** medido en el material (cuadros, ffprobe, ebur128, detección de cortes).
- **[E]** estimado: sale de una medición indirecta, hay que confirmarlo de oído o con transcripción.
- **[S]** suposición mía. No es regla hasta que Agus la confirme.

Material analizado: `2_estilo_referencias/` (18-4, 19_editado_v4, 20_final, 24, 30), el crudo `5_crudos_para_editar/31`, y 2 capturas de `6_marca/`.
Hojas de cuadros y datos: `Gabriel/_analisis/`.

---


## 0.a Decisión de Agus (2026-11-15, dicho en el chat)

- Gabriel quiere una **edición nueva, distinta** a la de los 5 videos de referencia.
- De esos videos **se conservan solo las fuentes y el juego de subtítulos** (secciones 3 y 4).
- Formatos, ritmo, B-roll y cierre de las secciones 2, 5 y 7 quedan como **registro de lo anterior, no como regla**.
- Agus pide que la propuesta sea creativa, al nivel de lo que hace NXT.
- El detalle de la edición nueva sale del feedback de Gabriel (pendiente de cargar).

## 0.b Decisiones de Agus (2026-11-15, segunda tanda, dicho en el chat)

- **Subtítulos: blanco con palabra clave en amarillo.** Confirmado.
- **La tele tiene que estar presente** en el formato mini charla. Ningún zoom ni encuadre la saca del cuadro.
- **NUNCA el armado "una toma abajo, una toma arriba"** (recortes apilados / pantalla partida). Queda prohibido el formato A de la sección 2.
- La primera edición del 31 la hizo un editor con IA y Agus la descartó: "lo editó no solo mal, sino sin criterio". Cada decisión de edición tiene que tener un motivo.
- Forma de trabajo: preguntar solo lo necesario y avanzar con lo que ya hay.

## 0.c Formato mini charla · parámetros de la v01 del video 31 (propuesta, sin aprobar)

Motor: `Gabriel/_kit/render_gabriel.py` · config: `Gabriel/_salidas/31/gabriel31_v01.json`.

- Espejado corregido (hflip): la tele se lee bien.
- **Sin zoom.** La tele ocupa de 0,29 a 0,60 del alto y todo el ancho: cualquier zoom la corta. **[M]**
- **Subtítulo en la pared, arriba de la tele**: centro en x 540, y 400 (0,21 del alto). Es la única zona libre en las 16 tomas: la cara se mueve entre 0,47 y 0,75 y de lado a lado. **[M]**
- Degradado negro suave arriba (0 a 600 px, 53 % a 0 %) para que el blanco se lea sobre la pared clara.
- Fuente Inter Display SemiBold (OFL, del kit NXT), 86 px, sombra suave, corte seco.
- Tarjetas de 2–4 palabras; ninguna termina en conector suelto; ninguna dura menos de 0,28 s.
- Amarillo `#FFE13C`: una palabra clave por frase como máximo (20 en 62 s).
- Voz −14,1 LUFS, pico −1,5 dBFS. Termina 0,2 s después de la última palabra.
- **Falta la capa de impacto** que pidió Gabriel: imágenes de apoyo y B-roll de 3 s como máximo. (Resuelto en la v05.)

### v05 (sin aprobar) · config `Gabriel/_salidas/31/gabriel31_v05.json`
- 10 insertos a pantalla completa, corte seco, entre 1,08 y 2,97 s. Suman 21 s de 62 (34 %).
- Cada inserto empieza y termina en un cambio de toma o de frase, para no dejar astillas de Gabriel de menos de 1 s. Plano más corto del video: 1,03 s; promedio 2,47 s.
- Fotos con acercamiento lento del 5 %; clips sin cortes internos.
- El bloque "estudios de creatina en mujeres" va sin inserto: la diapositiva de la tele ya lo muestra.
- El subtítulo sigue en el mismo lugar sobre los insertos, con sombra reforzada y oscurecido de arriba con caída suave (0 a 760 px).
- 4 sonidos distintos, sin pitido, solo en la entrada de un bloque de B-roll. Sin música (regla de Agus).
- v02, v03 y v04 quedaron en `_salidas/_descartadas/`: las frenó el control por planos de menos de 1 s.

## 0.d Juego de subtítulos pedido por Agus (2026-11-15) · aplicado en la v06

Dicho por Agus: "palabras simples, blancas o finitas… y la palabra clave en el medio", "palabra simple en blanco, palabra clave en amarillo", "que no esté encimada, y si está encimada, que esté un poquito más la amarilla", "no quiero nada de ruido visual". Vale para todos los clientes; acá va con las fuentes de Gabriel.

Referencia de animación: `WhatsApp Video 2026-11-06 at 5.14.46 PM (1).mp4` (Descargas). Medido cuadro por cuadro a 60 fps **[M]**: palabra chica blanca; cuando viene la clave, la chica queda arriba y la clave entra debajo, 2,3 veces más grande, por corte seco, encimada con la chica. Todo en el mismo lugar.

Cómo quedó en Gabriel (config `gabriel31_v06.json`):
- Palabras simples: Inter Display SemiBold, 72 px, blancas. Solas van en y 400.
- Palabra clave: Inter Display ExtraBold, 150 px (se achica sola si no entra en 900 px de ancho), amarilla `#FFE13C`.
- La clave **cierra** su tarjeta: las simples quedan arriba (y 322), la clave debajo (y 428). **No se enciman.** Siempre las mismas dos alturas.
- Aparición de la clave: fundido de 0,07 s y escala de 88 % a 100 % en 0,11 s. Sin rebote. Entra cuando Gabriel la dice y se ve al menos 0,5 s.
- Las palabras simples entran y salen por corte seco.
- Una clave por frase como máximo (20 en 62 s).
- **Ubicación:** queda en la pared, arriba de la tele. En el centro real de la pantalla tapa el texto de la diapositiva y la cabeza de Gabriel (ver `_salidas/31/MAQUETA_subtitulos_en_el_centro.jpg`). A confirmar con Agus.

## 0.e Ajustes de Agus sobre la v06 (2026-11-15) · aplicados en la v07

Dicho por Agus: "Noto mucho espacio entre las palabras. La blanca un poquito más abajo y hace falta que toquen entre las dos, pero que la amarilla siempre sea un poquito por encima. Es a la misma altura, nada más que estén más juntas. Ese mismo formato me encantó." · "Que no tape la cara ni la tele. Está bueno que sea arriba o a donde está el micrófono de él." · "Que los recortes estén todos en la misma sintonía, no haya nada de ruido visual."

### Subtítulos (config `gabriel31_v07.json`)
- En la v06 había 40 px de aire entre la base de la blanca y el tope de la amarilla (68 px si la clave no tiene letras altas). **[M]**
- Ahora la blanca baja 48 px: su base queda **8 px adentro** del tope de las letras altas de la amarilla. Se tocan. **[M]** (base blanca en y 390, tope amarilla en y 382).
- La amarilla se dibuja **siempre por encima** de la blanca (capa superior, con su sombra corta que las separa).
- La amarilla no se movió de lugar (y 428). La blanca sola sigue en y 400.
- Ubicación aprobada por Agus: arriba, en la pared. Alternativa que él mismo dio: a la altura del micrófono.

### Insertos "en la misma sintonía" (regla nueva)
1. **Solo va un inserto cuando suma algo que la diapositiva de la tele no muestra.** Si la tele ya lo dice, queda Gabriel con la tele. Por eso bajaron de 10 a 8 (26 % del video).
2. **Encuadre:** siempre a pantalla completa, con el sujeto entero y ningún texto del producto debajo del subtítulo.
3. **Movimiento:** todas las fotos se acercan a la misma velocidad (2,2 % por segundo), no el mismo porcentaje.
4. **Entrada y salida:** corte seco, en un cambio de toma o junto con la palabra clave.
5. **Tono:** brillo y saturación se acercan a los de las tomas de Gabriel (brillo 117, saturación 11), con tope: gamma entre 0,90 y 1,20; saturación como mucho −20 %. A las tomas de Gabriel **no** se les toca el color.
6. **Nitidez:** no se usa una imagen que haya que agrandar 3 veces.

Qué salió y por qué:
- Bolsa Growth: su título quedaba debajo del subtítulo (texto sobre texto) y era 2 veces más saturada que Gabriel.
- Impact Whey con fondo azul: dice "Unflavored" y se usaba para "su sabor favorito"; además tenía look de publicidad.
- Pared de bolsas MyProtein: 3 veces más saturada que Gabriel y con trama cargada debajo del subtítulo. La reemplaza la bolsa Impact Whey Blueberry.
- Foto del gimnasio (420 px de ancho): pixelada a pantalla completa. La reemplaza un plano HD de sogas del clip Podium.
- Laboratorio y "sabor favorito": sin inserto, la diapositiva ya lo muestra.

Medido en la v07 **[M]**: brillo de los insertos entre 74 y 138 (antes 60 a 152); saturación entre 4 y 15 (antes hasta 32). 24 planos, el más corto 1,03 s, promedio 2,58 s.

### Texto
- 24,7 s: en pantalla va "Lo que no sabe es que las mujeres…". El transcriptor escribe "Que no sabes que", con confianza baja en la primera palabra (0,27); la frase arranca justo en un corte. **[E]** Lectura elegida por sentido y por paralelo con "Lo que ella no sabe es que ese polvo…" (14,0 s). Falta confirmación de oído.

## 0.f Pedidos de Agus y de Gabriel sobre la v07 (2026-11-15) · aplicados en la v08

Dicho por Agus: "agregarle los sonidos. Los sonidos, clave" · "cuando aparezcan B-rolls, que los subtítulos estén en el medio, y cuando él está hablando, arriba de la tele… ese dinamismo" · "un poquito más grande en los B-rolls" · "el color de las palabras claves, que es amarillo, quiere cambiarlo… ese verde que predomina [en ggrowth.info]".

### Color de la palabra clave
- Paleta leída del CSS de https://ggrowth.info/ **[M]**: verde bosque `#1E3A2F` (el que más superficie ocupa: botones y secciones), `#1E4034`, verde medio `#2C6E49` (palabras resaltadas del sitio), salvia `#A9D3B4`, crema de fondo `#F2EFE7`, latón `#B08D4F`.
- En video: clave en **verde bosque `#1E3A2F` con filete crema `#F2EFE7` de 6 px**. Sin filete el verde bosque no se lee sobre fondos oscuros ni sobre la pared (es casi negro). **[M]** en cuadros reales.
- Comparación de 4 variantes en `Gabriel/_salidas/31/COMPARACION_verdes.jpg` (bosque con filete, salvia, menta, verde medio con filete). Falta que Agus/Gabriel confirmen la elegida.
- El amarillo `#FFE13C` queda fuera.

### Subtítulos: dos lugares fijos
- **Habla Gabriel:** arriba de la tele (y 400), como en la v07.
- **B-roll:** en el centro de la pantalla (y 960) y 20 % más grandes (blanca 86 px, clave 180 px).
- El cambio de lugar cae siempre en el mismo cuadro que el corte de imagen. Si una tarjeta empezaba o terminaba a menos de 0,2 s de un corte, entra o sale con el corte (no hay texto que salte dos cuadros).
- En el centro lleva una aureola oscura muy difusa para leerse sobre blanco (leche, vestido).
- Sobre los insertos ya no se oscurece la parte de arriba.
- La clave entra cuando Gabriel la dice; solo se adelanta lo justo para verse 0,33 s como mínimo.
- Las tarjetas se parten buscando el mejor corte de cada frase (no terminar en conector, no cruzar comas, la clave cierra su tarjeta con hasta 3 palabras chicas arriba).
- Un inserto que entra casi junto con una clave entra exacto con ella: "gimnasio" (23,21 s) y "menos" (26,23 s).

### Insertos
- Sale el tarro Gold Standard: con el subtítulo en el centro quedaba texto sobre la etiqueta. En su lugar va un segundo plano del mismo clip del ángel (plano abierto 6,03–7,27 s, plano cerrado 7,27–9,20 s), que es de lo que habla la frase.
- Quedan 8 insertos, 16 s de 62 (26 %). 24 planos, el más corto 1,07 s.

### Sonido (receta de la skill `nxt-reel-agus`)
- Por qué no se oían los 4 de antes: estaban 18,5 dB bajo la voz y eran graves solos, que en el celular no suenan.
- Ahora: 25 sonidos, cada uno con el pico entre 13 y 17,7 dB bajo el pico de la voz; los graves con capa de aire; clics distintos que rotan; 2 golpes clave ("difícil", "ahí sí"); glitch en "raro"; obturador en la foto de la góndola; subida suave en "Seguimos". Sin música.
- Detalle con tiempos y niveles: `Gabriel/_salidas/31/GABRIEL_31_v08_sonidos.txt`. Motor: `Gabriel/_kit/nxt_sonido.py`.
- Control de pitidos sobre la pista de efectos: 0 tonos sostenidos. **Nadie los escuchó todavía.**

### Reel de referencia que mandó Gabriel
- https://www.instagram.com/reel/DfsILrVS99X/ (realchasechappell, 104,6 s). Visto cuadro por cuadro en el navegador **[M]**:
 - el presentador va **recortado, abajo y siempre en pantalla** (ocupa el 30 % de abajo), con micrófono;
 - detrás, a pantalla completa: B-roll de la marca, o un fondo claro con puntos donde se arma un **diagrama** (logo arriba, títulos, flechas, columnas, grillas de caras);
 - **no lleva subtítulos palabra por palabra**: solo un título en el gancho (caja rosa) y las etiquetas del diagrama.
- Es el formato C de sus videos viejos (24 y 30) con diagramas. Para hacerlo con el crudo 31 hay que recortar a Gabriel del fondo en todo el video (rembg, sin instalar todavía) y rehacer sus diapositivas como gráficos (falta el archivo original).
- **Sin aplicar.** Pendiente de que Agus decida si la v09 va por ahí.

## 0.g Pedidos de Agus sobre la v08 (2026-11-15) · aplicados en la v09

Dicho por Agus: "Me gusta, pero también quiero que tengas el que hace al final following, y también usa overlays para pasar de transición a transición, y si querés algún zoom in y zoom out muy suave" · "cuando dice proteínas de sabor podés agregar una vez una foto, una vez otra, o las dos juntas al mismo tiempo" · "al cliente el que le gusta es el que tiene sin bordes" (mandó foto de la opción 3 de la comparación de verdes).

### Color de la clave (reemplaza lo de 0.f)
- **Verde menta `#4DCB84`, sin borde**, con la misma sombra que tenía el amarillo. Es la opción que eligió el cliente.
- Ojo: ese verde no está en el CSS de ggrowth.info; es un derivado más claro del verde de la página (`#2C6E49`) para que se lea en video. Si piden el tono exacto de la página, los disponibles son `#1E3A2F`, `#2C6E49` y `#A9D3B4`.

### Cierre "Seguir → Siguiendo"
- Recurso NXT (ver "Cierre la están siguiendo" en `ESTILO_SOFI.md` del kit): píldora blanca, cara sacada del propio material (no de Instagram), `@gabriel.growthp`, botón verde bosque "Seguir". Sin logo de Instagram, sin cursor.
- Entra con la tarjeta "a esa personita" (60,33 s), sube 26 px con fundido de 0,18 s; a los 0,72 s hay un toque (onda blanca, el botón se hunde) y pasa a "✓ Siguiendo" gris. Queda hasta el final (61,8 s).
- **Dónde:** en el lugar de la palabra clave (centro en y 462), arriba de la tele. Mientras está, la línea blanca va en su altura de "dos líneas" (y 370). No tapa cara ni tele.
- Aro del avatar en el color de la clave. Avatar: cuadro de 13,2 s del crudo.
- Sonidos: entra la tarjeta (detalle fino, 17,7 dB bajo la voz), toque (clic, 15,2 dB).

### Destellos en las transiciones
- Pasada de luz crema muy suave, de 14 cuadros (0,47 s), con el pico justo en el corte. Solo al **entrar y al salir de cada bloque de B-roll** (12 en el video); nunca en los cortes entre tomas de Gabriel ni dentro de un bloque.
- Va debajo de los subtítulos: el texto no se lava. Alterna el lado desde el que entra la luz.
- Hecho por código (`destellos` en el config), sin archivos de overlay externos.

### Zoom en las tomas de Gabriel
- Muy suave: 1 % por segundo, con tope de 3,5 %. Una toma acerca, la siguiente aleja (18 tomas).
- Hecho con `perspective` (interpolación cúbica): medido el borde de la tele, se mueve 4 px por segundo de forma pareja, sin saltos. **[M]**
- La tele sigue entera en el cuadro; los subtítulos no se mueven (se dibujan después).

### Proteínas de sabor
- En "una prote de su sabor favorito" (52,50–53,96 s) van **las dos juntas**: frutilla-kiwi arriba y chocolate abajo, cada una con su acercamiento lento y su tono igualado; el subtítulo cae en la franja del medio.
- Es el único lugar donde hay dos imágenes apiladas, por pedido explícito de Agus. No se usa con Gabriel en una de las mitades.
- Quedan 9 insertos, 17,6 s de 62 (28 %).

### Control de la v09 **[M]**
- Voz −14,1 LUFS, pico −1,4 dBFS. Sin cuadros negros ni congelados.
- 28 sonidos, 19 archivos distintos, 0 pitidos sostenidos.
- Todos los tramos duran 1,08 s o más (verificado contra la lista de cortes; el detector automático ya no ve los cortes con destello).
- Blanca y clave se tocan en los dos lugares (8 px de solape arriba y al centro).

## 0.h Pedidos de Agus sobre la v09 (2026-11-15) · aplicados en la v10

Dicho por Agus: "los subtítulos van muy rápido, no los llego a leer ni yo… que se lean más; están muy buenas las animaciones" · "cuando dice tu polvo de queso, no toca como un riser, eso sacalo. Y ahí meter un overlay… alguno de esos. Hacerlo un poco más artístico" · "la proteína de chocolate de abajo se ve muy mal. Elegí otra mejor."

### Velocidad de lectura (reemplaza la partición de 0.f)
- Gabriel habla a 279 palabras por minuto (4,6 por segundo): con 2-3 palabras por tarjeta, cada una duraba 0,6 s. **[M]**
- Ahora las tarjetas son de 4-5 palabras: **76 en vez de 101**, mediana 0,80 s (antes 0,61 s). Quedan 7 de menos de 0,5 s, todas frases cortas que no se pueden unir ("Seguimos", "mensual", "mejor dicho"). **[M]**
- Tope de largo: 24 caracteres arriba y 20 en B-roll (donde la letra es más grande). La línea más ancha mide 746 px, dentro de la zona segura. **[M]**
- La palabra clave se queda **al menos 0,6 s**: primero se le presta hasta 0,15 s a la tarjeta siguiente; si no alcanza, entra hasta 0,2 s antes de ser dicha.
- Al partir, pesa más no romper la frase que la duración: no se cruza una coma, una pregunta arranca tarjeta, no se termina en conector ("lo que" y "es que" sí cierran). Las frases de menos de 1,3 s van en una sola tarjeta ("Entonces ¿qué vas a / hacer?").
- Límite real: con todas las palabras en pantalla, se lee a la velocidad a la que habla. Más lento que esto solo se logra mostrando menos palabras, y eso rompe la regla NXT de que todo lo dicho aparece.

### Overlays más artísticos (reemplaza los destellos de 0.g)
- Hechos por código (`_quemado` en el motor): entre 3 y 5 manchas de luz orgánicas que cruzan la pantalla, cada una con su color, su recorrido y su pico un poco corrido, más un velo corto en el corte. Cada overlay sale distinto (semilla propia): no se repite el mismo.
- **Suave** (crema): al entrar y salir de cada bloque de B-roll, 12 en el video.
- **Fuerte** (quemado ámbar y naranja): en los dos cambios de capítulo, "Seguimos" → 21,17 s y "Bueno, ahora presta atención" → 34,73 s. Tapa el salto entre dos tomas de Gabriel.
- 16 cuadros (0,53 s) con el pico en el corte; siempre debajo de los subtítulos.

### Sonido
- Sale la subida de "Seguimos". En los dos overlays fuertes va un whoosh corto (17 dB bajo la voz).
- 29 sonidos, pico de la pista de efectos 12,5 dB bajo la voz, 0 pitidos.

### Proteínas de sabor
- Abajo va ahora el tarro Gold Standard con el bol de frutillas (entra entero, sin recorte lateral). Arriba sigue el Shark frutilla-kiwi.
- La foto de la bolsa Growth de chocolate no se usa más con Gabriel.

### Control de la v10 **[M]**
- Voz −14,0 LUFS, pico real −1,3 dBTP. Sin cuadros negros ni congelados. Dura 61,9 s (0,1 s más de aire al final).
- 27 tramos de video, el más corto 1,08 s. 9 insertos, 16,1 s (26 %).

## 0.i Música (pedido de Gabriel, 2026-11-15) · motor listo, falta el archivo

- Tema pedido: **"win again - slowed", de trucky** (1:19). Link que mandó: https://www.youtube.com/watch?v=31tLO-swqNc. Captura en `Gabriel/feedback_capturas/5_cancion_win_again_slowed.jpg`.
- Dicho por Gabriel: "tener cuidado con los sonidos de los efectos para que no queden mal agregándole la música; si queda raro, mejor quitarle el sonido al efecto o bajarle un poco".
- Para Gabriel se usa música desde ahora (antes la regla NXT era sin música).
- Motor (`musica` en el config): mide la sonoridad real de la voz y del tramo del tema y lo deja **19 dB por debajo de la voz** (receta de Agus); se agacha un poco más mientras Gabriel habla (ducking suave); fundido de entrada 0,6 s y de salida 1,2 s; efectos bajados 2 dB en bloque (`efectos_db`).
- Probado con un tema de `_COMPARTIDO/MUSICA`: mezcla final −14,1 LUFS, pico −1,4 dBFS **[M]**.
- No se baja de YouTube (tema con derechos). Decisión del 2026-11-15: **la canción la pone Gabriel desde la biblioteca de música de Instagram al publicar**.
- v11 (`gabriel31_v11.json`) queda lista para eso: sin música en el archivo, sin los clics de las palabras clave (de 29 sonidos a 16) y con los efectos que quedan 2 dB más bajos (golpes 3 dB). Pico de la pista de efectos 15,7 dB bajo la voz, 0 pitidos, mezcla −14,1 LUFS **[M]**.
- Si en algún momento llega el archivo con licencia, se agrega con `musica` en el config.

## 0.j Formato pantalla verde · video 32 "Las 6 piezas del sistema" (IM8) · APROBADO por Gabriel (2026-11-20)

Dicho por Gabriel sobre la v02: "de resto está brutal". Queda como base para todos sus reels de pantalla verde.

- Referente que pidió Gabriel para todos los formatos de pantalla verde: Chase Chappell (@realchasechappell). Su guía de edición (Drive, "Copy of Guia edición", una sección por video) trae reglas y lista de tomas.
- Motor: `gabriel/_kit/render_verde.py` (repo `agusvazquezcm22-cloud/-`, rama `claude/gabriel-session-mo1f56`) y dentro de la skill `nxt-reel-gabriel` (`kit/`). Lista de tomas del 32: `gabriel32_v03.py`.
- Gabriel recortado del verde, pegado abajo, siempre sobre imagen, video o gráfico a pantalla completa. Cinco lugares fijos: grande (media pantalla), medio izquierda/derecha, pequeño en esquina izquierda/derecha. Cambia de lugar en cada corte, nunca dentro de una toma.
- Corte seco, sin transiciones. Imagen nueva cada 1–2 s.
- Material real de la marca: anuncios de la Biblioteca de Anuncios de Meta (imagen y video), capturas de su página y de la fuente de cada cifra, con flecha + recuadro rojo sobre el dato. Sobre fondo rojo el recuadro va blanco.
- Gráficos propios: fondo claro punteado, logo de la marca arriba una sola vez, elementos simples que entran por partes. Aprobado por Gabriel ("fondo claro punteado con gráficos arriba y Gabriel abajo").
- Subtítulos: el mismo juego del 31 (blanca Inter Display SemiBold 86 px; clave ExtraBold 180 px verde menta `#4DCB84` debajo y tocándose, siempre encima; la clave entra cuando se dice con fundido 0,07 s y escala 88 → 100 % en 0,11 s; blancas por corte seco). Lugar fijo: línea sola en y 850, clave en y 880 (justo arriba de la cabeza de Gabriel cuando va grande). La guía de Gabriel decía "sin subtítulos propios"; los pidió Agus y Gabriel los aprobó.
- Voz a −14 LUFS, pico −1,5 dBFS. Sin música (la pone Gabriel en Instagram) y sin efectos de sonido: así se aprobó.
- No se muestra (regla 12 de su guía para IM8; revisar la de cada video): anuncios de peso o GLP-1, porcentajes de resultados del estudio clínico, antes y después, testimonios con nombre, avisos de Black Friday ni precios resaltados.

## 0.k Reglas aprobadas por Gabriel (2026-11-20) · valen para todos sus videos

Salen de sus correcciones a la v02 del 32. Frases textuales en `gabriel_correcciones_IM8_2026-11-20.md`.

1. **El título nunca tapa la cara de la persona de la portada.** El primer cuadro es la portada: la persona se ve entera y el título va arriba, por encima de ella. — "Me gustaría que se viera Beckham en la foto y el título quedara encima de él, porque le queda en toda la cara, y esa sería la portada". Cómo se resolvió: foto entera a lo ancho sobre su propia versión desenfocada, cara entre el título y la franja de subtítulos, título fijo desde el cuadro 0.
2. **No repetir el mismo logo o marca dos veces en un cuadro.** — "Aquí sale IM8 arriba dos veces". En gráficos propios el logo va una sola vez arriba; si el gráfico ya muestra la marca (un sobre, una caja con logo), va sin logo arriba. El título no lleva logo si ya nombra la marca.
3. **Cada visual representa la frase que suena en ese momento.** Si no aporta, se cambia por otro visual o por video. — "Esta representación no está alineada con lo que se está hablando, no dice mucho; reemplazarla por otros visuales u otro tipo de video" (eran tres cajas rojas dibujadas; se reemplazó por una clienta que recibe su pedido y el tramo "si lo tomara 90 días" del mismo anuncio).
4. **No usar el mismo B-roll o captura más de una vez por video.** — "Este creo que lo usamos dos veces, ¿cierto? ¿o 3?" (la captura de los US$285). Única repetición que queda: el cierre vuelve a la imagen de la portada, porque lo pide la regla 10 de su guía.
5. **El cierre también lleva apoyo visual.** — "Podemos buscar quizás imágenes o videos más visuales que representen eso". En el 32: muro de anuncios reales, dos anuncios en video, su página, su oferta y el programa para suscriptores.
6. **Subtítulos con tiempo de lectura.** Ninguna tarjeta menos de 0,7 s en pantalla; la palabra clave grande, al menos 0,8 s visible. Si no alcanza, se unen tarjetas o se corre el corte entre tarjetas (como mucho 0,3 s respecto de la voz); nunca se acorta el tiempo. Reemplaza los mínimos de 0.h (0,6 s).

Control obligatorio antes de entregar: tarjeta más corta, visuales repetidos, logos duplicados y la portada (`render_verde.py <config> --control` + hoja de cuadros).

### Qué quedó en la v03 del 32 (medido)
- 79 tarjetas; la más corta 0,70 s; la clave que menos se ve, 0,80 s; el corte más corrido respecto de la voz, 0,22 s.
- 50 fuentes distintas en 34 tomas; ninguna repetida salvo la portada en el cierre.
- Pendiente con Gabriel: dice "unos 1.500 anuncios" y la Biblioteca mostraba "~1,800 results" el día de la edición; la foto oficial de Beckham mide solo 692 px.

## 0.l Recorte fijo de Gabriel (referencia de Agus, 2026-11-20)

Referencia: reel de Chase Chappell "10 BFCM Meta Ads that Sell like CRAZY" (`instagram.com/reel/Df-d9U5y4nh`).
Pedido textual: "Mismo formato como venimos haciendo, pero que el recorte de Gabriel no pase de un lugar a otro, sino que se vea así.
Está buena la toma esa que pones, que se ve él más grande también en el medio… obviamente adaptado a la referencia, más que nada en
el recorte; subtítulo, dinamismo y demás, venimos re bien."

- Gabriel va **siempre abajo a la izquierda**, mismo tamaño, desde la portada: tope de la cabeza al 62 % del alto, centro de la cabeza al 25 % del ancho, hombro izquierdo cortado por el borde.
- El plano más grande al centro se usa una sola vez, en el cierre, y no vuelve.
- Nunca salta de lado entre cortes (reemplaza la regla 2 de sus guías).
- Lo que se señala va arriba de los subtítulos o a la derecha de Gabriel; nada importante en el rincón de abajo a la izquierda.
- Hechos así: 34 v02 y 33 v02.

## 0. Pendientes (bloquean partes del estilo)

- `feedback.txt` cargado (WhatsApp), pero faltan el punto 1 y el final del punto 3.
- Falta la versión editada del 31 sobre la que opinó Gabriel: va en `3_no_quiero/`.
- `preguntas_de_agus.txt` vacío.
- `1_editados/` y `3_no_quiero/` vacías. No sé si los 5 videos de referencias son trabajos de NXT aprobados o referencias externas.
- No hay un crudo con su versión editada: no se pudo deducir cómo se corta (qué toma queda, cuánto aire).
- Desfase voz/subtítulo: sin medir (hace falta leer los subtítulos cuadro por cuadro).
- No escuché el audio: no sé qué música ni qué SFX llevan.
- `_COMPARTIDO/SONIDOS` y `MUSICA` vacías. `4_brolls/` vacía.

---

## 1. Marca (solo lo que sirve para editar)

- @: `gabriel.growthp` · nombre: Gabriel Monsalve · verificado. **[M]**
- Foto de perfil: él con suéter blanco, Torre Eiffel de fondo. **[M]** Falta el archivo en buena calidad para un cierre con "Seguir".
- Tema: marcas de salud y suplementos (historias de marcas: Celsius, Tang, SILA, Blueprint). **[M]**
- Portadas del perfil: título en mayúsculas, blanco con una palabra en amarillo o azul. No hay una sola fuente: cambia entre portadas. **[M]**
- Color de acento que más se repite: amarillo (palabras clave, resaltador sobre artículos, CTA). Verde solo en los contadores de plata del video 30. **[M]**

---

## 2. Formatos: hay TRES distintos en 5 videos **[M]**

| Formato | Videos | Cómo es |
|---|---|---|
| A · Pantalla partida | 18-4, 19 | B-roll arriba (35 % del alto), Gabriel abajo en selfie. Subtítulo sobre la unión. |
| B · Exterior cuerpo entero | 20 | Gabriel de pie en la calle, sin B-roll. Notificaciones de WhatsApp e íconos arriba. |
| C · Recorte sobre B-roll | 24, 30 | B-roll a pantalla completa, Gabriel recortado (busto) abajo. Subtítulo al centro. |

- El crudo 31 es un cuarto formato: "mini charla" con una tele atrás que muestra diapositivas. **[M]**
- **[S]** Por la numeración (18 → 30), el formato C es el más nuevo y el que hay que tomar como principal. A confirmar.

---

## 3. Subtítulos

### Común a los 5 videos **[M]**
- Color blanco, sin caja, con sombra suave. Nunca contorno grueso.
- Minúsculas; mayúscula solo al empezar frase. Sin punto final.
- Centrados en horizontal, una sola línea.
- No hay palabra resaltada dentro del subtítulo: el acento va en un texto aparte (ver sección 4).

### Por formato

| | A (18-4, 19) | B (20) | C (24, 30) |
|---|---|---|---|
| Palabras por tarjeta **[M]** | 1–2 | 1–2 | 2–3 |
| Altura (0 = arriba, 1 = abajo) **[M, ±0,01]** | 0,34 (la unión de las dos mitades) | 0,65 (sobre el pecho) | 0,55 fijo |
| Tamaño **[E]** | chico, ~36 px de alto de letra | ~40 px | ~48 px |
| Fuente **[S]** | parecida a Arial/Helvetica Bold | sans geométrica apretada | sans geométrica apretada, peso medio (parecida a Inter / SF Pro) |

- En el video 24 el subtítulo baja a 0,71–0,73 cuando el recorte de Gabriel está en el centro (10–11 s y 43–44 s). **[M]** Choca con la regla base "texto que cambia de lugar".
- En el video 30 el subtítulo pisa texto de artículos de fondo y no se lee bien (13 s, 35–38 s). **[M]**
- En el formato B el subtítulo va encima del cuerpo de Gabriel (pecho), no de la cara. **[M]**
- Cómo entran y salen (medido cuadro por cuadro en el 30, de 0,4 a 1,4 s): **corte seco**. Una tarjeta reemplaza a la otra de un cuadro al siguiente, sin fundido, sin escala y sin movimiento. **[M]**
- La tarjeta se centra según su ancho: no hay posición fija de inicio de línea. **[M]**

---

## 4. Textos de acento y gráficos **[M]**

- **Palabra golpe** (formato A): una palabra grande sobre Gabriel, abajo (alto 0,79–0,86). Blanca ("¿Confiar?", "Dic. 2023") o amarilla ("millones").
- **Años** (video 19): número blanco grande sobre el B-roll de arriba (1959, 1965, 1968).
- **Contadores de plata** (video 30): cifra verde sobre pastilla oscura redondeada ("$587M", "$800M", "+100"), alto 0,77, a la izquierda del recorte.
- **Resaltador amarillo** sobre capturas de artículos (18-4, 24, 30).
- **Notificaciones de WhatsApp** (video 20): tarjeta arriba, alto 0,26–0,33, con la pregunta escrita.
- **Íconos en fila** (video 20): 3 íconos azules con etiqueta, arriba (alto 0,05–0,12), entran de a uno.
- **Logos** en tarjeta blanca redondeada (18-4, logo SILA).
- B-roll antiguo en blanco y negro cuando el tema es histórico (video 19).

Cómo entran (medido cuadro por cuadro) **[M]**:
- Palabra golpe (18-4, "¿Confiar?"): sube desde abajo y se asienta en 4 cuadros (0,13 s), con un rebote mínimo. Tiene sombra dura abajo a la derecha, además de la suave.
- Contador de plata (30): la pastilla entra chica y crece en 2 cuadros; el número cuenta rápido al principio y frena al llegar (de $56M a $786M en 12 cuadros, 0,4 s). Tipografía ancha y pesada (**[S]** parecida a Helvetica Neue Black Extended / Archivo Black), verde claro sobre pastilla casi negra con esquinas redondeadas.

---

## 5. Ritmo y B-roll **[M]**

| Video | Duración | Cortes de plano | Plano promedio |
|---|---|---|---|
| 18-4 (A) | 57,1 s | 13 | 4,1 s |
| 19 (A) | 66,3 s | 20 | 3,2 s |
| 20 (B) | 24,5 s | 5 | 4,1 s |
| 24 (C) | 63,9 s | 48 | 1,3 s |
| 30 (C) | 56,7 s | 39 | 1,4 s |

- El formato C corta tres veces más rápido que el A.
- En 24 y 30 hay planos de menos de 1 s (24: cerca de 4 s, 26 s, 28 s, 37 s, 59 s; 30: cerca de 4–6 s, 31–32 s, 43 s). **[M]** La base NXT los prohíbe. **[E]** Algunos pueden ser transiciones que el detector cuenta como corte.
- B-roll: casi el 100 % del tiempo hay B-roll en pantalla en A y C; 0 % en B. **[M]**
- Tipo de B-roll: publicidades y fotos de la marca de la que habla, capturas de notas de prensa, gráficos de bolsa, material de archivo. **[M]**
- El recorte de Gabriel cambia de lugar en el 24 (abajo centro, abajo derecha, arriba en burbuja). En el 30 queda fijo abajo a la derecha. **[M]**
- Zooms y transiciones: **sin medir**.

---

## 6. Audio

| Video | Volumen integrado **[M]** | Pico **[M]** | Voz fuerte − piso entre palabras **[E]** |
|---|---|---|---|
| 18-4 | −16,8 LUFS | −0,1 dBFS | 9,4 dB |
| 19 | −15,9 LUFS | −0,5 dBFS | 9,5 dB |
| 20 | −11,4 LUFS | +0,1 dBFS | 6,3 dB |
| 24 | −13,4 LUFS | −0,4 dBFS | 8,2 dB |
| 30 | −12,6 LUFS | −0,5 dBFS | 8,0 dB |

- El volumen varía 5,4 LU entre videos. Ninguno está en −14 LUFS exacto y todos pasan el pico de −1 dBTP de la base NXT. **[M]**
- No hay ni un silencio de más de 0,15 s por debajo de −35 dB en 4 de los 5 videos (uno solo de 0,31 s en el 24). **[M]**
- **[E]** Eso indica que hay música o ambiente continuo y que la voz va con cero aire. La diferencia real música/voz no la puedo medir sin separar pistas.
- SFX: **sin identificar** (no escuché el audio).

### Pausas y ritmo de voz (transcripción con Whisper large-v3; tiempos ±0,05–0,10 s) **[M]**

| Video | Ritmo | Pausa entre frases (mediana / máxima) | Huecos de 0,25 s o más | Primera palabra | Aire al final |
|---|---|---|---|---|---|
| 18-4 | 206 pal/min | 0,08 s / 0,42 s | 2 | 0,00 s | 0,36 s |
| 19 | 225 pal/min | 0,11 s / 0,18 s | 0 | 0,00 s | 0,11 s |
| 20 | 214 pal/min | 0,21 s / 0,32 s | 1 | 0,00 s | 0,35 s |
| 24 | 259 pal/min | 0,08 s / 0,30 s | 2 | 0,00 s | 0,37 s |
| 30 | 254 pal/min | 0,07 s / 0,26 s | 2 | 0,00 s | 0,17 s |
| crudo 31 | 279 pal/min | 0,09 s / 0,34 s | 1 | 0,00 s | 0,37 s |

- Los 5 arrancan hablando en el cuadro 0 y terminan a menos de 0,4 s de la última palabra. **[M]**
- Pausa entre frases típica: 0,07–0,11 s. Es **cero aire**, como Unai y Carlos, no el respiro de 0,30 s de Agus y Jesús. **[M]**
- El ritmo sube de 206 a 259 pal/min entre los videos viejos y los nuevos. **[M]**
- El crudo 31 ya viene más apretado (279 pal/min) que cualquiera de los editados. **[M]** **[S]** O Gabriel lo cortó antes de mandarlo, o está acelerado. No hay cortes de silencios por hacer ahí.
- Cierres hablados: "comenta marca y te paso mi biblioteca" (18-4), "mándaselo a esa persona…" (19), "escribe posicionamiento" (20), "compártelo… y sígueme" (24), "mándaselo a esa personita. Nos vemos." (31). **[M]**
- Gabriel tutea ("comenta", "escribe", "sígueme"). El texto en pantalla del 18-4 dice "comentá", con voseo: no coincide con lo que dice. **[M]**

---

## 7. Cierre **[M]**

- Los 5 terminan con un llamado a la acción dicho por Gabriel. Ninguno tiene tarjeta de "Seguir" ni logo de Instagram.
- 18-4: `comentá "MARCA"` en amarillo, cursiva, con contorno, sobre Gabriel (alto 0,78). De fondo, su página "biblioteca de recursos".
- 19: ícono de compartir blanco sobre Gabriel.
- 20: palabra amarilla que entra desde la izquierda junto a "escribe".
- 24: termina hablando ("más historias como…"), sin gráfico de cierre.
- 30: palabra clave verde entre comillas (“CONECTA”) y su página de recursos a pantalla completa.
- **[S]** Regla candidata: el cierre siempre es "comentá + palabra clave" con la página de recursos de fondo.

---

## 8. Crudo 31 ("Suplementos Novia · formato mini charla") **[M]**

- 1080×1920, 30 fps, HEVC, SDR (bt709). No hace falta pasar de HLG. Dura 61,9 s.
- **Ya viene cortado**: 15 saltos de plano y pausas de 0,26 s como máximo. No es una toma continua.
- **Está espejado**: el texto de la tele se lee al revés. Hay que decidir si se da vuelta.
- Volumen −13,3 LUFS, pico +0,1 dBFS.
- Encuadre: Gabriel abajo, tele con diapositivas atrás, pared vacía en el 28 % de arriba. La cara cambia de lugar entre tomas.
- Usa una espumadera como objeto en la mano.
- Las diapositivas ya traen los títulos de cada bloque ("Si tu novio te mandó este video…", "Mándaselo a esa personita").

---

## 9. NUNCA y SIEMPRE (propio de Gabriel)

Sale de `feedback.txt` (WhatsApp, sobre la primera edición del video 31). Cada regla lleva la frase de Gabriel que la origina. Faltan el punto 1 y el final del punto 3.

### NUNCA (dicho por Gabriel)
1. Subtítulos debajo de la cara, casi al fondo de la pantalla. — "no entiendo porque están debajo de mi cara casi al fondo de la pantalla"
2. Subtítulos que se mueven. — "creo que se van moviendo con algo no se porque" / "hay algo rarísimo en el movimiento de los subtítulos"
3. Zoom que deja afuera la diapositiva de la tele. — "el zoom no está malo pero se pierde la imagen"
4. Zoom tan cerrado que solo queda la cara. — "Estás tomas tampoco me convencen" (cuadros con solo ojos o cara)
5. Encuadre que lo corta contra un borde. — "No se ve bien a mi parecer" (él cortado en el borde izquierdo)
6. Entregar una edición que se sienta "floja". — "yo lo veo bastante flojo"

### SIEMPRE (dicho por Gabriel)
7. Si un zoom tapa la diapositiva, agregar una imagen que refuerce lo que dice, puesta debajo de él. — "toca agregar algo para generar más impacto, ejemplo, una imagen de una mujer con una tiara de ángel"
8. Si el zoom no queda bien por la distancia a la que grabó, usar B-roll corto en lugar del zoom, **3 segundos como máximo**. — "mejor miremos apoyar con b-rolls cortos de 3 segundos Max"
9. Proponerle ideas: pidió sugerencias de forma explícita. — "les dejo que me sugieran"

### Lectura mía **[S]**, a confirmar con Agus
- La causa de 3, 4 y 5 es la misma: en el crudo 31 Gabriel está abajo y la tele atrás; cualquier zoom sobre la cara saca la tele del cuadro.
- "Se van moviendo con algo": los subtítulos estaban atados al zoom o al seguimiento de cara. Regla técnica: el subtítulo se dibuja después del zoom, en coordenadas fijas de pantalla.
- La palabra en amarillo dentro del subtítulo ("queso entra", "la necesito") estaba en la edición criticada pero Gabriel no la criticó. En sus 5 referencias no existe. No sé si queda o se va.

Candidatas anteriores **[S]**, a confirmar:
- Subtítulo encima de texto de un artículo de fondo.
- Subtítulo que cambia de altura dentro del mismo video.
- Mezclar formatos (A, B, C) en un mismo video.

## 10. En qué se aparta de la base NXT (a definir con Agus)

- Planos de menos de 1 s en el formato C.
- Pico por encima de −1 dBTP y volumen fuera de −14 LUFS.
- Subtítulo en el centro de la pantalla (0,55), no en la zona baja.
- Cierre sin "Seguir".
