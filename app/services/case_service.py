from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.case import Case
from app.models.alert import Alert
from app.core.logging import logger


class CaseService:
    @staticmethod
    def create_case(
            db: Session,
            title: str,
            description: Optional[str] = None,
            priority: str = "MEDIUM",
            status: str = "OPEN",
            assigned_employee_id: Optional[str] = None,
            alert_ids: Optional[List[str]] = None
    ) -> Case:
        """Create and persist a new investigation case, optionally linking and escalating alerts."""
        case_id = f"CASE-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{abs(hash(title)) % 10000:04d}"

        new_case = Case(
            id=case_id,
            title=title,
            description=description,
            priority=priority.upper(),
            status=status.upper(),
            assigned_employee_id=assigned_employee_id
        )
        db.add(new_case)

        # Link and escalate associated alerts if provided
        if alert_ids:
            alerts = db.query(Alert).filter(Alert.id.in_(alert_ids)).all()
            for alert in alerts:
                alert.case_id = case_id
                alert.status = "ESCALATED"

        db.commit()
        db.refresh(new_case)
        logger.info(f"Created investigation case [{case_id}] with priority '{priority}'.")
        return new_case

    @staticmethod
    def update_case(
            db: Session,
            case_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            priority: Optional[str] = None,
            status: Optional[str] = None,
            assigned_employee_id: Optional[str] = None
    ) -> Optional[Case]:
        """Update an existing investigation case."""
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None

        if title is not None:
            case.title = title
        if description is not None:
            case.description = description
        if priority is not None:
            case.priority = priority.upper()
        if status is not None:
            case.status = status.upper()
        if assigned_employee_id is not None:
            case.assigned_employee_id = assigned_employee_id

        db.commit()
        db.refresh(case)
        logger.info(f"Updated investigation case [{case_id}].")
        return case