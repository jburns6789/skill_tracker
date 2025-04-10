#pydantic data validation library, validate input shape / output, serialization of python objects
#deserialization converts JSON into Python objects
#ensures requests have valid values for defined fields

from typing import Optional
from pydantic import BaseModel, ConfigDict 


class SkillCreate(BaseModel):
    name: str
    category_id: int
    user_id: int

class SkillOut(SkillCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SkillUpdate(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SkillDelete(BaseModel):
    pass

