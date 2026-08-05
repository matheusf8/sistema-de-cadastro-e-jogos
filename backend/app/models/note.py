"""
Modelo de nota
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.user import utcnow

class Note(Base):
    """Modelo de nota do banco de dados"""
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    
    # Relacionamento
    owner = relationship("User", back_populates="notes")
    
    def __repr__(self):
        return f"<Note {self.id} - {self.title}>"
