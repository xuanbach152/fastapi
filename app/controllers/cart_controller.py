from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.cart import CartItemCreate,CartItemResponse
from app.models.user import User
import app.services.cart_service as cart_service


router=APIRouter(prefix="/cart",tags=["Cart"])


@router.post("/add/item",response_model=CartItemResponse)
def add_to_cart(cart_item:CartItemCreate,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    return cart_service.add_to_cart(db,cart_item,user_id)