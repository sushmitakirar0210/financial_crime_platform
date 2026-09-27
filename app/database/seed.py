import os
import pandas as pd
from datetime import datetime
from app.database.database import SessionLocal, engine, Base
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.account import Account
from app.models.beneficiary import Beneficiary
from app.models.permission import Permission
from app.models.access_log import AccessLog
from app.models.transaction import Transaction
from app.core.security import get_password_hash

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Starting database seeding from CSV files...")

    # 1. Seed Employees
    emp_file = os.path.join(DATA_DIR, "employees.csv")
    if os.path.exists(emp_file):
        df_emp = pd.read_csv(emp_file)
        for _, row in df_emp.iterrows():
            emp = Employee(
                id=str(row.get("id")),
                employee_code=str(row.get("employee_code")),
                name=str(row.get("name")),
                email=str(row.get("email")),
                hashed_password=get_password_hash("Password@123"),
                department=str(row.get("department", "Operations")),
                role=str(row.get("role", "Analyst")),
                branch=str(row.get("branch", "Mumbai")),
                status=str(row.get("status", "ACTIVE")),
                risk_level=str(row.get("risk_level", "LOW"))
            )
            db.merge(emp)
        db.commit()
        print(f"Loaded employees from {emp_file}")

    # 2. Seed Customers
    cust_file = os.path.join(DATA_DIR, "customers.csv")
    if os.path.exists(cust_file):
        df_cust = pd.read_csv(cust_file)
        for _, row in df_cust.iterrows():
            cust = Customer(
                id=str(row.get("id")),
                customer_code=str(row.get("customer_code")),
                name=str(row.get("name")),
                customer_type=str(row.get("customer_type", "INDIVIDUAL")),
                occupation=str(row.get("occupation", "")),
                industry=str(row.get("industry", "")),
                city=str(row.get("city", "Mumbai")),
                country=str(row.get("country", "India")),
                risk_category=str(row.get("risk_category", "LOW")),
                expected_monthly_volume=float(row.get("expected_monthly_volume", 100000.0))
            )
            db.merge(cust)
        db.commit()
        print(f"Loaded customers from {cust_file}")

    # 3. Seed Accounts
    acc_file = os.path.join(DATA_DIR, "accounts.csv")
    if os.path.exists(acc_file):
        df_acc = pd.read_csv(acc_file)
        for _, row in df_acc.iterrows():
            acc = Account(
                id=str(row.get("id")),
                account_number=str(row.get("account_number")),
                customer_id=str(row.get("customer_id")),
                account_type=str(row.get("account_type", "SAVINGS")),
                currency=str(row.get("currency", "INR")),
                balance=float(row.get("balance", 0.0)),
                status=str(row.get("status", "ACTIVE"))
            )
            db.merge(acc)
        db.commit()
        print(f"Loaded accounts from {acc_file}")

    # 4. Seed Beneficiaries
    ben_file = os.path.join(DATA_DIR, "beneficiaries.csv")
    if os.path.exists(ben_file):
        df_ben = pd.read_csv(ben_file)
        for _, row in df_ben.iterrows():
            ben = Beneficiary(
                id=str(row.get("id")),
                beneficiary_code=str(row.get("beneficiary_code")),
                account_id=str(row.get("account_id")),
                beneficiary_name=str(row.get("beneficiary_name")),
                beneficiary_account=str(row.get("beneficiary_account")),
                bank_name=str(row.get("bank_name")),
                created_by_employee_id=str(row.get("created_by_employee_id")) if pd.notna(row.get("created_by_employee_id")) else None,
                status=str(row.get("status", "ACTIVE"))
            )
            db.merge(ben)
        db.commit()
        print(f"Loaded beneficiaries from {ben_file}")

    # 5. Seed Permissions
    perm_file = os.path.join(DATA_DIR, "permissions.csv")
    if os.path.exists(perm_file):
        df_perm = pd.read_csv(perm_file)
        for _, row in df_perm.iterrows():
            perm = Permission(
                id=str(row.get("id")),
                employee_id=str(row.get("employee_id")),
                permission_type=str(row.get("permission_type")),
                resource_type=str(row.get("resource_type")),
                resource_id=str(row.get("resource_id")) if pd.notna(row.get("resource_id")) else None,
                granted_by=str(row.get("granted_by", "SYSTEM")),
                status=str(row.get("status", "ACTIVE"))
            )
            db.merge(perm)
        db.commit()
        print(f"Loaded permissions from {perm_file}")

    # 6. Seed Access Logs & Login Events
    log_file = os.path.join(DATA_DIR, "access_logs.csv")
    if os.path.exists(log_file):
        df_log = pd.read_csv(log_file)
        for _, row in df_log.iterrows():
            log = AccessLog(
                id=str(row.get("id")),
                employee_id=str(row.get("employee_id")),
                customer_id=str(row.get("customer_id")) if pd.notna(row.get("customer_id")) else None,
                account_id=str(row.get("account_id")) if pd.notna(row.get("account_id")) else None,
                action=str(row.get("action")),
                resource_type=str(row.get("resource_type", "SYSTEM")),
                resource_id=str(row.get("resource_id")) if pd.notna(row.get("resource_id")) else None,
                ip_address=str(row.get("ip_address", "127.0.0.1")),
                device_id=str(row.get("device_id", "DEV-01")),
                timestamp=pd.to_datetime(row.get("timestamp")) if pd.notna(row.get("timestamp")) else datetime.utcnow(),
                success=bool(row.get("success", True))
            )
            db.merge(log)
        db.commit()
        print(f"Loaded access logs from {log_file}")

    # 7. Seed Transactions
    tx_file = os.path.join(DATA_DIR, "transactions.csv")
    if os.path.exists(tx_file):
        df_tx = pd.read_csv(tx_file)
        for _, row in df_tx.iterrows():
            tx = Transaction(
                id=str(row.get("id")),
                transaction_code=str(row.get("transaction_code")),
                source_account_id=str(row.get("source_account_id")),
                destination_account_id=str(row.get("destination_account_id")),
                beneficiary_id=str(row.get("beneficiary_id")) if pd.notna(row.get("beneficiary_id")) else None,
                employee_id=str(row.get("employee_id")) if pd.notna(row.get("employee_id")) else None,
                amount=float(row.get("amount")),
                currency=str(row.get("currency", "INR")),
                transaction_type=str(row.get("transaction_type", "TRANSFER")),
                channel=str(row.get("channel", "BRANCH")),
                status=str(row.get("status", "COMPLETED")),
                description=str(row.get("description", "")),
                timestamp=pd.to_datetime(row.get("timestamp")) if pd.notna(row.get("timestamp")) else datetime.utcnow()
            )
            db.merge(tx)
        db.commit()
        print(f"Loaded transactions from {tx_file}")

    print("Database seeding completed successfully from all CSV datasets!")
    db.close()

if __name__ == "__main__":
    seed_database()