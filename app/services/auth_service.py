from sqlalchemy.orm import Session
from app.core.security import (
    hash_password, verify_password, create_access_token, create_refresh_token)
from app.models.user import User
from app.schemas.user import UserCreate


def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    access_token = create_access_token(data={"sub": user.username})
    return access_token


def register_user(db: Session, user_create: UserCreate):

    user_data = user_create.model_dump()

    allowed_fields = {"username", "email", "password"}

    filtered_data = {k: v for k, v in user_data.items() if k in allowed_fields}
    if not filtered_data.get("username") or not filtered_data.get("email") or not filtered_data.get("password"):
        return None
    
    existing_user = db.query(User).filter(
        (User.username == filtered_data["username"]) |
        (User.email == filtered_data["email"])
    ).first()

    if existing_user:
        return None
    hashed_password = hash_password(filtered_data["password"])
    user = User(username=filtered_data["username"],
                email=filtered_data["email"], hashed_password=hashed_password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        return None
