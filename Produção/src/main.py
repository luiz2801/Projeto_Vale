import uvicorn
from fastapi import FastAPI
from api.routes import router
import os

# Cria a instância FastAPI
app = FastAPI(
    title="API de Manutenção Preditiva - Vale",
    description="Backbone de processamento de telemetria e inferência de anomalias",
    version="1.0.0"
)

# Adiciona as rotas que configuramos com o Pydantic / AnomalyDetector
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    # Garante a porta a partir das variaveis de ambiente
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"Iniciando o servidor FastAPI em {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
