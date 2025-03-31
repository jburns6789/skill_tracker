from sqlalchemy.orm import Session
from app.models.models import Skill
from app.schemas.skill import SkillCreate, SkillUpdate, SkillDelete, SkillOut
from typing import List
from fastapi import HTTPException

def create_skill(db: Session, skill: SkillCreate):
    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def update_skill_name(db:Session, skill_id:int, skill_data: SkillUpdate):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if skill_data.name is not None:
        skill.name = skill_data.name

    db.commit()
    db.refresh(skill)
    return skill
    

def delete_skill(db:Session, skill_id: int):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"message": f"Skill with id {skill_id} deleted"}

def get_all_skills(db:Session) -> List[Skill]:
    return db.query(Skill).all()