from src.constants import uuid_ids, encoding
from src.config import ARGS

media_type = {
    "css": "text/css",
    "jpg": "image/jpeg",
    "png": "image/png",
    "xhtml": "application/xhtml+xml",
}


def get_opf_file(lang, strings, dictionary, appendixes):
    manifest = [
        "Styles/style.css",
        "Assets/cover.jpg",
        "Cover.xhtml",
        "Copyright.xhtml",
        "TOC.xhtml",
        "Abbreviations.xhtml",
    ]
    spine = [v for v in manifest if v.endswith(".xhtml")]

    template = f"""<?xml version="1.0" encoding="{encoding}"?>
        
<package
  version="2.0"
  xmlns="http://www.idpf.org/2007/opf"
  unique-identifier="BookId"
>
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>{strings["title"]} ({strings["edition"]})</dc:title>
    <dc:creator opf:role="aut">Carlos Bonadeo</dc:creator>
    <dc:language>{lang}</dc:language>
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uuid_ids[lang]}</dc:identifier>
    <meta name="cover" content="Assets_cover.jpg"/>"""

    if not ARGS.epub:
        template += f"""\n    <x-metadata>
      <DictionaryInLanguage>{lang}</DictionaryInLanguage>
      <DictionaryOutLanguage>{lang}</DictionaryOutLanguage>
      <DefaultLookupIndex>default</DefaultLookupIndex>
    </x-metadata>\n"""

    template += """  </metadata>
  <manifest>\n"""

    template += (
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'
    )

    for file in manifest:
        template += f'    <item id="{file.replace("/", "_")}" href="{file}" media-type="{media_type[file.split(".")[1]]}"/>\n'

    for file in dictionary:
        template += f'    <item id="{file}" href="Dictionary/{file}.xhtml" media-type="application/xhtml+xml"/>\n'

    for folder, files in appendixes.items():
        for file in files:
            template += f'    <item id="{file}" href="{folder}/{file}.xhtml" media-type="application/xhtml+xml"/>\n'

    template += "  </manifest>\n"
    template += '  <spine toc="ncx">\n'

    for idref in spine:
        template += f'    <itemref idref="{idref.replace("/", "_")}"/>\n'

    for file in dictionary:
        template += f'    <itemref idref="{file}"/>\n'

    for folder, files in appendixes.items():
        for file in files:
            template += f'    <itemref idref="{file}"/>\n'

    template += "  </spine>\n"
    template += "  <guide>\n"
    template += (
        f'    <reference type="cover" title="{strings["cover"]}" href="Cover.xhtml"/>\n'
    )
    template += (
        f'    <reference type="toc" title="{strings["contents"]}" href="TOC.xhtml"/>\n'
    )
    template += f'    <reference type="text" title="{strings["about"]}" href="Copyright.xhtml"/>\n'
    template += "  </guide>\n"
    template += "</package>\n"

    return template
