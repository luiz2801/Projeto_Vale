# Relatório de Revisão de Código — Peer Review
## Projeto: Sistema de Manutenção Preditiva com Telemetria — Vale
**Data da Revisão:** 15/04/2026  
**Sprint:** 2  
**Revisor 1:** Christian Amarildo Amorim Morais → revisou código de Luiz Gabriel  
**Revisor 2:** Luiz Gabriel Santos Moreira → revisou código de Christian

---

## 1. Metodologia de Revisão

A revisão foi conduzida seguindo o guia de boas práticas de peer review com foco em:
- **Legibilidade e organização** do código
- **Corretude lógica** dos algoritmos implementados
- **Segurança e robustez** (validação de entradas, tratamento de exceções)
- **Performance** (complexidade, uso de memória)
- **Documentação** (docstrings, comentários)
- **Conformidade** com os padrões PEP 8 (Python)

---

## 2. Revisão 1 — Christian revisa código de Luiz Gabriel

### Módulo Revisado: `pipeline/preprocessing.py`
**Função principal:** Pré-processamento dos dados de telemetria (limpeza, normalização e remoção de outliers)

#### 2.1 Pontos Positivos
- Uso correto de `pandas` para manipulação do DataFrame de telemetria.
- Separação clara entre as funções `remove_nulls()`, `normalize_signals()` e `detect_outliers()`, facilitando a manutenção.
- Nomenclatura de variáveis clara e autoexplicativa.

#### 2.2 Problemas Encontrados

| ID | Severidade | Linha(s) | Descrição | Sugestão |
|----|-----------|---------|-----------|----------|
| PR-01 | 🔴 Crítico | 47-52 | A função `detect_outliers()` usa limite fixo de ±3σ sem validar se os dados têm distribuição normal. Em sensores industriais, isso pode gerar falsos positivos. | Adicionar verificação de normalidade (teste Shapiro-Wilk) ou adotar IQR como alternativa robusta. |
| PR-02 | 🔴 Crítico | 88 | `pd.read_csv()` chamado sem `encoding` explícito. Arquivos da Vale com caracteres especiais (ç, ã) podem causar `UnicodeDecodeError` em produção. | Adicionar `encoding='utf-8-sig'` ou `encoding='latin-1'`. |
| PR-03 | 🟡 Médio | 31 | Loop `for` iterando linha a linha em DataFrame grande (~500k linhas). Desempenho crítico. | Substituir por operações vetorizadas com `.apply()` ou operações nativas do pandas. |
| PR-04 | 🟡 Médio | 65-70 | Sem tratamento de exceção para arquivos corrompidos ou vazios. | Adicionar `try/except` com logging adequado. |
| PR-05 | 🟢 Menor | Global | Ausência de docstrings nas funções principais. | Adicionar docstrings no padrão Google (Args, Returns, Raises). |

#### 2.3 Aprovação
- **Status:** ✅ Aprovado com ressalvas — corrigir itens PR-01 e PR-02 antes do merge.

---

## 3. Revisão 2 — Luiz Gabriel revisa código de Christian

### Módulo Revisado: `api/routes.py` + `models/anomaly_detector.py`
**Função principal:** API de consulta de dados e modelo de detecção de anomalias com K-Means

#### 3.1 Pontos Positivos
- Estrutura da API REST bem organizada com separação de responsabilidades (routes, models, schemas).
- Uso adequado de `FastAPI` com validação de tipos via `Pydantic`.
- O modelo de clustering foi versionado com `joblib`, permitindo serialização.

#### 3.2 Problemas Encontrados

| ID | Severidade | Linha(s) | Descrição | Sugestão |
|----|-----------|---------|-----------|----------|
| PR-06 | 🔴 Crítico | 23 | Credenciais de banco de dados hardcoded no arquivo `routes.py`. Risco de segurança grave se commitado. | Utilizar variáveis de ambiente com `python-dotenv` e arquivo `.env` no `.gitignore`. |
| PR-07 | 🟡 Médio | 88-95 | `fit()` do K-Means chamado em cada requisição à API. O modelo deve ser pré-treinado e apenas o `predict()` deve ser executado em tempo real. | Carregar o modelo treinado na inicialização da aplicação (`startup_event`). |
| PR-08 | 🟡 Médio | 110 | Endpoint `/predict` sem nenhuma validação de schema. Pode receber payloads inválidos e quebrar o servidor. | Criar schema Pydantic para o input do endpoint. |
| PR-09 | 🟢 Menor | 45 | Magic number `k=5` sem justificativa. | Adicionar comentário explicando a escolha do número de clusters ou parametrizar via config. |
| PR-10 | 🟢 Menor | Global | Logs apenas com `print()`. | Substituir por `logging` do Python para controle de nível (DEBUG, INFO, ERROR). |

#### 3.3 Aprovação
- **Status:** ✅ Aprovado com ressalvas — corrigir item PR-06 imediatamente (risco de segurança). PR-07 e PR-08 devem ser corrigidos antes da próxima release.

---

## 4. Resumo Consolidado

| Métrica | Valor |
|---------|-------|
| Total de issues identificadas | 10 |
| Críticas (bloqueantes) | 3 |
| Médias | 4 |
| Menores | 3 |
| Issues resolvidas até 22/04 | 3 (PR-01, PR-02, PR-06) |
| Issues pendentes (Sprint 3) | 7 |

---

## 5. Lições do Peer Review

1. **Segurança first:** Nunca commitar credenciais. Configurar o SONAR para detectar esse padrão automaticamente.
2. **Performance importa cedo:** Loops em DataFrames grandes são um anti-pattern que peça ser pego na revisão, não em produção.
3. **Schemas e validação:** APIs sem validação de entrada são bombas-relógio. Pydantic torna isso trivial no FastAPI.
4. **Revisar código alheio melhora o próprio:** Ambos os revisores identificaram padrões que passarão a aplicar proativamente em seus próprios módulos.

---

*Revisão concluída em: 15/04/2026*  
*Assinaturas: Christian Amarildo Amorim Morais | Luiz Gabriel Santos Moreira*
