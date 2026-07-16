# Product Backlog Atualizado — ARO-PBB
## Projeto: Sistema de Manutenção Preditiva com Telemetria — Vale
**Sprint:** 2 → Atualização pós-sprint  
**Data:** 22/04/2026  
**Metodologia de Priorização:** ARO-PBB (Actors, Roles, Outcomes — Product Backlog Building)

---

## 1. Atores e Papéis (Actors & Roles)

| Ator | Papel | Necessidade Principal |
|------|-------|----------------------|
| **Engenheiro de Manutenção** (ex: Cristiano) | Usuário primário | Receber alertas preditivos antes da falha para planejar manutenção com antecedência |
| **Gestor de Operações** | Usuário secundário | Visualizar dashboard com status de frotas e custo evitado por manutenção preditiva |
| **Analista de Dados** | Usuário técnico | Treinar e auditar os modelos, ajustar thresholds de alerta |
| **Sistema de Telemetria Vale** | Sistema externo | Fornecer sinais contínuos de sensores dos equipamentos (escavadeiras, caminhões) |

---

## 2. Outcomes (Resultados Esperados)

1. **O engenheiro recebe alertas relevantes antes da falha** — com indicação clara do componente, severidade e ação recomendada.
2. **O gestor reduz custos de manutenção corretiva em campo** — através de manutenção planejada versus emergencial.
3. **O analista mantém os modelos atualizados e auditáveis** — com rastreabilidade de decisões e métricas de desempenho.
4. **O sistema processa dados de telemetria de forma confiável** — com tratamento de outliers, valores ausentes e redundâncias.

---

## 3. Product Backlog Priorizado

### 🔴 MUST HAVE — Sprint Atual e Próximo (Alta Prioridade)

| ID | User Story | Critério de Aceitação | SP | Status |
|----|-----------|----------------------|----|--------|
| **US-01** | **Como engenheiro**, quero que o sistema ingira automaticamente os arquivos de telemetria CSV/JSON, para que eu não precise fazer processamento manual dos dados. | Arquivos carregados em < 30s. Valores nulos e outliers tratados automaticamente. | 8 | ✅ Concluída |
| **US-02** | **Como analista**, quero que o modelo detecte padrões anômalos nos sinais de sensores, para que possamos identificar possíveis falhas mecânicas com antecedência. | Modelo treinado com histórico ≥ 6 meses. Precision ≥ 70%, Recall ≥ 65%. | 13 | 🟡 70% concluída |
| **US-03** | **Como engenheiro**, quero visualizar um painel de alertas com equipamento, componente e severidade, para que eu possa priorizar minha agenda de manutenção. | Dashboard carrega em < 3s. Alertas classificados em: Crítico, Alerta, Normal. | 8 | ✅ Protótipo entregue |
| **US-05** | **Como analista**, quero que o pipeline tenha testes automatizados com cobertura ≥ 60%, para garantir que refatorações não quebrem funcionalidades existentes. | Quality Gate SONAR aprovado. CI/CD executa testes automaticamente. | 5 | 🔴 38% atual |

---

### 🟡 SHOULD HAVE — Sprint 3 (Média Prioridade)

| ID | User Story | Critério de Aceitação | SP | Status |
|----|-----------|----------------------|----|--------|
| **US-04** | **Como gestor**, quero exportar um relatório PDF com o histórico de alertas do período, para apresentar em reuniões de operações. | Relatório gerado em < 10s. Inclui gráfico de tendência e tabela de alertas. | 5 | 🔴 Backlog |
| **US-06** | **Como engenheiro**, quero receber não só o alerta, mas também a recomendação de qual peça trocar e em quanto tempo, para planejar com precisão. | Recomendação prescritiva baseada em histórico de falhas similar. Janela de antecipação indicada em horas. | 13 | 🔴 Backlog |
| **US-07** | **Como analista**, quero comparar métricas de diferentes algoritmos (K-Means vs. DBSCAN vs. Isolation Forest), para escolher o mais eficaz por tipo de equipamento. | Relatório comparativo com Silhouette Score, F1, tempo de processamento. | 8 | 🔴 Backlog |
| **US-08** | **Como engenheiro**, quero filtrar o painel por modelo de equipamento (escavadeira vs. caminhão), para focar em um tipo de frota por vez. | Filtros aplicados em tempo real sem recarregamento de página. | 3 | 🔴 Backlog |

---

### 🟢 COULD HAVE — Versão Futura (Baixa Prioridade)

| ID | User Story | Critério de Aceitação | SP | Justificativa |
|----|-----------|----------------------|----|--------------|
| **US-09** | **Como gestor**, quero um módulo de simulação de custo evitado, para calcular o ROI da manutenção preditiva. | Cálculo baseado em custo por hora parada vs. custo da manutenção planejada. | 8 | Depende de dados financeiros da Vale — requer integração externa. |
| **US-10** | **Como analista**, quero suporte a imagens de OCR de documentos de manutenção escaneados, para incluir dados históricos não digitalizados. | Extração de texto com acurácia ≥ 90% em documentos A4 padrão. | 13 | Alta complexidade técnica — prioridade baixa no MVP. |
| **US-11** | **Como gestor**, quero integração com sistema de ERP da Vale, para que os alertas gerem ordens de serviço automaticamente. | Integração via API REST. OS criada em < 5min do alerta. | 21 | Dependência de acesso ao sistema interno da Vale — fora do escopo acadêmico. |

---

## 4. Justificativas de Priorização ARO-PBB

### Por que US-05 (Testes) é MUST HAVE?
A cobertura de testes não é burocracia — é o que garante que o pipeline de dados da Vale não produza falsos negativos em produção. Um falso negativo (falha não detectada) pode custar milhões por hora de operação parada. **Qualidade é parte do produto.**

### Por que US-06 (Manutenção Prescritiva) é SHOULD HAVE?
Identificado pela revisão de imersão (Revisão.docx) como a maior oportunidade de valor: não apenas prever a falha, mas recomendar *o quê* e *quando* trocar. No entanto, depende da conclusão de US-02 (detecção de anomalias), logo não pode ser MUST HAVE neste momento.

### Por que US-11 (ERP) é COULD HAVE?
Requer acesso a sistemas internos da Vale, o que está fora do escopo de um projeto acadêmico. Incluso no backlog para demonstrar visão de produto, mas sem comprometimento de implementação no contexto atual.

---

## 5. Velocidade e Capacidade

| Sprint | SP Planejados | SP Entregues | Velocidade |
|--------|-------------|-------------|-----------|
| Sprint 1 | 13 | 13 | 13 SP |
| Sprint 2 | 21 | 15 | 15 SP |
| **Sprint 3 (estimado)** | **18** | — | — |

> **Nota:** A velocidade do Sprint 3 foi ajustada para 18 SP (conservadora) considerando a dívida técnica de cobertura de testes que precisará ser endereçada.

---

## 6. Definition of Done — Sprint 2

Uma história é considerada **Concluída** quando:
- [ ] Código mergeado na branch `main` via Pull Request revisado
- [ ] Testes unitários escritos para os fluxos principais
- [ ] SONAR executado sem novos blockers
- [ ] Funcionalidade demonstrável no protótipo ou na API
- [ ] Documentação atualizada (README ou docstring)

---

*Backlog atualizado em: 22/04/2026*  
*Responsáveis: Christian Amarildo Amorim Morais | Luiz Gabriel Santos Moreira*
