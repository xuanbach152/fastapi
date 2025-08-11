from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel

class CartItemOption(BaseModel):
    __tablename__ = "cart_item_options"

    cart_item_id = Column(Integer,ForeignKey("cart_items.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
