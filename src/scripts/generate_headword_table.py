import csv
import os
import sys
from collections import defaultdict

import yaml

# Root path where dictionary folders are stored
ROOT_DIR = "dictionary"

# Data structure: id -> { lang: headword }
entries = defaultdict(dict)

# Traverse each language folder
for lang in os.listdir(ROOT_DIR):
    lang_path = os.path.join(ROOT_DIR, lang)
    if not os.path.isdir(lang_path):
        continue

    # Traverse each author's folder within the language
    for author in os.listdir(lang_path):
        author_path = os.path.join(lang_path, author)
        if not os.path.isdir(author_path):
            continue

        # Traverse each YAML file
        for filename in os.listdir(author_path):
            if not filename.endswith(".yaml"):
                continue

            file_path = os.path.join(author_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            # Collect entries with 'id' and 'headword'
            for section in data:
                if isinstance(data[section], list):
                    for item in data[section]:
                        if (
                            isinstance(item, dict)
                            and "id" in item
                            and "headword" in item
                        ):
                            entries[item["id"]][lang] = item["headword"]

# If an ID is passed as argument, show only that entry
if len(sys.argv) > 1:
    query_id = int(sys.argv[1])
    if query_id in entries:
        print(f"Headword variants for ID {query_id}:")
        for lang, word in entries[query_id].items():
            print(f"  {lang}: {word}")
    else:
        print(f"No entry found for ID {query_id}.")
    sys.exit(0)

# Collect all languages used
all_languages = sorted({lang for lang_dict in entries.values()
                       for lang in lang_dict})

# Generate CSV file
with open("output/headwords.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id"] + all_languages)

    for id_ in sorted(entries.keys()):
        row = [id_] + [entries[id_].get(lang, "") for lang in all_languages]
        writer.writerow(row)

print("CSV file 'headwords.csv' generated successfully.")
