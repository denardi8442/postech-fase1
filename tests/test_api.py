"""
Testes de integração para a API FastAPI (endpoints /health e /predict).
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """
    Fixture que cria um TestClient dentro de um contexto 'with',
    garantindo que os eventos de startup (carregamento do modelo)
    sejam executados antes dos testes.
    """
    with TestClient(app) as test_client:
        yield test_client


def test_health_retorna_status_ok(client):
    """
    Garante que o endpoint /health responde com sucesso e confirma
    que o modelo foi carregado.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


def test_predict_retorna_predicao_valida(client):
    """
    Garante que o endpoint /predict, recebendo um cliente valido,
    retorna uma predicao no formato esperado.
    """
    cliente_exemplo = {
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

    response = client.post("/predict", json=cliente_exemplo)

    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] in [0, 1]
    assert 0.0 <= data["churn_probability"] <= 1.0


def test_predict_rejeita_dado_invalido(client):
    """
    Garante que o endpoint /predict rejeita (com erro 422) um payload
    com valor invalido em um campo restrito (Contract).
    """
    cliente_invalido = {
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
        "Contract": "Mensal",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": 29.85
    }

    response = client.post("/predict", json=cliente_invalido)

    assert response.status_code == 422
