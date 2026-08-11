"""
Modelos de documento e trecho (chunk) indexado
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.user import utcnow


class Document(Base):
    """Documento enviado pelo usuário para consulta via chat"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=True)
    status = Column(String(20), default="processing")  # processing | ready | error
    error_message = Column(String(500), nullable=True)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=utcnow)

    owner = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document {self.id} - {self.filename}>"


class DocumentChunk(Base):
    """Um trecho de texto do documento, com seu vetor de embedding"""
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)  # vetor serializado em JSON
    created_at = Column(DateTime, default=utcnow)

    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        return f"<DocumentChunk {self.id} of Document {self.document_id}>"
