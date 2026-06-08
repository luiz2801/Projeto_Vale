# Projeto_Vale
# Desafio de Telemetria - Vale

## Estrutura do Repositório
- `data/raw/`: Contém os arquivos `.parquet` (base de dados principal).
- `docs/`: Manuais, orientações do desafio e dicionários de dados.
- `notebooks/`: Análise exploratória e desenvolvimento do modelo.
- `scripts/`: Utilitários para conversão de formatos.
- `src/`: Código fonte da aplicação e pipeline.

## Como iniciar
Os dados de telemetria estão em formato Parquet para otimização de espaço. Caso precise dos arquivos CSV originais:
1. Acesse a pasta `scripts/`.
2. Compile o conversor: `g++ -std=c++20 convert.cpp -o convert -larrow -lparquet`.
3. Execute o binário com o seguinte comando `./convert ../data/raw/telemetry_jan.parquet ../data/`.

O notebook em `notebooks/` está configurado para ler os dados diretamente via `pandas.read_parquet('../data/raw/arquivo.parquet')`.