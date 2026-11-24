# NXT · Estilo Amy (AmyFit) — guía de edición v0.2

## 0. Lo que pidió Amy (24/11) — manda sobre todo lo demás

Estas indicaciones vienen de Amy y de Agus después de ver la primera versión de la Tanda 2. Donde choquen con las secciones 1 a 6 (que describen las referencias viejas), vale esto.

**Look**

- **Minimalista, limpio, bonito.** Sin colores fuertes y sin letras muy grandes.
- Solo dos colores de texto: **blanco** y el **verde de marca `#BCCD9D`** (RGB 188, 205, 157), tomado de la portada «MI MÉTODO · VIDA FIT».
- El verde va **solo en las palabras clave**.
- Fuera: verde neón, Montserrat Black gigante con glow, tramos en blanco y negro.

**Cómo queda el texto**

- Subtítulo: Montserrat Light 52 px blanco, igual que antes. La palabra clave va en la misma línea, en **Montserrat SemiBold verde**.
- Título (gancho, idea central, llamado a la acción): 2 líneas de **92 px**; la primera en Light blanca, la segunda en SemiBold verde. Sin glow, solo sombra suave. Misma entrada (sube con fundido).
- Pocos títulos: 4 en 30 s alcanza.

**Cortes — esto no puede fallar**

- Cortar solo en silencios medidos (0,25 s o más), dejando unos 0,12 s de aire antes y después de la voz.
- Si Amy arranca una frase y la deja a medias, **se saca entera** y se pasa a la siguiente idea completa. Ejemplo: «ella se llama Ya…» afuera, directo a «Si quieres saber qué fue lo que hizo mi clienta».
- Nunca dos tramos seguidos con el mismo encuadre: se ve como un salto.
- El final no se recorta: la última palabra entra completa y después hay cierre.
- Antes de entregar: transcribir el audio del resultado y comparar con el guion, y medir el nivel en cada unión. Si una unión cae sobre voz, se corrige.

**Cierre**

- Tarjeta «Seguir» de **@amyfitcoach_** (blanca, botón verde de marca, toque que pasa a «Siguiendo»). Está en `kit/amy_seguir.py`.
- **Entra mientras Amy está terminando de hablar**, sobre la última frase, y pasa a «Siguiendo» cuando dice la última palabra. No va después de que termina.
- En videos sin voz entra sobre el último ejercicio, unos 2 s antes del final.
- Va debajo del subtítulo (centro en y = 1330). Sin logo de Instagram.

**Videos de ejercicio sin voz**

- Cortar en las pausas del movimiento, con repeticiones enteras.
- Alternar plano entero y plano cerrado en cada corte.

**Sonido**

- Efectos de la carpeta «sonidos» de NXT, siempre cortos y suaves. La mezcla está en `kit/amy_sonidos.py`.

| Cuándo | Sonido | Pico |
|---|---|---|
| Aparece una palabra clave en verde | Magnetic, Button (10) — clic de 17 ms | −10 dBFS |
| Cada renglón de una lista | Mini list (one shot) — tic de 11 ms | −11 dBFS |
| Entra la tarjeta de una foto | Deep, Mini, Whoosh (11) | −15 dBFS |
| Entra la tarjeta Seguir | Button, Cursor, Select (5) | −11 dBFS |
| Toque del botón Seguir | Magnetic, Button (7) | −10 dBFS |

- Ruido de fondo del gimnasio: reductor de voz (RNNoise, modelo `bd`) al 80 %. Baja el fondo unos 12 dB y la voz casi no cambia. No pasarlo al 100 %: la voz pierde cuerpo.
- Voz final a −14 LUFS.

**Entre clientes**

- Cada cliente de NXT tiene que verse distinto. No reciclar el mismo recurso con todos.

Hecha a partir de las 16 referencias de la carpeta de Drive «AMY - EDICIÓN / Referencias».

Qué tan firme es cada dato:

- **Medido**: sacado cuadro a cuadro de «T2 V8 Amy.mp4» y verificado recreándolo (ver sección 9).
- **Visto**: observado en las otras 15 referencias a 1 cuadro por segundo. Sirve como regla, pero los números finos faltan medir.
- **Sin verificar**: el audio. Medí volumen, pero no puedo escuchar, así que no sé qué música ni qué efectos de sonido usa.

## 1. Tipografía

| Uso | Fuente | Interletra |
|---|---|---|
| Subtítulos, líneas finas de título, notas | **Montserrat Light** | −70 (−0,07 em) |
| Palabra fuerte de título, rótulos | **Montserrat Black** (ExtraBold da casi igual) | −70; hasta −120 en palabras largas para que las letras se toquen |
| Cursiva | Montserrat Light **inclinada por el editor** (cursiva falsa, ~10°), no la Light Italic real | −70 |

- Todo blanco puro. Minúsculas siempre, salvo inicial de frase en los títulos.
- La «Helvetica-Bold.ttf» de la carpeta Tipografia **no aparece** en T2 V8: probé las palabras fuertes contra Helvetica Bold y calza mucho peor que Montserrat Black. Queda por confirmar dónde se usa.
- Montserrat es libre (licencia OFL), se puede usar sin pagar.

