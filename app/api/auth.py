#Only includes route handlers, handles request/response logic not internal auth mechanics
#Add rate limiting at some point

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal
from app.models.models import User
from app.auth.jwt import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterInput, LoginInput
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_csrf_protect import CsrfProtect

from app.database import get_db
from app.models.models import User

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.extension import Limiter
from fastapi import Request
from app.utils.rate_limiter import limiter

router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")
async def register(
    request: Request, 
    data: RegisterInput,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()

        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return{"message": "User created successfully"}
    
    except IntegrityError as e:
        await db.rollback()
        if "ix_users_username" in str(e):
            raise HTTPException(status_code=400, detail="Username already in use")
        elif "ix_users_email" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=500, detail="Database error")
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request, 
    form_data: OAuth2PasswordRequestForm = Depends(),
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await db.execute(select(User).where(User.email == form_data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(stauts_code=500, detail=str(e))