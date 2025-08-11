from sqlalchemy import Column, Integer, String, ForeignKey,Enum
from app.models.base import BaseModel
from app.utils.const import OrderStatusEnum


class Order(BaseModel):
    __tablename__ = "orders"

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    status = Column(Enum(OrderStatusEnum),nullable=False)
    total_price = Column(Integer,nullable=False)