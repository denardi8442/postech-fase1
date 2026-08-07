"""
API REST para predição de churn de clientes, usando FastAPI.

Endpoints:
- GET  /health   - verifica se a API esta no ar
- POST /predict  - recebe os dados de um cliente e retorna a predicao de churn
"""
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.model import load_model, predict_churn
from src.api.schemas import ClienteInput, PredictResponse

# Carrega o modelo uma unica vez, quando a aplicacao inicia
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo treinado na memoria quando a API sobe."""
    global model
    model = load_model()
    yield
    # (nenhuma limpeza necessaria ao desligar, neste caso)


app = FastAPI(
    title="API de Predicao de Churn",
    description="Prediz a propensao de cancelamento de clientes de telecomunicacoes.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    """
    Verifica se a API esta no ar e se o modelo foi carregado com sucesso.
    """
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictResponse)
def predict(cliente: ClienteInput):
    """
    Recebe os dados de um cliente e retorna a predicao de churn
    (classe prevista e probabilidade).
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo ainda nao foi carregado. Tente novamente em instantes."
        )

    # Converte o objeto Pydantic validado em DataFrame de uma linha,
    # no formato esperado pelo pipeline de predicao
    df = pd.DataFrame([cliente.model_dump()])

    result = predict_churn(model, df)

    return PredictResponse(
        churn_prediction=int(result.loc[0, 'churn_prediction']),
        churn_probability=float(result.loc[0, 'churn_probability'])
    )
