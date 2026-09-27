from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.models.case import Case
from app.core.security import get_current_user

router = APIRouter()


@router.get("/")
def get_dashboard_summary(
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve high-level intelligence and operational metrics for the compliance dashboard."""
    total_employees = db.query(Employee).count()
    total_customers = db.query(Customer).count()
    total_accounts = db.query(Account).count()
    total_transactions = db.query(Transaction).count()

    total_alerts = db.query(Alert).count()
    open_alerts = db.query(Alert).filter(Alert.status == "OPEN").count()
    high_severity_alerts = db.query(Alert).filter(Alert.severity == "HIGH").count()

    total_cases = db.query(Case).count()
    open_cases = db.query(Case).filter(Case.status == "OPEN").count()

    recent_alerts = db.query(Alert).order_by(Alert.id.desc()).limit(5).all()

    return {
        "metrics": {
            "total_employees": total_employees,
            "total_customers": total_customers,
            "total_accounts": total_accounts,
            "total_transactions": total_transactions,
            "total_alerts": total_alerts,
            "open_alerts": open_alerts,
            "high_severity_alerts": high_severity_alerts,
            "total_cases": total_cases,
            "open_cases": open_cases
        },
        "recent_alerts": recent_alerts
    }