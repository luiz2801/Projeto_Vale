import pandas as pd
import logging
from typing import Optional

# Configurando logger básico
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_telemetry_data(filepath: str, encoding: str = 'utf-8-sig') -> Optional[pd.DataFrame]:
    """
    Carrega o arquivo CSV de telemetria com segurança, tratando encodes do Brasil.
    
    Args:
        filepath (str): Caminho do arquivo a ser lido.
        encoding (str): Encoding para leitura (ex: latin-1, utf-8-sig).
        
    Returns:
        pd.DataFrame ou None caso haja falha.
    """
    try:
        logger.info(f"Iniciando carregamento do arquivo: {filepath}")
        df = pd.read_csv(filepath, encoding=encoding)
        if df.empty:
            logger.warning("O arquivo gerou um DataFrame vazio.")
            return None
            
        logger.info(f"Arquivo carregado com sucesso. Instâncias: {len(df)}")
        return df
        
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        logger.error(f"Erro imprevisto ao carregar o arquivo: {str(e)}")
        return None
