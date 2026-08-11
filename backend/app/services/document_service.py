"""
Serviço de processamento de documentos: extração de texto, chunking e
geração de embeddings.
"""
import os
from typing import List

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document, DocumentChunk
from app.services.embedding_service import embed_texts, serialize_embedding

ALLOWED_CONTENT_TYPES = {"application/pdf", "text/plain", "text/markdown"}


def _extract_text(file_path: str, content_type: str) -> str:
    """Extrai o texto de um arquivo PDF ou texto plano."""
    if content_type == "application/pdf" or file_path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Quebra o texto em pedaços de tamanho fixo, com sobreposição entre eles
    (a sobreposição evita perder contexto que ficaria cortado bem no meio)."""
    text = " ".join(text.split())  # normaliza espaços em branco
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap if end - overlap > start else end
    return chunks


class DocumentService:
    """Serviço para upload e processamento de documentos"""

    @staticmethod
    def save_and_process(db: Session, user_id: int, file: UploadFile) -> Document:
        """Salva o arquivo enviado, extrai o texto, quebra em chunks e gera
        os embeddings. Se algo falhar no processamento, o documento fica
        salvo com status "error" em vez de sumir silenciosamente."""
        if file.content_type not in ALLOWED_CONTENT_TYPES and not (file.filename or "").lower().endswith(
            (".pdf", ".txt", ".md")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato não suportado. Envie um PDF, .txt ou .md.",
            )

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        document = Document(
            user_id=user_id,
            filename=file.filename or "documento",
            content_type=file.content_type or "application/octet-stream",
            status="processing",
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        contents = file.file.read()
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(contents) > max_bytes:
            db.delete(document)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo maior que {settings.MAX_UPLOAD_SIZE_MB}MB",
            )

        file_path = os.path.join(settings.UPLOAD_DIR, f"{document.id}_{document.filename}")
        with open(file_path, "wb") as f:
            f.write(contents)

        try:
            text = _extract_text(file_path, document.content_type)
            chunks_text = _chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

            if not chunks_text:
                raise ValueError("Não foi possível extrair texto do documento")

            embeddings = embed_texts(chunks_text)

            for index, (chunk_text, vector) in enumerate(zip(chunks_text, embeddings)):
                db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=chunk_text,
                        embedding=serialize_embedding(vector),
                    )
                )

            document.status = "ready"
            document.chunk_count = len(chunks_text)
        except Exception as exc:  # noqa: BLE001 - queremos capturar qualquer falha de processamento
            document.status = "error"
            document.error_message = str(exc)[:500]

        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def list_for_user(db: Session, user_id: int) -> List[Document]:
        """Lista os documentos do usuário, mais recentes primeiro."""
        return (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.created_at.desc())
            .all()
        )

    @staticmethod
    def get_owned(db: Session, user_id: int, document_id: int) -> Document:
        """Busca um documento garantindo que pertence ao usuário autenticado."""
        document = (
            db.query(Document)
            .filter(Document.id == document_id, Document.user_id == user_id)
            .first()
        )
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado")
        return document

    @staticmethod
    def delete(db: Session, user_id: int, document_id: int) -> None:
        """Remove um documento (e seus chunks/sessões, via cascade) e o arquivo em disco."""
        document = DocumentService.get_owned(db, user_id, document_id)
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document.id}_{document.filename}")
        if os.path.exists(file_path):
            os.remove(file_path)
        db.delete(document)
        db.commit()
