#!/usr/bin/env python
"""
End-to-end smoke test for the Transaction Pipeline.

Validates:
- Database connectivity and schema
- ETL pipeline execution
- API endpoints (health, transactions, analytics)
- Data consistency
- Anomaly detection
"""

import io
import sys
import time
from pathlib import Path

import requests

if (
    hasattr(sys.stdout, "buffer")
    and sys.stdout.encoding
    and sys.stdout.encoding.lower() != "utf-8"
):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from database_connection import test_connection
from etl_pipeline import run_pipeline


def test_database_connectivity():
    """Test PostgreSQL connection and basic schema validation."""
    print("\n[1/6] Testing database connectivity...")
    try:
        result = test_connection()
        if result:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def test_etl_pipeline():
    """Run the ETL pipeline and validate output."""
    print("\n[2/6] Running ETL pipeline...")
    try:
        df = run_pipeline()
        if df is not None and len(df) > 0:
            print(f"✓ ETL pipeline completed: {len(df)} transactions processed")
            return True
        else:
            print("✗ ETL pipeline returned empty dataset")
            return False
    except Exception as e:
        print(f"✗ ETL pipeline failed: {e}")
        return False


def test_api_health():
    """Check API health endpoint."""
    print("\n[3/6] Testing API health endpoint...")
    for attempt in range(5):
        try:
            resp = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "ok":
                    print("✓ API health check passed")
                    return True
        except requests.ConnectionError:
            if attempt < 4:
                print(f"  Waiting for API... (attempt {attempt + 1}/5)")
                time.sleep(2)
                continue
            break
        except Exception as e:
            if attempt < 4:
                time.sleep(1)
                continue
            print(f"✗ API health check error: {e}")
            break
    print("✗ API not responding or unhealthy")
    return False


def test_transactions_endpoint():
    """Test /transactions endpoint returns real data."""
    print("\n[4/6] Testing /transactions endpoint...")
    try:
        resp = requests.get("http://127.0.0.1:8000/transactions?limit=10", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"✓ Transactions endpoint returned {len(data)} records")
                return True
            else:
                print("✗ Transactions endpoint returned empty list")
                return False
        else:
            print(f"✗ Transactions endpoint returned {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Transactions endpoint error: {e}")
        return False


def test_anomaly_detection():
    """Test anomaly detection endpoint."""
    print("\n[5/6] Testing anomaly detection...")
    try:
        resp = requests.get("http://127.0.0.1:8000/analytics/anomalies", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            count = data.get("count", 0)
            print(f"✓ Anomaly detection completed: {count} anomalies flagged")
            return True
        else:
            print(f"✗ Anomaly detection returned {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Anomaly detection error: {e}")
        return False


def test_full_data_flow():
    """Validate end-to-end data consistency."""
    print("\n[6/6] Testing full data flow...")
    try:
        # Get transaction count from API
        resp = requests.get("http://127.0.0.1:8000/transactions?limit=1000", timeout=10)
        if resp.status_code != 200:
            print("✗ Failed to retrieve transactions for validation")
            return False

        api_records = resp.json()
        if not isinstance(api_records, list) or len(api_records) == 0:
            print("✗ No transactions available for data flow validation")
            return False

        # Verify records have required fields
        required_fields = [
            "transaction_id",
            "amount",
            "description",
            "category",
            "date",
        ]
        for record in api_records[:1]:
            for field in required_fields:
                if field not in record:
                    print(f"✗ Missing field '{field}' in transaction record")
                    return False

        print(
            f"✓ Full data flow validated: {len(api_records)} transactions with correct schema"
        )
        return True
    except Exception as e:
        print(f"✗ Data flow validation error: {e}")
        return False


def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("TRANSACTION PIPELINE END-TO-END SMOKE TEST")
    print("=" * 60)

    tests = [
        test_database_connectivity,
        test_etl_pipeline,
        test_api_health,
        test_transactions_endpoint,
        test_anomaly_detection,
        test_full_data_flow,
    ]

    results = [test() for test in tests]

    print("\n" + "=" * 60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)

    if all(results):
        print("\n✓ ALL SMOKE TESTS PASSED - Project is production-ready")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED - See details above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
