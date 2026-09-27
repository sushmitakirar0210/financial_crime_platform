import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    account_type = Column(String, nullable=False) # SAVINGS, CURRENT, BUSINESS
    currency = Column(String, default="INR")
    balance = Column(Float, default=0.0)
    status = Column(String, default="ACTIVE")
    opened_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", backref="accounts")