from passlib.context import CryptContext
import concurrent.futures as fut
import os
from cryptography.hazmat.primitives import serialization
from fastapi.concurrency import run_in_threadpool
import jwt 
import asyncio
from base64 import b64decode
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone, timedelta

load_dotenv()

cpu_cores = os.cpu_count()

max_threads = cpu_cores * 2

executor = fut.ThreadPoolExecutor(max_workers=max_threads)



pwd_context = CryptContext(schemes=["argon2"])

algorithm = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE=timedelta(seconds=900)
REFRESH_TOKEN_EXPIRE=timedelta(days=7)


private_pem = b64decode(os.getenv("PRIVATE_KEY"))
public_pem = b64decode(os.getenv("PUBLIC_KEY"))

print(private_pem)
print(public_pem)

# Deserialize keys
private_key = serialization.load_pem_private_key(private_pem, password=None)
public_key = serialization.load_pem_public_key(public_pem)

payload = {
    "username": "maximus",
    "email": "anime@gmail.com",
    "password": "manikay24"
}

payload = jsonable_encoder(payload)


async def create_access_token(payload):
    expiration_time = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    payload['exp'] = int(expiration_time.timestamp())  # Convert datetime to Unix timestamp
    access_token = jwt.encode(payload, private_key, algorithm="ES256")
    print(f"Generated Access Token: {access_token}")  # Debug print
    return access_token

async def verify_access_token(token):
    print(f"Verifying token: {token}")  # Added log
    try:
        # Decode the token
        payload = jwt.decode(token, public_key, algorithms=["ES256"])
        print(f"Decoded payload: {payload}")  # Log the decoded payload
    except jwt.ExpiredSignatureError:
        print("Access token has expired")  # Added log for expired token
        return "Access token has expired"
    except jwt.InvalidTokenError:
        print("Invalid access token")  # Added log for invalid token
        return "Invalid access token"

    

async def main():
    access_token = await create_access_token(payload)
    
    await verify_access_token(access_token)

asyncio.run(main())

