from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import UserUpdate, UserOut
from app.models.user import User
from app.services.user_service import (
    get_user,
    get_users,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])



@router.put("/{user_id}", response_model=UserOut)
def updateUser(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = update_user(db, user_id, user_update)
    print(f"Current user: {current_user.username}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot update user")
    return user


@router.delete("/delete/{user_id}", response_model=UserOut)
def deleteUser(user_id:int,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = delete_user(db, user_id)
    print(f"Current user: {current_user.username}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
def getAllUsers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pagination parameters")
    print(f"Current user: {current_user.username}")
    return get_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserOut)
def getUserById(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user(db, user_id)
    print(f"Current user: {current_user.username}")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user