import os
import yaml
from collections import OrderedDict
from utils import CATEGORIES

ROOT_FOLDER = "dictionary"

# YAML ordenado
def represent_ordereddict(dumper, data):
    return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

yaml.add_representer(OrderedDict, represent_ordereddict)

def find_max_id():
    max_id = 0
    for root, _, files in os.walk(ROOT_FOLDER):
        for filename in files:
            if filename.endswith((".yaml")):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if not data:
                        continue
                except Exception:
                    continue

                for field in CATEGORIES:
                    if field in data:
                        for entry in data[field]:
                            if isinstance(entry, dict) and "id" in entry:
                                max_id = max(max_id, entry["id"])
    return max_id

def insert_id_after_headword(entry, new_id):
    if isinstance(entry, dict) and "headword" in entry and "id" not in entry:
        new_entry = OrderedDict()
        for key, value in entry.items():
            new_entry[key] = value
            if key == "headword":
                new_entry["id"] = new_id
        return new_entry
    return entry

def assign_ids_to_new_entries(filepath, start_id):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return start_id

    modified = False
    assigned = []

    for field in CATEGORIES:
        if field in data and isinstance(data[field], list):
            new_entries = []
            for entry in data[field]:
                if isinstance(entry, dict) and "headword" in entry and "id" not in entry:
                    assigned.append((field, entry["headword"], start_id))
                    entry = insert_id_after_headword(entry, start_id)
                    start_id += 1
                    modified = True
                new_entries.append(entry)
            data[field] = new_entries

    if modified:
        print(f"📝 Modificado: {filepath}")
        for field, headword, assigned_id in assigned:
            print(f"  → {field}: '{headword}' => id: {assigned_id}")
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

    return start_id

def main():
    current_id = find_max_id() + 1
    print(f"🔍 ID inicial: {current_id}")
    for root, _, files in os.walk(ROOT_FOLDER):
        for filename in sorted(files):
            if filename.endswith((".yaml")):
                filepath = os.path.join(root, filename)
                current_id = assign_ids_to_new_entries(filepath, current_id)

if __name__ == "__main__":
    main()
