from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from app.models.base import BaseModel
from app.utils.const import OptionTypeEnum


class OptionType(BaseModel):
    __tablename__ = "option_types"

    option_type = Column(Enum(OptionTypeEnum), nullable=False)
 

