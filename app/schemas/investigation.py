from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InvestigationNoteBase(BaseModel):
    case_id: str
    employee_id: str
    note_content: str

class InvestigationNoteCreate(InvestigationNoteBase):
    """Schema for adding an investigative note to a case."""
    id: Optional[str] = None

class InvestigationNoteResponse(InvestigationNoteBase):
    """Schema for returning investigative notes."""
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InvestigationSummaryResponse(BaseModel):
    """Schema for returning an aggregated investigative dossier summary."""
    case_id: str
    total_linked_alerts: int
    total_evidence_items: int
    total_notes: int
    risk_score_snapshot: float
    investigation_status: str