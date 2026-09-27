import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.database.database import Base

case_evidence_association = Table(
    "case_evidence",
    Base.metadata,
    Column("case_id", String, ForeignKey("cases.id", ondelete="CASCADE"), primary_key=True),
    Column("evidence_id", String, ForeignKey("evidence.id", ondelete="CASCADE"), primary_key=True)
)

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="MEDIUM")
    status = Column(String, default="OPEN") # OPEN, INVESTIGATING, ESCALATED, RESOLVED, CLOSED
    assigned_to = Column(String, ForeignKey("employees.id"), nullable=True)
    created_by = Column(String, ForeignKey("employees.id"), nullable=False)
    alert_id = Column(String, ForeignKey("alerts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    assignee = relationship("Employee", foreign_keys=[assigned_to], backref="assigned_cases")
    creator = relationship("Employee", foreign_keys=[created_by], backref="created_cases")
    alert = relationship("Alert", backref="cases")
    evidence_items = relationship("Evidence", secondary=case_evidence_association, backref="cases")