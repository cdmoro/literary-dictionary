import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.constants import uuid_ids, encoding
import re


def get_ncx_page(lang, dictionary, appendixes, strings):
    ET.register_namespace("", "http://www.daisy.org/z3986/2005/ncx/")
    ncx = ET.Element(
        "ncx", {"xmlns": "http://www.daisy.org/z3986/2005/ncx/", "version": "2005-1"}
    )

    head = ET.SubElement(ncx, "head")
    ET.SubElement(
        head,
        "meta",
        {"name": "dtb:uid", "content": f"urn:uuid:{uuid_ids[lang]}"},
    )
    ET.SubElement(head, "meta", {"name": "dtb:depth", "content": "2"})
    ET.SubElement(head, "meta", {"name": "dtb:totalPageCount", "content": "0"})
    ET.SubElement(head, "meta", {"name": "dtb:maxPageNumber", "content": "0"})

    docTitle = ET.SubElement(ncx, "docTitle")
    ET.SubElement(docTitle, "text").text = strings["title"]

    navMap = ET.SubElement(ncx, "navMap")
    play_order = 1

    pages = [
        ("cover", strings["cover"], "Cover.xhtml"),
        ("about", strings["about"], "Copyright.xhtml"),
        ("toc", strings["contents"], "TOC.xhtml"),
        ("abbr", strings["abbr_guide"], "Abbreviations.xhtml"),
    ]

    for pid, label, src in pages:
        nav_point = ET.SubElement(navMap, "navPoint", id=pid, playOrder=str(play_order))
        textEl = ET.Element("text")
        textEl.text = label
        ET.SubElement(nav_point, "navLabel").append(textEl)
        ET.SubElement(nav_point, "content", src=src)
        play_order += 1

    dictionary_point = ET.SubElement(
        navMap, "navPoint", id="D", playOrder=str(play_order)
    )
    dictionaryEl = ET.Element("text")
    dictionaryEl.text = strings["dictionary"]
    ET.SubElement(dictionary_point, "navLabel").append(dictionaryEl)
    ET.SubElement(dictionary_point, "content", src="Dictionary/Dictionary.xhtml")
    play_order += 1

    for file in dictionary:
        if file == "Dictionary":
            continue

        nav_point = ET.SubElement(
            dictionary_point, "navPoint", id=file, playOrder=str(play_order)
        )
        textEl = ET.Element("text")
        textEl.text = (
            file.split("_")[1]
            if re.fullmatch(r"[A-Z]_[A-Z]", file)
            else strings[f"ncx_{file.lower()}"]
        )
        ET.SubElement(nav_point, "navLabel").append(textEl)
        ET.SubElement(nav_point, "content", src=f"Dictionary/{file}.xhtml")
        play_order += 1

    for section, files in appendixes.items():
        if len(files) == 0:
            continue

        section_point = ET.SubElement(
            navMap, "navPoint", id=section[0].upper(), playOrder=str(play_order)
        )
        textEl = ET.Element("text")
        textEl.text = strings["appendix"] + ": " + strings[section.lower()]
        ET.SubElement(section_point, "navLabel").append(textEl)
        ET.SubElement(section_point, "content", src=f"{section}/{section}.xhtml")
        play_order += 1

    xml_declaration = f'<?xml version="1.0" encoding="{encoding}"?>\n'
    doctype = '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'

    output = minidom.parseString(ET.tostring(ncx, encoding="unicode")).toprettyxml(
        indent="  "
    )
    output = "\n".join(
        line for line in output.split("\n") if not line.strip().startswith("<?xml")
    )

    return xml_declaration + doctype + output
