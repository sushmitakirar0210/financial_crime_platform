from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.alert import Alert
from app.core.logging import logger


class AlertService:
    @staticmethod
    def create_alert(
            db: Session,
            description: str,
            rule_name: str,
            severity: str = "MEDIUM",
            status: str = "OPEN",
            case_id: Optional[str] = None
    ) -> Alert:
        """Create and persist a new intelligence alert."""
        alert_id = f"ALT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{abs(hash(description)) % 10000:04d}"

        new_alert = Alert(
            id=alert_id,
            severity=severity.upper(),
            status=status.upper(),
            description=description,
            rule_name=rule_name,
            case_id=case_id
        )
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        logger.info(f"Created new alert [{alert_id}] with rule '{rule_name}' and severity '{severity}'.")
        return new_alert

    @staticmethod
    def update_alert_status(
            db: Session,
            alert_id: str,
            new_status: str
    ) -> Optional[Alert]:
        """Update the status of an existing alert (e.g., OPEN, INVESTIGATING, RESOLVED, DISMISSED)."""
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None

        alert.status = new_status.upper()
        db.commit()
        db.refresh(alert)
        logger.info(f"Updated alert [{alert_id}] status to '{alert.status}'.")
        return alert

    @staticmethod
    def escalate_alert_to_case(
            db: Session,
            alert_id: str,
            case_id: str
    ) -> Optional[Alert]:
        """Link an alert to an investigation case and mark it as escalated."""
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None

        alert.case_id = case_id
        alert.status = "ESCALATED"
        db.commit()
        db.refresh(alert)
        logger.info(f"Escalated alert [{alert_id}] to case [{case_id}].")
        return alert