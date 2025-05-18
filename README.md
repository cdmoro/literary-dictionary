# Diccionario Literario

Este proyecto es un diccionario literario para libros electrónicos que organiza personajes, conceptos y elementos de distintas sagas y libros famosos.

# Uso

El diccionario está optimizado para ser usado en los dispositivos Kindle (ya que no tengo otro lector). Podés bajar el __archivo MOBI__ desde [acá](https://github.com/cdmoro/literature-clock/releases/latest).

# Historia

Después de leer _Cien años de soledad_ y ya no saber qué personaje hizo tal o cuál cosa, me puse en la tarea de hacer un diccionario que contenga personajes y términos de la literatura universal para que no me vuelva a pasar.

Y qué mejor para esto que aprovechar el sistema de diccionarios del Kindle, donde se puede buscar por palabras (sí, más de una) y te muestra la definición en una forma muy cómoda para el lector.

# Diccionario

Dentro de la carpeta `dictionary` se encuentran las entradas para el diccionario separadas por autor, en archivos YAML. Cada archivo puede corresponderse con un libro, con una saga o simplemente puede contener registros que forman parte del universo del autor, sin estar necesariamente conectadas con un libro o saga en particular.

## Formato

Cada archivo YAML contiene:
- `author`: Nombre del autor.
- `book` (opcional): Nombre del libro.
- `saga` (opcional): Nombre de la saga.
- `characters`: Lista de personajes.
    - `alias` (opcional): Lista de variantes del nombre.
    - `description`: Descripción del personaje
- `glossary`: Lista de términos, lugares, frases.
    - `alias` (opcional): Lista de variantes del término.
    - `description`: Descripción del término.

# Cómo contribuir

Cualquier tipo de contribución será más que bienvenida. Se puede hacer a través de varias formas. Desde contribuciones al código fuente, cargar sugerencias o issues, hasta contribuciones monetarias.

- Agregar nuevos personajes siguiendo la estructura `YALM` mencionada.
- Mejorar scripts para procesamiento y generación de datos.
- Reportar issues o sugerencias en el repositorio.
- Enviarme un mail o contactarme por las redes sociales.
- Comprarme un [coffee](https://buymeacoffee.com/cdmoro) o un [cafecito](http://cafecito.app/cdmoro)
- Contribuir en la plataforma [Patreon](https://patreon.com/cdmoro)

## Desarrollo

Si querés colaborar estos son los pasos para poder compilar el proyecto y subir tu archivo al Kindle.

1. Clonar el repositorio
1. Instalar dependencias:
    ```
    pip install -r requirements.txt
    ```
1. Compilar proyecto
    ```
    python build.py
    ```
    Esto generará tres archivos:
    - EPUB
    - CSV
    - JSON
1. Compilar el EPUB usando KindleGen o Kindle Previewer
1. Copiar el archivo MOBI generado en el paso anterior a la carpeta dictionary de tu Kindle

Y listo, ya deberías poder usar el diccionario en tu lector electrónico!

# Contacto

Hola, me llamo Carlos y podés encontrarme en:

- [Twitter](https://twitter.com/CarlosBonadeo)
- [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)