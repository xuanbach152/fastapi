from sqlalchemy.orm import Session
from app.core.security import (verify_token,
                               hash_password, verify_password, create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS)
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.user import UserCreate
from app.exception import BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, InternalServerError
from datetime import datetime, timedelta, timezone


def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise NotFoundException("User not found")
    if not user.is_active:
        raise ForbiddenException("User is not active")
    if not verify_password(password, user.hashed_password):
        raise UnauthorizedException("Password is not true")
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    db_refresh = RefreshToken(user_id=user.id, token=refresh_token, expires_at=datetime.now(
        timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    try:
        db.add(db_refresh)
        db.commit()
        return access_token, refresh_token
    except Exception as e:
        db.rollback()
        raise InternalServerError("Save token Failed")


def register_user(db: Session, user_create: UserCreate):

    existing_user = db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

    if existing_user:
        raise ConflictException("Username or Email already exists")

    hashed_password = hash_password(user_create.password)

    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise InternalServerError("Register Failed")


def logout_user(db: Session, user_id: int):
    try:
        db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        db.commit()
        return {"message": "Logged out successfully"}
    except Exception as e:
        db.rollback()
        raise BadRequestException("Logout failed")


def refresh_token(db: Session, refresh_token: str):
    try:
        username = verify_token(refresh_token)
    except:
        raise UnauthorizedException("Invalid refresh token")

    token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token,
                                          RefreshToken.revoked == False, RefreshToken.expires_at > datetime.now(timezone.utc)).first()
    if not token:
        raise NotFoundException("Not Found Refresh token")
    user = db.query(User).filter(User.id==token.user_id).first()
    if not user:
        raise NotFoundException("Not found user")
    new_access_token = create_access_token(data={"sub": user.username})
    return new_access_token