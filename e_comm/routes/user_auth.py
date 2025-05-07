from fastapi import APIRouter, status, Depends, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse
from sqlmodel import select
from e_comm.schemes.user_schemas import CreateUser, UserOut, LogIn, LoginResponse
from e_comm.db.models import UsersDB
from e_comm.db.main import AsyncSession, get_db
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from e_comm.auth.auth import hash_password, verify_password
from e_comm.auth.jwt import create_access_token, create_refresh_token, verify_refresh_token

login_service = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/login")

@login_service.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    statement = select(UsersDB).where(user.email == UsersDB.email)
    result = await db.exec(statement)
    result = result.first()
    if result or None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    else:
        try:
            hashpassword = hash_password(user.password)


            new_user = UsersDB(username=user.username, email=user.email, hashpassword=hashpassword, role=user.role)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            
            
            return {"message": "User created successfully"}, RedirectResponse(url=f"/api/auth/login", status_code=status.HTTP_308_PERMANENT_REDIRECT)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create user: {str(e)}")
    
    
@login_service.post("/login", response_model= LoginResponse,  status_code=status.HTTP_200_OK)
async def login(response: Response, user: LogIn, db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(UsersDB).where(UsersDB.email == user.email))
    result = result.first()

    if not result or not verify_password(user.password, result.hashpassword):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_data = {
        "uid": str(result.uid),
        "username": result.username,
        "role": result.role,
        "is_verified": result.is_verified
    }

    access_token = await create_access_token(user_data)
    refresh_token = await create_refresh_token(user_data)

    response.headers["Authorization"] = access_token

    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=15 * 60,
    )


    
    response.set_cookie(
        key="refresh_token",
        value= refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age= 7 * 24 * 60 * 60,
    )

    allowed_fields = {"uid", "username", "role", "is_verified","created_at"}
    return {
        "message": "Login successful",
        "user": UserOut.model_validate(result.model_dump(include=allowed_fields)),
    }

# 3. Refresh
@login_service.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        user_data = await verify_refresh_token(refresh_token)   
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access = await create_access_token(user_data)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=15 * 60,
    )

    return {"message": "Token refreshed", "access_token": new_access}

# 4. Logout
@login_service.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
