import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=True)
    action = Column(String, nullable=False) # LOGIN, VIEW_CUSTOMER, VIEW_ACCOUNT, CREATE_BENEFICIARY, MODIFY_CUSTOMER, CREATE_TRANSACTION, APPROVE_TRANSACTION, EXPORT_DATA
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    ip_address = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)

    employee = relationship("Employee", backref="access_logs")
    customer = relationship("Customer", backref="access_logs")
    account = relationship("Account", backref="access_logs")