from sqlalchemy import Column, Integer, String, ForeignKey,Enum
from app.models.base import BaseModel
from app.utils.const import PaymentStatus,Method

class Payment(BaseModel):
    __tablename__ = "payments"

    order_id = Column(Integer,ForeignKey("orders.id"),nullable=False)
    amount = Column(Integer,nullable=False)
    status = Column(Enum(PaymentStatus),nullable=False,default=PaymentStatus.PENDING)
    method = Column(Enum(Method),nullable=False)