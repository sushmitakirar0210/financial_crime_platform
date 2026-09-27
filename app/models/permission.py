import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    permission_type = Column(String, nullable=False) # VIEW_CUSTOMER, VIEW_ACCOUNT, TRANSFER, CREATE_BENEFICIARY, MODIFY_CUSTOMER, EXPORT_DATA
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    granted_by = Column(String, nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    status = Column(String, default="ACTIVE")

    employee = relationship("Employee", backref="permissions")