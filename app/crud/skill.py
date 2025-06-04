#all restful routes validation is built in with pydantic

from sqlalchemy.orm import Session
from app.models.models import Skill, User
from app.schemas.skill import SkillCreate, SkillUpdate, SkillDelete, SkillOut
from typing import List
from fastapi import HTTPException
from app.auth.dependencies import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession


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

# def create_skill(db: Session, skill: SkillCreate, current_user: User):
#     db_skill = Skill(
#         **skill.model_dump())
#     db.add(db_skill)
#     db.commit()
#     db.refresh(db_skill)
#     return db_skill


async def update_skill_name(db: AsyncSession, skill_id: int, skill_data: SkillUpdate, current_user: User):
    skill = await db.get(Skill, skill_id)
    if not skill or skill.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill.name = skill_data.name
    await db.commit()
    await db.refresh(skill)
    return SkillOut(**skill.__dict__)
    

async def delete_skill(db:AsyncSession, skill_id: int, current_user: User):
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user.id
        
    ).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found or not owned by user")
    
    db.delete(skill)
    db.commit()
    return {"message": f"Skill with id {skill_id} deleted"}

async def get_all_skills(db:AsyncSession) -> List[Skill]:
    return db.query(Skill).all()