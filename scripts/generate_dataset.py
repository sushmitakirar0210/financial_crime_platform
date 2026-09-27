import sys
import os
from datetime import datetime, timedelta

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal, engine, Base
from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.employee import Employee
from app.models.access_log import AccessLog
from app.core.security import get_password_hash
from app.core.logging import logger


def seed_database():
    """Seeds the database with robust sample data for INSIGHT-X."""
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        existing_cust_count = db.query(Customer).count()
        if existing_cust_count > 0:
            logger.info("Database already contains data. Skipping seeding process.")
            return

        logger.info("Seeding employees (investigators)...")
        emp1 = Employee(
            id="EMP-001",
            employee_code="E1001",
            name="Aarav Sharma",
            email="aarav.sharma@insightx.com",
            hashed_password=get_password_hash("SecurePass123!"),
            department="COMPLIANCE",
            role="SENIOR_INVESTIGATOR",
            is_active=True
        )
        emp2 = Employee(
            id="EMP-002",
            employee_code="E1002",
            name="Priya Deshmukh",
            email="priya.deshmukh@insightx.com",
            hashed_password=get_password_hash("SecurePass123!"),
            department="RISK",
            role="ANALYST",
            is_active=True
        )
        db.add_all([emp1, emp2])
        db.commit()

        logger.info("Seeding customers...")
        cust1 = Customer(
            id="CUST-001",
            customer_code="C1001",
            name="Rajesh Verma",
            email="rajesh.verma@example.com",
            phone="+919876543210",
            city="Pune",
            risk_category="HIGH",
            expected_monthly_volume=150000.0
        )
        cust2 = Customer(
            id="CUST-002",
            customer_code="C1002",
            name="Sneha Kulkarni",
            email="sneha.k@example.com",
            phone="+919123456789",
            city="Mumbai",
            risk_category="MEDIUM",
            expected_monthly_volume=300000.0
        )
        db.add_all([cust1, cust2])
        db.commit()

        logger.info("Seeding accounts...")
        acc1 = Account(
            id="ACC-001",
            account_number="100050001234",
            customer_id="CUST-001",
            account_type="CURRENT",
            currency="INR",
            balance=1250000.0,
            status="ACTIVE"
        )
        acc2 = Account(
            id="ACC-002",
            account_number="100050005678",
            customer_id="CUST-001",
            account_type="SAVINGS",
            currency="INR",
            balance=450000.0,
            status="ACTIVE"
        )
        acc3 = Account(
            id="ACC-003",
            account_number="200060009999",
            customer_id="CUST-002",
            account_type="CURRENT",
            currency="INR",
            balance=3200000.0,
            status="ACTIVE"
        )
        db.add_all([acc1, acc2, acc3])
        db.commit()

        logger.info("Seeding sample transactions...")
        now = datetime.utcnow()
        tx1 = Transaction(
            id="TXN-001",
            transaction_code="TRX998811",
            source_account_id="ACC-001",
            destination_account_id="ACC-003",
            amount=450000.0,
            currency="INR",
            status="COMPLETED",
            timestamp=now - timedelta(hours=2)
        )
        tx2 = Transaction(
            id="TXN-002",
            transaction_code="TRX998812",
            source_account_id="ACC-003",
            destination_account_id="ACC-002",
            amount=449000.0,
            currency="INR",
            status="COMPLETED",
            timestamp=now - timedelta(hours=1)
        )
        db.add_all([tx1, tx2])
        db.commit()

        logger.info("Seeding sample access logs (for insider threat rules)...")
        log1 = AccessLog(
            id="LOG-001",
            employee_id="EMP-002",
            resource_type="CUSTOMER_RECORD",
            resource_id="CUST-001",
            success=True,
            timestamp=now - timedelta(hours=5)  # Occurred at odd hours
        )
        db.add(log1)
        db.commit()

        logger.info("Dataset generation completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()