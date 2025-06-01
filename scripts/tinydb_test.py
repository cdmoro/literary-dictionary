from tinydb import TinyDB, Query

db = TinyDB("dictionary/abbreviations.json", indent=2, ensure_ascii=False)
Item = Query()

abbreviations_en = [
    {
        "id": "character",
        "en": {
            "label": "Character",
            "abbreviation": "char.",
            "description": "Main characters, secondary ones, etc.",
        },
    },
    {
        "id": "concept",
        "en": {
            "label": "Concept",
            "abbreviation": "cncpt.",
            "description": "Specific concepts.",
        },
    },
    {
        "id": "creature",
        "en": {
            "label": "Creature",
            "abbreviation": "crt.",
            "description": "Real or mythical creatures, animals, etc.",
        },
    },
    {
        "id": "event",
        "en": {
            "label": "Event",
            "abbreviation": "evt.",
            "description": "Events relevant to the plot.",
        },
    },
    {
        "id": "institution",
        "en": {
            "label": "Institution",
            "abbreviation": "inst.",
            "description": "Institution. Similar to <em>plc.</em> but more specific.",
        },
    },
    {
        "id": "language",
        "en": {
            "label": "Language",
            "abbreviation": "lang.",
            "description": "Artificial or constructed languages.",
        },
    },
    {
        "id": "object",
        "en": {
            "label": "Object",
            "abbreviation": "obj.",
            "description": "Special objects mentioned in the book.",
        },
    },
    {
        "id": "place",
        "en": {
            "label": "Place",
            "abbreviation": "plc.",
            "description": "Places important to the story.",
        },
    },
    {
        "id": "quote",
        "en": {
            "label": "Quote",
            "abbreviation": "qte.",
            "description": "Quotes with special meaning in the story.",
        },
    },
    {
        "id": "spell",
        "en": {
            "label": "Spell",
            "abbreviation": "spl.",
            "description": "Spells, ideal for fantasy novels.",
        },
    },
]

# db.insert_multiple(
#     {
#         "id": item["id"],
#         "en": {
#             "label": item["en"]["label"],
#             "abbreviation": item["en"]["abbreviation"],
#             "description": item["en"]["description"],
#         },
#     }
#     for item in abbreviations_en
# )

