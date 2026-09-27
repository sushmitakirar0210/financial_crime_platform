from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.access_log import AccessLog
from app.models.transaction import Transaction
from app.models.permission import Permission


def detect_insider_access(db: Session, transaction: Transaction, window_minutes: int = 30):
    if not transaction.source_account_id:
        return None

    source_acc = transaction.source_account
    if not source_acc:
        return None

    customer_id = source_acc.customer_id
    tx_time = transaction.timestamp
    window_start = tx_time - timedelta(minutes=window_minutes)

    # Find employee access logs to this customer or account right before the transaction
    logs = db.query(AccessLog).filter(
        AccessLog.customer_id == customer_id,
        AccessLog.timestamp >= window_start,
        AccessLog.timestamp <= tx_time
    ).all()

    if not logs:
        return None

    evidence_list = []
    for log in logs:
        # Check if employee has permission
        permission = db.query(Permission).filter(
            Permission.employee_id == log.employee_id,
            Permission.status == "ACTIVE"
        ).first()

        time_diff = int((tx_time - log.timestamp).total_seconds() / 60)
        evidence_list.append({
            "evidence_type": "ACCESS_LOG",
            "title": "Employee accessed customer before transfer",
            "description": f"Employee {log.employee_id} accessed customer {customer_id} {time_diff} minutes before transaction {transaction.transaction_code}.",
            "source_type": "access_log",
            "source_id": log.id,
            "severity": "HIGH",
            "meta_data": {
                "employee_id": log.employee_id,
                "customer_id": customer_id,
                "minutes_before_transaction": time_diff,
                "transaction_id": transaction.id
            }
        })

    return {
        "triggered": True,
        "rule_code": "INSIDER_ACCESS_BEFORE_TRANSFER",
        "severity": "HIGH",
        "risk_contribution": 35,
        "title": "Potential Insider Activity: Access Before Transfer",
        "description": f"Detected employee access to customer profile shortly before large funds movement.",
        "evidence": evidence_list
    }