"""
Schemas de validação para documentos
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Schema de resposta de um documento"""
    id: int
    filename: str
    status: str
    error_message: Optional[str] = None
    chunk_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
