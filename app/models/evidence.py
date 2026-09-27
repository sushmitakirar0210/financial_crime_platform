import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_id = Column(String, ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False)
    evidence_type = Column(String, nullable=False) # TRANSACTION, ACCESS_LOG, PERMISSION, BENEFICIARY, PROFILE_MISMATCH, GRAPH_PATTERN, BEHAVIOR_ANOMALY, TIMELINE_EVENT
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    source_type = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    severity = Column(String, default="MEDIUM")
    meta_data = Column(JSON, nullable=True) # Renamed to avoid keyword conflict
    created_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", backref="evidence_items")