#Only includes route handlers, handles request/response logic not internal auth mechanics
#Add rate limiting at some point

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import User
from app.auth.jwt import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterInput, LoginInput

router = APIRouter()

@router.post("/register")
def register(data: RegisterInput):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return{"message": "User created successfully"}
    
    finally:
        db.close()

@router.post("/login")
def login(data: LoginInput):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    
    finally:
        db.close()