import json
import sys

for nb_path in sys.argv[1:]:
    print(f"\n--- {nb_path} ---")
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        for i, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                print(f"Cell {i}:\n{source}\n")
    except Exception as e:
        print(f"Error reading {nb_path}: {e}")
