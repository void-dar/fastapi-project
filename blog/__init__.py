from fastapi import FastAPI
from contextlib import asynccontextmanager
from blog.db.main import init_db, engine
from sqlmodel import text
from blog.routes.users import reg_service, log_service
from blog.routes.posts import post, postone

version = "1.0.0"

@asynccontextmanager
async def lifespan(app: FastAPI):
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

app = FastAPI(
    title="Blog Application",
    description="A practical blog app",
    version=version,
    lifespan=lifespan
)

app.include_router(reg_service, prefix="/register")
app.include_router(log_service, prefix="/login")
app.include_router(post, prefix="/post")
app.include_router(postone, prefix="/mypost")