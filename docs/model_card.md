# Model Card — Modelo de Predição de Churn

## Visão Geral

| | |
|---|---|
| **Tipo de modelo** | Classificação binária |
| **Algoritmo** | Regressão Logística (scikit-learn) |
| **Versão** | 1.0.0 |
| **Data de treinamento** | Agosto de 2026 |
| **Formato de entrega** | Pipeline scikit-learn (pré-processamento + classificador), salvo em `.joblib` |

## Uso Pretendido

O modelo estima a probabilidade de um cliente de telecomunicações cancelar o
serviço (churn), a partir de dados cadastrais, de contrato e de serviços
contratados. O objetivo é apoiar o time de retenção a priorizar contatos
proativos com clientes de alto risco.

**Uso apropriado:** priorização de ações de retenção, apoio à decisão humana.

**Uso inadequado:** o modelo não deve ser usado como único critério para
decisões automatizadas que afetem diretamente o cliente (ex.: negar serviços,
alterar condições contratuais sem revisão humana).

## Dados de Treinamento

- **Fonte:** Telco Customer Churn (IBM/Kaggle), dataset público.
- **Tamanho:** 7.043 registros, 21 colunas originais (19 features após remoção
  de `customerID` e da variável-alvo `Churn`).
- **Período/contexto:** dataset estático, sem indicação de período temporal
  específico ou sazonalidade.
- **Distribuição do alvo:** ~73,5% não-churn / ~26,5% churn (classes
  desbalanceadas).
- **Tratamento de dados:** a coluna `TotalCharges` continha 11 registros com
  valor em branco (clientes com `tenure=0`); esses valores foram convertidos
  para `0.0`, refletindo a ausência de cobrança acumulada para clientes novos.

## Metodologia

Foram treinados e comparados três modelos: Regressão Logística (baseline),
Random Forest e MLPClassifier (rede neural). A comparação utilizou validação
cruzada estratificada (5 folds) sobre o conjunto de treino, seguida de
avaliação final em um conjunto de teste isolado (20% dos dados, nunca usado
durante o desenvolvimento).

## Métricas de Performance (conjunto de teste)

| Modelo | F1-score | AUC-ROC |
|---|---|---|
| **Regressão Logística (campeão)** | **0.6040** | 0.8421 |
| Random Forest | 0.5791 | 0.8364 |
| MLPClassifier | 0.5701 | 0.8430 |

**Métrica principal:** F1-score, escolhida por equilibrar precisão e recall
em um cenário de classes desbalanceadas — mais adequada que acurácia para
este problema de negócio.

**Detalhamento do modelo campeão (Regressão Logística) na classe Churn:**
- Precisão: 0.66
- Recall: 0.56
- F1-score: 0.60

## Justificativa da Escolha do Modelo

A Regressão Logística foi escolhida como modelo campeão por apresentar o
melhor F1-score na avaliação final em teste isolado, além de performance
competitiva na validação cruzada (F1 médio de 0.5923, dentro da margem de
variação dos demais modelos). Adicionalmente, sua maior interpretabilidade e
menor custo computacional são vantagens práticas relevantes para
explicabilidade junto à área de negócio e para manutenção em produção.

## Limitações Conhecidas

- **Recall moderado (0.56):** o modelo deixa de identificar cerca de 44% dos
  clientes que de fato cancelariam o serviço. Em um cenário de negócio real,
  isso significa que nem todos os clientes em risco serão contatados
  proativamente.
- **Dataset estático:** os dados não refletem mudanças de mercado,
  sazonalidade ou alterações na estratégia comercial da operadora ao longo
  do tempo. O modelo pode perder acurácia se os padrões de comportamento dos
  clientes mudarem significativamente (data drift).
- **Classes desbalanceadas:** apesar do uso de F1-score como métrica
  principal, o desbalanceamento (73%/27%) ainda impacta a capacidade do
  modelo de identificar todos os casos de churn.
- **Ausência de teste formal de viés:** não foram conduzidos testes
  específicos para verificar se o modelo apresenta desempenho
  desproporcional entre subgrupos demográficos (ex.: gênero, faixa etária).
  Como o dataset inclui atributos como `gender` e `SeniorCitizen`, existe
  risco potencial de viés não quantificado.
- **Escopo geográfico/contextual limitado:** o dataset representa uma única
  operadora fictícia; a generalização para outras empresas ou mercados não
  foi validada.

## Riscos e Considerações Éticas

O modelo não deve ser utilizado como justificativa automática para negar
serviços, alterar preços individualmente ou tomar decisões que afetem
diretamente o cliente sem revisão humana. Seu uso pretendido é
exclusivamente de apoio à priorização de ações de retenção.

## Manutenção

Recomenda-se reavaliação periódica do modelo (ex.: trimestral) com dados mais
recentes da operadora, para monitorar possível degradação de performance
(data drift) e reavaliar a necessidade de retreinamento.