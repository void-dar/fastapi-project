import jwt
from task.config import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

JWT_SECRET = settings.JWT_SECRET
algorithm = settings.JWT_ALGORITM
ACCESS_TOKEN_EXPIRE=timedelta(seconds=900)
REFRESH_TOKEN_EXPIRE=timedelta(days=7)



async def create_access_token(payload):
    expiration_time = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    payload['exp'] = expiration_time
    try:
        token = jwt.encode(payload, JWT_SECRET, algorithm=algorithm)
        return f"Bearer {token}"
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create access token")

async def verify_token(token):
    try:
        user_data = jwt.decode(token, JWT_SECRET, algorithms=algorithm)
        return user_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is invalid")
    
async def create_refresh_token(payload):
    expiration_time = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE
    payload['exp'] = expiration_time
    try:
        refresh_token = jwt.encode(payload, JWT_SECRET, algorithm=algorithm)
        return refresh_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create refresh token")

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()  # looks for Authorization: Bearer <token>

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = await verify_token(token)
        print (payload)
        return payload # or payload["sub"], etc.
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token error",
            headers={"WWW-Authenticate": "Bearer"},
        )