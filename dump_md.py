import json
import sys
import glob

notebooks = glob.glob('/home/luiz/desktop/UFPA/2026.2/lab_eng_software/Projeto_vale/notebooks/*.ipynb')

data = {}
for nb_path in notebooks:
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        cells = []
        for i, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                cells.append({'index': i, 'source': ''.join(cell.get('source', []))})
        if cells:
            data[nb_path.split('/')[-1]] = cells
    except Exception as e:
        pass

with open('/home/luiz/desktop/UFPA/2026.2/lab_eng_software/Projeto_vale/md_cells.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
