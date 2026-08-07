"""
Configurações centrais do projeto: caminhos e constantes.
"""
from pathlib import Path

# Raiz do projeto: sobe 2 níveis a partir deste arquivo (src/config.py -> src/ -> raiz/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Caminho do modelo treinado (pipeline completo: pré-processamento + classificador)
MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.joblib"

# Caminho do dataset bruto (útil para scripts de retraining futuros)
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "telco_churn.csv"
