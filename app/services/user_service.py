from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.exception import BadRequestException,ConflictException,ForbiddenException,NotFoundException,UnauthorizedException,InternalServerError

def get_user(db: Session, user_id: int):
    if user_id <= 0:
        raise BadRequestException("Id is not valid")
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    if skip < 0 or limit <= 0:
        raise BadRequestException("Parameter are not valid")
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db:Session,user_id:int):
    if user_id <= 0:
        raise BadRequestException("Id is not valid")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")
    try:
        db.delete(user)
        db.commit()
        return  {"message": "User deleted successfully", "id": user_id}

    except Exception as e:
        db.rollback()
        raise BadRequestException

def update_user(db:Session,user_id:int,user_update:UserUpdate):
     if user_id <= 0:
        raise BadRequestException("Id is not valid")

     user = db.query(User).filter(User.id == user_id).first()
     if not user:
        raise NotFoundException("user not found")
     user_data = user_update.model_dump(exclude_unset=True)
     try:
       for field, value in user_data.items():
                if field == "password":
                    user.hashed_password = hash_password(value)
                elif field == "username":
                    existing = db.query(User).filter(
                        User.username == value, User.id != user_id
                    ).first()
                    if existing:
                        raise ConflictException("User name is exist") 
                    user.username = value
                elif field == "email":
                    existing = db.query(User).filter(
                        User.email == value, User.id != user_id
                    ).first()
                    if existing:
                        raise ConflictException("Email is exist")
                    user.email = value
        
       db.commit()
       db.refresh(user)
       return user        
     except Exception as e:
       db.rollback()
       print(f"Update error: {e}")
       raise BadRequestException("failed")