import json

with open('notebooks/04_LSTM.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        
        # Substituição para carregar os dados temporais (Cell 6 do original)
        if "df = pd.read_csv('dados_lstm.csv')" in source:
            new_load = """# Defina o mês que deseja trabalhar (ex: 'jan', 'feb', 'marco')
months = ["jan", "feb", "marco", "apr", "may", "jun"]
mes = 4
mes_escolhido = months[mes] 
arquivo_mes = f"{mes_escolhido}_dados_lstm.csv"

df = pd.read_csv(arquivo_mes)"""
            source = source.replace("df = pd.read_csv('dados_lstm.csv')", new_load)
            
        # Modificação para salvar os tensores (Cell 10)
        if "np.save('X_train.npy', X_train)" in source:
            new_save = """import os
os.makedirs('../resultados', exist_ok=True)

np.save(f'../resultados/{mes_escolhido}_X_train.npy', X_train)
np.save(f'../resultados/{mes_escolhido}_y_train.npy', y_train)
np.save(f'../resultados/{mes_escolhido}_X_test.npy', X_test)
np.save(f'../resultados/{mes_escolhido}_y_test.npy', y_test)
print(f"Tensores isolados e salvos com sucesso em ../resultados/ com o prefixo {mes_escolhido}_ !")"""
            # Substituir as linhas originais pelas novas
            source = source.replace("np.save('X_train.npy', X_train)", new_save)
            source = source.replace("np.save('y_train.npy', y_train)\n", "")
            source = source.replace("np.save('X_test.npy', X_test)\n", "")
            source = source.replace("np.save('y_test.npy', y_test)\n", "")
            source = source.replace("print(\"Tensores isolados e salvos com sucesso!\")", "")
            
        # Modificação para salvar a matriz de confusão antes do plt.show()
        if "plt.title(f'Matriz de Confusão" in source and "plt.show()" in source:
            if "plt.savefig" not in source:
                new_savefig = """import os
os.makedirs('../resultados', exist_ok=True)
plt.savefig(f'../resultados/{mes_escolhido}_matriz_confusao.png', bbox_inches='tight', dpi=300)
plt.savefig(f'../resultados/{mes_escolhido}_matriz_confusao.svg', bbox_inches='tight')
plt.show()"""
                source = source.replace("plt.show()", new_savefig)
                
        if isinstance(cell.get('source'), list):
            cell['source'] = [line + '\n' for line in source.split('\n')]
            if cell['source']:
                cell['source'][-1] = cell['source'][-1].rstrip('\n')
        else:
            cell['source'] = source

with open('notebooks/04_LSTM.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
