from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.option import Option
from app.schemas.option import OptionOut,OptionCreate
import app.services.option_service as option_service

router = APIRouter(prefix="/option",tags=["Option"])

@router.post("/",response_model=OptionOut)
def create_option(option:OptionCreate,db:Session=Depends(get_db)):
    return option_service.create_option(db,option)