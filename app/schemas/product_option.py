from pydantic import BaseModel
from typing import Optional


class ProductOptionBase(BaseModel):
    product_id: int
    option_type_ids:list[int]


class ProductOptionOut(BaseModel):
    id: int
    product_id: int
    option_type_id: int

    class Config:
        from_attributes = True
