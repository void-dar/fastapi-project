from sqlmodel import SQLModel, Field, Column, ForeignKey, text, Relationship, Enum as SQLEnum
import sqlalchemy.dialects.postgresql as pg
from pydantic import EmailStr
from uuid import uuid4, UUID
from typing import List, Annotated
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    WORKER= "worker"
    USER= "user"

class UsersDB(SQLModel, table= True):
    __tablename__= "usersdb"
    uid: UUID = Field(default_factory=uuid4, sa_column=Column(pg.UUID, nullable=False, primary_key=True))
    username: str = Field(sa_column=Column(pg.VARCHAR(50), unique=True, nullable=False))
    email: EmailStr = Field(sa_column=Column(pg.VARCHAR(60), unique=True, nullable=False))
    hashpassword: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False), exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP")))
    is_verified: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    role : Role = Field(sa_column=Column(SQLEnum(Role), nullable=False, default=Role.USER.value))
    reviews: List["Reviews"] = Relationship(back_populates="usersdb")


class Products(SQLModel, table= True):
    __tablename__= "products"
    prod_uid: UUID = Field(default_factory=uuid4, sa_column=Column(pg.UUID, nullable=False, primary_key=True))
    prod_image:str =  Field(sa_column=Column(pg.VARCHAR(1000), nullable=False))
    prod_name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    description: str = Field(sa_column=Column(pg.VARCHAR(10000), nullable=False))
    inventory: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    uploaded_by: str = Field(sa_column=Column(pg.VARCHAR(50), ForeignKey("usersdb.username"), nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP")))
    reviews: List["Reviews"] = Relationship(back_populates="products")
    completed: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))

class Reviews(SQLModel, table=True):
    __tablename__= "reviews"
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement="auto"))
    content: str
    rating: Annotated[int, Field(min_length=1, max_length=1, gt=0, le=5)] = Field(sa_column=Column(pg.INTEGER, nullable=True)) # Only allows values from 1 to 5

    user_uid: int = Field(sa_column=Column(pg.UUID, ForeignKey("usersdb.uid"), nullable=False))
    prod_uid: int = Field(sa_column=Column(pg.UUID, ForeignKey("products.prod_uid"), nullable=False))

    usersdb: UsersDB = Relationship(back_populates="reviews")
    products: Products = Relationship(back_populates="reviews")