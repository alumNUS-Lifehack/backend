from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    linkedin: str
    headline: str
    gradyear: int
    course: str
    is_mentor: bool

class User(BaseModel):
    uid: str
    name: str
    linkedin: str
    headline: str
    gradyear: int
    course: str
    is_mentor: bool
