from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    email: EmailStr
    department: Optional[str] = "COMPLIANCE"
    role: Optional[str] = "INVESTIGATOR"
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    """Schema for registering a new employee/investigator."""
    id: Optional[str] = None
    password: str

class EmployeeUpdate(BaseModel):
    """Schema for updating an existing employee profile."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    """Schema for returning employee details in API responses (excluding hashed password)."""
    id: str

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects