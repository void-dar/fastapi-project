from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from to_do_list.schema import UserModel, Dos, Retrieve, Verify
from sqlalchemy.ext.asyncio.session import AsyncSession
from to_do_list.db.main import get_db
from sqlmodel import select, and_
from to_do_list.db.models import User as UserDB, To_dos as Do
from sqlalchemy.orm import selectinload

profile = APIRouter()
todo = APIRouter()

@profile.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel, db: AsyncSession = Depends(get_db)):
    statement = select(UserDB).where(UserDB.name == user.name)
    result = await db.execute(statement)
    result = result.scalars().first()
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = UserDB(
        name=user.name
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create user: {str(e)}")
    
@profile.get("/", status_code=status.HTTP_200_OK)
async def get_user(data : Verify, db: AsyncSession = Depends(get_db)):
    try:
       # Fetch the user and load `to_dos` relationship
        statement = select(UserDB).where(UserDB.uid == data.uid).options(selectinload(UserDB.to_dos))
        result = await db.execute(statement)
        user = result.scalars().first()

    
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        to_dos = [{"title": todo.title, "description": todo.description} for todo in user.to_dos]

        return {
            "uid": str(user.uid),
            "name": user.name,
            "to_dos": to_dos
        }
    except Exception as e:
        return(f"Error: {e}")
              
@todo.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Dos, db: AsyncSession = Depends(get_db)):
    new_todo = Do(
        title=todo.title,
        description=todo.description,
        uid=todo.uid
    )
    try:
        db.add(new_todo)
        await db.commit()
        await db.refresh(new_todo)
        return new_todo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create todo: {str(e)}")

@todo.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def change(data: Retrieve, id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Do).where(and_(Do.uid == data.uid, Do.id == id))
    result = await db.execute(statement)
    existing_todo = result.scalars().first()

    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")


    existing_todo.title=data.title
    existing_todo.description=data.description
    
    
    await db.commit()
    await db.refresh(existing_todo)
    return existing_todo

@todo.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, data: Verify, db: AsyncSession = Depends(get_db)):
    # Check if the entry exists
    statement = select(Do).where(and_(Do.uid == data.uid, Do.id == id))
    result = await db.execute(statement)
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    # Explicitly delete the record
    await db.delete(todo)
    
    await db.commit()

    # Verify if deletion was successful
    verify_statement = select(Do).where(Do.id == id)
    verify_result = await db.execute(verify_statement)
    deleted_entry = verify_result.scalars().first()

    if deleted_entry:
        raise HTTPException(status_code=500, detail="Failed to delete entry")
    
    