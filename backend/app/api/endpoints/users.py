from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.phone_number == user_in.phone_number).first()
    if user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
