from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db import get_db
from src.controllers.user_controller import create_user, authenticate_user

router = APIRouter()

@router.post("/users")
def register_user(user: dict, db: Session = Depends(get_db)):
    return create_user(db, user["email"], user["username"], user["password"])

@router.post("/users/login")
def login_user(user: dict, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user["email"], user["password"])
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login success"}