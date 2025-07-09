from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db:Session,user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
def update_user(db:Session,user_id:int,user_update:UserUpdate):
     user = db.query(User).filter(User.id == user_id).first()
     if user:
        if user_update.username:
            user.username = user_update.username
        if user_update.email:
            user.email = user_update.email
        if user_update.password:
            user.hashed_password = hash_password(user_update.password)

        db.commit()
        db.refresh(user)
        return user
def create_user(db:Session,user_create:UserCreate):
    existing_user = db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()
    if existing_user:
        return None
    hashed_password = hash_password(user_create.password)
    user = User(username=user_create.username,email=user_create.email,hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
