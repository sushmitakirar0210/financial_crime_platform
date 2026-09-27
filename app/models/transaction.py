import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_code = Column(String, unique=True, index=True, nullable=False)
    source_account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    destination_account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    beneficiary_id = Column(String, ForeignKey("beneficiaries.id"), nullable=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    transaction_type = Column(String, nullable=False) # TRANSFER, CASH, WITHDRAWAL, DEPOSIT, PAYMENT
    channel = Column(String, nullable=False) # BRANCH, ONLINE, MOBILE, API
    status = Column(String, default="COMPLETED")
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    source_account = relationship("Account", foreign_keys=[source_account_id], backref="outgoing_transactions")
    destination_account = relationship("Account", foreign_keys=[destination_account_id], backref="incoming_transactions")
    beneficiary = relationship("Beneficiary", backref="transactions")
    employee = relationship("Employee", backref="transactions")