from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config

DATABASE_URL=Config.DATABASE_URL


engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
    future=True
)


async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async with async_session_factory() as session:
        yield session