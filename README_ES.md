# 📚 Diccionario Literario para Kindle

**Tu compañero de lectura definitivo.**  
¿Perdiste la cuenta de los nombres en _Cien años de soledad_? ¿No recordás si ese objeto mágico era de Frodo o de Harry? Este **Diccionario Literario** de código abierto te ayuda a seguirle el ritmo a personajes, lugares y conceptos de libros y sagas famosas, directamente desde tu Kindle.

El diccionario está disponible actualmente en **español**. La versión en **inglés** está en desarrollo y se publicará pronto. Se planea ofrecer versiones separadas para cada idioma, para facilitar la lectura y navegación en los dispositivos Kindle.


## 🚀 ¿Qué es?

Un diccionario literario optimizado para Kindle, pensado para mejorar tu experiencia de lectura. Solo tenés que descargarlo, instalarlo y empezar a buscar nombres o frases desconocidas sin salir de la página.

- Funciona con **palabras individuales** y **expresiones compuestas**
- Compatible con libros en **cualquier idioma**
- Totalmente integrado al **sistema de diccionarios del Kindle**

|Palabra individual|Expresión compuesta|Libro en otro idioma|
|---|---|---|
|﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿![image](https://github.com/user-attachments/assets/43fe84ab-9879-4b0f-a888-9b71d4f11e88)|![image](https://github.com/user-attachments/assets/826923f0-74ec-4d70-b62f-1fe823747b08)|![image](https://github.com/user-attachments/assets/8491310c-d80a-490f-a90a-2963b9d1badf)|

🎯 [Descargar el archivo MOBI más reciente desde acá](https://github.com/cdmoro/diccionario-literario/releases/latest)

---

## ✍️ Cómo funciona

Las entradas están organizadas en archivos YAML por autor. Cada archivo puede cubrir un libro, una saga completa o el universo general del autor.

### ✅ Estructura de cada entrada

Cada entrada incluye:
- `entry`: Término principal
- `alias` (opcional): Nombres alternativos
- `description`: Breve explicación

Además, podés categorizar las entradas usando:
- `characters`, `places`, `objects`, `concepts`, `events`, `creatures`, `institutions`, `spells`, `languages`, `quotes`

Desde lenguas élficas hasta frases memorables.  
Todo se encuentra en `dictionary/*.yaml`.

---

## 🛠️ Cómo contribuir

¿Te gustan los libros y la tecnología? ¡Sumate!

- Agregá nuevas entradas (formato YAML)
- Mejorá los scripts en Python
- Reportá errores o sugerí mejoras
- Compartí tus universos literarios favoritos

También podés:
- ☕ [Invitarme un café](https://buymeacoffee.com/cdmoro)
- 🧉 [Convidarme un cafecito](http://cafecito.app/cdmoro)
- 🎁 [Colaborar en Patreon](https://patreon.com/cdmoro)

---

## 🧪 Entorno de desarrollo

Para compilar y testear el diccionario localmente:

```bash
git clone https://github.com/cdmoro/diccionario-literario.git
cd diccionario-literario
pip install -r requirements.txt
python scripts/build.py
```

Después:

1. Abrí Kindle Previewer
1. Cargá el archivo EPUB generado o dictionary_files/Dictionary.opf
1. Exportalo como MOBI
1. Copialo a la carpeta dictionaries/ de tu Kindle

¡Listo! 🔍📖

## 🙋‍♂️ Sobre mí

Hola, soy Carlos — lector empedernido, programador y hacker de Kindle.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Llevemos la literatura al siguiente nivel, una búsqueda a la vez.
