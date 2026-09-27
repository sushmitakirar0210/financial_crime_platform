from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

def detect_transaction_splitting(db: Session, transaction: Transaction, threshold: float, window_minutes: int, min_txns: int):
    window_start = transaction.timestamp - timedelta(minutes=window_minutes)
    window_end = transaction.timestamp + timedelta(minutes=window_minutes)

    similar_txns = db.query(Transaction).filter(
        Transaction.source_account_id == transaction.source_account_id,
        Transaction.id != transaction.id,
        Transaction.timestamp >= window_start,
        Transaction.timestamp <= window_end,
        Transaction.amount < threshold
    ).all()

    if len(similar_txns) + 1 >= min_txns:
        all_txns = similar_txns + [transaction]
        total_sum = sum(t.amount for t in all_txns)
        evidence = [{
            "evidence_type": "TRANSACTION",
            "title": "Transaction Structuring / Splitting Detected",
            "description": f"Found {len(all_txns)} transactions totaling {total_sum} from account {transaction.source_account_id} within {window_minutes} minutes.",
            "source_type": "transaction",
            "source_id": transaction.id,
            "severity": "HIGH",
            "meta_data": {
                "transaction_ids": [t.id for t in all_txns],
                "total_amount": total_sum,
                "count": len(all_txns)
            }
        }]
        return {
            "triggered": True,
            "rule_code": "TRANSACTION_SPLITTING",
            "severity": "HIGH",
            "risk_contribution": 30,
            "title": "Transaction Structuring (Smurfing/Splitting)",
            "description": "Multiple transactions just under reporting thresholds executed in close succession.",
            "evidence": evidence
        }
    return None