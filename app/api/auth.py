#Only includes route handlers, handles request/response logic not internal auth mechanics
#Add rate limiting at some point

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import User
from app.auth.jwt import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterInput, LoginInput
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_csrf_protect import CsrfProtect

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.extension import Limiter
from fastapi import Request
from app.utils.rate_limiter import limiter

router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, data: RegisterInput):
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
@limiter.limit("10/minute")
def login(request: Request, 
          form_data: OAuth2PasswordRequestForm = Depends(),
          csrf_protect: CsrfProtect = Depends()
):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    
    finally:
        db.close()