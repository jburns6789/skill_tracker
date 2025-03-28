from pydantic import BaseModel, ConfigDict

class SkillCreate(BaseModel):
    name: str
    category_id: int
    user_id: int

class SkillOut(SkillCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SkillUpdate(BaseModel):
    pass

class SkillDelete(BaseModel):
    pass

