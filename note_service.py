
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Note, User

from security import (
    encrypt_content,
    decrypt_content
)


# CREATE NOTEe
def create_note(note_data, user: User, db: Session):

    new_note = Note(
        title=note_data.title,

        content=encrypt_content(
            note_data.content
        ),

        owner_id=user.id
    )

    try:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)

    except Exception:

        db.rollback()
        raise

    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": decrypt_content(new_note.content),
        "owner_id": new_note.owner_id
    }


# GET ALL USER NOTES
def get_notes(user: User, db: Session):

    notes = db.query(Note).filter(
        Note.owner_id == user.id
    ).all()

    return [
        {
            "id": note.id,
            "title": note.title,
            "content": decrypt_content(note.content),
            "owner_id": note.owner_id
        }
        for note in notes
    ]


# GET SINGLE NOTE

def get_note(note_id: int, user: User, db: Session):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {
        "id": note.id,
        "title": note.title,
        "content": decrypt_content(note.content),
        "owner_id": note.owner_id
    }


# UPDATE NOTE

def update_note(
    note_id: int,
    note_data,
    user: User,
    db: Session
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if note_data.title is not None:

        note.title = note_data.title

    if note_data.content is not None:

        note.content = encrypt_content(
            note_data.content
        )

    try:

        db.commit()

        db.refresh(note)

    except Exception:

        db.rollback()
        raise

    return {
        "id": note.id,
        "title": note.title,
        "content": decrypt_content(note.content),
        "owner_id": note.owner_id
    }


# DELETE NOTE

def delete_note(note_id: int, user: User, db: Session):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)

    db.commit()

    return {
        "message": "Note deleted successfully"
    }