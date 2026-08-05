"""
Schemas de validação para notas
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    """Schema base para nota"""
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None

class NoteCreate(NoteBase):
    """Schema para criação de nota"""
    pass

class NoteUpdate(BaseModel):
    """Schema para atualização de nota"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None

class NoteResponse(NoteBase):
    """Schema para resposta de nota"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
