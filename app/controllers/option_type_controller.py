from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.option_type import OptionType
from app.utils.const import OptionTypeEnum
from app.schemas.option_type import OptionTypeOut
import app.services.option_type_service as option_type_service

router = APIRouter(prefix="/optiontype", tags=["OptionType"])


@router.post("/", response_model=OptionTypeOut)
def create_option_type(option_type: OptionTypeEnum = Query(...), db: Session = Depends(get_db)):
    return option_type_service.create_option_type(db, option_type)

@router.get("/",response_model=list[OptionTypeOut])
def get_all_option_type(db:Session=Depends(get_db)):
    return option_type_service.get_all_option_type(db)