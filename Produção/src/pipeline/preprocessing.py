import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class TelemetryPreprocessor:
    """
    Classe responsável pela limpeza e normalização dos dados de telemetria da Vale.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def remove_nulls_and_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove dados corrompidos ou redundantes (vetorizado)."""
        logger.info(f"Shape inicial: {df.shape}")
        
        # Remove duplicatas exatas de telemetria
        df_clean = df.drop_duplicates()
        
        # Preenche valores nulos com mediana para não perder a linha
        # Apenas colunas numéricas
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
        
        logger.info(f"Shape após limpeza: {df_clean.shape}")
        return df_clean
        
    def normalize_signals(self, df: pd.DataFrame, is_training: bool = False) -> pd.DataFrame:
        """Aplica Z-Score nos dados de sensores."""
        features_to_scale = [col for col in df.columns if col not in ['timestamp', 'equipamento_id', 'status']]
        
        df_scaled = df.copy()
        
        if is_training:
            df_scaled[features_to_scale] = self.scaler.fit_transform(df[features_to_scale])
            self.is_fitted = True
            logger.info("Scaler ajustado para a base de treino.")
        else:
            if not self.is_fitted:
                logger.warning("Scaler não foi fitado! Inferência pode ter escala incorreta.")
            df_scaled[features_to_scale] = self.scaler.transform(df[features_to_scale])
            
        return df_scaled
