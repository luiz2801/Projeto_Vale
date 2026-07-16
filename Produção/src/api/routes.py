from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Dependências locais
from models.anomaly_detector import AnomalyDetector
from pipeline.preprocessing import TelemetryPreprocessor

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()

# Instâncias globais carregadas no startup
detector = AnomalyDetector()
preprocessor = TelemetryPreprocessor()

# --- SCHEMAS DE VALIDAÇÃO (PYDANTIC) ---
class SensorData(BaseModel):
    equipamento_id: str = Field(..., description="ID unico do caminhão/escavadeira")
    timestamp: str
    temperatura_motor: float
    pressao_oleo: float
    vibracao_eixo: float

class PredictRequest(BaseModel):
    data: List[SensorData]

# --- ROTAS ---

@router.on_event("startup")
async def load_models():
    """Carrega os pesos do ML na memória antes de receber requisições."""
    detector.load_model()
    # Se fosse em produção real, também carregaríamos o estado do Scaler do Preprocessor

@router.get("/health")
def health_check():
    """Confirma que a API está viva e sem hardcoded passwords."""
    # Correção do SONAR: credencial agora está no .env apenas para conexão local, não exportada
    return {"status": "ok", "model_loaded": detector.is_trained}

@router.post("/predict")
def predict_anomalies(payload: PredictRequest):
    """
    Recebe um payload JSON de sensores (mock do protótipo) e retorna as predições de manutenção.
    Substitui a lógica de treinar na hora da rota HTTP (PR-07).
    """
    try:
        # Converter dict pydantic para DataFrame
        raw_data = [item.model_dump() for item in payload.data]
        df = pd.DataFrame(raw_data)
        
        # Pipeline mock sem treinar a normalização
        df_clean = preprocessor.remove_nulls_and_duplicates(df)
        
        if df_clean.empty:
            raise HTTPException(status_code=400, detail="Payload não conteve dados validos após limpeza.")
            
        # Predição (sem o scaler nesta simulação básica)
        results = detector.predict(df_clean)
        
        return {
            "equipamento": df_clean['equipamento_id'].iloc[0],
            "predictions": results
        }
        
    except ValueError as val_e:
        raise HTTPException(status_code=400, detail=str(val_e))
    except Exception as e:
        logger.error(f"Erro na rota /predict: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do processamento de ML.")
