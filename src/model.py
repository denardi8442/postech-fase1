"""
Funções para carregar o modelo treinado e gerar predições de churn.
"""
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from src.config import MODEL_PATH
from src.preprocessing import preprocess_raw_data


def load_model() -> Pipeline:
    """
    Carrega o pipeline treinado (pré-processamento + classificador) a
    partir do arquivo .joblib definido em MODEL_PATH.

    Returns
    -------
    Pipeline
        Pipeline scikit-learn pronto para uso (.predict / .predict_proba).

    Raises
    ------
    FileNotFoundError
        Se o arquivo do modelo não existir no caminho esperado.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo nao encontrado em {MODEL_PATH}. "
            "Execute o notebook de treinamento antes de usar a API."
        )
    return joblib.load(MODEL_PATH)


def predict_churn(model: Pipeline, df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera predições de churn para um conjunto de clientes.

    Parameters
    ----------
    model : Pipeline
        Pipeline treinado (carregado via load_model()).
    df : pd.DataFrame
        DataFrame com os dados brutos dos clientes (mesmo formato do
        dataset original, sem a coluna Churn).

    Returns
    -------
    pd.DataFrame
        DataFrame original com duas colunas adicionais:
        'churn_prediction' (0 ou 1) e 'churn_probability' (0.0 a 1.0).
    """
    df_clean = preprocess_raw_data(df)

    predictions = model.predict(df_clean)
    probabilities = model.predict_proba(df_clean)[:, 1]

    result = df.copy()
    result['churn_prediction'] = predictions
    result['churn_probability'] = probabilities

    return result
