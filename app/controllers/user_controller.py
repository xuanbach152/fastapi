from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import (
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def createUser(user_create: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_create)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user


@router.put("/{user_id}", response_model=UserOut)
def updateUser(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/delete/{user_id}", response_model=UserOut)
def deleteUser(user_id:int,db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
def getAllUsers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserOut)
def getUserById(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user