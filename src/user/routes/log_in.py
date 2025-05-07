from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
import src.user.schemas as m
from src.user.service import UserService
from src.user.models import User
from src.db.main import get_db
from sqlmodel.ext.asyncio.session import AsyncSession


user_routes = APIRouter()
log_routes = APIRouter()
reg_routes = APIRouter()


@user_routes.get("/", status_code=status.HTTP_200_OK)
async def info(user_id, db: AsyncSession = Depends(get_db)):
    users = await UserService().get_user(user_id, db)
    return users

@reg_routes.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: m.RegisterModel, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
  
    new_user = await UserService().create_user(user_data, db)
    return new_user

@user_routes.get("/all", status_code=status.HTTP_200_OK)
async def info(db: AsyncSession = Depends(get_db)):
    """Fetch all users"""
    users = await UserService().get_users(db)
    return users

@log_routes.post("/", status_code=status.HTTP_202_ACCEPTED)
async def log_in_user(user_data: m.LogModel, db: AsyncSession = Depends(get_db)):
    users = await UserService().log_in(user_data, db)
    return users