## 2. Subtítulos (medido)

- Montserrat Light, **52 px** de cuerpo en 1080×1920, interletra −70.
- Centrados en x = 540. Una sola línea.
- Altura: línea base en **y = 1081** en T2 V8 (sobre el pecho, debajo del mentón). En otras referencias va entre y ≈ 800 y y ≈ 1200: se acomoda por video para no tapar la cara, pero **dentro de un video no se mueve**.
- Sombra negra suave (desenfoque ~5 px, 50 %), sin borde ni caja.
- **Corte seco**: aparecen y desaparecen sin animación.
- Mientras hay un título en pantalla **no hay subtítulo**: el título reemplaza esas palabras.
- Sin signos de puntuación ni mayúsculas.

Hay dos formas de agrupar las palabras:

| Modo | Dónde | Cómo |
|---|---|---|
| **Frase corta** | T2 V8 (medido) | 1 a 4 palabras por bloque, 39 bloques en 33 s, ~0,6 s cada uno. Se corta por sentido: «esa hambre» / «no es ansiedad» / «ni falta» / «de voluntad». |
| **Palabra por palabra** | Tanda 1 y T2 V1, V4, V6, V7 (visto) | 1 palabra por bloque, ~0,3 s. En Tanda 1 algunas claves van en negrita («líquidos», «muscular», «las fotos»). |

Recomendación: usar **frase corta**, que es el modo del video más nuevo y el más fácil de leer. Confirmar con Amy.

## 3. Títulos de las referencias viejas (medido) — reemplazado por la sección 0

Es el recurso principal del estilo: frase de 2 o 3 líneas, **línea fina + palabra fuerte**.

- Líneas finas en Montserrat Light, la palabra clave en Montserrat Black en la última línea.
- Bloque alineado a la **izquierda**, y el bloque entero centrado en pantalla.
- Líneas casi pegadas: la fuerte arranca donde termina la fina, sin aire.
- Tamaños usados en T2 V8 (cuerpo en px):

| Título | Fina | Fuerte |
|---|---|---|
| Reina / no eres / **tú** | 174–178 | 178 |
| son las / **hormonas** | 188 | 160 |
| entonces... / **escucha esto** | 116 | 112 |
| es / **fisiología** | 134 | 132 |
| priorices / **proteína** | 98 | 160 |
| que aporten / mucha mas / **fibra** | 94–96 | 164 |

  Regla práctica: gancho del arranque 160–190 px; títulos del medio 100–135 px; cuando se quiere remarcar, la fuerte va ~1,6 veces más grande que la fina.
- Glow blanco suave alrededor (más notorio en la palabra fuerte) y una sombra oscura muy difusa.
- Ubicación: misma zona que los subtítulos (y ≈ 1000–1400), sobre el pecho.
- Cuándo: en el gancho (dos títulos seguidos en los primeros 2 s) y después uno cada 4–8 s, en la idea clave de cada tramo. T2 V8 tiene 6 en 33 s.
- Duración en pantalla: 0,6 a 1,1 s. Se van en corte seco.

### Animación de entrada (medido)

- El bloque entero **sube ~75 px y aparece con fundido**, frenando al llegar. Tarda ~0,75 s en asentarse, pero a los 0,25 s ya se lee.
  - Desplazamiento en el cuadro `i`: `78 × 0,875^i − 3` px (30 fps).
  - Opacidad: `1 − (1 − i/14)²`, llega al 100 % en el cuadro 14.
- Las líneas **se revelan de a una**, en corte seco, sincronizadas con la voz: primero la fina, y la palabra fuerte aparece justo cuando la dice (entre 0,2 y 0,6 s después). Ya revelada, sigue el movimiento del bloque.

## 4. Notas y rótulos (medido)

- **Nota en cursiva**: Light inclinada, 54 px, con glow. Ejemplos: «¿Te pasa?» arriba del subtítulo durante todo un B-roll (y = 877); «Parte 2: "la báscula te miente"» abajo a la izquierda en el cierre (x = 285, y ≈ 1476 y 1524).
- **Rótulo**: Montserrat Black 124 px con glow fuerte, centrado arriba (línea base y = 374). Ejemplo: «Parte 1», fijo durante todo el cierre.
- Los dos entran en corte seco, junto con un corte de plano.

## 5. Otros recursos de las referencias viejas (visto) — usar solo si Amy los pide

