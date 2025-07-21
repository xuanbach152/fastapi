# Table
from app.models.user import User
from app.models.base import BaseModel

from app.db.database import SessionLocal, engine, Base

def init_database():
    BaseModel.metadata.create_all(bind=engine)