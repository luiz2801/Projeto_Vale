import json
import glob
import re

notebooks = glob.glob('/home/luiz/desktop/UFPA/2026.2/lab_eng_software/Projeto_vale/notebooks/*.ipynb')

explicit_replacements = {
    "7.7% dos casos críticos gera um dont go?\nO que isso quer dizer, será que essa feature está correta ou eu estou interpretando errado?": "> ❓ **Dúvida Operacional:** Os dados indicam que apenas 7.7% dos casos críticos resultam em um evento *Don't Go*. Esta proporção reflete o comportamento real da frota ou há algum viés/erro de interpretação na extração da métrica?",
    "Removendo colunas consideradas redundantes. \nId telemetria: identificador de linha, não causa impacto no modelo \nNome do operador: como o hash é fornecido há uma redundância\nDia: existe data_evento, redundância": "### 🧹 Remoção de Colunas Redundantes\nPara otimizar o modelo e evitar ruídos, as seguintes colunas foram descartadas:\n- **`Id_Eventos_Telemetria`**: Identificador único de linha (chave primária), sem poder preditivo.\n- **`Nome_Operador_Anon`**: Redundante, pois a identidade já está mapeada de forma segura na coluna de *hash*.\n- **`Dia`**: Informação redundante, já contemplada na variável `Data_Evento`.",
    "Como todas medidass são em Itabira imagino que essa coluna não faz sentido ser mantida dado que, imagino, a correlação com o target seria sem 0": "> 💡 **Nota de Descarte:** A coluna de Localidade indica apenas \"Itabira\" para todos os registros. Por ter variância nula (constante), ela não possui poder discriminatório e sua correlação com a variável alvo será sempre 0. Portanto, foi descartada.",
    "Caminhão e escavadeira são os dois únicos veículos que a telemetria acusa.\nDevo checar se em outros meses há outro tipo de veículo, se não houver devo mudar a coluna para um boleano is_truck?\n": "> 💡 **Nota sobre Veículos:** Atualmente, a base registra apenas \"Caminhão\" e \"Escavadeira\". É necessário validar com outras amostras (meses) se existem novos tipos de equipamentos. Caso seja restrito a esses dois, a variável poderá ser otimizada para um formato booleano (ex: `is_truck`).",
    "Posso agrupar avisos operacionais e não criticos?": "> ❓ **Dúvida de Negócio:** É viável e correto (do ponto de vista operacional) agrupar \"Avisos Operacionais\" e \"Não Críticos\" em uma única categoria de criticidade para simplificar a modelagem?",
    "Dividindo dados entre treino e teste": "### 🛠️ 4.1 Divisão Estocástica (Treino / Teste)\nPartição dos dados mantendo a proporção de classes (estratificação).",
    "Treinamento usando regressão logística": "### 🛠️ 4.2 Treinamento do Modelo (Regressão Logística)\nAjuste do modelo utilizando balanceamento de classes para compensar a raridade dos eventos *Don't Go*."
}

# Explicit replacement for the long bulleted list
list_orig = "- Existem alarmes sem um valor correspondente, essas linhas podem ser descartadas?\n- Features como inicio do turno e fim do turno podem ser agrupados em categorias como manha1, manha2, tarde1, tarde2?\n- Classe tem 97% dos dados faltando, essa feature deve ser descartada?\n- Ids devem ser considerados categóricos?\n- O que eu devo fazer com alarme considerando que existem diversos tipos e é custoso visualizar todas as flags a olho nu?\n- Quais features eu posso remover sem prejuízo?\n- Posso agrupar diferentes tipos de \"Alarme\"? Se freio tem as possibilidades temperatura, pressão e auxiliar eu posso juntar tudo em freio ou devo separar em freio 1 para mais criticos e freios 2 para menos críticos?\n- "
list_new = "- **Valores Ausentes:** Existem alarmes sem um valor correspondente. Essas linhas podem ser descartadas com segurança?\n- **Sazonalidade:** As features de início e fim do turno podem ser agrupadas em categorias temporais (ex: Manhã 1, Manhã 2, Tarde 1, Tarde 2)?\n- **Feature 'Classe':** Possui 97% de dados faltantes. Essa feature deve ser descartada do modelo?\n- **IDs:** Os identificadores (IDs) devem ser tratados estritamente como variáveis categóricas?\n- **Variedade de Alarmes:** Como lidar com a alta dimensionalidade dos tipos de alarmes, considerando que a visualização de todas as flags simultaneamente é impraticável?\n- **Seleção de Features:** Quais atributos podem ser removidos sem causar perda de informação ou impacto preditivo?\n- **Agrupamento Semântico:** É possível agrupar diferentes tipos de \"Alarme\"? (Ex: Se 'Freio' possui as categorias temperatura, pressão e auxiliar, eles podem ser unificados ou devem ser segregados por criticidade?)"

explicit_replacements[list_orig] = list_new

def process_source(source):
    # Apply explicit replacements first
    for orig, new in explicit_replacements.items():
        if source.strip() == orig.strip():
            return new + ("\n" if source.endswith("\n") else "")
        # Also try replacing if it's a substring (for safety)
        if orig in source:
            source = source.replace(orig, new)

    # Apply regex standardizations
    
    # 1. Title formatting
    source = re.sub(r'^#\s+(Pipeline.*)', r'# 📚 \1', source, flags=re.MULTILINE)
    # Prevent double emojis if already processed
    source = re.sub(r'# 📚 📚', r'# 📚', source)
    
    # 2. H2 formatting
    source = re.sub(r'^##\s+(?!\🔍)(?!\d+\.\s)(.*)', r'## \1', source, flags=re.MULTILINE)
    source = re.sub(r'^##\s+(?!\🔍)(\d+\.\s+.*)', r'## 🔍 \1', source, flags=re.MULTILINE)
    source = re.sub(r'## 🔍 🔍', r'## 🔍', source)

    # 3. H3 formatting
    source = re.sub(r'^###\s+(?!\🛠️)(?!\d+\.\d+\.?\s)(.*)', r'### \1', source, flags=re.MULTILINE)
    source = re.sub(r'^###\s+(?!\🛠️)(\d+\.\d+\.?\s+.*)', r'### 🛠️ \1', source, flags=re.MULTILINE)
    source = re.sub(r'### 🛠️ 🛠️', r'### 🛠️', source)
    
    # 4. Notes
    source = re.sub(r'>\s*\*Nota.*:\*', r'> 💡 **Nota:**', source)
    
    return source

for nb_path in notebooks:
    print(f"Processing {nb_path}...")
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        modified = False
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                if isinstance(cell['source'], list):
                    source_str = ''.join(cell['source'])
                    new_source = process_source(source_str)
                    if source_str != new_source:
                        # Split back to lines preserving newlines
                        lines = new_source.splitlines(True)
                        cell['source'] = lines
                        modified = True
                elif isinstance(cell['source'], str):
                    source_str = cell['source']
                    new_source = process_source(source_str)
                    if source_str != new_source:
                        cell['source'] = new_source
                        modified = True
        
        if modified:
            with open(nb_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
                # Ensure ending newline if nbformat requires it
                f.write('\n')
            print(f"  -> Modified and saved.")
        else:
            print(f"  -> No modifications needed.")
    except Exception as e:
        print(f"  -> Error: {e}")

