"""
Configurações da aplicação, carregadas de variáveis de ambiente (.env)

Todos os campos têm um valor padrão sensato para desenvolvimento, então a
aplicação sobe mesmo sem um arquivo `.env` presente. Para produção, sempre
defina SECRET_KEY (e o resto que fizer sentido) via `.env` ou variáveis de
ambiente reais — veja `.env.example`.
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

    # API
    API_TITLE: str = "Sistema de Cadastro e Funcionalidades"
    API_DESCRIPTION: str = "API com autenticação JWT e funcionalidades integradas"
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
