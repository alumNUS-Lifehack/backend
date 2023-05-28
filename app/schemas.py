from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    uid: str
    name: str
    linkedin: str
    headline: str
    gradyear: int
    course: str
    is_mentor: bool

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

class Message(BaseModel):
    createdAt: datetime
    sentBy: str
    text: str