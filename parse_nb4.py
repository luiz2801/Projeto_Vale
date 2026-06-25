import json

with open('notebooks/04_LSTM.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('nb4_code.txt', 'w', encoding='utf-8') as out:
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            out.write(f"--- Cell {i} ---\n")
            out.write("".join(cell.get('source', [])))
            out.write("\n\n")
