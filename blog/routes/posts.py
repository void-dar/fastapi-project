from fastapi import APIRouter, Depends, status
from sqlmodel import select, text, and_
from blog.schemas import PostIn, PostOut, UpdatePost
from blog.db.models import UserDB, PostDB
from blog.db.main import AsyncSession, get_db
from blog.auth_depends import get_current_user
from typing import List
from sqlalchemy.orm import selectinload

post = APIRouter()
postone = APIRouter()

@postone.get("/", status_code=status.HTTP_201_CREATED)
async def get_posts(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    uid = user["uid"]
    statement = select(UserDB).where(UserDB.uid == uid).options(selectinload(UserDB.postdb))
    result = await db.exec(statement)
    user = result.first()
    posts = [{"title": post.title, "content": post.content} for post in user.postdb]
    return {
            "uid": str(uid),
            "posts": posts
        }

@post.post("/",status_code=status.HTTP_201_CREATED)
async def create_post(post: PostIn, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    uid = user["uid"]
    statement = select(UserDB).where(UserDB.uid == uid)
    result = await db.exec(statement)
    user = result.first()
    if not user:
         return {"error": "User not found"}
    new_post = PostDB(
        title=post.title,
        content=post.content,
        uid=uid
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@post.put("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: UpdatePost, db: AsyncSession = Depends(get_db), user : dict= Depends(get_current_user)):
    uid = user.get("uid")
    statement = select(PostDB).where(PostDB.uid == uid)
    result = await db.exec(statement)
    user = result.all()
    if not user:
        return {"error": "User not found"}
    statement = select(user).where(PostDB.post_id == post.id)
    result = await db.exec(statement)
    result = result.first()
    if not result:
        return {"error": "Post not found"}
    try:
        updated_post = PostDB(
            title=post.title,
            content=post.content
        )
        db.add(updated_post)
        await db.commit()
        await db.refresh(updated_post)
        PostOut.model_validate(updated_post.model_dump())
        return updated_post
    except Exception as e:
        return {"error": str(e)}
    
@post.get("/{post_id}", status_code=status.HTTP_201_CREATED)
async def get_posts(post_id: int, db: AsyncSession = Depends(get_db), user : dict= Depends(get_current_user)):
    uid = user["uid"]
    statement = select(PostDB).where(and_(PostDB.uid == uid, PostDB.post_id == post_id))
    result = await db.exec(statement)
    user = result.first()
    return user