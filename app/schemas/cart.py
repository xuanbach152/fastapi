from pydantic import BaseModel
from typing import Optional

class CartItemOptionBase(BaseModel):
    option_id:int

class CartItemOptionCreate(CartItemOptionBase):
    pass

class CartItemOptionResponse(CartItemOptionBase):
    id: int
    name: Optional[str] = None 
    value: Optional[str] = None 

    class Config:
        from_attributes = True 


class CartItemBase(BaseModel):
    product_id:int
    quantity:int
class CartItemCreate(CartItemBase):
    options: Optional[list[int]] = []

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    options: Optional[list[int]] = None


class CartItemResponse(CartItemBase):
    id:int 
    options: Optional[list[int]]
    class Config:
        from_attributes = True 


class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: int
    items: list[CartItemResponse] = []

    class Config:
        from_attributes = True 
