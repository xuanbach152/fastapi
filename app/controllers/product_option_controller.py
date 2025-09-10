from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.product_option import ProductOptionOut,ProductOptionBase
from app.dependencies import get_db, get_current_user
import app.services.product_option_service as product_option_service
router=APIRouter(prefix="/productoption",tags=["ProductOption"])

@router.post("/",response_model=list[ProductOptionOut])
def create_product_option(product_option:ProductOptionBase,db:Session=Depends(get_db)):
    return product_option_service.create_product_option(db,product_option)