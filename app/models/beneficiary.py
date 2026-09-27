import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_code = Column(String, unique=True, index=True, nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    beneficiary_name = Column(String, nullable=False)
    beneficiary_account = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    created_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ACTIVE")

    account = relationship("Account", backref="beneficiaries")
    creator = relationship("Employee", foreign_keys=[created_by_employee_id])