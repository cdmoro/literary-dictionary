from ebooklib import epub
from collections import defaultdict
import unicodedata
import os
from dotenv import load_dotenv

from utils import get_entries
from copyright import get_copyright_html

epub_filename = f'output/Bonadeo, Carlos - Diccionario Literario (v{os.getenv('DICT_VERSION')}).epub'

def limpiar_letra(letra):
    return unicodedata.normalize('NFKD', letra).encode('ASCII', 'ignore').decode('utf-8').upper()

def generar_epub():
    load_dotenv()
    entries = get_entries()

    # Crear un libro EPUB
    book = epub.EpubBook()

    # Definir metadatos
    book.set_title('Diccionario Literario')
    book.set_language('es')

    # Incluir la portada
    with open('assets/cover.jpg', 'rb') as f:
        book.set_cover('cover.jpg', f.read())

    # Incluir estilos
    with open('styles/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    style = epub.EpubItem(uid="style1", file_name="style.css", media_type="text/css", content=css_content)
    book.add_item(style)

    portada_html = epub.EpubHtml(title='Portada', file_name='portada.xhtml', lang='es')
    portada_html.set_content(f"""
    <html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>
        <div class="portada">
            <img src="cover.jpg" alt="Portada" style="width: 100%; height: auto;"/>
        </div>
    </body></html>
    """)
    book.add_item(portada_html)

    # Crear página de copyright
    copyright_page = epub.EpubHtml(title='Créditos', file_name='creditos.xhtml', lang='es')
    copyright_page.set_content(get_copyright_html(entries))
    book.add_item(copyright_page)

    # Agrupar personajes por letra inicial
    grupos_por_letra = defaultdict(list)
    for personaje in entries:
        letra = limpiar_letra(personaje['headword'][0])
        grupos_por_letra[letra].append(personaje)

    # Ordenar las letras
    letras_ordenadas = sorted(grupos_por_letra.keys())

    grupo_items = []

    for letra in letras_ordenadas:
        grupo = grupos_por_letra[letra]

        html_content = f"""<html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>
                           <h1>{letra}</h1>"""

        for personaje in sorted(grupo, key=lambda x: x['headword']):
            html_content += f"""<dl><dt>{personaje['headword']}</dt><dd>"""

            html_content += f"""<p class="descripcion">{personaje['description']}</p>"""

            if personaje.get('alias'):
                html_content += f"""<p><strong>Alias:</strong> <em>{', '.join(personaje.get('alias', []))}</em></p>"""

            if personaje.get('book'):
                html_content += f"""<p>{personaje['category']} aparecido en <em>{personaje['book']}</em> ({personaje['author']})</p>"""
            elif personaje.get('saga'):
                html_content += f"""<p>{personaje['category']} de la saga <em>{personaje['saga']}</em> ({personaje['author']})</p>"""
            else:
                html_content += f"""<p>{personaje['category']} creado por {personaje['author']}</p>"""

            html_content += "</dd><hr></dl>"

        html_content += "</body></html>"

        item = epub.EpubHtml(title=f"{limpiar_letra(letra)}", file_name=f"letra-{limpiar_letra(letra)}.xhtml", lang='es')
        item.set_content(html_content)
        book.add_item(item)
        grupo_items.append(item)

    # Tabla de contenido (TOC)
    book.toc = [epub.Link(item.file_name, item.title, f"letra-{i+1}") for i, item in enumerate(grupo_items)]

    # Definir el spine (orden de navegación)
    book.spine = ['cover', portada_html, copyright_page] + grupo_items + ['nav']

    # Agregar navegación
    book.add_item(epub.EpubNav())

    # Guardar el archivo
    epub.write_epub('output/diccionario.epub', book)

if __name__ == '__main__':
    generar_epub()
