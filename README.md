# Diccionario Literario

Este proyecto es un diccionario literario para libros electrónicos que organiza personajes, conceptos y elementos de distintas sagas y libros famosos.

# Uso

El diccionario está optimizado para ser usado en los dispositivos Kindle (ya que no tengo otro lector). Podés bajar el __archivo MOBI__ desde [acá](https://github.com/cdmoro/diccionario-literario/releases/latest).

Se pueden buscar tanto palabras individuales como grupos de palabras. Y, por supuesto, sirve para libros en cualquier idioma.

|Palabra individual|Grupo de palabras|Libro en otro idioma|
|---|---|---|
|﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿![image](https://github.com/user-attachments/assets/43fe84ab-9879-4b0f-a888-9b71d4f11e88)|![image](https://github.com/user-attachments/assets/826923f0-74ec-4d70-b62f-1fe823747b08)|![image](https://github.com/user-attachments/assets/8491310c-d80a-490f-a90a-2963b9d1badf)|


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
 
El campo `glossary` es más que suficience para agregar registros, pero si queremos ser más específicos podemos usar los siguientes campos:
- `characters`: _(per.)_ - Personajes principales, secundarios, etc.
- `places`: _(lugar)_ - Lugares importantes para la historia.
- `objects`: _(obj.)_ - Objetos especiales que se mencionen en el libro.
- `concepts`: _(concep.)_ - Conceptos particulares.
- `events`: _(evento)_ - Eventos relevantes para la historia.
- `creatures`: _(criatura)_ - Animales reales o mitológicos, tribus, etc.
- `institutions`: _(inst.)_ - Parecido a `places` pero más específico.
- `spells`: _(hechizo)_ - Ideal para las novelas de fantasía.
- `languages`: _(lang.)_ - Por si se menciona algún lenguaje ficticio.
- `quotes`: _(cita)_ - Citas que tienen algún significado especial para la historia.

lo que resultará en la adición de abreviaturas en la definición, dichos campos tienen la misma estructura que `glossary` (`entry`, `alias`, `description`):

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
    python scripts/build.py
    ```
    Esto generará un archivo EPUB y una carpeta llamada `dictionary_files` en la carpeta `output`
1. Abrir el programa Kindle Previewer y cargar el EPUB (o el archivo `Dictionary.opf` dentro de `dictionary_files`)
1. Generar un archivo MOBI
1. Copiar el archivo MOBI generado en el paso anterior a la carpeta dictionary de tu Kindle

Y listo, ya deberías poder usar el diccionario!

# Contacto

Hola, me llamo Carlos y podés encontrarme en:

- [Twitter](https://twitter.com/CarlosBonadeo)
- [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)
