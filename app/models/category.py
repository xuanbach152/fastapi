from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))