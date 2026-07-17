"""
Rotas de autenticação (cadastro e login)
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import create_access_token, get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para cadastro de novo usuário

    - **username**: Nome de usuário único (3-50 caracteres)
    - **email**: Email único e válido
    - **password**: Senha com no mínimo 6 caracteres
    - **full_name**: Nome completo (opcional)
    """
    user = UserService.create_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint para login de usuário

    Retorna um token JWT que deve ser usado em requisições autenticadas
    """
    user = UserService.authenticate_user(db, user_data)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obter informações do usuário autenticado
    """
    user = UserService.get_user_by_id(db, current_user["user_id"])
    return user
