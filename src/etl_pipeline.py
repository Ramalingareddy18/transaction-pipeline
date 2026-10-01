import os
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, inspect, text
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database_config import build_database_url
from project_paths import find_csv_file, resolve_project_path, resolve_user_path
from transform import transform_transactions
from validation import validate_transactions


def ensure_transactions_table(connection):
    expected_columns = {
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

    inspector = inspect(connection)
    existing = {
        column["name"].lower() for column in inspector.get_columns("transactions")
    }
    if "transaction_id" not in existing:
        raise RuntimeError(
            "The existing transactions table has no transaction_id key; "
            "migrate it explicitly before loading data."
        )
    primary_key = (
        inspector.get_pk_constraint("transactions").get("constrained_columns") or []
    )
    unique_keys = [
        constraint.get("column_names") or []
        for constraint in inspector.get_unique_constraints("transactions")
    ]
    unique_indexes = [
        index.get("column_names") or []
        for index in inspector.get_indexes("transactions")
        if index.get("unique")
    ]
    if not any(
        columns == ["transaction_id"]
        for columns in [primary_key, *unique_keys, *unique_indexes]
    ):
        raise RuntimeError(
            "The transactions table must have a unique transaction_id key for safe upserts."
        )

    for column_name, column_type in expected_columns.items():
        if column_name not in existing:
            connection.execute(
                text(f"ALTER TABLE transactions ADD COLUMN {column_name} {column_type}")
            )


def load_transactions(connection, frame, replace_all=False):
    """Idempotently insert/update rows; replace the full table only on request."""
    if frame.empty:
        return

    if replace_all:
        connection.execute(text("DELETE FROM transactions"))

    metadata = MetaData()
    transactions = Table("transactions", metadata, autoload_with=connection)
    if connection.dialect.name == "postgresql":
        insert = postgresql_insert
    elif connection.dialect.name == "sqlite":
        insert = sqlite_insert
    else:
        raise RuntimeError(
            f"Upsert is not configured for database dialect {connection.dialect.name!r}."
        )

    column_names = [
        "transaction_id",
        "date",
        "description",
        "amount",
        "currency",
        "category",
        "account",
        "transaction_type",
        "month",
        "year",
    ]
    values = frame.reindex(columns=column_names).astype(object)
    values = values.where(pd.notna(values), None)
    records = values.to_dict(orient="records")
    for record in records:
        parsed_date = pd.to_datetime(record["date"], errors="coerce")
        record["date"] = None if pd.isna(parsed_date) else parsed_date.date()

    batch_size = 5000 if connection.dialect.name == "postgresql" else 90
    for start in range(0, len(records), batch_size):
        statement = insert(transactions).values(records[start : start + batch_size])
        updates = {
            name: getattr(statement.excluded, name)
            for name in column_names
            if name != "transaction_id"
        }
        statement = statement.on_conflict_do_update(
            index_elements=[transactions.c.transaction_id], set_=updates
        )
        connection.execute(statement)


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
        replace_all = os.getenv("ETL_REPLACE_ALL", "").strip().lower() in {
            "1",
            "true",
            "yes",
        }
        load_transactions(
            connection,
            transformed_df,
            replace_all=replace_all,
        )

    load_mode = "replace" if replace_all else "upsert"
    print(f"Pipeline completed successfully ({load_mode}). Output: {output_file}")
    return transformed_df


if __name__ == "__main__":
    run_pipeline()
