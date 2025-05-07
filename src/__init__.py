from fastapi import FastAPI
from sqlmodel import text
from src.user.routes.log_in import user_routes, log_routes, reg_routes
from contextlib import asynccontextmanager #determines which code runs at the start and end of our application
from src.db.main import init_db, engine

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting ...")
    try:
        await init_db()  # Initialize the database
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # Test DB connection
        print("Connection established")
    except Exception as e:
        print(f"Connection failed: {e}")

    yield  # App runs while yielding

    print("Server is shutting down ...")
    await engine.dispose()  # Close the DB connection properly
    print("Server terminated")


version = "v1"

app = FastAPI(
    title="project",
    description="fastapi practice",
    version=version,
    lifespan=life_span
)

app.include_router(user_routes, prefix=f"/api", tags=['view'])
app.include_router(reg_routes, prefix=f"/api/reg_user", tags=['register'])
app.include_router(log_routes, prefix="/auth/login_user", tags=['login'])
