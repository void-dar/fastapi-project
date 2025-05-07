from pydantic import BaseModel
from uuid import UUID

class Dos(BaseModel):
    title: str
    description: str
    uid: UUID


class UserModel(BaseModel):
    name: str

class Retrieve(BaseModel):
    
    uid: UUID
    title: str
    description: str

class Update(BaseModel):
    title: str
    description: str

class Verify(BaseModel):
    uid: UUID