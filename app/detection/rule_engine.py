from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.access_log import AccessLog
from app.models.alert import Alert
from app.core.config import settings
from app.core.logging import logger


def evaluate_structuring_rules(db: Session):
    """
    Detects structuring (smurfing) where multiple transactions
    just below the reporting threshold occur within a time window.
    """
    logger.info("Evaluating structuring rules...")
    alerts_created = 0

    # Query recent completed transactions
    transactions = db.query(Transaction).filter(Transaction.status == "COMPLETED").all()

    # Group by source account
    account_txs = {}
    for tx in transactions:
        if tx.source_account_id not in account_txs:
            account_txs[tx.source_account_id] = []
        account_txs[tx.source_account_id].append(tx)

    for acc_id, txs in account_txs.items():
        # Sort by timestamp
        sorted_txs = sorted(txs, key=lambda x: x.timestamp)

        for i in range(len(sorted_txs)):
            window_txs = [sorted_txs[i]]
            for j in range(i + 1, len(sorted_txs)):
                time_diff = sorted_txs[j].timestamp - sorted_txs[i].timestamp
                if time_diff <= timedelta(minutes=settings.STRUCTURING_WINDOW_MINUTES):
                    window_txs.append(sorted_txs[j])
                else:
                    break

            # Check if count meets criteria and amounts are near threshold
            if len(window_txs) >= settings.STRUCTURING_MIN_TRANSACTIONS:
                total_amt = sum([t.amount for t in window_txs])
                # Verify they are individual transactions below the direct threshold but accumulating high volume
                if all(t.amount < settings.STRUCTURING_THRESHOLD for t in
                       window_txs) and total_amt >= settings.STRUCTURING_THRESHOLD:
                    alert_id = f"ALT-STRUCT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{acc_id[:4]}"
                    existing = db.query(Alert).filter(Alert.id == alert_id).first()

                    if not existing:
                        alert = Alert(
                            id=alert_id,
                            severity="HIGH",
                            status="OPEN",
                            description=f"Structuring rule triggered: {len(window_txs)} transactions totaling {total_amt:,.2f} executed within {settings.STRUCTURING_WINDOW_MINUTES} minutes on account {acc_id}.",
                            rule_name="STRUCTURING_DETECTION"
                        )
                        db.add(alert)
                        alerts_created += 1
                        break

    db.commit()
    logger.info(f"Structuring evaluation completed. Generated {alerts_created} alerts.")
    return {"rule": "STRUCTURING_DETECTION", "alerts_generated": alerts_created}


def evaluate_insider_access_rules(db: Session):
    """
    Detects unauthorized or suspicious after-hours employee access
    to sensitive customer accounts.
    """
    logger.info("Evaluating insider access rules...")
    alerts_created = 0

    logs = db.query(AccessLog).filter(AccessLog.success == True).all()
    for log in logs:
        if log.timestamp:
            hour = log.timestamp.hour
            # Check if access occurred outside standard working hours
            if hour < settings.WORK_START_HOUR or hour > settings.WORK_END_HOUR:
                alert_id = f"ALT-INSIDER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{log.employee_id[:4]}"
                existing = db.query(Alert).filter(Alert.id == alert_id).first()

                if not existing:
                    alert = Alert(
                        id=alert_id,
                        severity="MEDIUM",
                        status="OPEN",
                        description=f"After-hours access detected: Employee {log.employee_id} accessed resource {log.resource_type} at {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} (Outside work hours).",
                        rule_name="AFTER_HOURS_INSIDER_ACCESS"
                    )
                    db.add(alert)
                    alerts_created += 1

    db.commit()
    logger.info(f"Insider access rule evaluation completed. Generated {alerts_created} alerts.")
    return {"rule": "AFTER_HOURS_INSIDER_ACCESS", "alerts_generated": alerts_created}


def run_all_rule_engines(db: Session):
    """Executes all defined compliance and anomaly rule engines."""
    struct_res = evaluate_structuring_rules(db)
    insider_res = evaluate_insider_access_rules(db)

    return {
        "status": "success",
        "results": [struct_res, insider_res]
    }