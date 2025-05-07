from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"  
    
    uid: UUID = Field(default_factory=uuid4, sa_column=Column(pg.UUID, primary_key=True, nullable=False, unique=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    
   
    to_dos: list["To_dos"] = Relationship(back_populates="user")

class To_dos(SQLModel, table=True):
    __tablename__ = "to_dos" 
    
    id: int = Field(default=None, sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True)) 
    title: str = Field(sa_column=Column(pg.VARCHAR(200), nullable=False))
    description: str = Field(sa_column=Column(pg.VARCHAR(1000), nullable=False))
    uid: UUID = Field(sa_column=Column(pg.UUID, ForeignKey("users.uid"), nullable=False)) 
    
    
    user: "User" = Relationship(back_populates="to_dos")
