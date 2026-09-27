from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_code: str
    source_account_id: str
    destination_account_id: str
    amount: float
    currency: str = "INR"
    status: str = "COMPLETED"

class TransactionCreate(TransactionBase):
    """Schema for recording a new financial transaction."""
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class TransactionResponse(TransactionBase):
    """Schema for returning transaction details in API responses."""
    id: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects