from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id = Column(Integer,ForeignKey("carts.id"),nullable=False)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,default=1)
