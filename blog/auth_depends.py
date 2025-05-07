# auth_dependency.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from blog.auth import verify_access_token as verify_acc

security = HTTPBearer()  # looks for Authorization: Bearer <token>

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = await verify_acc(token)
        print (payload)
        return payload # or payload["sub"], etc.
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