- **Verde neón** para números y datos: «↓5kg», «50%», «90°», «1500kcal», «PLAN B». También líneas y glow verde sobre el cuerpo en tutoriales.
- **Rojo** para lo negativo («PEOR») y zonas marcadas en rojo. **Amarillo** en «rico / dulce».
- **Blanco y negro** en tramos de «antes», problema o cita ajena (T1 V5, T2 V1, T2 V2, T2 V6).
- **Tarjeta gráfica**: gráfico o captura en tarjeta blanca redondeada debajo del subtítulo; entra subiendo con fundido (~0,4 s) y queda 3–4 s (T2 V8).
- **Cita tipeada**: pregunta de seguidora entre comillas que se escribe letra a letra con cursor (T2 V6).
- **Cuentas apiladas**: «1500kcal ×5», «13500kcal ×7 días» en negrita, una debajo de otra (T2 V6).
- **Listas apiladas** a la izquierda que se van sumando: «proteína / fibra / agua / volumen» (T1 V4).
- **Stickers PNG** de comida, **flechas punteadas** blancas y **líneas de ángulo** en tutoriales (T1 V3, T1 V4, T2 V4, T2 V7).
- **Destello naranja** (film burn) como transición (T1 V6).
- **Acercamientos**: cortes entre plano abierto y cerrado del mismo plano fijo, cada 3–6 s.
- **Cierre**: «Sigue a: **AmyFit**» en fina + fuerte (T1 V8), o «Parte 1 / Parte 2» para series.

## 6. Formatos que aparecen en las referencias

| Formato | Referencias |
|---|---|
| Charla a cámara + B-roll (el principal) | T1 V1, V2, V5, V6, V7 · T2 V1, V6, V8 |
| Tutorial o corrección en el gym, con líneas y flechas | T1 V3, V8 · T2 V4, V7 |
| Explicación con pizarra y productos | T1 V4 |
| Vlog con clienta | T2 V2 |
| Montaje de B-roll con texto fijo arriba (sin voz) | T2 V5 |
| Testimonio: fondo beige, título con serifa, video horizontal al centro, pie «VIDA FIT» | T2 V3 |

## 7. Las 16 referencias

| Archivo | Duración | Cortes | Volumen (LUFS) |
|---|---|---|---|
| Video 1 - Amy (T1 V1) | 36 s | 13 | −22,8 |
| Video 2 editado (T1 V2) | 82 s | 23 | −18,1 |
| Video 3 editado (T1 V3) | 44 s | 8 | −14,6 |
| Video 4 editado (T1 V4) | 71 s | 20 | −18,2 |
| video 5 editado (T1 V5) | 77 s | 18 | −14,6 |
| Video 6 editado (T1 V6) | 27 s | 18 | −13,4 |
| video editado 7 (T1 V7) | 72 s | 33 | −16,1 |
| Video 8 editado (T1 V8) | 27 s | 13 | −19,0 |
| T2 video 1 | 37 s | 9 | −12,8 |
| T2 video 2 | 79 s | 16 | −19,0 |
| T2 video 3 | 179 s | 22 | −18,7 |
| T2 V4 | 33 s | 0 | −17,4 |
| T2 V5 | 22 s | 6 | −15,8 |
| T2 V6 | 64 s | 1 | −19,9 |
| T2 V7 | 54 s | 0 | −16,0 |
| T2 V8 | 33 s | 5 | −21,7 |

«Cortes» cuenta solo cambios fuertes de imagen (B-roll, cambio de lugar); los acercamientos sobre el mismo plano no entran. Todas son 1080×1920 a 30 fps.

El volumen va de −12,8 a −22,8 LUFS: no hay un nivel fijo. Para entregar, normalizar a −14 LUFS como en el resto de NXT.

## 8. Pendientes

- Escuchar las referencias: música, efectos de sonido y si hay algún golpe en la entrada de los títulos.
- Confirmar modo de subtítulo (frase corta o palabra por palabra) y si la Tanda 2 reemplaza a la Tanda 1.
- Confirmar dónde va la Helvetica Bold.
- Medir fino los recursos de la sección 5 cuando toque usarlos (verde exacto, tarjeta, cita tipeada).
- Usuario exacto de Instagram para el cierre.

## 9. El kit y la prueba

`kit/amy_render.py` dibuja subtítulos, títulos, notas y rótulos con estas reglas sobre un video 1080×1920.

```
python3 -I kit/amy_render.py kit/recreacion_T2V8.json
```

- `kit/recreacion_T2V8.json` es el proyecto de la prueba: los 39 subtítulos, 7 títulos y 2 notas de T2 V8 con sus cuadros. Sirve de plantilla para un reel nuevo.
- Necesita Python con numpy, opencv-python y Pillow, más ffmpeg.
- El video de referencia no está en el repo: va al lado del JSON como `T2_V8.mp4`.
- `"limpiar_original": true` borra el texto que ya trae la referencia antes de dibujar el nuevo. Es solo para recrear un video ya editado; con tomas en bruto va en `false`.

**Resultado de la prueba (v04):** tomé T2 V8, le borré todo el texto original y lo volví a generar con el kit. Comparado cuadro a cuadro con la referencia, posición, tamaño, interletra y animación coinciden; las diferencias que quedan son de 1–2 px en bordes y en la intensidad del glow.

Límites de la prueba: los cortes, acercamientos, B-roll, color, audio y la tarjeta del gráfico vienen de la referencia, no los rehíce. Lo que quedó probado es la capa de texto. El montaje completo se prueba con tomas en bruto.
