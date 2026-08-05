"""
Ponto de entrada para rodar o servidor de desenvolvimento.

A aplicação FastAPI em si vive em `app/main.py` (é o que o Uvicorn importa
como "app.main:app"); este arquivo só existe para permitir `python main.py`
a partir da pasta `backend/`, com auto-reload ligado.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
