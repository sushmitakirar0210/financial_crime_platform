import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float
from app.database.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    customer_type = Column(String, nullable=False) # INDIVIDUAL, BUSINESS
    occupation = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    risk_category = Column(String, default="LOW")
    expected_monthly_volume = Column(Float, default=100000.0)
    created_at = Column(DateTime, default=datetime.utcnow)