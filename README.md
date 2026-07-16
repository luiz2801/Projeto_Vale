# 🏗️ Projeto Vale — Desafio de Telemetria e Manutenção Preditiva

> Sistema de detecção de anomalias em dados de telemetria de equipamentos pesados da Vale, desenvolvido como projeto acadêmico na disciplina de **Laboratório de Engenharia de Software** — UFPA 2026.2.

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura da Solução](#arquitetura-da-solução)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Dados](#dados)
- [Pipeline de ML](#pipeline-de-ml)
- [API REST](#api-rest)
- [Instalação e Execução](#instalação-e-execução)
- [Conversão Parquet → CSV](#conversão-parquet--csv)
- [Notebooks de Análise](#notebooks-de-análise)
- [Documentação](#documentação)
- [Sprints e Entregas](#sprints-e-entregas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## 🔍 Visão Geral

O projeto consiste em uma solução de **manutenção preditiva** que processa dados de telemetria de equipamentos pesados (caminhões, escavadeiras) para identificar padrões anômalos e emitir alertas de falha antes que ocorram paradas não programadas.

O sistema é composto por:
- **Pipeline de pré-processamento** de dados de sensores (temperatura, pressão, vibração)
- **Modelo de detecção de anomalias** baseado em K-Means clustering
- **API REST** (FastAPI) para inferência em tempo real
- **Notebooks Jupyter** para análise exploratória e validação do modelo

---

## 🏛️ Arquitetura da Solução

```
Dados de Sensores (Parquet)
        │
        ▼
┌─────────────────────┐
│ TelemetryPreprocessor│  ← Limpeza, remoção de nulos/duplicatas
│  (pipeline/)        │     e normalização Z-Score (StandardScaler)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  AnomalyDetector    │  ← K-Means (5 clusters: Desligado, Ocioso,
│  (models/)          │     Normal, Sobrecarga Leve, Sobrecarga Crítica)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   FastAPI (api/)    │  ← Expõe endpoints /health e /predict
│   Porta 8000        │     com validação Pydantic
└─────────────────────┘
```

---

## 📁 Estrutura do Repositório

```
Projeto_vale/
│
├── data/                          # Dados brutos e processados
│   ├── telemetry/
│   │   ├── raw/                   # Arquivos .parquet de telemetria (Jan–Jun)
│   │   └── processed/             # Dados após limpeza/transformação
│   └── apontamentos/              # Dados de apontamentos operacionais
│       ├── desenvolver_apontamentos.parquet
│       ├── desenvolver_apontamentos.csv
│       └── desenvolver_apontamentos.xlsx
│
├── docs/                          # Documentação técnica e de negócio
│   ├── Dicionario_Dados.xlsx      # Descrição de cada campo dos datasets
│   ├── Alarmes - Regra de Negocio.xlsx
│   ├── Desenvolver_Template.docx
│   └── Estudo Guiado - Análise Avançada de Dados.pdf
│
├── notebooks/                     # Jupyter Notebooks de EDA e modelagem
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_transforming.ipynb
│   ├── head_janeiro.png/svg       # Visualizações dos dados
│   ├── matriz_confusao.png/svg    # Métricas do modelo
│   └── janeiro.pdf
│
├── scripts/                       # Utilitários auxiliares
│   ├── convert.cpp                # Conversor Parquet → CSV (C++/Arrow)
│   └── convert                    # Binário compilado
│
├── Produção/                      # Código de produção e artefatos de sprint
│   ├── src/                       # Código-fonte da aplicação
│   │   ├── main.py                # Entry-point da API FastAPI
│   │   ├── requirements.txt       # Dependências Python
│   │   ├── api/
│   │   │   └── routes.py          # Endpoints REST (/health, /predict)
│   │   ├── models/
│   │   │   └── anomaly_detector.py # Motor K-Means de detecção de anomalias
│   │   ├── pipeline/
│   │   │   └── preprocessing.py   # Limpeza e normalização dos dados
│   │   ├── data/                  # Dados internos do módulo
│   │   └── utils/                 # Funções auxiliares
│   ├── Sprint 1/                  # Entregáveis da Sprint 1
│   │   └── Canvas.pdf
│   ├── Sprint 2/                  # Entregáveis da Sprint 2
│   │   ├── srs.tex                # Documento de Requisitos (LaTeX)
│   │   ├── 2.1_Revisao_Codigo/
│   │   ├── 2.2_Metricas_Qualidade/
│   │   ├── 2.3_Retrospectiva/
│   │   └── 2.4_Entrega_Final/
│   ├── Canvas.pdf
│   ├── Backlog da Solução de Telemetria Vale.xlsx
│   └── Revisão.pdf
│
├── Material/                      # Material de apoio e referência
├── .venv/                         # Ambiente virtual Python (não versionado)
├── .gitignore
└── README.md
```

---

## 📊 Dados

### Telemetria

Os dados de telemetria cobrem o período de **Janeiro a Junho**, armazenados em formato **Apache Parquet** para otimização de espaço e velocidade de leitura:

| Arquivo                          | Tamanho aprox. | Período    |
|----------------------------------|----------------|------------|
| `telemetry_jan.parquet`          | ~34 MB         | Janeiro    |
| `telemetry_feb.parquet`          | ~33 MB         | Fevereiro  |
| `telemetry_mar.parquet`          | ~33 MB         | Março      |
| `telemetry_abr.parquet`          | ~38 MB         | Abril      |
| `telemetry_may.parquet`          | ~35 MB         | Maio       |
| `telemetry_jun.parquet`          | ~45 MB         | Junho      |

### Sensores monitorados (por equipamento)

- `temperatura_motor` — Temperatura do motor (°C)
- `pressao_oleo` — Pressão do óleo hidráulico (bar)
- `vibracao_eixo` — Vibração no eixo (mm/s)
- `timestamp` — Timestamp da leitura
- `equipamento_id` — Identificador único do equipamento

> Consulte `docs/Dicionario_Dados.xlsx` para a descrição completa de todos os campos.

---

## 🤖 Pipeline de ML

### Pré-processamento (`pipeline/preprocessing.py`)

A classe `TelemetryPreprocessor` realiza duas etapas:

1. **`remove_nulls_and_duplicates(df)`** — Remove linhas duplicadas e preenche valores nulos numéricos com a **mediana** da coluna (evitando descarte de registros).
2. **`normalize_signals(df, is_training)`** — Aplica normalização **Z-Score** (StandardScaler do scikit-learn) em todos os sinais dos sensores.

### Modelo de Anomalias (`models/anomaly_detector.py`)

O `AnomalyDetector` usa **K-Means com 5 clusters**, definidos para representar os estados operacionais históricos dos equipamentos:

| Cluster | Estado Operacional     | Alarme  | Ação recomendada          |
|---------|------------------------|---------|---------------------------|
| 0       | Desligado              | ❌ Não  | Normal                    |
| 1       | Ocioso                 | ❌ Não  | Normal                    |
| 2       | Operação Normal        | ❌ Não  | Normal                    |
| 3       | Sobrecarga Leve        | ⚠️ Sim | Agendar inspeção em 48h   |
| 4       | Sobrecarga Crítica     | 🚨 Sim | Parada Imediata Necessária|

O modelo treinado é persistido em disco via **joblib** (`models/kmeans_model.joblib`).

---

## 🌐 API REST

A API é construída com **FastAPI** e exposta na porta `8000`.

### Endpoints

#### `GET /api/v1/health`
Verifica o status da API e se o modelo foi carregado.

**Resposta:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

#### `POST /api/v1/predict`
Recebe leituras de sensores e retorna predições de anomalia.

**Body (JSON):**
```json
{
  "data": [
    {
      "equipamento_id": "CAM-001",
      "timestamp": "2025-01-15T08:30:00",
      "temperatura_motor": 95.4,
      "pressao_oleo": 210.5,
      "vibracao_eixo": 3.2
    }
  ]
}
```

**Resposta:**
```json
{
  "equipamento": "CAM-001",
  "predictions": [
    {
      "alarme": false,
      "severidade": "Baixa",
      "acao": "Normal"
    }
  ]
}
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10+
- pip
- (Opcional) g++ com suporte a C++20, librarrow e libparquet para conversão de arquivos

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Projeto_vale
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# ou
.venv\Scripts\activate      # Windows
```

### 3. Instalar dependências

```bash
pip install -r Produção/src/requirements.txt
```

### 4. Configurar variáveis de ambiente (opcional)

Crie um arquivo `.env` na raiz de `Produção/src/`:

```env
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/kmeans_model.joblib
```

### 5. Iniciar a API

```bash
cd Produção/src
python main.py
```

A documentação interativa (Swagger UI) estará disponível em:
**http://localhost:8000/docs**

---

## 🔄 Conversão Parquet → CSV

Os dados de telemetria estão no formato **Parquet** para otimização de espaço. Para converter para CSV (necessário apenas para inspeção manual):

### Pré-requisitos (C++)

```bash
# Ubuntu/Debian
sudo apt install libarrow-dev libparquet-dev
```

### Compilar o conversor

```bash
cd scripts/
g++ -std=c++20 convert.cpp -o convert -larrow -lparquet
```

### Executar a conversão

```bash
./convert ../data/telemetry/raw/telemetry_jan.parquet ../data/telemetry/processed/telemetry_jan.csv
```

> **Alternativa Python:** Os notebooks estão configurados para ler Parquet diretamente via `pandas.read_parquet()`, sem necessidade de conversão.

---

## 📓 Notebooks de Análise

| Notebook                         | Descrição                                                         |
|----------------------------------|-------------------------------------------------------------------|
| `01_data_understanding.ipynb`    | Análise exploratória (EDA): distribuições, outliers, correlações |
| `02_data_transforming.ipynb`     | Transformações, feature engineering e preparação do dataset      |

### Executar os notebooks

```bash
# Com o ambiente virtual ativo
pip install jupyter
jupyter notebook notebooks/
```

Os notebooks carregam os dados diretamente via:

```python
import pandas as pd
df = pd.read_parquet('../data/telemetry/raw/telemetry_jan.parquet')
```

---

## 📄 Documentação

| Arquivo                                        | Conteúdo                                          |
|------------------------------------------------|---------------------------------------------------|
| `docs/Dicionario_Dados.xlsx`                   | Glossário completo dos campos dos datasets        |
| `docs/Alarmes - Regra de Negocio.xlsx`         | Regras de negócio para disparos de alarme         |
| `docs/Estudo Guiado - Análise Avançada de Dados.pdf` | Material de referência técnica              |
| `Produção/Sprint 2/srs.tex`                    | Documento de Requisitos de Software (SRS)         |
| `Produção/Canvas.pdf`                          | Business Model Canvas do projeto                  |
| `Produção/Backlog da Solução de Telemetria Vale.xlsx` | Backlog e histórias de usuário             |

---

## 🗓️ Sprints e Entregas

### Sprint 1
- Entendimento do problema e dos dados (EDA)
- Definição do Canvas de solução
- Configuração do ambiente e estrutura do repositório

### Sprint 2
- Revisão de código e análise de métricas de qualidade
- Documento de Requisitos de Software (SRS)
- Desenvolvimento do pipeline de pré-processamento
- Implementação inicial do modelo K-Means
- Criação da API REST com FastAPI
- Retrospectiva e entrega final

---

## 🛠️ Tecnologias Utilizadas

| Categoria         | Tecnologia                  | Versão     |
|-------------------|-----------------------------|------------|
| **API**           | FastAPI                     | 0.104.1    |
| **Servidor**      | Uvicorn                     | 0.24.0     |
| **ML**            | scikit-learn                | 1.3.2      |
| **Dados**         | Pandas                      | 2.1.2      |
| **Dados**         | NumPy                       | 1.26.1     |
| **Validação**     | Pydantic                    | 2.4.2      |
| **Persistência**  | Joblib                      | 1.3.2      |
| **Visualização**  | Matplotlib / Seaborn        | latest     |
| **Config**        | python-dotenv               | 1.0.0      |
| **Formato dados** | Apache Parquet (via pandas) | —          |
| **Conversor**     | Apache Arrow / C++20        | —          |
| **Notebooks**     | Jupyter Notebook            | —          |

---

## 👥 Equipe

Projeto desenvolvido no âmbito da disciplina **Laboratório de Engenharia de Software** — Universidade Federal do Pará (UFPA), 2026.2.

---

*📌 Para dúvidas sobre os dados ou regras de negócio, consulte os arquivos na pasta `docs/`.*