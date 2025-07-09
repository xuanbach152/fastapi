# Table
from app.models.user import User

from app.db.database import SessionLocal, engine, Base

def init_database():
    Base.metadata.create_all(bind=engine)