from fastapi import FastAPI
from sqlmodel import text
from contextlib import asynccontextmanager
from e_comm.db.main import init_db, engine
from e_comm.routes.user_auth import login_service


@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        print("server is starting")
        await init_db()
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
            print("connection established")
    except Exception as e:
        print(f"Connection failed: {e}")

    yield
    print("Server shutting down....")
    await engine.dispose()
    print("Server shut down")

version = "1.0.0"

app = FastAPI(
    title="E-Commerce App",
    description="An app that faciltates global trade",
    version=version,
    lifespan=lifespan
)

app.include_router(login_service, prefix="/api/auth", tags=["user authentication"])
