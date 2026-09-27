import pytest
from app.database.database import SessionLocal
from app.services.detection.beneficiary_engine import run_beneficiary_detection
from app.services.detection.circular_engine import run_circular_detection
from app.services.detection.profile_mismatch_engine import run_profile_mismatch_detection
from app.services.detection.rule_engine import evaluate_structuring_rules, evaluate_insider_access_rules
from app.services.detection.risk_engine import calculate_composite_risk_scores

@pytest.fixture
def db_session():
    """Provides a transactional database session for detection tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_beneficiary_detection_engine(db_session):
    """Test running beneficiary risk detection."""
    result = run_beneficiary_detection(db_session)
    assert result is not None
    assert isinstance(result, dict)

def test_circular_detection_engine(db_session):
    """Test running circular layering detection."""
    result = run_circular_detection(db_session)
    assert result is not None
    assert isinstance(result, dict)

def test_profile_mismatch_detection_engine(db_session):
    """Test running profile volume mismatch detection."""
    result = run_profile_mismatch_detection(db_session)
    assert result is not None
    assert isinstance(result, dict)

def test_structuring_rule_engine(db_session):
    """Test evaluating transaction structuring (smurfing) rules."""
    result = evaluate_structuring_rules(db_session)
    assert result is not None
    assert isinstance(result, dict)

def test_insider_access_rule_engine(db_session):
    """Test evaluating insider access after-hours rules."""
    result = evaluate_insider_access_rules(db_session)
    assert result is not None
    assert isinstance(result, dict)

def test_composite_risk_scoring_engine(db_session):
    """Test calculating composite risk scores and customer reclassification."""
    result = calculate_composite_risk_scores(db_session)
    assert result is not None
    assert isinstance(result, dict)