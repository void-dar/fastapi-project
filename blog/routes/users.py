from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlmodel import select
from blog.schemas import UserIn, UserOut, LogIn
from blog.db.models import UserDB
from blog.db.main import AsyncSession, get_db
from fastapi.encoders import jsonable_encoder
from blog.auth import create_hash, verify_hash, create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordBearer

reg_service = APIRouter()
log_service = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

@reg_service.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(response: Response, user: UserIn, db: AsyncSession = Depends(get_db)):
    hashed_password = await create_hash(user.password)

    statement = select(UserDB).where(UserDB.email == user.email)
    result = await db.exec(statement)
    user_check = result.first()

    if user_check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")

    new_user = UserDB(email=user.email, username=user.username, hashpassword=hashed_password)
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        await login_user(response, LogIn(email=user.email, password=user.password), db)
        return UserOut.model_validate(new_user.model_dump())

    except Exception as e:
        await db.rollback()
        await db.delete(new_user)
        await db.commit()
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to create user")

@log_service.post("/", status_code=status.HTTP_200_OK)
async def login_user(response: Response, user: LogIn, db: AsyncSession = Depends(get_db)):
    
    statement = select(UserDB).where(UserDB.email == user.email)
    result = await db.exec(statement)
    user_db = result.first()
    ver = await verify_hash(user.password, user_db.hashpassword)
    
    if user_db is None or not ver:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

   
    payload = {**user_db.model_dump()}
    payload = jsonable_encoder(payload)

    #Generate both access and refresh tokens
    access_token = await create_access_token(payload)
    refresh_token = await create_refresh_token(payload)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevent JavaScript access
        secure=True,    # Only send over HTTPS
        max_age=60*15,  # Access token valid for 15 minutes
        samesite="Strict"  # Prevent CSRF attacks
    )

  
    

    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        secure=True, 
        max_age=60*60*24*7 
    )
    


    user = UserOut.model_validate(user_db.model_dump())
    return user, {"access_token": access_token, "token_type": "bearer"}
   
    



