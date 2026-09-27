# Ensure all models are imported so SQLAlchemy registers relationships properly
import app.models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, employees, customers, accounts, transactions, alerts, investigations, cases, dashboard

app = FastAPI(
    title="INSIGHT-X: Financial Crime & Insider Risk Intelligence Platform",
    version="1.0.0",
    description="Production-grade investigation backend for financial crime, insider threat detection, and fraud analysis."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(investigations.router, prefix="/api/v1/investigations", tags=["Investigations"])
app.include_router(cases.router, prefix="/api/v1/cases", tags=["Cases"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
def read_root():
    return {
        "platform": "INSIGHT-X",
        "status": "Operational",
        "docs": "/docs",
        "version": "1.0.0"
    }