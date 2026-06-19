import json

def separar_notebook(input_file):
    # Carregar o notebook original
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook.get("cells", [])
    split_index = -1

    # Procurar o índice da célula onde começa o treinamento
    for i, cell in enumerate(cells):
        if cell.get("cell_type") == "markdown":
            # Junta o texto da célula
            source_text = "".join(cell.get("source", []))
            if "Dividindo dados entre treino e teste" in source_text:
                split_index = i
                break

    if split_index != -1:
        # Separar as células
        prep_cells = cells[:split_index]
        train_cells = cells[split_index:]
        
        # Estrutura do primeiro notebook (Preparação de Dados)
        notebook_prep = {
            "cells": prep_cells,
            "metadata": notebook.get("metadata", {}),
            "nbformat": notebook.get("nbformat", 4),
            "nbformat_minor": notebook.get("nbformat_minor", 2)
        }
        
        # Estrutura do segundo notebook (Treinamento e Análise)
        notebook_train = {
            "cells": train_cells,
            "metadata": notebook.get("metadata", {}),
            "nbformat": notebook.get("nbformat", 4),
            "nbformat_minor": notebook.get("nbformat_minor", 2)
        }
        
        # Salvar o primeiro notebook
        with open("02_preparacao_de_dados.ipynb", 'w', encoding='utf-8') as f:
            json.dump(notebook_prep, f, indent=1)
            
        # Salvar o segundo notebook
        with open("03_treinamento_e_analise.ipynb", 'w', encoding='utf-8') as f:
            json.dump(notebook_train, f, indent=1)
            
        print("Notebooks divididos com sucesso!")
        print(f"-> '02_preparacao_de_dados.ipynb' salvo com {len(prep_cells)} células.")
        print(f"-> '03_treinamento_e_analise.ipynb' salvo com {len(train_cells)} células.")
    else:
        print("Não foi possível encontrar a célula de corte.")

# Executar a função
separar_notebook("02_data_transforming.ipynb")