abbr = {
    "es": [
        {
            "id": "character",
            "label": "character",
            "abbreviation": "per.",
            "description": "Personajes principales, secundarios, etc.",
        },
        {
            "id": "concept",
            "label": "concept",
            "abbreviation": "con.",
            "description": "Concepto particulares.",
        },
        {
            "id": "creature",
            "label": "creature",
            "abbreviation": "cri.",
            "description": "Criaturas reales o mitológicos, animales, etc.",
        },
        {
            "id": "event",
            "label": "event",
            "abbreviation": "ev.",
            "description": "Eventos relevantes para la historia.",
        },
        {
            "id": "institution",
            "label": "institution",
            "abbreviation": "inst.",
            "description": "Institución. Parecido a <em>lug.</em> pero más específico.",
        },
        {
            "id": "language",
            "label": "language",
            "abbreviation": "leng.",
            "description": "Lengua o idioma artificial.",
        },
        {
            "id": "object",
            "label": "object",
            "abbreviation": "obj.",
            "description": "Objetos especiales que se mencionen en el libro.",
        },
        {
            "id": "place",
            "label": "place",
            "abbreviation": "lug.",
            "description": "Lugares importantes para la historia.",
        },
        {
            "id": "quote",
            "label": "quote",
            "abbreviation": "cit.",
            "description": "Citas que tienen algún significado especial para la historia.",
        },
        {
            "id": "spell",
            "label": "spell",
            "abbreviation": "hech.",
            "description": "Hechizos, ideal para las novelas de fantasía.",
        },
    ],
    "fr": [
        {
            "id": "character",
            "label": "character",
            "abbreviation": "pers.",
            "description": "Personnages principaux, secondaires, etc.",
        },
        {
            "id": "concept",
            "label": "concept",
            "abbreviation": "conc.",
            "description": "Concepts spécifiques.",
        },
        {
            "id": "creature",
            "label": "creature",
            "abbreviation": "créat.",
            "description": "Créatures réelles ou mythiques, animaux, etc.",
        },
        {
            "id": "event",
            "label": "event",
            "abbreviation": "év.",
            "description": "Événements pertinents pour l'intrigue.",
        },
        {
            "id": "institution",
            "label": "institution",
            "abbreviation": "inst.",
            "description": "Institution. Semblable à <em>lieux</em> mais plus spécifique.",
        },
        {
            "id": "language",
            "label": "language",
            "abbreviation": "lang.",
            "description": "Langues artificielles ou construites.",
        },
        {
            "id": "object",
            "label": "object",
            "abbreviation": "obj.",
            "description": "Objets spéciaux mentionnés dans le livre.",
        },
        {
            "id": "place",
            "label": "place",
            "abbreviation": "lieux",
            "description": "Lieux importants dans l'histoire.",
        },
        {
            "id": "quote",
            "label": "quote",
            "abbreviation": "cit.",
            "description": "Citations ayant une signification particulière dans l'histoire.",
        },
        {
            "id": "spell",
            "label": "spell",
            "abbreviation": "sort.",
            "description": "Sortilèges, idéal pour les romans fantastiques.",
        },
    ],
    "it": [
        {
            "id": "character",
            "label": "character",
            "abbreviation": "pers.",
            "description": "Personaggi principali, secondari, ecc.",
        },
        {
            "id": "concept",
            "label": "concept",
            "abbreviation": "conc.",
            "description": "Concetti specifici.",
        },
        {
            "id": "creature",
            "label": "creature",
            "abbreviation": "creat.",
            "description": "Creature reali o mitiche, animali, ecc.",
        },
        {
            "id": "event",
            "label": "event",
            "abbreviation": "ev.",
            "description": "Eventi rilevanti per la trama.",
        },
        {
            "id": "institution",
            "label": "institution",
            "abbreviation": "ist.",
            "description": "Istituzioni. Simili a <em>luog.</em> ma più specifiche.",
        },
        {
            "id": "language",
            "label": "language",
            "abbreviation": "ling.",
            "description": "Lingue artificiali o costruite.",
        },
        {
            "id": "object",
            "label": "object",
            "abbreviation": "ogg.",
            "description": "Oggetti speciali menzionati nel libro.",
        },
        {
            "id": "place",
            "label": "place",
            "abbreviation": "luog.",
            "description": "Luoghi importanti per la storia.",
        },
        {
            "id": "quote",
            "label": "quote",
            "abbreviation": "cit.",
            "description": "Citazioni con significato speciale nella storia.",
        },
        {
            "id": "spell",
            "label": "spell",
            "abbreviation": "inc.",
            "description": "Incantesimi, ideale per romanzi fantasy.",
        },
    ],
    "pt": [
        {
            "id": "character",
            "label": "character",
            "abbreviation": "pers.",
            "description": "Personagens principais, secundários, etc.",
        },
        {
            "id": "concept",
            "label": "concept",
            "abbreviation": "conc.",
            "description": "Conceitos específicos.",
        },
        {
            "id": "creature",
            "label": "creature",
            "abbreviation": "criat.",
            "description": "Criaturas reais ou míticas, animais, etc.",
        },
        {
            "id": "event",
            "label": "event",
            "abbreviation": "evt.",
            "description": "Eventos relevantes para a trama.",
        },
        {
            "id": "institution",
            "label": "institution",
            "abbreviation": "inst.",
            "description": "Instituição. Similar a <em>lug.</em> mas mais específica.",
        },
        {
            "id": "language",
            "label": "language",
            "abbreviation": "idiom.",
            "description": "Línguas artificiais ou construídas.",
        },
        {
            "id": "object",
            "label": "object",
            "abbreviation": "obj.",
            "description": "Objetos especiais mencionados no livro.",
        },
        {
            "id": "place",
            "label": "place",
            "abbreviation": "lug.",
            "description": "Lugares importantes para a história.",
        },
        {
            "id": "quote",
            "label": "quote",
            "abbreviation": "cit.",
            "description": "Citações com significado especial na história.",
        },
        {
            "id": "spell",
            "label": "spell",
            "abbreviation": "fei.",
            "description": "Feitiços, ideal para romances de fantasia.",
        },
    ],
}

# for locale in abbr:
#     for x, item in enumerate(abbr["es"]):
#         db.update(
#             {
#                 locale: {
#                     "label": abbr[locale][x]["label"],
#                     "abbreviation": abbr[locale][x]["abbreviation"],
#                     "description": abbr[locale][x]["description"],
#                 }
#             },
#             Item.id == item["id"],
#         )

