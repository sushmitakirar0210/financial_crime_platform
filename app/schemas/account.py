from pydantic import BaseModel
from typing import Optional

class AccountBase(BaseModel):
    account_number: str
    customer_id: str
    account_type: str = "SAVINGS"
    currency: str = "INR"
    balance: float = 0.0
    status: str = "ACTIVE"

class AccountCreate(AccountBase):
    """Schema for creating a new bank account."""
    id: Optional[str] = None

class AccountResponse(AccountBase):
    """Schema for returning account details in API responses."""
    id: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy model instances to be converted to Pydantic models automatically