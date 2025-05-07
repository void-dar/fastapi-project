from pydantic import BaseModel, EmailStr
from typing import Optional


class AnonRegModel(BaseModel):
    name: Optional[str] = "User"
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class RegisterModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_no: str


class LogModel(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_no: Optional[str] = None
    password: str



class UserModel(BaseModel):
    email: str
    phone_no: int
    created_at: str
    last_seen: str


class UserResponse(BaseModel):
    username: str
    email: str
    phone_no: int
