from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import UserUpdate, UserOut
from app.models.user import User

import app.services.user_service as user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_service.update_user(db, user_id, user_update)
    return user


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mess = user_service.delete_user(db, user_id)
    return mess


@router.get("/", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return user_service.get_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_service.get_user(db, user_id)

    return user
