from fastapi import APIRouter, status, Depends, HTTPException, Response, Cookie, UploadFile, File, Form
from fastapi.responses import RedirectResponse
from sqlmodel import select, and_
from ..schemes.product_schemas import GetProduct, CreateProduct
from ..db.models import UsersDB, Products, Reviews
from ..db.main import AsyncSession, get_db
from ..auth.auth_depends import get_token, get_current_user, check_role
from fastapi.encoders import jsonable_encoder
from ..auth.file_name_checker import upload_product_image
from uuid import uuid4, UUID
import os
import shutil



prod_route = APIRouter()

@prod_route.post("/create_product", response_model=GetProduct, status_code=status.HTTP_201_CREATED)
async def create_product(data: CreateProduct, db: AsyncSession = Depends(get_db), token = Depends(get_token), user: dict = Depends(get_current_user), role = Depends(check_role)):
    username = user.get("username")
    try:
        new_product = Products(prod_name= CreateProduct.prod_name, 
                            description= CreateProduct.description, 
                            inventory= CreateProduct.inventory,
                            uploaded_by=username)

        
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        prod_uid = new_product.prod_uid
        return RedirectResponse(url=f"/upload_image/{prod_uid}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create product")
    





@prod_route.put("/upload_image/{prod_uid}", status_code=status.HTTP_201_CREATED)
async def upload_image(
    prod_uid: UUID,  
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token), 
    user = Depends(get_current_user),
    role = Depends(check_role)
):
    if not prod_uid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
    upload = upload_product_image(file)
    statement = select(Products).where(prod_uid == Products.prod_uid)
    result = await db.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    try:
        Products.prod_image = upload
        Products.completed = True
        await db.commit()
        await db.refresh(result)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

