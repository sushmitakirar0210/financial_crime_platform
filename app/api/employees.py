from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.employee import Employee
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
def get_employees(db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employees = db.query(Employee).all()
    return employees

@router.get("/{employee_id}")
def get_employee(employee_id: str, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.get("/{employee_id}/activity")
def get_employee_activity(employee_id: str, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.access_logs

@router.get("/{employee_id}/permissions")
def get_employee_permissions(employee_id: str, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.permissions