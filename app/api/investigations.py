from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.alert import Alert
from app.models.access_log import AccessLog
from app.models.permission import Permission
from app.models.beneficiary import Beneficiary

router = APIRouter()


@router.get("/{alert_id}")
def get_complete_investigation(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    tx = alert.primary_transaction
    employee = alert.primary_employee
    customer = alert.primary_customer

    access_logs = []
    permissions = []
    beneficiaries = []

    if employee:
        access_logs = db.query(AccessLog).filter(AccessLog.employee_id == employee.id).all()
        permissions = db.query(Permission).filter(Permission.employee_id == employee.id).all()

    if tx and tx.source_account:
        beneficiaries = db.query(Beneficiary).filter(Beneficiary.account_id == tx.source_account_id).all()

    # Build chronological timeline
    timeline = []
    for log in access_logs:
        timeline.append({"timestamp": log.timestamp.isoformat(), "event": f"Employee action: {log.action}"})
    if tx:
        timeline.append({"timestamp": tx.timestamp.isoformat(),
                         "event": f"Transaction executed: {tx.transaction_code} for ₹{tx.amount}"})

    timeline.sort(key=lambda x: x["timestamp"])

    return {
        "alert": alert,
        "risk": {
            "risk_score": alert.risk_score,
            "risk_level": alert.risk_level
        },
        "reasons": [e.description for e in alert.evidence_items],
        "transactions": [tx] if tx else [],
        "employee": employee,
        "customer": customer,
        "permissions": permissions,
        "access_logs": access_logs,
        "beneficiaries": beneficiaries,
        "timeline": timeline,
        "graph": {"nodes": [], "edges": []},
        "evidence": alert.evidence_items,
        "related_alerts": []
    }