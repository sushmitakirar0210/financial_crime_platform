from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.transaction import Transaction
from app.core.logging import logger


class TransactionService:
    @staticmethod
    def create_transaction(
            db: Session,
            transaction_code: str,
            source_account_id: str,
            destination_account_id: str,
            amount: float,
            currency: str = "INR",
            status: str = "COMPLETED"
    ) -> Transaction:
        """Record and persist a new financial transaction."""
        tx_id = f"TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{abs(hash(transaction_code)) % 10000:04d}"

        new_transaction = Transaction(
            id=tx_id,
            transaction_code=transaction_code,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id,
            amount=amount,
            currency=currency.upper(),
            status=status.upper(),
            timestamp=datetime.utcnow()
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        logger.info(f"Recorded new transaction [{tx_id}] of amount {amount:,.2f} {currency}.")
        return new_transaction

    @staticmethod
    def get_transactions(
            db: Session,
            source_account_id: Optional[str] = None,
            destination_account_id: Optional[str] = None,
            min_amount: Optional[float] = None,
            max_amount: Optional[float] = None
    ) -> List[Transaction]:
        """Retrieve transactions with optional filtering by account and amount ranges."""
        query = db.query(Transaction)
        if source_account_id:
            query = query.filter(Transaction.source_account_id == source_account_id)
        if destination_account_id:
            query = query.filter(Transaction.destination_account_id == destination_account_id)
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)

        return query.all()