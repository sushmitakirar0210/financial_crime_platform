from datetime import datetime
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.core.logging import logger


def run_profile_mismatch_detection(db: Session):
    """
    Detects discrepancies where a customer's actual transaction volume
    significantly exceeds their declared expected monthly volume profile.
    """
    logger.info("Running Profile Mismatch risk detection engine...")
    alerts_generated = 0

    customers = db.query(Customer).all()
    for cust in customers:
        # Find all accounts owned by this customer
        accounts = db.query(Account).filter(Account.customer_id == cust.id).all()
        acc_ids = [acc.id for acc in accounts]

        if not acc_ids:
            continue

        # Calculate actual transaction volume (sum of amounts where account is the source)
        tx_amounts = db.query(Transaction.amount).filter(
            Transaction.source_account_id.in_(acc_ids)
        ).all()

        actual_volume = sum([t[0] for t in tx_amounts])
        expected_vol = cust.expected_monthly_volume or 100000.0

        # Flag if actual volume exceeds 2x the declared expected monthly volume
        if actual_volume > (expected_vol * 2.0):
            alert_id = f"ALT-PROF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{cust.id[:4]}"
            existing = db.query(Alert).filter(Alert.id == alert_id).first()

            if not existing:
                alert = Alert(
                    id=alert_id,
                    severity="HIGH",
                    status="OPEN",
                    description=f"Profile Mismatch: Actual transaction volume ({actual_volume:,.2f}) significantly exceeds declared expected monthly volume ({expected_vol:,.2f}) for customer '{cust.name}' (ID: {cust.customer_code}).",
                    rule_name="CUSTOMER_VOLUME_MISMATCH"
                )
                db.add(alert)
                alerts_generated += 1

    db.commit()
    logger.info(f"Profile mismatch detection completed. Generated {alerts_generated} new alerts.")
    return {"status": "success", "alerts_generated": alerts_generated}