from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut
import app.services.auth_service as auth_service
from app.core.security import REFRESH_TOKEN_EXPIRE_DAYS


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login_user(login_request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    access_token, refresh_token = auth_service.login_user(
        db, login_request.username, login_request.password)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, user_create)
    return user


@router.post("/logout", response_model=dict)
def logout_user(response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    logout = auth_service.logout_user(db, current_user.id)
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return logout


@router.post("/refresh-token", response_model=dict)
def refresh_token(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token_refresh = request.cookies.get("refresh_token")
    if not token_refresh:
        return {"error": "No refresh token found"}

    access_token = auth_service.refresh_token(db, token_refresh)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }