from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlmodel import select
from task.schemas import CreateUser, UserOut, LogIn
from task.db.models import UserDB
from task.db.main import AsyncSession, get_db
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from task.routes.auth import hash_password, verify_password
from datetime import datetime, timezone
from task.jwt import create_access_token, create_refresh_token

login_service = APIRouter()

@login_service.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    statement = select(UserDB).where(user.email == UserDB.email)
    result = await db.exec(statement)
    result = result.first()
    if result or None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    else:
        try:
            hashpassword = hash_password(user.password)


            new_user = UserDB(username=user.username, email=user.email, hashpassword=hashpassword, role=user.role)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            return {"message": "User created successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create user: {str(e)}")
    
    
@login_service.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_user(response: Response,user: LogIn, db: AsyncSession = Depends(get_db)):

    statement = select(UserDB).where(user.email == UserDB.email)
    result = await db.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    checker = verify_password(user.password, result.hashpassword)
    if checker:
        try:
            
            result.last_seen = datetime.now(timezone.utc)
            
            await db.commit()
            result = {**result.model_dump()}
            user_data = {"uid": jsonable_encoder(result["uid"]),"username":result["username"], "role": result["role"]}
            access = await create_access_token(user_data)
            response.headers["Authorization"] = access
            refresh = await create_refresh_token(user_data)
            response.set_cookie(key="refresh",
                                value=refresh,
                                httponly=True,
                                secure=True, 
                                max_age=60*60*24*7)
            return {"message": "User logged in successfully", "user": result }
        except Exception as e:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login failed")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
