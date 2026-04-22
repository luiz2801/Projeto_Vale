# Relatório de Métricas de Qualidade — SONAR
## Projeto: Sistema de Manutenção Preditiva com Telemetria — Vale
**Sprint:** 2 | **Data de Análise:** 20/04/2026  
**Ferramenta:** SonarQube / SonarCloud  
**Equipe:** Christian Amarildo Amorim Morais | Luiz Gabriel Santos Moreira

---

## 1. Resumo Executivo

A análise de qualidade foi executada sobre o repositório principal do projeto, abrangendo o backend Python (pipeline de dados + API FastAPI) e os scripts de pré-processamento. Os resultados indicam um projeto com base de código saudável para um protótipo em estágio inicial, com oportunidades claras de melhoria para a entrega final.

---

## 2. Painel de Qualidade Geral

| Dimensão | Rating | Valor |
|----------|--------|-------|
| **Reliability (Confiabilidade)** | 🟡 B | 2 bugs |
| **Security (Segurança)** | 🔴 C | 1 vulnerabilidade crítica |
| **Maintainability (Manutenibilidade)** | 🟢 A | 12 code smells |
| **Coverage (Cobertura de Testes)** | 🔴 D | 38,2% |
| **Duplications (Duplicações)** | 🟢 A | 2,1% |
| **Quality Gate** | ⚠️ **FAILED** | Coverage < 60% |

---

## 3. Bugs Identificados

### BUG-001 — Severidade: Major
- **Arquivo:** `pipeline/preprocessing.py`, linha 88
- **Descrição:** `pd.read_csv()` sem parâmetro `encoding`, podendo causar falha silenciosa com dados em Latin-1 (padrão de sistemas legados da Vale).
- **Regra SONAR:** `python:S5542`
- **Status:** ✅ Corrigido em commit `fix/encoding-csv-reader`

### BUG-002 — Severidade: Minor
- **Arquivo:** `api/routes.py`, linha 110
- **Descrição:** Variável `result` pode ser `None` caso o DataFrame esteja vazio, mas é acessada sem verificação logo após.
- **Regra SONAR:** `python:S2259` (Null pointer dereference)
- **Status:** 🟡 Em correção

---

## 4. Vulnerabilidade de Segurança

### SEC-001 — Severidade: Critical (Blocker)
- **Arquivo:** `api/routes.py`, linha 23
- **Descrição:** Credencial de banco de dados hardcoded como string literal (`DB_PASSWORD = "vale@2024"`).
- **Regra SONAR:** `python:S2068` (Hard-coded credentials)
- **Status:** ✅ Corrigido em commit `fix/remove-hardcoded-credentials` — migrado para `.env`

---

## 5. Code Smells (12 Identificados)

| ID | Arquivo | Linha | Descrição | Esforço | Status |
|----|---------|-------|-----------|---------|--------|
| CS-01 | `preprocessing.py` | 31-45 | Função com 47 linhas (limite recomendado: 30) | 15min | Pendente |
| CS-02 | `preprocessing.py` | 47 | Magic number `3` sem constante nomeada | 5min | Pendente |
| CS-03 | `anomaly_detector.py` | 88 | Parâmetro `k=5` sem documentação | 5min | ✅ Resolvido |
| CS-04 | `anomaly_detector.py` | 65 | `print()` usado para logging | 10min | Pendente |
| CS-05 | `routes.py` | 23 | Credencial hardcoded | 10min | ✅ Resolvido |
| CS-06 | `routes.py` | 88 | Treino do modelo dentro de rota HTTP | 20min | Pendente |
| CS-07 | `routes.py` | 45 | Método com complexidade ciclomática = 12 (limite: 10) | 30min | Pendente |
| CS-08 | `database.py` | 15 | String de conexão concatenada com `+` | 10min | Pendente |
| CS-09 | `preprocessing.py` | Global | 3 funções sem docstring | 20min | Pendente |
| CS-10 | `anomaly_detector.py` | Global | Módulo sem bloco `if __name__ == '__main__':` | 5min | Pendente |
| CS-11 | `routes.py` | 112 | Variável `temp_df` nunca usada | 5min | Pendente |
| CS-12 | `routes.py` | 130 | Catch genérico `except Exception:` | 15min | Pendente |

**Total de esforço estimado para resolução:** ~2h 30min

---

## 6. Cobertura de Testes

```
Módulo                          | Linhas | Cobertas | Cobertura
--------------------------------|--------|----------|----------
pipeline/preprocessing.py       |   120  |    58    |  48,3%
api/routes.py                   |    95  |    25    |  26,3%
models/anomaly_detector.py      |    80  |    37    |  46,2%
utils/file_handler.py           |    45  |    27    |  60,0%
TOTAL                           |   340  |   147    |  43,2%
```

> **Meta para Sprint 3:** Atingir mínimo de **60% de cobertura** para passar no Quality Gate.

---

## 7. Duplicações de Código

```
Duplicação identificada: 2,1% (~72 linhas duplicadas)
Arquivo principal: preprocessing.py e anomaly_detector.py
Padrão duplicado: lógica de carregamento de DataFrame
Ação: Extrair para módulo utilitário compartilhado 'utils/data_loader.py'
```

---

## 8. Plano de Ação para Próximo Sprint

| Prioridade | Ação | Responsável |
|-----------|------|-------------|
| 🔴 High | Aumentar cobertura de testes para ≥60% | Ambos |
| 🔴 High | Corrigir BUG-002 (Null dereference) | Luiz Gabriel |
| 🟡 Medium | Refatorar funções longas (CS-01, CS-07) | Christian |
| 🟡 Medium | Migrar todos os `print()` para `logging` | Luiz Gabriel |
| 🟢 Low | Adicionar docstrings faltantes (CS-09) | Ambos |
| 🟢 Low | Eliminar duplicações — criar `data_loader.py` | Christian |

---

## 9. Tendência de Qualidade

```
Sprint 1 → Sprint 2:
  Bugs:        5 → 2  ✅ Melhora
  Smells:     20 → 12  ✅ Melhora
  Coverage:  N/A → 38%  📈 Base estabelecida
  Security:    0 → 1  ⚠️ (credencial remediada no mesmo sprint)
```

---

*Análise SONAR gerada em: 20/04/2026*  
*Repositório: GitHub — LABVIS-UFPA / Projeto-Vale-Telemetria*
