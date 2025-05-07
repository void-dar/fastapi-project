from fastapi import Depends, HTTPException, status, Cookie, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt import verify_access_token


security = HTTPBearer()  # looks for Authorization: Bearer <token>

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    try:
        payload = await verify_access_token(token)
        print (payload)
        return payload # or payload["sub"], etc.
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_token(access_token: str = Cookie(...)):
    try:
        token = Response.headers["Authorization"] = f"Bearer {access_token}"
        return token
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Get Authorization Token"})
    

async def check_admin(user: dict = Depends(get_current_user)):
    user = user.get("role")
    if user != "admin": 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient Priviledges")
    
async def check_role(user: dict = Depends(get_current_user)):
    user = user.get("role")
    if user not in ("admin", "worker"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient Privileges")
    
async def check_all_role(user: dict = Depends(get_current_user)):
    user = user.get("role")
    if user not in ("admin", "worker", "user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient Privileges")