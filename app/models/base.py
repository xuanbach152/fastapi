from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)