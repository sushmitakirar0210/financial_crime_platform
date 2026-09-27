import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import engine, Base
from app.core.logging import logger

# Import all models so Base knows about them before dropping/creating tables
from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.employee import Employee
from app.models.alert import Alert
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.access_log import AccessLog


def reset_database():
    """Drops all existing database tables and recreates them clean."""
    logger.warning("Dropping all existing database tables...")
    Base.metadata.drop_all(bind=engine)

    logger.info("Recreating database tables from models...")
    Base.metadata.create_all(bind=engine)

    logger.info("Database reset completed successfully! All tables are now clean.")


if __name__ == "__main__":
    reset_database()