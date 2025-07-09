from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.auth import LoginRequest,TokenResponse
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import (login_user, register_user)



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login",response_model=TokenResponse)
def loginUser(login_request: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, login_request.username, login_request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return TokenResponse(access_token=token, token_type="bearer")

