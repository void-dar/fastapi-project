from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union
from e_comm.db.models import Role
from datetime import datetime
from uuid import UUID


class CreateUser(BaseModel):
    username: str = Field(min_length=2,max_length=50)
    email: EmailStr = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    role: Optional[Role] = Role.USER.value

class LogIn(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=30)

class UserOut(BaseModel):
    uid: Union[UUID, str]
    username: str
    role: Role
    is_verified: bool
    created_at: Union[datetime, int]
  
   
class LoginResponse(BaseModel):
    message: str
    user: UserOut

class Verify(BaseModel):
    verified: bool
    username: str
 
 