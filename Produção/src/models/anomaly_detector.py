import os
import joblib
import logging
from sklearn.cluster import KMeans
import pandas as pd

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Motor de detecção de anomalias baseado em K-Means.
    Identifica comportamentos fora do padrão no sinal dos sensores.
    """
    
    def __init__(self, n_clusters: int = 5):
        # 5 foi escolhido porque historicamente representam (Desligado, Ocioso, Operação Normal, Sobrecarga leve, Sobrecarga Crítica)
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
        self.model_path = os.getenv("MODEL_PATH", "models/kmeans_model.joblib")
        self.is_trained = False
        
    def train(self, df: pd.DataFrame):
        """Treina o modelo com dados históricos limpos e normalizados."""
        logger.info(f"Iniciando treinamento K-Means com {len(df)} amostras.")
        features = df.select_dtypes(include=['float64', 'int64'])
        
        self.model.fit(features)
        self.is_trained = True
        
        # Salva o modelo
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Modelo treinado e salvo em: {self.model_path}")
        
    def load_model(self):
        """Carrega modelo pré-treinado do disco."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            logger.info("Modelo carregado da memória com sucesso.")
        else:
            logger.warning("Modelo não encontrado no disco. É necessário treinar primeiro.")
            
    def predict(self, df: pd.DataFrame) -> list:
        """Classifica os dados e identifica distâncias ao centro (anomalias)."""
        if not self.is_trained:
            raise ValueError("O modelo precisa ser treinado ou carregado antes.")
            
        features = df.select_dtypes(include=['float64', 'int64'])
        clusters = self.model.predict(features)
        
        # Transforma o cluster em probabilidade fictícia de falha por enquanto
        # Na versão 2, mediremos a distância Euclidiana até o centróide
        severities = ["Baixa", "Media", "Alta"]
        anomalies = []
        
        for c in clusters:
             # Cluster 4 será sempre considerado a zona de "anomalia máxima" no nosso mock inicial
             if c == 4:
                 anomalies.append({"alarme": True, "severidade": "Alta", "acao": "Parada Imediata Necessária"})
             elif c == 3:
                 anomalies.append({"alarme": True, "severidade": "Media", "acao": "Agendar inspeção em 48h"})
             else:
                 anomalies.append({"alarme": False, "severidade": "Baixa", "acao": "Normal"})
                 
        return anomalies

if __name__ == "__main__":
    print("Este arquivo deve ser importado como um módulo.")
