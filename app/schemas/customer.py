from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    customer_code: str
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    risk_category: str = "LOW"
    expected_monthly_volume: float = 100000.0

class CustomerCreate(CustomerBase):
    """Schema for registering a new customer profile."""
    id: Optional[str] = None

class CustomerResponse(CustomerBase):
    """Schema for returning customer details in API responses."""
    id: str

    class Config:
        from_attributes = True  # Automatically converts SQLAlchemy model instances to Pydantic objects