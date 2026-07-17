"""
Rotas para CRUD de notas
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.core.security import get_current_user
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova nota
    
    - **title**: Título da nota (obrigatório, 1-200 caracteres)
    - **content**: Conteúdo da nota (opcional)
    """
    note = NoteService.create_note(db, note_data, current_user["user_id"])
    return note

@router.get("/", response_model=List[NoteResponse])
def list_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as notas do usuário autenticado
    
    - **skip**: Número de registros a pular (paginação)
    - **limit**: Máximo de registros a retornar (máximo 100)
    """
    notes = NoteService.get_user_notes(db, current_user["user_id"], skip, limit)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém uma nota específica
    
    - **note_id**: ID da nota
    """
    note = NoteService.get_note(db, note_id, current_user["user_id"])
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza uma nota existente
    
    - **note_id**: ID da nota
    - **title**: Novo título (opcional)
    - **content**: Novo conteúdo (opcional)
    """
    note = NoteService.update_note(db, note_id, note_data, current_user["user_id"])
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta uma nota
    
    - **note_id**: ID da nota
    """
    NoteService.delete_note(db, note_id, current_user["user_id"])
    return None
