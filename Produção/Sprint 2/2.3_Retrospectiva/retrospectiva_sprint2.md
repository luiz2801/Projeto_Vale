# Retrospectiva do Sprint 2
## Projeto: Sistema de Manutenção Preditiva com Telemetria — Vale
**Equipe:** Christian Amarildo Amorim Morais | Luiz Gabriel Santos Moreira  
**Data da Retrospectiva:** 20/04/2026  
**Sprint:** 2 (13/04/2026 – 22/04/2026)

---

## 1. Contexto do Sprint

O Sprint 2 concentrou-se na evolução do sistema de suporte a decisões para manutenção preditiva de equipamentos de mineração (escavadeiras e caminhões de grande porte) com base nos dados de telemetria fornecidos pela Vale. Neste sprint, os principais objetivos foram: validação de requisitos, construção de protótipos navegáveis, revisão de código entre pares, análise de qualidade via SONAR e entrega do código final no GitHub.

---

## 2. O que fizemos bem? ✅

| # | Ponto Positivo | Descrição |
|---|---------------|-----------|
| 1 | **Validação de Requisitos** | Confirmamos com sucesso os requisitos prioritários do sistema: pipeline de ingestão de dados de telemetria, módulo de detecção de anomalias e interface de visualização de alertas. |
| 2 | **Prototipagem Navegável** | Construímos protótipos de alta fidelidade das telas principais: Dashboard de Saúde dos Equipamentos, Histórico de Alertas e Painel de Recomendações Prescritivas. |
| 3 | **Esqueleto Técnico** | Montamos a estrutura base do pipeline de dados (ingestão → pré-processamento → modelo → visualização) com sucesso. |
| 4 | **Peer Review** | A revisão entre pares ocorreu conforme planejado em 15/04, garantindo qualidade mínima do código antes da entrega. |
| 5 | **Comunicação da Equipe** | Mantivemos boa comunicação e divisão clara de responsabilidades entre os dois integrantes. |

---

## 3. O que pode melhorar? 🔧

| # | Ponto de Melhoria | Proposta de Ação |
|---|-------------------|-----------------|
| 1 | **Tempo de integração** | Iniciar integração frontend/backend mais cedo no sprint para evitar acúmulo nos últimos dias. |
| 2 | **Commits mais frequentes** | Realizar commits menores e mais frequentes para evidenciar progresso contínuo e facilitar rastreabilidade. |
| 3 | **Documentação inline** | Aumentar a quantidade de comentários no código durante o desenvolvimento, e não apenas ao final. |
| 4 | **Planejamento do SONAR** | Reservar um slot específico no início do sprint para configurar a análise SONAR, evitando configuração tardia. |
| 5 | **Testes unitários** | Implementar testes desde as primeiras camadas do pipeline para não acumular dívida técnica. |

---

## 4. Análise das User Stories

### Story US-01 — Ingestão de Dados de Telemetria
- **Critério de Aceitação:** Receber arquivos CSV/JSON do data pack da Vale e armazenar em banco de dados estruturado.
- **Status:** ✅ Concluída
- **Lição Aprendida:** O tratamento de valores ausentes (outliers e NaN) exigiu mais tempo do que estimado. Na próxima sprint, adicionar um ponto específico para análise de qualidade dos dados na estimativa.

### Story US-02 — Detecção de Anomalias no Sinal de Telemetria
- **Critério de Aceitação:** O sistema deve identificar desvios nos sinais que precedem falha mecânica com base no histórico.
- **Status:** 🟡 Em andamento (70% concluída)
- **Lição Aprendida:** A seleção do método de clustering (K-Means vs. DBSCAN) gerou debate interno. Decidimos prototipar os dois e comparar métricas de silhueta nas próximas iterações.

### Story US-03 — Painel de Alertas e Recomendações
- **Critério de Aceitação:** O engenheiro de manutenção deve visualizar alertas com indicação do componente afetado, severidade e ação recomendada.
- **Status:** ✅ Protótipo navegável entregue
- **Lição Aprendida:** O feedback da persona (engenheiro "Cristiano") reforçou a necessidade de uma linguagem simples e prática, evitando jargão técnico de IA na interface.

### Story US-04 — Exportação de Relatório de Saúde do Equipamento
- **Critério de Aceitação:** Gerar relatório PDF com histórico de alertas e recomendações do período selecionado.
- **Status:** 🔴 Não iniciada (backlog priorizado para Sprint 3)
- **Lição Aprendida:** Prematura no MVP. Será inserida como item prioritário do Sprint 3 após validação do motor de detecção.

---

## 5. Métricas do Sprint

| Métrica | Valor |
|---------|-------|
| Total de Story Points planejados | 21 SP |
| Story Points entregues | 15 SP |
| Velocidade do Sprint (média) | 7,5 SP/dev |
| Número de commits realizados | ~28 commits |
| Defeitos identificados no Peer Review | 5 (2 críticos, 3 menores) |
| Code Smells detectados no SONAR | 12 |
| Cobertura de testes estimada | ~38% |

---

## 6. Itens de Ação para o Sprint 3

| # | Ação | Responsável | Prazo |
|---|------|-------------|-------|
| 1 | Concluir módulo de detecção de anomalias (US-02) | Luiz Gabriel | Início Sprint 3 |
| 2 | Reduzir code smells identificados no SONAR de 12 para <5 | Christian | Semana 1 Sprint 3 |
| 3 | Implementar testes unitários para o pipeline de dados | Ambos | Semana 1 Sprint 3 |
| 4 | Configurar SONAR automaticamente via CI/CD | Christian | Sprint 3 |
| 5 | Iniciar US-04 (Exportação de Relatório) | Luiz Gabriel | Semana 2 Sprint 3 |

---

## 7. Sentimento da Equipe

> *"O Sprint 2 foi desafiador mas produtivo. Conseguimos validar a viabilidade técnica do pipeline e entregar um protótipo funcional que reflete a dor real do engenheiro de manutenção da Vale. A revisão de código fortaleceu a qualidade do que entregamos. Para o próximo sprint, queremos focar em integração mais cedo e cobertura de testes mais abrangente."*
>
> — Christian Amarildo & Luiz Gabriel

---

*Documento gerado em: 20/04/2026 | Revisão em: 22/04/2026*
