# pip install --upgrade pip
# pip install ruamel.yaml

import os
from ruamel.yaml import YAML

def standardize_yaml_files(repo_path):
    """
    Recursively standardizes all `.yml` files by loading them in round-trip mode
    (preserving structure/comments) and rewriting them with consistent indentation,
    but without forcing line wraps.
    """
    yaml = YAML(typ='rt')  # 'rt' = round-trip
    # Control indentation and line wrapping:
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 9999  # Effectively disable line wrapping
    yaml.preserve_quotes = True

    for root, dirs, files in os.walk(repo_path):
        for file_name in files:
            if file_name.lower().endswith('schema.yml'): # just modifying the documentation
                file_path = os.path.join(root, file_name)

                # Load in round-trip mode (preserves structure & comments):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.load(f)
                except Exception as e:
                    print(f"Skipping {file_path} due to parse error: {e}")
                    continue

                if data is None:
                    data = {}

                # Write it back out to file:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f)

                print(f"Standardized (round-trip): {file_path}")

standardize_yaml_files("/Users/dvaliaiev/PycharmProjects/dbt/")      
