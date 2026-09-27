import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

def run_isolation_forest(db: Session):
    transactions = db.query(Transaction).all()
    if len(transactions) < 10:
        return {}

    amounts = np.array([t.amount for t in transactions]).reshape(-1, 1)
    clf = IsolationForest(contamination=0.05, random_state=42)
    preds = clf.fit_predict(amounts)
    scores = clf.decision_function(amounts)

    anomalies = {}
    for idx, tx in enumerate(transactions):
        if preds[idx] == -1:
            anomalies[tx.id] = {
                "anomaly": True,
                "anomaly_score": float(abs(scores[idx])),
                "features": {"amount": tx.amount}
            }
    return anomalies