# 📚 Diccionario Literario para Kindle

Documento disponible en [[English](README.md)]

**Tu compañero de lectura definitivo.**  
¿Perdido entre los nombres de _Cien años de soledad_? ¿No recordás si ese objeto mágico era de Frodo o de Harry? Este **Diccionario Literario** de código abierto te ayuda a seguir personajes, lugares y conceptos de libros y sagas icónicas—directamente desde tu Kindle.

El diccionario está disponible actualmente en inglés y español. Se planean más idiomas para futuras versiones. Cada versión está diseñada cuidadosamente para asegurar una lectura fluida y una navegación simple en Kindle y otros dispositivos de lectura.

🎯 Descargá la última versión del diccionario [acá](https://github.com/cdmoro/literary-dictionary/releases/latest)

## ✨ Características

El **Diccionario Literario para Kindle** está hecho para que tu lectura sea más inmersiva y menos confusa—accesible directamente desde el diccionario integrado del dispositivo.

### ✅ Funcionalidades Clave

- **Funciona con palabras sueltas y expresiones de varias palabras**  
- **Compatible con libros en cualquier idioma**
- **Totalmente integrado con el sistema de diccionarios de Kindle**
- **Referencias cruzadas entre personajes, lugares y conceptos de distintos universos literarios**
- **Muestra múltiples definiciones si un nombre tiene más de una entrada (por ejemplo, apellidos familiares)**
- **Entradas claras y concisas, optimizadas para búsquedas rápidas**
- **Liviano, fácil de instalar y sin distracciones**

### 📸 Capturas de pantalla

| Búsqueda de una sola palabra | Frase de varias palabras | Soporte para otros idiomas |
|------------------------------|---------------------------|-----------------------------|
| ![Single Word Screenshot](./screenshots/single-word.png) | ![Multi-word Screenshot](./screenshots/multi-word.png) | ![Foreign Language Screenshot](./screenshots/foreign-language.png) |

| Entrada con referencias cruzadas | Múltiples definiciones | Guía de abreviaciones |
|----------------------------------|--------------------------|------------------------|
| ![Cross-reference Screenshot](./screenshots/cross-reference.png) | ![Multiple Definitions Screenshot](./screenshots/multiple-definitions.png) | ![Abbreviation Guide Screenshot](./screenshots/abbreviation-guide.png) |

---

## 🛠️ Cómo Contribuir

¿Te apasionan los libros y la tecnología? ¡Sumate al proyecto!

- Proponé libros para agregar  
- Mejorá los scripts en Python  
- Reportá errores o sugerí funciones  
- Compartí tu universo literario favorito  

También podés:
- ☕ [Invitarme un café](https://buymeacoffee.com/cdmoro)  
- 🧉 [Invitarme un cafecito](http://cafecito.app/cdmoro)  
- 🎁 [Apoyar en Patreon](https://patreon.com/cdmoro)  

---

## 🧪 Configuración para Desarrollo

Para generar y probar el diccionario localmente:

```bash
git clone https://github.com/cdmoro/literary-dictionary.git
cd literary-dictionary
pip install -r requirements.txt
python ./main.py
```

Después:

1. Abrí Kindle Previewer
1. Cargá el archivo EPUB generado o dictionary_files/Dictionary.opf
1. Exportalo como MOBI
1. Copialo a la carpeta `dictionaries` de tu Kindle

¡Listo! 🔍📖

## 🙋‍♂️ Sobre mí

Hola, soy Carlos — lector empedernido, programador y hacker de Kindle.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Llevemos la literatura al siguiente nivel, una búsqueda a la vez.
