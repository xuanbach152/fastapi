from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(50), nullable=False)
    description = Column(String(200))
    price = Column(Integer,nullable=False)
    image = Column(String(200),nullable=False)
    category_name = Column(String(100), ForeignKey("categories.name"), nullable=False)

