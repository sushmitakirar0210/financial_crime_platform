import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.case import Case
from app.models.employee import Employee
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def db_session():
    """Provides a transactional database session for case tests."""
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
            role="SENIOR_INVESTIGATOR",
            is_active=True
        )
        db_session.add(employee)
        db_session.commit()

    token = create_access_token(data={"sub": employee.email})
    return {"Authorization": f"Bearer {token}"}

def test_get_cases_unauthorized():
    """Verify that accessing cases without a token returns 401 Unauthorized."""
    response = client.get("/api/v1/cases/")
    assert response.status_code == 401

def test_get_cases(db_session, auth_headers):
    """Test retrieving all investigation cases."""
    response = client.get("/api/v1/cases/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_case(db_session, auth_headers):
    """Test creating a new investigation case dossier."""
    payload = {
        "title": "Suspicious Layering Activity",
        "description": "Investigating potential circular transactions across accounts.",
        "priority": "HIGH",
        "status": "OPEN",
        "alert_ids": []
    }
    response = client.post("/api/v1/cases/", json=payload, headers=auth_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["priority"] == "HIGH"
    assert "id" in data

def test_get_case_by_id_not_found(auth_headers):
    """Test fetching a non-existent case returns 404 Not Found."""
    response = client.get("/api/v1/cases/CASE-NONEXISTENT", headers=auth_headers)
    assert response.status_code == 404