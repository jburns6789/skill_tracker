#auth related pydantic schemas

from pydantic import BaseModel

class RegisterInput(BaseModel):
    username: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

