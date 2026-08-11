"""
Schemas de validação para chat (sessões e mensagens)
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatSessionCreate(BaseModel):
    """Schema para criar uma nova sessão de chat"""
    document_id: int
    title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    """Schema de resposta de uma sessão de chat"""
    id: int
    document_id: int
    title: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    """Schema para enviar uma mensagem na sessão"""
    content: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    """Schema de resposta de uma mensagem"""
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
