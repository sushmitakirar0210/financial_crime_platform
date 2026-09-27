import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal
from app.services.detection.beneficiary_engine import run_beneficiary_detection
from app.services.detection.circular_engine import run_circular_detection
from app.services.detection.profile_mismatch_engine import run_profile_mismatch_detection
from app.services.detection.rule_engine import evaluate_structuring_rules, evaluate_insider_access_rules
from app.services.detection.risk_engine import calculate_composite_risk_scores
from app.core.logging import logger

def run_all_detections():
    """Executes all financial crime detection engines and updates risk profiles."""
    logger.info("Starting master compliance detection scan...")
    db = SessionLocal()

    try:
        logger.info("-" * 50)
        logger.info("1. Running Beneficiary Risk Detection...")
        ben_res = run_beneficiary_detection(db)
        logger.info(f"   Result: {ben_res}")

        logger.info("-" * 50)
        logger.info("2. Running Circular Layering Detection...")
        circ_res = run_circular_detection(db)
        logger.info(f"   Result: {circ_res}")

        logger.info("-" * 50)
        logger.info("3. Running Profile Mismatch Detection...")
        prof_res = run_profile_mismatch_detection(db)
        logger.info(f"   Result: {prof_res}")

        logger.info("-" * 50)
        logger.info("4. Evaluating Transaction Structuring Rules...")
        struct_res = evaluate_structuring_rules(db)
        logger.info(f"   Result: {struct_res}")

        logger.info("-" * 50)
        logger.info("5. Evaluating Insider Access Rules...")
        insider_res = evaluate_insider_access_rules(db)
        logger.info(f"   Result: {insider_res}")

        logger.info("-" * 50)
        logger.info("6. Calculating Composite Risk Scores & Reclassifying Risk...")
        risk_res = calculate_composite_risk_scores(db)
        logger.info(f"   Result: {risk_res}")

        logger.info("-" * 50)
        logger.info("Master compliance detection scan completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during detection execution: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_all_detections()