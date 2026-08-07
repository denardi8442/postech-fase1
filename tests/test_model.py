"""
Testes unitários para as funções de carregamento e predição do modelo.
"""
import pandas as pd
import pytest
from src.model import load_model, predict_churn


def test_load_model_retorna_pipeline_treinado():
    """
    Garante que o modelo salvo pode ser carregado sem erros e que o
    objeto retornado possui o metodo predict (comportamento esperado
    de um Pipeline do scikit-learn).
    """
    model = load_model()
    assert hasattr(model, 'predict')
    assert hasattr(model, 'predict_proba')


def test_predict_churn_retorna_colunas_esperadas():
    """
    Garante que predict_churn adiciona as colunas de predicao e que a
    probabilidade esta sempre entre 0 e 1.
    """
    model = load_model()

    df = pd.read_csv('data/raw/telco_churn.csv').head(3)
    result = predict_churn(model, df)

    assert 'churn_prediction' in result.columns
    assert 'churn_probability' in result.columns
    assert result['churn_prediction'].isin([0, 1]).all()
    assert (result['churn_probability'] >= 0).all()
    assert (result['churn_probability'] <= 1).all()
