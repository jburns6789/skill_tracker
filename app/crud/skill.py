#all restful routes validation is built in with pydantic

#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Skill, User
from app.schemas.skill import SkillCreate, SkillUpdate, SkillDelete, SkillOut
from typing import List
from fastapi import HTTPException
from app.auth.dependencies import get_current_user


async def get_all_skills(db:AsyncSession, current_user: User) -> List[Skill]:
    result = await db.execute(
        select(Skill).where(Skill.user_id == current_user.id)
    )
    skills = result.scalars().all()
    return skills


async def create_skill(db: AsyncSession, skill: SkillCreate, current_user: User):
    db_skill = Skill(
        name=skill.name,
        category_id=skill.category_id,
        user_id=current_user.id
    )

    db.add(db_skill)
    await db.commit()
    await db.refresh(db_skill)
    return db_skill


async def update_skill_name(db: AsyncSession, skill_id: int, skill_data: SkillUpdate, current_user: User):
    result = await db.execute(
        select(Skill).where(
            Skill.id == skill_id,
            Skill.user_id == current_user.id
        )
    )

    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill.name = skill_data.name
    await db.commit()
    await db.refresh(skill)
    return SkillOut(**skill.__dict__)
    

async def delete_skill(db:AsyncSession, skill_id: int, current_user: User):
    result = await db.execute(
        select(Skill).where(
            Skill.id == skill_id,
            Skill.user_id == current_user.id
        )
    )
    skill = result.scalar_one_or_none()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found or not owned by user")
    
    await db.delete(skill)
    await db.commit()
    return {"message": f"Skill with id {skill_id} deleted"}

