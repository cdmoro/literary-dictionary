import os
import yaml
from collections import OrderedDict
from utils import CATEGORY_KEYS

ROOT_FOLDER = "dictionary"  # Reemplazá esto

# Esta clase permite que OrderedDict se represente como un mapeo normal (pero manteniendo el orden)
def represent_ordereddict(dumper, data):
    return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

yaml.add_representer(OrderedDict, represent_ordereddict)

def insert_id_after_headword(entry, entry_id):
    if isinstance(entry, dict) and "headword" in entry:
        new_entry = OrderedDict()
        for key, value in entry.items():
            new_entry[key] = value
            if key == "headword":
                new_entry["id"] = entry_id
        return new_entry
    return entry

def add_ids_to_file(filepath, start_id):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return start_id

    modified = False

    for field in CATEGORY_KEYS:
        if field in data and isinstance(data[field], list):
            new_entries = []
            for entry in data[field]:
                new_entry = insert_id_after_headword(entry, start_id)
                new_entries.append(new_entry)
                start_id += 1
            data[field] = new_entries
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

    return start_id

def main():
    current_id = 1
    for root, _, files in os.walk(ROOT_FOLDER):
        for filename in sorted(files):
            if filename.endswith((".yaml")):
                filepath = os.path.join(root, filename)
                current_id = add_ids_to_file(filepath, current_id)

if __name__ == "__main__":
    main()
