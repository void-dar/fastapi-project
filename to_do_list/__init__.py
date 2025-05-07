from fastapi import FastAPI
from sqlmodel import text
from contextlib import asynccontextmanager
from to_do_list.db.main import init_db, engine
from to_do_list.routes.user import profile, todo

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
    title="TO DO List App",
    description="A simple TO DO List App",
    version=version,
    lifespan=lifespan
)

app.include_router(profile, prefix="/user", tags=["User"])
app.include_router(todo, prefix="/todo", tags=["Todo"])