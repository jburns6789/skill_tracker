#auth related pydantic schemas

from pydantic import BaseModel, constr, Field, field_validator
from typing import Annotated

class RegisterInput(BaseModel):
    username: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: Annotated[
        str, 
        Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"),
        constr(min_length=5, max_length=50)
    ]
    password: Annotated[
        str, 
        Field(..., min_length=8, max_length=50),
        constr(pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).*$")  
    ]

