from pydantic import BaseModel
from typing import Optional
from app.utils.const import OptionTypeEnum
class OptionTypeBase(BaseModel):
    option_type:Optional[OptionTypeEnum]
class OptionTypeOut(OptionTypeBase):
    id: int

    class Config:
        from_attributes = True 
