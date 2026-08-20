"""
Health check module for production monitoring.

Provides comprehensive health diagnostics for:
- Database connectivity
- API responsiveness
- Data pipeline status
- Service dependencies
"""

from datetime import datetime
from typing import Any

from app.database import SessionLocal
from sqlalchemy import text


def check_database_health() -> dict[str, Any]:
    """Check database connectivity and basic statistics."""
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT version()")).scalar()
            count = session.execute(
                text("SELECT COUNT(*) FROM transactions")
            ).scalar()
            return {
                "status": "healthy",
                "version": result,
                "transaction_count": count,
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


def check_api_health() -> dict[str, Any]:
    """Check API readiness and dependencies."""
    db_health = check_database_health()
    return {
        "status": "ok" if db_health["status"] == "healthy" else "degraded",
        "database": db_health["status"],
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


def check_data_quality() -> dict[str, Any]:
    """Check data quality in the database."""
    try:
        with SessionLocal() as session:
            total = session.execute(
                text("SELECT COUNT(*) FROM transactions")
            ).scalar()
            with_amount = session.execute(
                text("SELECT COUNT(*) FROM transactions WHERE amount IS NOT NULL")
            ).scalar()
            with_category = session.execute(
                text("SELECT COUNT(*) FROM transactions WHERE category IS NOT NULL")
            ).scalar()

            quality_score = (
                ((with_amount + with_category) / (total * 2) * 100)
                if total > 0
                else 0
            )

            return {
                "status": "ok",
                "total_records": total,
                "records_with_amount": with_amount,
                "records_with_category": with_category,
                "quality_score": round(quality_score, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }
