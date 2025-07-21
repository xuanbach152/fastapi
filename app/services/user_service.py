from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_user(db: Session, user_id: int):
    if user_id <= 0:
        return "Invalid user id"
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    if skip < 0 or limit <= 0:
        return "Invalid pagination parameters"
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db:Session,user_id:int):
    if user_id <= 0:
        return None
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    try:
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        return None

def update_user(db:Session,user_id:int,user_update:UserUpdate):
     if user_id <= 0:
        return None

     user = db.query(User).filter(User.id == user_id).first()
     if not user:
        return None
     
     allowed_fields = {"username", "email", "password"}
     user_data = user_update.model_dump(exclude_unset=True)
     try:
       for field, value in user_data.items():
            if field in allowed_fields and value:
                if field == "password":
                    user.hashed_password = hash_password(value)
                elif field == "username":
                    existing = db.query(User).filter(
                        User.username == value, User.id != user_id
                    ).first()
                    if existing:
                        return None  
                    user.username = value
                elif field == "email":
                    existing = db.query(User).filter(
                        User.email == value, User.id != user_id
                    ).first()
                    if existing:
                        return None  
                    user.email = value
        
       db.commit()
       db.refresh(user)
       return user        
     except Exception:
       db.rollback()
       return None