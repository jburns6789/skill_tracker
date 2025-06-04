from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
import os

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DATABASE_URL').split('://')[1]}"

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Add this async initialization function
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session



# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import declarative_base, sessionmaker
# from app.config import DATABASE_URL
# from sqlalchemy import create_engine
# from typing import AsyncGenerator

# Base = declarative_base()

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set")

# async_engine = create_async_engine(
#     DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))

# AsyncSessionLocal = async_sessionmaker(
#     bind=async_engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
#     autoflush=False,
#     autocommit=False
# )

# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     """Async dependency for database sessions"""
#     async with AsyncSessionLocal() as session:
#         yield session

# # For synchronous operations (if needed)
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=create_engine(DATABASE_URL)  # Regular sync engine
# )

# def init_db():
#     """Initialize sync database (for migrations/cli)"""
#     Base.metadata.create_all(bind=sync_engine)