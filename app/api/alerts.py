from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database.database import get_db
from app.models.alert import Alert
from app.models.employee import Employee
from app.core.security import get_current_user

router = APIRouter()


@router.get("/")
def get_alerts(
        severity: Optional[str] = None,
        status_filter: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve all intelligence alerts with optional filters for severity or investigation status."""
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    if status_filter:
        query = query.filter(Alert.status == status_filter.upper())
    return query.all()


@router.get("/{alert_id}")
def get_alert_by_id(
        alert_id: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve a specific intelligence alert and its associated transparent evidence trail."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.patch("/{alert_id}/status")
def update_alert_status(
        alert_id: str,
        new_status: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Update the status of an alert (e.g., OPEN, UNDER_REVIEW, CLOSED, ESCALATED)."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    valid_statuses = ["OPEN", "UNDER_REVIEW", "CLOSED", "ESCALATED"]
    upper_status = new_status.upper()
    if upper_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    alert.status = upper_status
    db.commit()
    db.refresh(alert)
    return {"message": "Alert status updated successfully", "alert": alert}