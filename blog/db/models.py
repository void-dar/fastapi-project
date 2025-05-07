from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey, text
from pydantic import EmailStr
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import List 


class UserDB(SQLModel, table=True):
    __tablename__ = "users"
    uid: UUID = Field(default_factory=uuid4, sa_column=Column(pg.UUID, primary_key=True))
    username: str = Field(sa_column=Column(pg.VARCHAR(30), unique=True, nullable=False))
    email: EmailStr = Field(sa_column=Column(pg.VARCHAR(60), unique=True, nullable=False))
    hashpassword: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False), exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP")))
    last_seen: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP")))
    postdb: List["PostDB"] = Relationship(back_populates="userdb")

class PostDB(SQLModel, table=True):
    __tablename__= "posts"
    uid : UUID = Field(sa_column=Column(pg.UUID, ForeignKey("users.uid"), nullable=False))
    post_id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, index=True))
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    content: str = Field(sa_column=Column(pg.VARCHAR(3000), nullable=False))
    userdb : 'UserDB' = Relationship(back_populates="postdb")
    posted_at : datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))