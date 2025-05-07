from fastapi import FastAPI
from task.routes.user import login_service
from task.routes.tasks import task_router
from contextlib import asynccontextmanager
from task.db.main import init_db, engine
from sqlmodel import text


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


app = FastAPI(
    title="Task Manager app",
    description="A simple task manager API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(login_service, prefix="/api/auth", tags=["UserAuth"])
app.include_router(task_router, prefix="/api/app", tags=["Task Service"])