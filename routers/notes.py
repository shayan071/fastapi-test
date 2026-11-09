
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import (NoteCreate,NoteUpdate,NoteResponse)
from dependencies import get_current_user
import note_service


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


# CREATE NOTEe
@router.post("/", response_model=NoteResponse)
def create(note_data: NoteCreate,db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return note_service.create_note(
        note_data,
        user,
        db)


# GET ALL NOTES
@router.get("/", response_model=list[NoteResponse])
def get_all(db: Session = Depends(get_db),user: User = Depends(get_current_user)
):

    return note_service.get_notes(
        user,
        db)


# GET SINGLE NOTEe
@router.get("/{note_id}", response_model=NoteResponse)
def get_one(note_id: int,db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return note_service.get_note(
        note_id,
        user,
        db)


# UPDATE NOTE
@router.put("/{note_id}", response_model=NoteResponse)
def update(note_id: int,note_data: NoteUpdate,db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return note_service.update_note(
        note_id,
        note_data,
        user,
        db
    )


# DELETE NOTEe
@router.delete("/{note_id}")
def delete(note_id: int,db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return note_service.delete_note(
        note_id,
        user,
        db)