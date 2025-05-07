from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status
from src.user.schemas import RegisterModel, LogModel, UserResponse
from sqlmodel import select, and_, or_
from sqlalchemy.orm import load_only
from src.user.models import User, HashTable, Role
from datetime import datetime, timezone
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
from src.user.auth import pwd_context

class UserService:
    """async def get_users(self, db: AsyncSession):
        statement = select(User.user_id, User.email, User.phone_no, User.created_at, User.last_seen)
        results = await db.exec(statement)
        return results"""
    
    async def get_users(self, db: AsyncSession):
        statement = select(User).options(load_only(User.email, User.phone_no, User.created_at, User.last_seen))
        result = await db.exec(statement)
        #users = [dict(zip(["user_id", "email", "phone_no", "created_at", "last_seen"], row)) for row in result]
        return result.all()


    async def get_user(self, user_id: str, db: AsyncSession):
        statement = select(User).where(User.user_id == user_id)
        result = await db.exec(statement)
        return result.first()

    async def create_user(self, user_data: RegisterModel, db: AsyncSession) -> UserResponse :
        # Check if a user with the same email or phone number already exists
        result = await db.exec(select(User).where(
            (User.email == user_data.email) | 
            (User.phone_no == user_data.phone_no) |
            (User.username == user_data.username)
        ))
        existing_user = result.first()

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")

        # Hash password before storing
        hashed_password = generate_password_hash(user_data.password, method='pbkdf2:sha256', salt_length=15)

        # Create User object (without storing password in User table)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            phone_no=user_data.phone_no,
        )

        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)  # Get updated data after insert

            # Create HashTable entry
            hash_entry = HashTable(hashes=hashed_password, uid=new_user.uid)
            db.add(hash_entry)
            await db.commit()
            await db.refresh(hash_entry)

            return UserResponse(username=new_user.username, email=new_user.email, phone_no=new_user.phone_no)

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")
            

    async def log_in(self, user_data: LogModel, db: AsyncSession):
        """Logs in a user by verifying email/phone and password."""
        statement = select(User).where(and_
                                       (or_
                                        (User.email == user_data.email, User.phone_no == user_data.phone_no), (User.username == user_data.username)))
        result = await db.exec(statement)
        user = result.first()  # Fix here

        if not user:
            return {"error": "Invalid credentials"}

        # Fetch password hash from HashTable
        statement = select(HashTable).where(HashTable.uid == user.uid)
        result = await db.exec(statement)
        hash_entry = result.first()  # Fix here
        print(hash_entry)
        password = str(user_data.password)
        if not hash_entry:
            raise HTTPException(status_code=401, detail="Ivalid credentials")
        hash = hash_entry.hashes
        hash = hash.strip()
        if not check_password_hash(hash, password):
            raise HTTPException(status_code=401, detail="Ivalid credentials")
            #print("Stored hash:", hash_entry.hashes)
           # raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # If password verification passed, update last_seen timestamp
        user.last_seen = datetime.now(timezone.utc)
        await db.commit()
        return {"message": "Login successful", "user_id": user.user_id}

        
            

    async def delete_user(self, uid: str, db: AsyncSession):
        """Deletes a user by UID."""
        statement = select(User).where(User.uid == uid)
        result = await db.exec(statement)
        user = result.first()

        if user:
            await db.delete(user)
            await db.commit()
            return {"message": "User deleted successfully"}
        return {"error": "User not found"}