# print(db.all())
# character = db.get(Item.id == 'character')
# print(character["es"])

# spanish_strings = {
#     entry["id"]: entry.get("es", "") for entry in db.all()
# }

# print(spanish_strings)

# from tinydb import TinyDB, Query

# # Abrimos la base de datos
# db = TinyDB('dictionary/categories.json')

# Category = Query()

# descriptions = {
#     "character": {
#         "en": "Individuals in the story, such as heroes or villains.",
#         "es": "Individuos de la historia, como héroes o villanos.",
#         "fr": "Individus de l'histoire, tels que des héros ou des méchants.",
#         "it": "Individui della storia, come eroi o cattivi.",
#         "pt": "Indivíduos da história, como heróis ou vilões."
#     },
#     "place": {
#         "en": "Locations or settings where the story takes place.",
#         "es": "Lugares o escenarios donde ocurre la historia.",
#         "fr": "Lieux ou décors où se déroule l'histoire.",
#         "it": "Luoghi o ambientazioni dove si svolge la storia.",
#         "pt": "Locais ou cenários onde a história acontece."
#     },
#     "object": {
#         "en": "Relevant items, tools, or artifacts in the story.",
#         "es": "Objetos, herramientas o artefactos relevantes en la historia.",
#         "fr": "Objets, outils ou artefacts importants dans l'histoire.",
#         "it": "Oggetti, strumenti o manufatti rilevanti nella storia.",
#         "pt": "Objetos, ferramentas ou artefatos relevantes na história."
#     },
#     "concept": {
#         "en": "Abstract or thematic ideas present in the story.",
#         "es": "Ideas abstractas o temáticas presentes en la historia.",
#         "fr": "Idées abstraites ou thématiques présentes dans l'histoire.",
#         "it": "Idee astratte o tematiche presenti nella storia.",
#         "pt": "Ideias abstratas ou temáticas presentes na história."
#     },
#     "event": {
#         "en": "Important happenings or turning points in the plot.",
#         "es": "Acontecimientos importantes o puntos de giro en la trama.",
#         "fr": "Événements importants ou tournants dans l'intrigue.",
#         "it": "Eventi importanti o punti di svolta nella trama.",
#         "pt": "Acontecimentos importantes ou viradas na trama."
#     },
#     "creature": {
#         "en": "Fantasy or real animals and beings.",
#         "es": "Criaturas fantásticas o reales.",
#         "fr": "Créatures fantastiques ou réelles.",
#         "it": "Creature fantastiche o reali.",
#         "pt": "Criaturas fantásticas ou reais."
#     },
#     "institution": {
#         "en": "Organizations, groups, or formal bodies.",
#         "es": "Organizaciones, grupos o entidades formales.",
#         "fr": "Organisations, groupes ou entités officielles.",
#         "it": "Organizzazioni, gruppi o enti formali.",
#         "pt": "Organizações, grupos ou entidades formais."
#     },
#     "spell": {
#         "en": "Magical actions or incantations.",
#         "es": "Hechizos o actos mágicos.",
#         "fr": "Sortilèges ou actions magiques.",
#         "it": "Incantesimi o azioni magiche.",
#         "pt": "Feitiços ou ações mágicas."
#     },
#     "language": {
#         "en": "Spoken or written forms of communication in the story.",
#         "es": "Formas de comunicación habladas o escritas en la historia.",
#         "fr": "Formes de communication parlées ou écrites dans l'histoire.",
#         "it": "Forme di comunicazione parlate o scritte nella storia.",
#         "pt": "Formas de comunicação faladas ou escritas na história."
#     },
#     "quote": {
#         "en": "Memorable or significant excerpts from the story.",
#         "es": "Fragmentos memorables o significativos de la historia.",
#         "fr": "Extraits mémorables ou significatifs de l'histoire.",
#         "it": "Estratti memorabili o significativi della storia.",
#         "pt": "Trechos memoráveis ou significativos da história."
#     }
# }

# Actualiza solo el campo "desc", manteniendo los demás datos del idioma
# for cat_id, langs in descriptions.items():
#     entry = db.get(Category.id == cat_id)
#     if not entry:
#         continue  # Salta si no existe
#     for lang_code, desc_text in langs.items():
#         if lang_code in entry:
#             updated_lang_data = entry[lang_code].copy()
#             updated_lang_data['desc'] = desc_text
#             db.update({lang_code: updated_lang_data}, Category.id == cat_id)
