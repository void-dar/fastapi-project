from passlib.context import CryptContext
import concurrent.futures as fut
import os
from cryptography.hazmat.primitives import serialization
from fastapi.concurrency import run_in_threadpool
import jwt 
from base64 import b64decode
from datetime import datetime, timezone, timedelta

cpu_cores = os.cpu_count()

max_threads = cpu_cores * 2

executor = fut.ThreadPoolExecutor(max_workers=max_threads)



pwd_context = CryptContext(schemes=["argon2"])

algorithm = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE=timedelta(seconds=900)
REFRESH_TOKEN_EXPIRE=timedelta(days=7)


private_pem = b64decode(os.getenv("PRIVATE_KEY"))
public_pem = b64decode(os.getenv("PUBLIC_KEY"))

# Deserialize keys
private_key = serialization.load_pem_private_key(private_pem, password=None)
public_key = serialization.load_pem_public_key(public_pem)


async def create_hash(password: str) -> str :
    return await run_in_threadpool(pwd_context.hash, password)
async def verify_hash(plain_password: str, hashed_password:str):
    return await run_in_threadpool(pwd_context.verify, plain_password, hashed_password)

async def create_access_token(payload):
    expiration_time = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    payload['exp'] = int(expiration_time.timestamp())  # Convert datetime to Unix timestamp
    access_token = jwt.encode(payload, private_key, algorithm="ES256")
    return access_token

async def verify_access_token(token):
  
    try:
        # Decode the token
        payload = jwt.decode(token, public_key, algorithms=["ES256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Access token has expired"
    except jwt.InvalidTokenError:
        return "Invalid access token"
    
async def create_refresh_token(payload):
    expiration_time = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE  
    payload['exp'] = expiration_time
    refresh_token = jwt.encode(payload, private_key, algorithm="ES256")
    return refresh_token

async def verify_refresh_token(token):
    try:
        payload = jwt.decode(token, public_key, algorithms=["ES256"])
        return payload  # Returns the decoded payload if the token is valid
    except jwt.ExpiredSignatureError:
        return "Refresh token has expired"
    except jwt.InvalidTokenError:
        return "Invalid refresh token"