from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(Integer,ForeignKey("orders.id"),nullable=False)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    unit_price = Column(Integer,nullable=False)