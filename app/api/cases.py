from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.database.database import get_db
from app.models.case import Case
from app.models.alert import Alert
from app.models.employee import Employee
from app.core.security import get_current_user

router = APIRouter()


class CaseCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM"
    assigned_employee_id: Optional[str] = None
    alert_ids: Optional[List[str]] = []


@router.get("/")
def get_cases(
        priority: Optional[str] = None,
        status_filter: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve all investigation cases with optional filters for priority or status."""
    query = db.query(Case)
    if priority:
        query = query.filter(Case.priority == priority.upper())
    if status_filter:
        query = query.filter(Case.status == status_filter.upper())
    return query.all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_case(
        payload: CaseCreateRequest,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Create a new investigation case, optionally linking alerts and assigning an investigator."""
    new_case = Case(
        id=f"CASE-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        title=payload.title,
        description=payload.description,
        priority=payload.priority.upper(),
        status="OPEN",
        assigned_employee_id=payload.assigned_employee_id or current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # Link alerts if provided
    if payload.alert_ids:
        alerts = db.query(Alert).filter(Alert.id.in_(payload.alert_ids)).all()
        for alert in alerts:
            alert.case_id = new_case.id
            alert.status = "ESCALATED"
        db.commit()

    return {"message": "Case created successfully", "case": new_case}


@router.get("/{case_id}")
def get_case_by_id(
        case_id: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve details of a specific investigation case along with its linked alerts and evidence."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    return case


@router.patch("/{case_id}/status")
def update_case_status(
        case_id: str,
        new_status: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Update the lifecycle status of a case (e.g., OPEN, IN_PROGRESS, RESOLVED, CLOSED)."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )

    valid_statuses = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]
    upper_status = new_status.upper()
    if upper_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    case.status = upper_status
    db.commit()
    db.refresh(case)
    return {"message": "Case status updated successfully", "case": case}