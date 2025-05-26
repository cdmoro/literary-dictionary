# 📚 Diccionario Literario para Kindle

**Tu compañero de lectura definitivo.**  
¿Perdiste la cuenta de los nombres en _Cien años de soledad_? ¿No recordás si ese objeto mágico era de Frodo o de Harry? Este **Diccionario Literario** de código abierto te ayuda a seguirle el ritmo a personajes, lugares y conceptos de libros y sagas famosas, directamente desde tu Kindle.

El diccionario está disponible actualmente en inglés y en español. Se planean más idiomas para futuras ediciones. Cada versión se diseña de forma independiente para garantizar una lectura fluida y una navegación óptima en Kindle y otros dispositivos de lectura electrónica.

🎯 Descarga la última versión del diccionario [acá](https://github.com/cdmoro/literary-dictionary/releases/latest)


## ✨ Funcionalidades

El **Diccionario Literario para Kindle** está diseñado para hacer tu lectura más inmersiva y menos confusa, directamente desde el diccionario integrado del dispositivo.

### ✅ Características principales

- **Funciona con palabras sueltas y expresiones compuestas**
- **Compatible con libros en cualquier idioma**
- **Totalmente integrado con el sistema de diccionario de Kindle**
- **Incluye referencias cruzadas entre personajes, lugares y conceptos de distintos universos literarios**
- **Muestra múltiples definiciones cuando un nombre coincide con varias entradas (por ejemplo, apellidos familiares)**
- **Entradas claras y concisas, optimizadas para búsquedas rápidas**
- **Ligero, fácil de instalar y sin distracciones**

### 📸 Capturas de pantalla

| Búsqueda de palabra | Expresión compuesta | Soporte multilingüe |
|---------------------|---------------------|----------------------|
| ![Búsqueda palabra](./screenshots/single-word.png) | ![Expresión compuesta](./screenshots/multi-word.png) | ![Multilingüe](./screenshots/foreign-language.png) |

| Referencia cruzada | Múltiples definiciones | Guía de abreviaciones |
|--------------------|------------------------|------------------------|
| ![Referencia cruzada](./screenshots/cross-reference.png) | ![Múltiples definiciones](./screenshots/multiple-definitions.png) | ![Guía de abreviaciones](./screenshots/abbreviation-guide.png) |

---

## ✍️ Cómo funciona

Las entradas están organizadas en archivos YAML por autor. Cada archivo puede cubrir un libro, una saga completa o el universo general del autor.

### ✅ Estructura de cada entrada

Cada entrada incluye:
- `entry`: Término principal
- `displayValue` (opcional): Reemplaza visualmente a `entry`
- `alias` (opcional): Nombres alternativos
- `description`: Definición del término

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
