#pydantic data validation library, validate input shape / output, serialization of python objects
#deserialization converts JSON into Python objects
#ensures requests have valid values for defined fields

from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, constr, Field, field_validator
 

class SkillCreate(BaseModel):
    name: Annotated[
        str,
        Field(...,min_length=8, max_length=50),
        constr(pattern=r"^[a-zA-Z0-9\-_]+$")
    ]
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if "script" in v.lower():
            raise ValueError("Invalid skill name")
        return v

class SkillOut(SkillCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SkillUpdate(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SkillDelete(BaseModel):
    pass

