import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.transaction import Transaction
from app.models.employee import Employee
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def db_session():
    """Provides a transactional database session for transaction tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def auth_headers(db_session):
    """Generates valid authentication headers for test requests."""
    employee = db_session.query(Employee).first()
    if not employee:
        employee = Employee(
            id="EMP-TEST",
            employee_code="E9999",
            name="Test Investigator",
            email="test.investigator@insightx.com",
            hashed_password="hashed_dummy_password",
            department="COMPLIANCE",
            role="SENIOR_INVESTIGATOR"
        )
        db_session.add(employee)
        db_session.commit()

    token = create_access_token(data={"sub": employee.email})
    return {"Authorization": f"Bearer {token}"}
def test_get_transactions_unauthorized():
    """Verify that accessing transactions without a token returns 401 Unauthorized."""
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 401

def test_get_transactions(db_session, auth_headers):
    """Test retrieving all financial transactions with optional filters."""
    response = client.get("/api/v1/transactions/?min_amount=100.0", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_transaction(db_session, auth_headers):
    """Test recording a new financial transaction into the system."""
    payload = {
        "transaction_code": "TRX-TEST-8888",
        "source_account_id": "ACC-001",
        "destination_account_id": "ACC-002",
        "amount": 75000.0,
        "currency": "INR",
        "status": "COMPLETED"
    }
    response = client.post("/api/v1/transactions/", json=payload, headers=auth_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["transaction_code"] == payload["transaction_code"]
    assert data["amount"] == 75000.0
    assert "id" in data