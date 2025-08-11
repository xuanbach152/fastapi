from sqlalchemy import Column, Integer, String, ForeignKey,Enum
from app.models.base import BaseModel



class OrderItemOption(BaseModel):
    __tablename__ = "order_item_options"

    order_item_id = Column(Integer,ForeignKey("order_items.id"),nullable=False)
    option_id = Column(Integer,ForeignKey("options.id"),nullable=False)