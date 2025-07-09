from sqlalchemy.orm import Session
from app.core.security import (hash_password, verify_password,create_access_token,create_refresh_token)
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
    existing_user = db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()
    if existing_user:
        return None
    hashed_password = hash_password(user_create.password)
    user = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

