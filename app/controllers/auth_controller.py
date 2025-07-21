from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.auth import LoginRequest,TokenResponse
from app.schemas.user import UserCreate, UserOut
import app.services.auth_service as auth_service



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login",response_model=TokenResponse)
def loginUser(login_request: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, login_request.username, login_request.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return TokenResponse(access_token=token, token_type="bearer")

@router.post("/register", response_model=UserOut)
def registerUser(user_create: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, user_create)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return UserOut.model_validate(user)
