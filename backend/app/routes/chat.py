"""
Rotas de chat (sessões e mensagens)
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.chat import ChatSession, Message
from app.schemas.chat import ChatSessionCreate, ChatSessionResponse, MessageCreate, MessageResponse
from app.services.document_service import DocumentService
from app.services.rag_service import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


def _get_owned_session(db: Session, user_id: int, session_id: int) -> ChatSession:
    """Busca uma sessão de chat garantindo que pertence ao usuário autenticado."""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == user_id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão não encontrada")
    return session


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    data: ChatSessionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cria uma nova sessão de chat associada a um documento já processado"""
    document = DocumentService.get_owned(db, current_user["user_id"], data.document_id)
    if document.status != "ready":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O documento ainda está sendo processado ou falhou ao processar",
        )

    session = ChatSession(
        user_id=current_user["user_id"],
        document_id=document.id,
        title=data.title or document.filename,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista as sessões de chat do usuário autenticado, mais recentes primeiro"""
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user["user_id"])
        .order_by(ChatSession.created_at.desc())
        .all()
    )


@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def list_messages(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista o histórico de mensagens de uma sessão de chat"""
    _get_owned_session(db, current_user["user_id"], session_id)
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
def send_message(
    session_id: int,
    data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Envia uma pergunta na sessão de chat.

    Busca os trechos mais relevantes do documento associado e responde
    usando a API da Claude, com a resposta baseada apenas nesse contexto.
    """
    session = _get_owned_session(db, current_user["user_id"], session_id)

    previous_messages = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in previous_messages]

    user_message = Message(session_id=session.id, role="user", content=data.content)
    db.add(user_message)
    db.commit()

    try:
        answer, _chunks_used = answer_question(db, session.document_id, data.content, history)
    except Exception as exc:  # noqa: BLE001 - erro de rede/API externa vira 502, não 500
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao consultar a IA: {exc}",
        )

    assistant_message = Message(session_id=session.id, role="assistant", content=answer)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    return assistant_message
