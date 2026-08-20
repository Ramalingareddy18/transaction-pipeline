import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
for entry in (str(ROOT_DIR), str(SRC_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from sqlalchemy import create_engine, text

from database_config import build_admin_url, get_db_settings

settings = get_db_settings()
admin_url = build_admin_url()

try:
    engine = create_engine(admin_url)
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text(f'CREATE DATABASE "{settings["name"]}"'))
    print(f"Database '{settings['name']}' created (or already exists).")
except Exception as e:
    print("Failed to create database:", e)
    print("Make sure PostgreSQL server is running and credentials are correct.")
