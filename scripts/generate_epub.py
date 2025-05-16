from ebooklib import epub
from utils import get_entries
from collections import defaultdict

def generar_epub():
    personajes = get_entries()

    # Crear un libro EPUB
    book = epub.EpubBook()

    # Definir metadatos
    book.set_title('Diccionario de Personajes')
    book.set_language('es')

    # Incluir la portada
    with open('assets/cover.jpg', 'rb') as f:
        book.set_cover('cover.jpg', f.read())

    # Incluir estilos
    with open('styles/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    style = epub.EpubItem(uid="style1", file_name="style.css", media_type="text/css", content=css_content)
    book.add_item(style)

    # Crear página de copyright
    copyright_page = epub.EpubHtml(title='Créditos', file_name='creditos.xhtml', lang='es')
    copyright_page.set_content("""
    <html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>
    <h1>Diccionario de Personajes</h1>
    <p>© 2025 Carlos Bonadeo. Ningún derecho reservados.</p>
    <p>Este diccionario es una obra de referencia educativa sin fines comerciales.</p>
    </body></html>
    """)
    book.add_item(copyright_page)

    # Agrupar personajes por letra inicial
    grupos_por_letra = defaultdict(list)
    for personaje in personajes:
        letra = personaje['word'][0].upper()
        grupos_por_letra[letra].append(personaje)

    # Ordenar las letras
    letras_ordenadas = sorted(grupos_por_letra.keys())

    grupo_items = []

    for letra in letras_ordenadas:
        grupo = grupos_por_letra[letra]

        html_content = f"""<html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>
                           <h1>{letra}</h1>"""

        for personaje in sorted(grupo, key=lambda x: x['word']):
            html_content += f"""<h2>{personaje['word']}</h2>"""

            if personaje.get('alias'):
                html_content += f"""<p><strong>Alias:</strong> <em>{', '.join(personaje.get('alias', []))}</em></p>"""

            html_content += f"""<p class="descripcion">{personaje['description']}</p>"""

            if personaje.get('book'):
                html_content += f"""<p>{personaje['category']} del libro <em>{personaje['book']}</em> de {personaje['author']}</p>"""
            elif personaje.get('saga'):
                html_content += f"""<p>{personaje['category']} de la saga <em>{personaje['saga']}</em> de {personaje['author']}</p>"""
            else:
                html_content += f"""<p>{personaje['category']} de {personaje['author']}</p>"""

            html_content += "<hr>"

        html_content += "</body></html>"

        item = epub.EpubHtml(title=f"{letra}", file_name=f"letra-{letra}.xhtml", lang='es')
        item.set_content(html_content)
        book.add_item(item)
        grupo_items.append(item)

    # Tabla de contenido (TOC)
    book.toc = [epub.Link(item.file_name, item.title, f"letra-{i+1}") for i, item in enumerate(grupo_items)]

    # Definir el spine (orden de navegación)
    book.spine = ['cover', 'nav', copyright_page] + grupo_items

    # Agregar navegación
    book.add_item(epub.EpubNav())

    # Guardar el archivo
    epub.write_epub('output/diccionario.epub', book)

if __name__ == '__main__':
    generar_epub()
