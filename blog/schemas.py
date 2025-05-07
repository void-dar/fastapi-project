from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Union
from datetime import datetime



class PostIn(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class UpdatePost(BaseModel):
    id : int
    title: str
    content: str

class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=30)

class UserOut(BaseModel):
    uid: Union[UUID, str]
    username: str
    email: EmailStr
    created_at: Union[datetime, str]
    last_seen: Union[datetime, str]

class LogIn(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=30)