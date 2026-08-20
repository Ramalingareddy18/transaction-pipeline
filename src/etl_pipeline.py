import os
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database_config import build_database_url
from project_paths import find_csv_file, resolve_project_path, resolve_user_path
from transform import transform_transactions
from validation import validate_transactions


def ensure_transactions_table(connection):
    expected_columns = {
        "transaction_id": "INTEGER PRIMARY KEY",
        "date": "DATE",
        "description": "TEXT",
        "amount": "NUMERIC",
        "currency": "TEXT",
        "category": "TEXT",
        "account": "TEXT",
        "transaction_type": "TEXT",
        "month": "INTEGER",
        "year": "INTEGER",
    }

    existing_rows = connection.execute(
        text(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'transactions'"
        )
    ).fetchall()
    existing = {row[0].lower() for row in existing_rows}

    create_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            date DATE,
            description TEXT,
            amount NUMERIC,
            currency TEXT,
            category TEXT,
            account TEXT,
            transaction_type TEXT,
            month INTEGER,
            year INTEGER
        )
    """
    connection.execute(text(create_sql))

    for column_name, column_type in expected_columns.items():
        if column_name not in existing:
            connection.execute(
                text(f"ALTER TABLE transactions ADD COLUMN {column_name} {column_type}")
            )


def run_pipeline(csv_path=None):
    file_path = csv_path or os.getenv("CSV_PATH") or str(find_csv_file())
    if file_path:
        file_path = str(resolve_user_path(file_path))

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    raw_df = pd.read_csv(file_path)
    validated_df = validate_transactions(raw_df)
    transformed_df = transform_transactions(validated_df)

    output_dir = resolve_project_path("data", "processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "cleaned_transactions.csv"
    transformed_df.to_csv(output_file, index=False)

    engine = create_engine(build_database_url(), pool_pre_ping=True)
    with engine.begin() as connection:
        ensure_transactions_table(connection)
        connection.execute(text("DELETE FROM transactions"))
        transformed_df.to_sql(
            "transactions",
            connection,
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi",
        )

    print(f"Pipeline completed successfully. Output: {output_file}")
    return transformed_df


if __name__ == "__main__":
    run_pipeline()
