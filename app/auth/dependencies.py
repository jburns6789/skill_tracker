#fastapi dependency functions for extracting user from JWT

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi_csrf_protect import CsrfProtect
from pydantic_settings import BaseSettings

from jose import JWTError, jwt

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


from app.database import AsyncSessionLocal
from app.models.models import User
from app.auth.jwt import SECRET_KEY, ALGORITHM


class CsrfSettings(BaseSettings):
    secret_key: str = "secret-key"
    cookie_samesite: str = 'lax'

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
                           ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        
        user_id = int(user_id_str)
    except(JWTError, ValueError):
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return user
    
