from fastapi import APIRouter,Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db, get_current_user
from app.schemas.product import ProductOut,ProductUpdate,ProductCreate

import app.services.product_service as product_service


router = APIRouter(prefix="/product",tags=["Product"])

@router.get("/",response_model=list[ProductOut])
def get_all_product(db:Session=Depends(get_db)):
    return product_service.get_all_product(db)

@router.get("/{product_id}",response_model=ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
    return product_service.get_product(db,product_id)

@router.post("/",response_model=ProductOut)
def create_product(product_data:ProductCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return product_service.create_product(db,product_data)

@router.patch("/{product_id}",response_model=ProductOut)
def update_product(product_id:int,product_data:ProductUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return product_service.update_product(db,product_id,product_data)

@router.delete("/{product_id}",response_model=dict)
def delete_product(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return product_service.delete_product(db,product_id)

@router.post("/upload-image/{product_id}")
def upload_product_image(product_id:int,file:UploadFile=File(...),db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return product_service.upload_product_image(db,product_id,file)