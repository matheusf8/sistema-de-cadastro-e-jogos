"""
Rotas de documentos (upload, listagem, remoção)
"""
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Envia um documento (PDF, .txt ou .md).

    O texto é extraído, quebrado em trechos e indexado com embeddings —
    tudo síncrono nesta requisição, então o upload leva alguns segundos
    dependendo do tamanho do arquivo.
    """
    return DocumentService.save_and_process(db, current_user["user_id"], file)


@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista os documentos enviados pelo usuário autenticado"""
    return DocumentService.list_for_user(db, current_user["user_id"])


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove um documento, seus trechos indexados e as sessões de chat associadas"""
    DocumentService.delete(db, current_user["user_id"], document_id)
