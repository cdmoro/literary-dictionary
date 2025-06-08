from src.constants import uuid_ids, encoding

media_type = {
    "css": "text/css",
    "jpg": "image/jpeg",
    "xhtml": "application/xhtml+xml",
}


def get_opf_file(lang, strings, pages_by_section):
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
    <dc:title>{strings["title"]} ({lang.upper()})</dc:title>
    <dc:language>{lang}</dc:language>
    <dc:creator>Carlos Bonadeo</dc:creator>
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uuid_ids[lang]}</dc:identifier>
    <x-metadata>
      <DictionaryInLanguage>{lang}</DictionaryInLanguage>
      <DictionaryOutLanguage>{lang}</DictionaryOutLanguage>
      <DefaultLookupIndex>headword</DefaultLookupIndex>
    </x-metadata>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>\n"""

    template += (
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
    )

    for file in manifest:
        template += f'    <item id="{file.replace("/", "_")}" href="{file}" media-type="{media_type[file.split(".")[1]]}"/>\n'

    for folder, files in pages_by_section.items():
        for file in files:
            template += f'    <item id="{file}" href="{folder}/{file}.xhtml" media-type="application/xhtml+xml"/>\n'

    template += "  </manifest>\n"
    template += '  <spine toc="ncx">\n'

    for idref in spine:
        template += f'    <itemref idref="{idref.replace("/", "_")}"/>\n'

    for folder, files in pages_by_section.items():
        for file in files:
            template += f'    <itemref idref="{file}"/>\n'

    template += "  </spine>\n"
    template += "  <guide>\n"
    template += '    <reference type="cover" title="Cover" href="Cover.xhtml"/>\n'
    template += (
        '    <reference type="toc" title="Table of Contents" href="TOC.xhtml"/>\n'
    )
    template += '    <reference type="text" title="Start" href="Copyright.xhtml"/>\n'
    template += "  </guide>\n"
    template += "</package>\n"

    return template
