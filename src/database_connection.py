import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
for entry in (str(SRC_DIR),):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from sqlalchemy import create_engine, text

from database_config import build_database_url


def test_connection():
    try:
        engine = create_engine(build_database_url(), pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful! Test result:", result.scalar())
            return True
    except Exception as e:
        print("Database connection failed.")
        print("Error:", e)
        return False


if __name__ == "__main__":
    engine = create_engine(build_database_url(), pool_pre_ping=True)
    with engine.connect() as connection:
        cursor = connection.connection.cursor()
        cursor.execute("SELECT version();")
        print(cursor.fetchone())

    test_connection()
