from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.skill import SkillCreate, SkillOut
from app.crud.skill import create_skill, get_all_skills, delete_skill

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message": "SkillTree API is working!"}

@router.post("/skills", response_model=SkillOut)
def add_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    return create_skill(db, skill)

@router.get("/skills", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return get_all_skills(db)

@router.delete("/skills/{skill_id}")
def remove_skill(
    skill_id: int = Path(..., title="ID of skill to delete"),
    db: Session = Depends(get_db)
):
    return delete_skill(db, skill_id)