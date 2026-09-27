import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Float
from app.database.database import Base
import enum

class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    department = Column(String, nullable=False)
    role = Column(String, nullable=False) # Teller, Relationship Manager, Branch Manager, Operations, Compliance, Analyst, Admin
    branch = Column(String, nullable=False)
    status = Column(SQLEnum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    risk_level = Column(String, default="LOW")
    created_at = Column(DateTime, default=datetime.utcnow)