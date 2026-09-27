from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.core.logging import logger


def run_circular_detection(db: Session):
    """
    Detects circular transaction patterns (layering/round-tripping)
    where funds flow from A -> B -> C -> A.
    """
    logger.info("Running Circular Transaction detection engine...")

    # Fetch all completed transactions
    transactions = db.query(Transaction).filter(Transaction.status == "COMPLETED").all()

    # Map out outgoing transactions per account: source -> list of (destination, amount, timestamp, tx_id)
    outflows = {}
    for tx in transactions:
        if tx.source_account_id not in outflows:
            outflows[tx.source_account_id] = []
        outflows[tx.source_account_id].append({
            "dest": tx.destination_account_id,
            "amount": tx.amount,
            "timestamp": tx.timestamp,
            "id": tx.id
        })

    alerts_generated = 0
    detected_cycles = set()

    # Simple 3-step cycle detection: A -> B -> C -> A
    for acc_a, txs_a in outflows.items():
        for tx1 in txs_a:
            acc_b = tx1["dest"]
            if acc_b == acc_a or acc_b not in outflows:
                continue

            for tx2 in outflows[acc_b]:
                acc_c = tx2["dest"]
                # Check if tx2 happens after tx1
                if acc_c == acc_b or tx2["timestamp"] < tx1["timestamp"]:
                    continue
                if acc_c not in outflows:
                    continue

                for tx3 in outflows[acc_c]:
                    # Check if tx3 loops back to acc_a and happens after tx2
                    if tx3["dest"] == acc_a and tx3["timestamp"] > tx2["timestamp"]:
                        # Ensure time window is tight (e.g., within 24 hours total)
                        time_diff = tx3["timestamp"] - tx1["timestamp"]
                        if timedelta(0) <= time_diff <= timedelta(hours=24):
                            cycle_key = tuple(sorted([acc_a, acc_b, acc_c]))
                            if cycle_key not in detected_cycles:
                                detected_cycles.add(cycle_key)

                                # Create an alert for this circular flow
                                alert_id = f"ALT-CIRC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{tx1['id'][:4]}"
                                existing = db.query(Alert).filter(Alert.id == alert_id).first()

                                if not existing:
                                    alert = Alert(
                                        id=alert_id,
                                        severity="HIGH",
                                        status="OPEN",
                                        description=f"Circular transaction pattern detected across accounts: {acc_a} -> {acc_b} -> {acc_c} -> {acc_a} within {time_diff.total_seconds() / 3600:.1f} hours.",
                                        rule_name="CIRCULAR_TRANSACTION_LAYERING"
                                    )
                                    db.add(alert)
                                    alerts_generated += 1

    db.commit()
    logger.info(f"Circular detection completed. Generated {alerts_generated} new alerts.")
    return {"status": "success", "cycles_detected": len(detected_cycles), "alerts_generated": alerts_generated}