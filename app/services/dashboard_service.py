from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.alert import Alert
from app.models.case import Case
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.core.logging import logger

class DashboardService:
    @staticmethod
    def get_dashboard_metrics(db: Session) -> dict:
        """
        Aggregates core platform metrics for compliance monitoring and executive reporting.
        """
        logger.info("Aggregating dashboard compliance metrics...")

        # Alert metrics
        total_alerts = db.query(Alert).count()
        open_alerts = db.query(Alert).filter(Alert.status == "OPEN").count()
        high_severity_alerts = db.query(Alert).filter(Alert.severity == "HIGH", Alert.status == "OPEN").count()

        # Case metrics
        total_cases = db.query(Case).count()
        open_cases = db.query(Case).filter(Case.status == "OPEN").count()

        # Customer risk distribution
        high_risk_customers = db.query(Customer).filter(Customer.risk_category == "HIGH").count()
        medium_risk_customers = db.query(Customer).filter(Customer.risk_category == "MEDIUM").count()
        low_risk_customers = db.query(Customer).filter(Customer.risk_category == "LOW").count()
        total_customers = db.query(Customer).count()

        # Transaction metrics
        total_transactions = db.query(Transaction).count()
        total_transaction_volume = db.query(func.sum(Transaction.amount)).scalar() or 0.0

        return {
            "status": "success",
            "metrics": {
                "alerts": {
                    "total": total_alerts,
                    "open": open_alerts,
                    "high_severity_open": high_severity_alerts
                },
                "cases": {
                    "total": total_cases,
                    "open": open_cases
                },
                "customers": {
                    "total": total_customers,
                    "high_risk": high_risk_customers,
                    "medium_risk": medium_risk_customers,
                    "low_risk": low_risk_customers
                },
                "transactions": {
                    "total_count": total_transactions,
                    "total_volume_inr": total_transaction_volume
                }
            }
        }