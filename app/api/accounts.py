from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.beneficiary import Beneficiary
from app.models.employee import Employee
from app.core.security import get_current_user

router = APIRouter()


@router.get("/")
def get_accounts(
        customer_id: Optional[str] = None,
        status_filter: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve all accounts with optional filtering by customer ID or status."""
    query = db.query(Account)
    if customer_id:
        query = query.filter(Account.customer_id == customer_id)
    if status_filter:
        query = query.filter(Account.status == status_filter)
    return query.all()


@router.get("/{account_id}")
def get_account_by_id(
        account_id: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve a specific account record by its unique identifier."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account


@router.get("/{account_id}/transactions")
def get_account_transactions(
        account_id: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve all financial transactions where the account acts as a source or destination."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    transactions = db.query(Transaction).filter(
        (Transaction.source_account_id == account_id) |
        (Transaction.destination_account_id == account_id)
    ).all()
    return transactions


@router.get("/{account_id}/beneficiaries")
def get_account_beneficiaries(
        account_id: str,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    """Retrieve all linked beneficiaries associated with this account."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    beneficiaries = db.query(Beneficiary).filter(Beneficiary.account_id == account_id).all()
    return beneficiaries