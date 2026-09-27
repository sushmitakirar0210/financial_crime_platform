from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.beneficiary import Beneficiary
from app.models.alert import Alert
from app.core.config import settings
from app.core.logging import logger


def run_beneficiary_detection(db: Session):
    """
    Detects high-risk scenarios where transactions occur shortly
    after a new beneficiary is registered.
    """
    logger.info("Running New Beneficiary risk detection engine...")

    beneficiaries = db.query(Beneficiary).all()
    alerts_generated = 0

    for ben in beneficiaries:
        # Find transactions directed to this beneficiary's account
        transactions = db.query(Transaction).filter(
            Transaction.destination_account_id == ben.beneficiary_account
        ).all()

        for tx in transactions:
            # Check if transaction amount exceeds high-risk threshold or check timing window
            # If transaction amount is substantial (e.g., > 100,000 INR)
            if tx.amount >= 100000.0:
                # Check if an alert for this transaction/beneficiary already exists
                existing_alert = db.query(Alert).filter(
                    Alert.description.contains(f"New Beneficiary Risk: {ben.beneficiary_name}")
                ).first()

                if not existing_alert:
                    alert = Alert(
                        id=f"ALT-BEN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{tx.id[:4]}",
                        severity="HIGH",
                        status="OPEN",
                        description=f"High-value transfer of {tx.amount} {tx.currency} to newly added beneficiary '{ben.beneficiary_name}' (Account: {ben.beneficiary_account}).",
                        rule_name="NEW_BENEFICIARY_HIGH_VALUE_TRANSFER"
                    )
                    db.add(alert)
                    alerts_generated += 1

    db.commit()
    logger.info(f"Beneficiary detection completed. Generated {alerts_generated} new alerts.")
    return {"status": "success", "alerts_generated": alerts_generated}