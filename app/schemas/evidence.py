from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvidenceBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    case_id: str

class EvidenceCreate(EvidenceBase):
    """Schema for uploading or linking new evidence to a case."""
    id: Optional[str] = None

class EvidenceResponse(EvidenceBase):
    """Schema for returning evidence details in API responses."""
    id: str
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects