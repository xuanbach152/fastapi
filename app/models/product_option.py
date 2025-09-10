from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class ProductOption(BaseModel):
    __tablename__ = "product_options"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    option_type_id = Column(Integer, ForeignKey("option_types.id"), nullable=False)

