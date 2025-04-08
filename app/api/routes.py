#endpoint logic

from typing import List
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.skill import SkillCreate, SkillOut, SkillUpdate
from app.crud.skill import create_skill, get_all_skills, update_skill_name, delete_skill
from pydantic import BaseModel

from app.auth.dependencies import get_current_user
from app.models.models import User

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

@router.get("/whoami")
def read_skills(current_user: User = Depends(get_current_user)):
    return{"message": f"User {current_user.username} is authorized"}

@router.post("/skills", response_model=SkillOut)
def add_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    return create_skill(db, skill)

@router.get("/skills", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return get_all_skills(db)

@router.put("/skills/{skill_id}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db)
):
    return update_skill_name(db, skill_id, skill_data)

@router.delete("/skills/{skill_id}")
def remove_skill(
    skill_id: int = Path(..., title="ID of skill to delete"),
    db: Session = Depends(get_db)
):
    return delete_skill(db, skill_id)

