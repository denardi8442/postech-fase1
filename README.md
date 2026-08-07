# Tech Challenge — Fase 1: Pipeline Preditivo de Churn

Projeto de Machine Learning para prever churn (cancelamento) de clientes de
uma operadora de telecomunicações, desde a análise exploratória de dados até
a disponibilização do modelo via API REST.

Desenvolvido individualmente como parte do Tech Challenge da Fase 1 da
POSTECH.

## Sobre o Projeto

Uma operadora de telecomunicações enfrenta perda acelerada de clientes. Este
projeto constrói um pipeline preditivo de churn, comparando três algoritmos
de classificação (Regressão Logística, Random Forest e MLPClassifier), e
disponibiliza o modelo campeão via uma API REST construída com FastAPI.

**Dataset:** [Telco Customer Churn (IBM/Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
— 7.043 registros, 21 colunas.

**Modelo campeão:** Regressão Logística (F1-score: 0.6040, AUC-ROC: 0.8421)

Para detalhes completos sobre a formulação do problema, veja o
[ML Canvas](docs/ml_canvas.md). Para detalhes sobre performance, limitações e
uso responsável do modelo, veja o [Model Card](docs/model_card.md).

## Estrutura do Projeto

tech_challenge/
├── data/
│ └── raw/ # dataset bruto (nunca modificado)
├── docs/ # ML Canvas, Model Card, enunciado do desafio
├── models/ # modelo treinado (.joblib)
├── notebooks/ # notebooks de experimentação
│ ├── 01_eda.ipynb
│ ├── 02_baseline.ipynb
│ ├── 03_random_forest.ipynb
│ ├── 04_mlp.ipynb
│ └── 05_comparacao_modelos.ipynb
├── src/ # código produtivo
│ ├── config.py # caminhos e constantes
│ ├── preprocessing.py # limpeza e tratamento de dados
│ ├── model.py # carregamento do modelo e predição
│ └── api/
│ ├── main.py # aplicação FastAPI
│ └── schemas.py # validação de entrada/saída (Pydantic)
├── tests/ # testes automatizados (Pytest)
├── requirements.txt
└── pytest.ini

## Como Executar o Projeto

### Pré-requisitos

- Python 3.13+
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/denardi8442/postech-fase1.git
cd postech-fase1
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
# ou: source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixar o dataset

Baixe o dataset [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
do Kaggle e salve o arquivo CSV em `data/raw/telco_churn.csv`.

### 5. (Opcional) Retreinar o modelo

O modelo campeão já está salvo em `models/churn_model.joblib`. Caso queira
retreinar, execute os notebooks em ordem, de `01_eda.ipynb` até
`05_comparacao_modelos.ipynb`.

### 6. Rodar a API localmente

```bash
uvicorn src.api.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação
interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

### 7. Rodar os testes automatizados

```bash
pytest -v
```

## Endpoints da API

### `GET /health`

Verifica se a API está no ar e se o modelo foi carregado com sucesso.

**Resposta:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `POST /predict`

Recebe os dados de um cliente e retorna a predição de churn.

**Exemplo de requisição:**
```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}
```

**Resposta:**
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.6137
}
```

## Metodologia

1. **EDA e Baseline** — análise exploratória do dataset, tratamento de dados
   (correção da coluna `TotalCharges`), e treinamento de um baseline com
   Regressão Logística.
2. **Modelagem e Avaliação** — treinamento de Random Forest e MLPClassifier,
   validação cruzada estratificada (5 folds), e comparação dos três modelos
   em um conjunto de teste isolado.
3. **Engenharia de Software** — refatoração da lógica de pré-processamento e
   predição para módulos Python testáveis (`src/`), com testes automatizados
   via Pytest.
4. **API** — disponibilização do modelo campeão via FastAPI, com validação
   de entrada via Pydantic.

## Documentação Adicional

- [ML Canvas](docs/ml_canvas.md) — formulação do problema de negócio.
- [Model Card](docs/model_card.md) — performance, limitações e uso
  responsável do modelo.

## Autor

Desenvolvido individualmente por Alexandre Denardi (rm376341), como parte do Tech
Challenge da Fase 1 — POSTECH.