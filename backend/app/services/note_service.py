"""
Serviço de negócio para notas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

class NoteService:
    """Serviço para operações de notas"""
    
    @staticmethod
    def create_note(db: Session, note_data: NoteCreate, user_id: int) -> Note:
        """Cria uma nova nota"""
        db_note = Note(
            title=note_data.title,
            content=note_data.content,
            user_id=user_id
        )
        
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    
    @staticmethod
    def get_note(db: Session, note_id: int, user_id: int) -> Note:
        """Obtém uma nota específica do usuário"""
        note = db.query(Note).filter(
            (Note.id == note_id) & (Note.user_id == user_id)
        ).first()
        
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota não encontrada"
            )
        
        return note
    
    @staticmethod
    def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list:
        """Obtém todas as notas do usuário"""
        return db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_note(db: Session, note_id: int, note_data: NoteUpdate, user_id: int) -> Note:
        """Atualiza uma nota"""
        note = NoteService.get_note(db, note_id, user_id)
        
        if note_data.title is not None:
            note.title = note_data.title
        if note_data.content is not None:
            note.content = note_data.content
        
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def delete_note(db: Session, note_id: int, user_id: int) -> bool:
        """Deleta uma nota"""
        note = NoteService.get_note(db, note_id, user_id)
        
        db.delete(note)
        db.commit()
        return True
