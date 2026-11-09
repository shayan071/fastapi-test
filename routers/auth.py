from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas import (
    UserCreate, UserLogin, UserResponse, Token, RefreshRequest)

import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#register
@router.post("/register",response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    #will call register_user in auth_service file to register user
    return auth_service.register_user(user_data,db)

#login
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    return auth_service.login_user(user_data.email, user_data.password, db)

# REFRESH TOKEN
@router.post("/refresh", response_model=Token)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):

    return auth_service.refresh_user_token(request.refresh_token,db)