import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.employee import Employee
from app.core.security import get_password_hash

client = TestClient(app)

@pytest.fixture
def db_session():
    """Provides a transactional database session for auth tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_login_success(db_session):
    """Test successful employee login and JWT token generation."""
    email = "auth.test@insightx.com"
    existing = db_session.query(Employee).filter(Employee.email == email).first()
    if not existing:
        emp = Employee(
            id="EMP-AUTH-TEST",
            employee_code="E9988",
            name="Auth Tester",
            email=email,
            hashed_password=get_password_hash("CorrectPassword123!"),
            department="COMPLIANCE",
            role="INVESTIGATOR",
            is_active=True
        )
        db_session.add(emp)
        db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "CorrectPassword123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(db_session):
    """Test login failure with an incorrect password."""
    email = "auth.test@insightx.com"
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "WrongPassword!"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json().get("detail", "")

def test_login_nonexistent_user():
    """Test login failure with a non-existent email."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nobody@insightx.com", "password": "SomePassword123!"}
    )
    assert response.status_code == 401