"""
Testes unitários para as funções de pré-processamento.
"""
import pandas as pd
from src.preprocessing import clean_total_charges, preprocess_raw_data


def test_clean_total_charges_converte_espacos_em_branco_para_zero():
    """
    Garante que valores em branco (' ') em TotalCharges - comuns em
    clientes com tenure=0 - sao convertidos corretamente para 0.0,
    e que a coluna passa a ser numerica (float).
    """
    df = pd.DataFrame({
        'tenure': [0, 5, 12],
        'TotalCharges': [' ', '350.5', '840.0']
    })

    df_clean = clean_total_charges(df)

    assert df_clean['TotalCharges'].dtype == 'float64'
    assert df_clean.loc[0, 'TotalCharges'] == 0.0
    assert df_clean.loc[1, 'TotalCharges'] == 350.5


def test_preprocess_raw_data_remove_customer_id():
    """
    Garante que a coluna customerID (identificador, nao preditivo) e
    removida apos o pre-processamento.
    """
    df = pd.DataFrame({
        'customerID': ['1234-ABCD', '5678-EFGH'],
        'tenure': [10, 20],
        'TotalCharges': ['100.0', '200.0']
    })

    df_clean = preprocess_raw_data(df)

    assert 'customerID' not in df_clean.columns
