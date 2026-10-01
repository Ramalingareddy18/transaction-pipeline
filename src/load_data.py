import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

from database_config import build_database_url
from project_paths import find_csv_file, resolve_user_path


def resolve_input_path():
    env_path = os.getenv("CSV_PATH")
    if env_path:
        return str(resolve_user_path(env_path))
    if len(sys.argv) > 1:
        return str(resolve_user_path(sys.argv[1]))
    return str(find_csv_file())


def ensure_transactions_table(connection, columns):
    normalized_columns = [str(col).strip() for col in columns]
    column_defs = []

    for column in normalized_columns:
        name = column.lower()
        if name == "transaction_id":
            column_defs.append("transaction_id INTEGER PRIMARY KEY")
        elif name == "amount":
            column_defs.append("amount NUMERIC")
        elif name == "date":
            column_defs.append("date DATE")
        else:
            column_defs.append(f"{name} TEXT")

    create_sql = f"""
        CREATE TABLE IF NOT EXISTS transactions (
            {', '.join(column_defs)}
        )
    """
    connection.execute(text(create_sql))


def load_csv_to_db(file_path):
    df = pd.read_csv(file_path)
    print("CSV loaded successfully!")
    print(df.head())

    engine = create_engine(build_database_url(), pool_pre_ping=True)
    with engine.begin() as connection:
        ensure_transactions_table(connection, df.columns)

        for _, row in df.iterrows():
            payload = {str(column): row[column] for column in df.columns}
            column_names = ", ".join(str(column) for column in df.columns)
            placeholders = ", ".join(f":{str(column)}" for column in df.columns)

            sql = text(f"""
                INSERT INTO transactions ({column_names})
                VALUES ({placeholders})
                ON CONFLICT (transaction_id) DO NOTHING
            """)
            connection.execute(sql, payload)

    print("Data loaded into PostgreSQL successfully!")
    return df


if __name__ == "__main__":
    file_path = resolve_input_path()

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print(
            "Place your CSV at that path or run:\n"
            "  python src\\load_data.py <path/to/transactions.csv>\n"
            "Or set environment variable CSV_PATH"
        )
        sys.exit(1)

    df = load_csv_to_db(file_path)

    print(f"\nLoading CSV from: {file_path}")
    print("Number of rows loaded:", len(df))
    print("\nDataset shape:")
    print(df.shape)
    print("\nColumn names:")
    print(df.columns.tolist())
