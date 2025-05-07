from pydantic import BaseModel, Field
from typing import Union, Optional, Annotated, Any, List
from uuid import UUID
from datetime import datetime


class CreateProduct(BaseModel):
    prod_name: str
    description: str
    inventory: int


   

class GetProduct(BaseModel):
    prod_image: str
    prod_name: str
    description: str
    inventory: int
    created_at: Union[int, datetime]
    reviews: List[dict[str, Any]]
