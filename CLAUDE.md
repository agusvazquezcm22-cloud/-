# NXT Media — reglas para todos los chats de edición

Estas reglas valen para todos los clientes (Gabriel, Unai, Carlos, Jesús, Sofi, Antonio, David, Izan y los que se sumen) y para cualquier chat que edite un video en este repositorio.

## Al terminar cada video (o cada versión que se le envía a Agus)

1. **Guardar el proyecto editable en este repositorio**, en `<cliente>/<número de video>/`:
   - la configuración del video (lista de tomas, tiempos, textos, palabras clave);
   - el motor de render y los scripts que se usaron o se modificaron;
   - una lista de los B-rolls, capturas y sonidos usados, con su origen (carpeta de Drive, URL o script que los baja), para poder recuperarlos.
2. **Commit y push** a la rama de la sesión. Si el push falla, decirlo en el chat con el error; no dar el video por cerrado sin avisar.
3. **No subir a git los videos** (`.mp4`, `.mov`) ni los crudos: van en `.gitignore`. El video final lo sube Agus al Drive del cliente.
4. **Guardar en git los B-rolls y capturas que no se puedan volver a bajar** (los que pesen menos de 20 MB). Los demás se anotan con su origen.

El objetivo: que cualquier chat nuevo pueda aplicar correcciones a un video ya entregado sin rehacer la edición.

## Correcciones de clientes

1. Cada corrección que mande un cliente se anota en `<cliente>/correcciones.md` con la frase textual, la fecha, el video y la regla que sale de ella.
2. Antes de editar un video, leer `<cliente>/correcciones.md` y las notas de estilo del cliente.
3. Antes de entregar, revisar el video contra esas reglas y decir en el chat qué se controló.

## Drive de clientes

- No borrar, mover ni renombrar nada en el Drive de los clientes.
- No subir archivos al Drive de un cliente salvo que Agus lo pida en ese chat.
