import sys
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
STATIC_DIR = ROOT / "static"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from anomaly_detection import detect_anomalies
from app.database import SessionLocal, Transaction
from app.health_check import check_api_health, check_database_health, check_data_quality
from app.schemas import TransactionRead

app = FastAPI(
    title="Transaction Pipeline API",
    version="1.0.0",
    description="Production-grade transaction processing and analytics API",
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/portal", response_class=HTMLResponse)
def get_dashboard_portal():
    """Enterprise Portal Web Dashboard."""
    dashboard_file = STATIC_DIR / "dashboard.html"
    if dashboard_file.exists():
        return FileResponse(dashboard_file)
    return HTMLResponse("<h1>Dashboard template missing</h1>")


@app.get("/health")
def health_check():
    """Basic health check endpoint for load balancers."""
    return {"status": "ok"}


@app.get("/health/detailed")
def detailed_health():
    """Comprehensive health check including dependencies."""
    return check_api_health()


@app.get("/health/database")
def database_health():
    """Database-specific health check."""
    return check_database_health()


@app.get("/health/data-quality")
def data_quality():
    """Data quality metrics."""
    return check_data_quality()


@app.get("/transactions", response_model=list[TransactionRead])
def list_transactions(
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    category: str | None = None,
):
    """List transactions with optional filtering by category."""
    with SessionLocal() as session:
        query = select(Transaction).offset(offset).limit(limit)
        if category:
            query = query.where(Transaction.category == category)
        rows = session.execute(query).scalars().all()
        return rows


@app.get("/transactions/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int):
    """Get a single transaction by ID."""
    with SessionLocal() as session:
        row = session.get(Transaction, transaction_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return row


@app.get("/analytics/anomalies")
def analytics_anomalies():
    """Detect and return transaction anomalies using Isolation Forest."""
    with SessionLocal() as session:
        rows = session.execute(select(Transaction)).scalars().all()

    if not rows:
        return {"count": 0, "anomalies": []}

    frame = pd.DataFrame(
        [
            {
                "transaction_id": row.transaction_id,
                "amount": row.amount,
                "category": row.category,
                "date": row.date.isoformat() if row.date else None,
                "description": row.description,
            }
            for row in rows
            if row.amount is not None
        ]
    )

    if frame.empty:
        return {"count": 0, "anomalies": []}

    flagged = detect_anomalies(frame)
    anomalies = flagged[flagged["is_anomaly"]].to_dict(orient="records")
    return {
        "count": len(anomalies),
        "model": "IsolationForest",
        "anomalies": anomalies,
    }


@app.get("/analytics/summary")
def analytics_summary():
    """Get summary analytics for all transactions."""
    with SessionLocal() as session:
        rows = session.execute(select(Transaction)).scalars().all()

    if not rows:
        return {"status": "no_data"}

    frame = pd.DataFrame(
        [
            {
                "amount": row.amount,
                "category": row.category,
                "transaction_type": row.transaction_type,
            }
            for row in rows
            if row.amount is not None
        ]
    )

    if frame.empty:
        return {"status": "insufficient_data"}

    return {
        "total_amount": float(frame["amount"].sum()),
        "average_amount": float(frame["amount"].mean()),
        "max_amount": float(frame["amount"].max()),
        "min_amount": float(frame["amount"].min()),
        "transaction_count": len(frame),
        "categories": frame["category"].nunique(),
        "status": "ok",
    }


@app.get("/")
def root():
    """API root endpoint with links to documentation."""
    return {
        "message": "Transaction Pipeline API v1.0.0 is running",
        "endpoints": {
            "health": "/health",
            "health_detailed": "/health/detailed",
            "transactions": "/transactions",
            "anomalies": "/analytics/anomalies",
            "summary": "/analytics/summary",
            "docs": "/docs",
        },
    }

