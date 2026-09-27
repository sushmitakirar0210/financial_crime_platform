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
    """Provides a transactional database session for investigation tests."""
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

def test_add_investigation_note_unauthorized():
    """Verify that adding an investigation note without a token returns 401 Unauthorized."""
    response = client.post("/api/v1/investigation/notes", json={"case_id": "CASE-001", "note_content": "Test note"})
    assert response.status_code == 401

def test_add_investigation_note(db_session, auth_headers):
    """Test adding a secure compliance note to an active investigation case."""
    # Ensure a sample case exists or use a dummy ID
    payload = {
        "case_id": "CASE-TEST-001",
        "note_content": "Reviewed transaction logs and verified high risk indicators."
    }
    response = client.post("/api/v1/investigation/notes", json=payload, headers=auth_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["case_id"] == payload["case_id"]
    assert data["note_content"] == payload["note_content"]

def test_get_investigation_dossier_not_found(auth_headers):
    """Test fetching a dossier for a non-existent case returns 404 Not Found."""
    response = client.get("/api/v1/investigation/dossier/CASE-NONEXISTENT", headers=auth_headers)
    assert response.status_code == 404