from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.evidence import Evidence
from app.core.logging import logger


class EvidenceService:
    @staticmethod
    def add_evidence(
            db: Session,
            title: str,
            case_id: str,
            description: Optional[str] = None,
            file_path: Optional[str] = None
    ) -> Evidence:
        """Attach and persist new investigative evidence linked to a compliance case."""
        evidence_id = f"EVID-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{abs(hash(title)) % 10000:04d}"

        new_evidence = Evidence(
            id=evidence_id,
            title=title,
            description=description,
            file_path=file_path,
            case_id=case_id
        )
        db.add(new_evidence)
        db.commit()
        db.refresh(new_evidence)
        logger.info(f"Added evidence item [{evidence_id}] to case [{case_id}].")
        return new_evidence

    @staticmethod
    def get_evidence_by_case(db: Session, case_id: str) -> List[Evidence]:
        """Retrieve all evidence items linked to a specific investigation case."""
        return db.query(Evidence).filter(Evidence.case_id == case_id).all()

    @staticmethod
    def delete_evidence(db: Session, evidence_id: str) -> bool:
        """Remove an evidence item from an investigation case."""
        evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
        if not evidence:
            return False

        db.delete(evidence)
        db.commit()
        logger.info(f"Deleted evidence item [{evidence_id}].")
        return True