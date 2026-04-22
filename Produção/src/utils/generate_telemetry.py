import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_mock_telemetry():
    """Gera um arquivo CSV falso com comportamento normal e algumas anomalias injetadas."""
    print("Gerando dados falsos de telemetria da Vale...")
    
    np.random.seed(42)
    rows = 1000
    
    timestamps = [datetime.now() - timedelta(minutes=i*5) for i in range(rows)]
    
    # Comportamento Base (Normal)
    temp = np.random.normal(90, 5, rows)
    pressao = np.random.normal(40, 2, rows)
    vibra = np.random.normal(1.2, 0.1, rows)
    
    # Injetando 50 anomalias no final para teste
    temp[-50:] = np.random.normal(120, 10, 50) # Superaquecimento
    vibra[-50:] = np.random.normal(3.5, 0.5, 50) # Eixo tremendo muito
    
    status = ['Normal'] * (rows - 50) + ['Falha_Iminente'] * 50
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'equipamento_id': ['CAT-793F'] * rows,
        'temperatura_motor': temp,
        'pressao_oleo': pressao,
        'vibracao_eixo': vibra,
        'status': status
    })
    
    os.makedirs('data', exist_ok=True)
    filepath = 'data/telemetria_mock.csv'
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"Arquivo gerado salvo em {filepath} com {rows} registros.")
    
if __name__ == '__main__':
    create_mock_telemetry()
