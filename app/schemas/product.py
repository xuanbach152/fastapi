from pydantic import BaseModel, EmailStr
from typing import Optional


class ProductBase(BaseModel):
    name:str
    description:Optional[str] = "Chưa có mô tả"
    price:int
    image:Optional[str]="default.png"
    category_name: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    category_name: Optional[str] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True 
