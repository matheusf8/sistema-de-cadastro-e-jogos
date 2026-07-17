"""
Schemas de validação para usuários
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuário"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str

class UserResponse(UserBase):
    """Schema para resposta de usuário"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    """Schema para dados do token"""
    user_id: Optional[int] = None
