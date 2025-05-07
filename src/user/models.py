from sqlmodel import SQLModel, Field, Column,Relationship, ForeignKey, text
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from uuid import UUID, uuid4
from src.user.auth import generate_user_id as sec


class User(SQLModel, table=True):
    __tablename__ = "Users"
    
    uid : UUID = Field(default_factory=sec,sa_column=Column(pg.CHAR(40), nullable=False, unique=True))

    user_id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            pg.UUID,
            nullable=False,
            unique=True
        )
    )
   
    username: str = Field(
        sa_column=Column(
            pg.VARCHAR(100),
            nullable=False,
        )
    )
    email: str = Field(
        sa_column=Column(
            pg.VARCHAR(50),
            nullable=False,
            primary_key=True,
            unique=True
        )
    )
    
    phone_no: str = Field(Column(pg.VARCHAR(15), nullable=False, unique=True))

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP")  
        )
    )

    last_seen: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),  
            onupdate=text("CURRENT_TIMESTAMP") 
        )
    )
    role: "Role" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    hash_table: "HashTable" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})


class Role(SQLModel, table=True):
    __tablename__ = "Roles"

    uid: str = Field(
        sa_column=Column(pg.CHAR(500), ForeignKey("Users.uid"), primary_key=True)
    )

    Admin: bool = Field(
        sa_column=Column(
            pg.BOOLEAN,
            default=False
        )
    )
    user: "User" = Relationship(back_populates="role")

class HashTable(SQLModel, table=True):
    __tablename__ = "pass_hash"

    uid: str = Field(
        sa_column=Column(pg.CHAR(500), ForeignKey("Users.uid"), primary_key=True)
    )

    hashes: str = Field(
        sa_column=Column(
            pg.CHAR(500),
            unique=True,
            nullable=False
        )
    )
    user: "User" = Relationship(back_populates="hash_table")

