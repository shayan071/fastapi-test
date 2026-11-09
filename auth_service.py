
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token)


# REGISTER USER
def register_user(user_data, db: Session):

    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise

    return new_user


# LOGIN USER
def login_user(email: str, password: str, db: Session):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(
        password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="Account is disabled"
        )

    access_token = create_access_token(
        user.id,
        user.role
    )

    refresh_token = create_refresh_token(
        user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# REFRESH TOKEN
def refresh_user_token(refresh_token: str, db: Session):

    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user or not user.is_active:

        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    return {
        "access_token": create_access_token(
            user.id,
            user.role
        ),

        "refresh_token": create_refresh_token(
            user.id
        ),

        "token_type": "bearer"
    }