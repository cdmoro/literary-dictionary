# Diccionario Literario

Este proyecto es un diccionario literario para libros electrónicos que organiza personajes, conceptos y elementos de distintas sagas y libros famosos.

# Uso

El diccionario está optimizado para ser usado en los dispositivos Kindle (ya que no tengo otro lector). Podés bajar el __archivo MOBI__ desde [acá](https://github.com/cdmoro/diccionario-literario/releases/latest).

Se pueden buscar tanto palabras individuales como grupos de palabras. Y, por supuesto, sirve para libros en cualquier idioma.

|Palabra individual|Grupo de palabras|Libro en otro idioma|
|---|---|---|
|![image](https://github.com/user-attachments/assets/6793015d-ac4f-4679-ac9d-4b16ded026cc)|![image](https://github.com/user-attachments/assets/2512ae4f-89b6-4065-a06d-0ce7738cd0f7)|![image](https://github.com/user-attachments/assets/26d1416c-046d-4ffb-bed4-17013c94760d)|


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
- `glossary`: Lista de términos, lugares, frases, etc. sin categorizar.
    - `entry`: Palabra principal. 
    - `alias` (opcional): Lista de variantes del término.
    - `description`: Descripción del término.
 
El campo `glossary` es más que suficience para agregar registros, pero si queremos ser más específicos podemos usar los siguientes campos, lo que resultará en la adición de abreviaturas en la definición, dichos campos tienen la misma estructura que `glossary` ():

- `characters`: _(per.)_ - Personajes principales, secundarios, etc.
- `places`: _(lugar)_ - Lugares importantes para la historia.
- `objects`: _(obj.)_ - Objetos especiales que se mencionen en el libro
- `concepts`: _(concep.)_ - Conceptos particulares
- `events`: _(evento)_ - Eventos relevantes para la historia
- `creatures`: _(criatura)_ - Animales reales o mitológicos, tribus, etc.
- `institutions`: _(inst.)_ - Parecido a `places` pero más específico
- `spells`: _(hechizo)_ - Ideal para las novelas de fantasía
- `languages`: _(lang.)_ - Por si se menciona algún lenguaje ficticio
- `quotes`: _(cita)_ - Citas que tienen algún significado especial para la historia

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
