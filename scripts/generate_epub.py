from ebooklib import epub
import yaml
import os
from utils import get_characters

def generar_epub():
    personajes = get_characters()

    # Crear un libro EPUB
    book = epub.EpubBook()

    # Definir metadatos
    book.set_title('Diccionario de Personajes')
    book.set_language('es')

    # Incluir la portada
    # portada = epub.EpubImage()
    # portada.set_file_name('assets/cover.png')
    # portada.set_content(open('assets/cover.png', 'rb').read())
    # book.add_item(portada)

    with open('styles/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    style = epub.EpubItem(uid="style1", file_name="style.css", media_type="text/css", content=css_content)
    book.add_item(style)

    for personaje in personajes:
        item = epub.EpubHtml(title=personaje['nombre'], file_name=f"{personaje['nombre'].lower().replace(' ', '-')}.xhtml", lang='es')
        content = f"""<html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>
                    <h1>{personaje['nombre']}</h1>
                    <p><strong>alias:</strong> <span class="variantes">{', '.join(personaje.get('variantes', []))}</span></p>
                    <p class="descripcion">{personaje['descripcion']}</p>
                    </body></html>"""
        item.set_content(content)
        book.add_item(item)

    book.add_item(epub.EpubNav())

    epub.write_epub('output/diccionario.epub', book)

if __name__ == '__main__':
    generar_epub()
