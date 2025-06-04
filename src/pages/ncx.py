import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_ncx_page(lang, pages_by_section, strings):
    ET.register_namespace('', "http://www.daisy.org/z3986/2005/ncx/")
    ncx = ET.Element("ncx", {
        "xmlns": "http://www.daisy.org/z3986/2005/ncx/",
        "version": "2005-1"
    })
    
    head = ET.SubElement(ncx, "head")
    ET.SubElement(head, "meta", {"name": "dtb:uid", "content": f"literary-diectionary-{lang}"})
    ET.SubElement(head, "meta", {"name": "dtb:depth", "content": "2"})
    # ET.SubElement(head, "meta", {"name": "dtb:totalPageCount", "content": "0"})
    # ET.SubElement(head, "meta", {"name": "dtb:maxPageNumber", "content": "0"})
    
    docTitle = ET.SubElement(ncx, "docTitle")
    ET.SubElement(docTitle, "text").text = strings["title"]

    navMap = ET.SubElement(ncx, "navMap")
    play_order = 1

    pages = [
        ("about", strings["about"], "Copyright.xhtml"),
        ("toc", strings["contents"], "Contents.xhtml"),
        ("abbr", strings["abbr_guide"], "Abbreviations.xhtml")
    ]

    for pid, label, src in pages:
        nav_point = ET.SubElement(navMap, "navPoint", id=pid, playOrder=str(play_order))
        ET.SubElement(nav_point, "navLabel").append(ET.Element("text", text=label))
        ET.SubElement(nav_point, "content", src=src)
        play_order += 1

    for section, files in pages_by_section.items():
        section_point = ET.SubElement(navMap, "navPoint", id=section[0].upper(), playOrder=str(play_order))
        ET.SubElement(section_point, "navLabel").append(ET.Element("text", text=section))
        ET.SubElement(section_point, "content", src=f"{section}.xhtml")
        play_order += 1

        for file in files:
            prefix = section[0].upper()
            entry_id = f"{file}"
            nav_point = ET.SubElement(section_point, "navPoint", id=entry_id, playOrder=str(play_order))
            ET.SubElement(nav_point, "navLabel").append(ET.Element("text", text=file.split('_')[1]))
            ET.SubElement(nav_point, "content", src=f"{section}/{file}.xhtml")
            play_order += 1

    xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n'
    doctype = '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'

    return xml_declaration + doctype + minidom.parseString(ET.tostring(ncx, encoding="unicode")).toprettyxml(indent="  ")