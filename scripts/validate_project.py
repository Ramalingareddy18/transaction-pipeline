#!/usr/bin/env python
"""
Comprehensive project validation script.

Validates:
- Project structure and files
- Python environment and dependencies
- Database connectivity
- API functionality
- Data pipeline
- Full system readiness
"""

import io
import sys
from pathlib import Path

if (
    hasattr(sys.stdout, "buffer")
    and sys.stdout.encoding
    and sys.stdout.encoding.lower() != "utf-8"
):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def check_project_structure():
    """Verify all required project directories and files exist."""
    print("\n[1/8] Checking project structure...")
    required_dirs = [
        "app",
        "src",
        "tests",
        "scripts",
        "dags",
        "data",
        "data/raw",
        ".github/workflows",
    ]
    required_files = [
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        ".env.example",
        ".dockerignore",
        "README.md",
        "QUICKSTART.md",
        "dashboard.py",
        "anomaly_detection.py",
    ]

    issues = []
    for d in required_dirs:
        if not (ROOT / d).exists():
            issues.append(f"Missing directory: {d}")
        else:
            pass  # print(f"  ✓ {d}/")

    for f in required_files:
        if not (ROOT / f).exists():
            issues.append(f"Missing file: {f}")
        else:
            pass  # print(f"  ✓ {f}")

    if issues:
        print("✗ Project structure issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(
            "✓ Project structure is complete "
            f"({len(required_dirs)} dirs, {len(required_files)} files)"
        )
        return True


def check_python_environment():
    """Verify Python version and critical dependencies."""
    print("\n[2/8] Checking Python environment...")
    if sys.version_info < (3, 11):
        print(
            f"✗ Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}"
        )
        return False

    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pandas",
        "psycopg2",
        "streamlit",
        "plotly",
        "scikit-learn",
    ]

    missing = []
    for pkg in required_packages:
        mod_name = "sklearn" if pkg == "scikit-learn" else pkg.replace("-", "_")
        try:
            __import__(mod_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"✗ Missing packages: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        return False

    print(
        f"✓ Python {sys.version_info.major}.{sys.version_info.minor} with all required packages"
    )
    return True


def check_database_connectivity():
    """Test connection to PostgreSQL."""
    print("\n[3/8] Checking database connectivity...")
    try:
        from database_connection import test_connection

        result = test_connection()
        if result:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def check_environment_file():
    """Verify .env file configuration."""
    print("\n[4/8] Checking environment configuration...")
    env_file = ROOT / ".env"
    if not env_file.exists():
        print("✗ .env file not found")
        print("  Run: copy .env.example .env")
        return False

    try:
        from dotenv import dotenv_values

        env = dotenv_values(env_file)
        required_keys = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = [k for k in required_keys if k not in env]
        if missing:
            print(f"✗ Missing keys in .env: {', '.join(missing)}")
            return False
        print(f"✓ Environment file configured with {len(env)} variables")
        return True
    except Exception as e:
        print(f"✗ Error reading .env: {e}")
        return False


def check_data_files():
    """Verify input data files exist."""
    print("\n[5/8] Checking data files...")
    try:
        from project_paths import find_csv_file

        csv_file = find_csv_file()
        if csv_file and csv_file.exists():
            print(f"✓ CSV file found: {csv_file}")
            return True
        else:
            print("⚠ No CSV file found. Place data in data/raw/transactions.csv")
            return True  # Not critical for startup
    except Exception as e:
        print(f"⚠ Could not check CSV files: {e}")
        return True


def check_database_schema():
    """Verify database schema and tables."""
    print("\n[6/8] Checking database schema...")
    try:
        from sqlalchemy import create_engine, inspect

        from database_config import build_database_url

        engine = create_engine(build_database_url())
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if "transactions" in tables:
            cols = [c["name"] for c in inspector.get_columns("transactions")]
            print(f"✓ Transactions table exists with {len(cols)} columns")
            return True
        else:
            print("⚠ Transactions table not yet created")
            print("  Run: python src/etl_pipeline.py")
            return True
    except Exception as e:
        print(f"✗ Schema check failed: {e}")
        return False


def check_api_imports():
    """Verify FastAPI and related imports."""
    print("\n[7/8] Checking API imports...")
    try:
        import sys

        sys.path.insert(0, str(ROOT))
        from app.database import SessionLocal, Transaction  # noqa: F401
        from app.health_check import check_api_health  # noqa: F401
        from app.main import app  # noqa: F401
        from app.schemas import TransactionRead  # noqa: F401

        print("✓ All API modules import successfully")
        return True
    except Exception as e:
        print(f"✗ API import failed: {e}")
        return False


def check_pipeline_modules():
    """Verify ETL pipeline modules."""
    print("\n[8/8] Checking pipeline modules...")
    try:
        from anomaly_detection import detect_anomalies  # noqa: F401
        from etl_pipeline import run_pipeline  # noqa: F401
        from transform import transform_transactions  # noqa: F401
        from validation import validate_transactions  # noqa: F401

        print("✓ All pipeline modules import successfully")
        return True
    except Exception as e:
        print(f"✗ Pipeline import failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("TRANSACTION PIPELINE - PROJECT VALIDATION")
    print("=" * 60)

    checks = [
        check_project_structure,
        check_python_environment,
        check_database_connectivity,
        check_environment_file,
        check_data_files,
        check_database_schema,
        check_api_imports,
        check_pipeline_modules,
    ]

    results = [check() for check in checks]

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"VALIDATION RESULTS: {passed}/{total} checks passed")
    print("=" * 60)

    if all(results):
        print("\n✓ PROJECT IS READY FOR DEPLOYMENT")
        print("\nNext steps:")
        print("  1. Run the ETL pipeline: python src/etl_pipeline.py")
        print("  2. Start API: python -m uvicorn app.main:app")
        print("  3. Start Dashboard: streamlit run dashboard.py")
        print("  4. Run smoke tests: python scripts/smoke_test_e2e.py")
        return 0
    else:
        print("\n✗ SOME VALIDATION CHECKS FAILED")
        print("Please resolve the issues above before deployment.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
