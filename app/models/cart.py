from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel

class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

