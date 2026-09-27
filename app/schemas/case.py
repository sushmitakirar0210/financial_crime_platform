from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    status: str = "OPEN"
    assigned_employee_id: Optional[str] = None

class CaseCreate(CaseBase):
    """Schema for creating a new investigation case."""
    id: Optional[str] = None
    alert_ids: Optional[List[str]] = []

class CaseUpdate(BaseModel):
    """Schema for updating an existing investigation case."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_employee_id: Optional[str] = None

class CaseResponse(CaseBase):
    """Schema for returning case details in API responses."""
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects