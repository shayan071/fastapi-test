
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from dependencies import require_admin
from schemas import UserResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# GET ALL USERS
@router.get("/users",response_model=list[UserResponse])
def get_all_users(

    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return db.query(User).all()


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == admin.id:

        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account here"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }