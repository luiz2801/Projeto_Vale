import json

with open('notebooks/04_LSTM.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        
        # Inject seed in cell 2 if it's the import cell
        if "import pandas as pd" in source and "import tensorflow as tf" in source:
            if "SEED = 42" not in source:
                new_source = source + """\n\nimport random
import os
# --- CONFIGURANDO SEED PARA REPRODUTIBILIDADE ---
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)
print(f"Seed fixada em {SEED} para garantir a reprodutibilidade.")"""
                source = new_source
                
        if isinstance(cell.get('source'), list):
            cell['source'] = [line + '\n' for line in source.split('\n')]
            if cell['source']:
                cell['source'][-1] = cell['source'][-1].rstrip('\n')
        else:
            cell['source'] = source

with open('notebooks/04_LSTM.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
