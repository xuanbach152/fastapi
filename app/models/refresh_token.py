from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,DateTime
from app.models.base import BaseModel

class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    token = Column(String,unique=True,index=True)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)