"""
Configurações da aplicação, carregadas de variáveis de ambiente (.env)

Todos os campos têm um valor padrão sensato para desenvolvimento, então a
aplicação sobe mesmo sem um arquivo `.env` presente. Para produção, sempre
defina SECRET_KEY e ANTHROPIC_API_KEY via `.env` ou variáveis de ambiente
reais — veja `.env.example`.
"""
import json
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Security - MUDE SECRET_KEY EM PRODUÇÃO
    SECRET_KEY: str = "dev-secret-key-troque-isso-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Claude API - obrigatório para o chat responder (sem isso, upload/lista
    # de documentos funciona normalmente, só o chat falha)
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-opus-5"

    # Documentos e RAG
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 20
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    TOP_K_CHUNKS: int = 5

    # API
    API_TITLE: str = "Chat com Documentos (RAG)"
    API_DESCRIPTION: str = "API com autenticação JWT e chat com documentos via IA (RAG + Claude)"
    API_VERSION: str = "1.0.0"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        """Aceita tanto JSON ('["a","b"]') quanto lista separada por vírgula ('a,b')"""
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("["):
                return json.loads(value)
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
