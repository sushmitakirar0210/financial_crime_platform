from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database.database import get_db
from app.models.customer import Customer
from app.models.account import Account
from app.models.employee import Employee
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
def get_customers(
    risk_category: Optional[str] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Retrieve all customer profiles with optional filtering by risk category or city."""
    query = db.query(Customer)
    if risk_category:
        query = query.filter(Customer.risk_category == risk_category.upper())
    if city:
        query = query.filter(Customer.city.ilike(f"%{city}%"))
    return query.all()

@router.get("/{customer_id}")
def get_customer_by_id(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Retrieve a specific customer profile by their unique identifier."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.get("/{customer_id}/accounts")
def get_customer_accounts(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Retrieve all bank accounts owned by a specific customer."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    accounts = db.query(Account).filter(Account.customer_id == customer_id).all()
    return accounts