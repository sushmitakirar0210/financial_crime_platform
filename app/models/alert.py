import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_code = Column(String, unique=True, index=True, nullable=False)
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    status = Column(String, default="NEW") # NEW, INVESTIGATING, ESCALATED, CLOSED, FALSE_POSITIVE
    primary_transaction_id = Column(String, ForeignKey("transactions.id"), nullable=True)
    primary_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    primary_customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    fingerprint = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    primary_transaction = relationship("Transaction", backref="alerts")
    primary_employee = relationship("Employee", backref="alerts")
    primary_customer = relationship("Customer", backref="alerts")