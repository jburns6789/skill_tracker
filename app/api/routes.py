#endpoint logic

from typing import List
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal
from app.schemas.skill import SkillCreate, SkillOut, SkillUpdate
from app.crud.skill import create_skill, get_all_skills, update_skill_name, delete_skill
from pydantic import BaseModel

from app.auth.dependencies import get_current_user
from app.models.models import User, Skill
from fastapi import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@router.get("/")
async def root():
    return {"message": "SkillTree API is working!"}

@router.get("/whoami")
async def read_skills(current_user: User = Depends(get_current_user)):
    return{"message": f"User {current_user.username} is authorized"}

@router.post("/skills", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
async def add_skill(
    skill: SkillCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return await create_skill(db, skill, current_user)

@router.get("/skills", response_model=List[SkillOut])
async def list_skills(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Skill).where(Skill.user_id == current_user.id))
    return result.scalars().all()

@router.put("/skills/{skill_id}", response_model=SkillOut, status_code=201)
async def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_skill_name(db, skill_id, skill_data, current_user)

@router.delete("/skills/{skill_id}")
async def remove_skill(
    skill_id: int = Path(..., title="ID of skill to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_skill(db, skill_id, current_user)

