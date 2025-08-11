from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel


class Option(BaseModel):
    __tablename__ = "options"

    name = Column(String(100), nullable=False)               
    extra_price = Column(Integer, default=0.0)              
    option_type_id = Column(Integer, ForeignKey("option_types.id"), nullable=False)