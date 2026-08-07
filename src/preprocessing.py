"""
Funções de pré-processamento e limpeza de dados para o pipeline de churn.
"""
import pandas as pd


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige a coluna TotalCharges, que chega como string devido a valores
    em branco para clientes com tenure=0 (clientes novos, sem cobrança
    acumulada ainda).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo a coluna 'TotalCharges'.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame com 'TotalCharges' convertida para float,
        com valores ausentes preenchidos com 0.
    """
    df = df.copy()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    return df


def preprocess_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as etapas de limpeza necessárias nos dados brutos,
    antes de alimentar o pipeline de modelo (pré-processamento +
    classificador).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto, no formato original do dataset Telco Churn.

    Returns
    -------
    pd.DataFrame
        DataFrame limpo, pronto para ser usado como entrada do pipeline
        de modelo (sem customerID, com TotalCharges numérico).
    """
    df = df.copy()

    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    df = clean_total_charges(df)

    return df
