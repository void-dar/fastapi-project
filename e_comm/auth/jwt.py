import jwt
from e_comm.config import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import Dict, Any

JWT_SECRET = settings.JWT_SECRET
algorithm = settings.JWT_ALGORITM
ACCESS_TOKEN_EXPIRE=timedelta(seconds=900)
REFRESH_TOKEN_EXPIRE=timedelta(days=7)



async def create_access_token(payload: dict):
    expiration_time = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    payload = payload.copy()  # prevent side-effects if reused
    payload.update({
        'exp': expiration_time,
        'token_type': 'access'
    })
    try:
        token = jwt.encode(payload, JWT_SECRET, algorithm=algorithm)
        return token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create access token")

async def verify_access_token(token: str):
    try:
        payload: Dict[str, Any] = jwt.decode(token, JWT_SECRET, algorithms=[algorithm])
        if payload.get("token_type") != "access":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is invalid")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is invalid signature")
    
 
async def create_refresh_token(payload: dict):
    expiration_time = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE
    payload = payload.copy()
    payload.update({
        'exp': expiration_time,
        'token_type': 'refresh'
    })
    try:
        refresh_token = jwt.encode(payload, JWT_SECRET, algorithm=algorithm)
        return refresh_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create refresh token")

async def verify_refresh_token(token: str):
    try:
        payload: Dict[str, Any] = jwt.decode(token, JWT_SECRET, algorithms=[algorithm])
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is invalid")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is invalid signature")

    





