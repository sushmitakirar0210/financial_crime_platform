from datetime import datetime
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.account import Account
from app.models.alert import Alert
from app.core.logging import logger


def calculate_composite_risk_scores(db: Session):
    """
    Aggregates open alerts and behavioral metrics to calculate
    composite risk scores and update risk categories for customers.
    """
    logger.info("Running Composite Risk Engine calculation...")

    customers = db.query(Customer).all()
    updated_count = 0

    for cust in customers:
        # Count open high-severity alerts associated with this customer
        high_alerts = db.query(Alert).filter(
            Alert.severity == "HIGH",
            Alert.status == "OPEN"
        ).count()

        # Base score evaluation from initial risk profile
        base_score = 10.0
        if cust.risk_category == "HIGH":
            base_score += 40.0
        elif cust.risk_category == "MEDIUM":
            base_score += 20.0

        # Add increments based on active threats
        score_increment = min(high_alerts * 15.0, 50.0)
        final_risk_score = min(base_score + score_increment, 100.0)

        # Re-classify risk category dynamically
        if final_risk_score >= 70.0:
            cust.risk_category = "HIGH"
        elif final_risk_score >= 40.0:
            cust.risk_category = "MEDIUM"
        else:
            cust.risk_category = "LOW"

        updated_count += 1

    db.commit()
    logger.info(f"Risk engine execution complete. Updated risk profiles for {updated_count} customers.")
    return {"status": "success", "customers_evaluated": updated_count}