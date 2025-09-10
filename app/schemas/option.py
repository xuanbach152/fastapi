from pydantic import BaseModel
from typing import Optional


class OptionBase(BaseModel):
    name:str
    extra_price:int
    option_type_id:int

class OptionCreate(OptionBase):
    pass
class OptionOut(OptionBase):
    id:int
    class Config:
        from_attributes = True 

    