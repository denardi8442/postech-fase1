# ML Canvas — Predição de Churn

## 1. Objetivo de negócio
Reduzir a taxa de cancelamento de clientes de uma operadora de telecomunicações,
identificando com antecedência aqueles com alta probabilidade de churn, para que
o time de retenção possa agir de forma proativa e direcionada.

## 2. Stakeholders
- Diretoria: interessada na redução da taxa de churn e no impacto financeiro.
- Time de Retenção/CRM: consumidor direto das predições, para priorizar contatos.
- Time de Engenharia/Dados: responsável por manter o pipeline e a API em produção.

## 3. Como o modelo será usado
O modelo gera um score de propensão ao churn por cliente, consumido via API REST
(endpoint /predict). O time de retenção usa esse score para priorizar quais
clientes contatar primeiro, oferecendo ações de retenção (descontos, upgrades,
mudança de plano).

## 4. Fonte e tipo de dados
Dataset público "Telco Customer Churn" (IBM/Kaggle), com 7.043 registros e 21
colunas, contendo dados de contrato, serviços contratados (internet, streaming,
suporte técnico), forma de pagamento e dados demográficos.

## 5. Variável alvo (target)
Churn (Yes/No) — classificação binária. Convertida para 0 (não cancelou) e
1 (cancelou) durante o pré-processamento.

## 6. Métrica de negócio
Redução do número de cancelamentos não identificados previamente pelo time de
retenção (ou seja, maximizar a captura de clientes em risco real de churn).

## 7. Métrica técnica
F1-score como métrica principal, pois equilibra precisão e recall em um cenário
de classes desbalanceadas (~73% não-churn / 27% churn). AUC-ROC como métrica
secundária, para avaliar a capacidade geral de separação do modelo entre as
duas classes, independente do threshold de decisão.

## 8. Principais achados da EDA (que embasam a modelagem)
- Clientes com tempo de contrato (tenure) baixo têm taxa de churn
  significativamente maior — sugerindo que o risco é maior nos primeiros meses.
- Contratos mensais (month-to-month) apresentam taxa de churn muito mais alta
  que contratos anuais ou bianuais.
- [Ajustar conforme os padrões reais observados nos seus gráficos de
  InternetService e PaymentMethod]

## 9. Riscos e limitações
- Dataset estático (não reflete sazonalidade ou mudanças de mercado ao longo
  do tempo).
- Classes desbalanceadas exigem cuidado na escolha de métrica e possivelmente
  técnicas de balanceamento.
- Modelo pode refletir vieses presentes no dataset original (ex.: se certos
  perfis de clientes estão sub-representados).

## 10. Baseline mínimo aceitável
Modelo de Regressão Logística como baseline. Modelos subsequentes (Random
Forest, MLPClassifier) devem superar esse baseline no F1-score para serem
considerados como "modelo campeão".