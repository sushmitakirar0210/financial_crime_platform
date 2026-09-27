from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    """Schema for employee/user login credentials."""
    email: str
    password: str

class Token(BaseModel):
    """Schema for the returned JWT access token."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for data extracted from a verified JWT token."""
    email: Optional[str] = None
    employee_id: Optional[str] = None