# Guia de Entrevista Semiestruturada
## Projeto: Sistema de Manutenção Preditiva com Telemetria — Vale
**Sprint:** 2 | **Data:** 22/04/2026  
**Objetivo:** Validar requisitos do sistema junto ao usuário-alvo (Engenheiro de Manutenção)

---

## 1. Objetivo da Entrevista

Coletar feedback qualitativo do usuário-alvo para validar as hipóteses de valor do sistema, refinar o backlog e identificar gaps entre o que foi construído e as necessidades reais do dia a dia do engenheiro de manutenção da mineração.

---

## 2. Perfil do Entrevistado

| Campo | Informação |
|-------|-----------|
| **Persona** | Engenheiro de Manutenção |
| **Experiência** | ≥ 5 anos em manutenção de equipamentos pesados (mineração) |
| **Contato com dados** | Utiliza planilhas e relatórios de telemetria no dia a dia |
| **Dor principal** | Sobrecarga de dados, manutenção reativa e "apagar incêndios" |

---

## 3. Aquecimento (5 min)

1. Pode se apresentar brevemente — há quanto tempo trabalha com manutenção de equipamentos neste segmento?
2. Como é uma manhã típica de trabalho para você em termos de análise de dados dos equipamentos?
3. Quantas fontes diferentes de dados você consulta antes de tomar uma decisão de manutenção?

---

## 4. Bloco 1 — Coleta e Análise de Dados (10 min)

4. Quais são os sinais de telemetria que você considera mais críticos para prever uma falha mecânica? (Ex: temperatura, vibração, pressão hidráulica)
5. Com que frequência você consegue revisar os dados de telemetria de todos os equipamentos da sua frota?
6. Já aconteceu de você ter os dados disponíveis, mas não ter tempo de analisá-los antes da falha acontecer? Pode descrever essa situação?
7. *[Mostrar dashboard protótipo]* O que você acha desse painel de alertas? Consegue entender o que está sendo mostrado sem explicação prévia?

---

## 5. Bloco 2 — Alertas e Decisões (10 min)

8. Quando um equipamento apresenta um sinal de alerta, qual é o seu fluxo de decisão atual? (Ex: consulta histórico, chama técnico, agenda parada)
9. Quanta antecedência mínima você precisaria de um alerta para conseguir planejar uma manutenção sem impactar a operação?
10. *[Hipótese]* Suponha que o sistema indique: "Componente: Sistema hidráulico do caminhão CAT-793. Risco de falha estimado em 72h. Ação sugerida: substituir filtro hidráulico." — Isso seria útil? O que mudaria se o prazo fosse 24h?
11. Você confiaria em uma recomendação de sistema de IA para agendar uma parada de manutenção sem confirmar manualmente com um técnico? Por quê?

---

## 6. Bloco 3 — Usabilidade e Integração (10 min)

12. Quais ferramentas você usa hoje para registrar ordens de serviço? O sistema precisaria se integrar com elas?
13. *[Mostrar tela de relatório]* Se você pudesse exportar automaticamente um relatório semanal com os alertas e ações tomadas, isso te ajudaria em reuniões com a gestão? Com que frequência?
14. O que tornaria esse sistema parte do seu fluxo de trabalho diário? O que impediria?
15. Existe alguma funcionalidade que você considera **obrigatória** para usar essa ferramenta? E alguma que definitivamente **não usaria**?

---

## 7. Encerramento (5 min)

16. Em uma escala de 0 a 10, o quanto você recomendaria uma ferramenta como essa para um colega engenheiro? O que levou a esse número?
17. Há algo que eu não perguntei mas que você consider importante para o desenvolvimento desta ferramenta?

---

## 8. Modelo de Registro das Respostas

```
Entrevistado: ___________________________
Data/Hora: ______________________________
Entrevistador: __________________________

P4 - Sinais críticos mencionados:
_________________________________________

P7 - Reação ao protótipo do dashboard:
_________________________________________

P9 - Antecedência mínima desejada para alertas:
_________________________________________

P11 - Nível de confiança em IA para manutenção:
_________________________________________

P14 - O que tornaria o sistema parte do fluxo:
_________________________________________

P16 - NPS (0-10): ___
Justificativa: ___________________________

Observações gerais:
_________________________________________
```

---

## 9. Indicadores de Sucesso da Entrevista

- [ ] Confirmação de pelo menos 3 sinais de telemetria críticos identificados pelo usuário
- [ ] Entendimento do prazo mínimo de antecedência dos alertas
- [ ] Feedback qualitativo sobre o protótipo do dashboard
- [ ] Identificação de pelo menos 1 gap não previsto no backlog atual
- [ ] NPS ≥ 7 para o conceito do produto

---

*Documento preparado em: 22/04/2026*  
*Christian Amarildo Amorim Morais | Luiz Gabriel Santos Moreira*
