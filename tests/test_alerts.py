import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.alert import Alert
from app.models.employee import Employee
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def db_session():
    """Provides a transactional database session for tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def auth_headers(db_session):
    """Generates valid authentication headers using an existing or test employee."""
    employee = db_session.query(Employee).first()
    if not employee:
        # Fallback create if no employee seeded yet
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

def test_get_alerts_unauthorized():
    """Verify that accessing alerts without token returns 401 Unauthorized."""
    response = client.get("/api/v1/alerts/")
    assert response.status_code == 401

def test_get_alerts(db_session, auth_headers):
    """Test retrieving all intelligence alerts."""
    response = client.get("/api/v1/alerts/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_alerts_with_filters(db_session, auth_headers):
    """Test retrieving alerts filtered by severity or status."""
    response = client.get("/api/v1/alerts/?severity=HIGH&status_filter=OPEN", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for alert in data:
        assert alert["severity"] == "HIGH"
        assert alert["status"] == "OPEN"

def test_get_alert_by_id_not_found(auth_headers):
    """Test fetching a non-existent alert returns 404 Not Found."""
    response = client.get("/api/v1/alerts/ALT-NONEXISTENT", headers=auth_headers)
    assert response.status_code == 404

def test_update_alert_status_invalid(auth_headers):
    """Test updating an alert with an invalid status returns 400 Bad Request."""
    response = client.patch(
        "/api/v1/alerts/ALT-SAMPLE/status?new_status=INVALID_STATUS",
        headers=auth_headers
    )
    assert response.status_code == 400