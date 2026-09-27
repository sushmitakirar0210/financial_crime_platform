from pydantic import BaseModel
from typing import Optional

class AlertBase(BaseModel):
    severity: str = "MEDIUM"
    status: str = "OPEN"
    description: str
    rule_name: str
    case_id: Optional[str] = None

class AlertCreate(AlertBase):
    """Schema for creating a new intelligence alert."""
    id: Optional[str] = None

class AlertResponse(AlertBase):
    """Schema for returning alert details in API responses."""
    id: str

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects