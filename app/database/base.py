"""
Database Base Module.
Defines the declarative base class for all SQLAlchemy models in the INSIGHT-X platform.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy database models."""
    pass

# Import all models here so that Base.metadata has full visibility
# of all tables during creation, dropping, or migrations.
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.account import Account
from app.models.beneficiary import Beneficiary
from app.models.permission import Permission
from app.models.access_log import AccessLog
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.models.case import Case