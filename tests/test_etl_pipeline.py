import pandas as pd
import pytest
from sqlalchemy import create_engine, inspect, text

from src.etl_pipeline import ensure_transactions_table, load_transactions


def test_ensure_transactions_table_creates_schema_and_is_repeatable():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as connection:
        ensure_transactions_table(connection)
        ensure_transactions_table(connection)

    columns = {
        column["name"] for column in inspect(engine).get_columns("transactions")
    }
    assert columns == {
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
    }
    engine.dispose()


def test_ensure_transactions_table_adds_missing_optional_columns():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE transactions (transaction_id INTEGER PRIMARY KEY, "
                "description TEXT)"
            )
        )
        ensure_transactions_table(connection)

    columns = {
        column["name"] for column in inspect(engine).get_columns("transactions")
    }
    assert "year" in columns
    assert "description" in columns
    engine.dispose()


def test_ensure_transactions_table_rejects_unkeyed_legacy_table():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE transactions (description TEXT)"))
        with pytest.raises(RuntimeError, match="no transaction_id key"):
            ensure_transactions_table(connection)

    engine.dispose()


def test_load_transactions_upserts_without_deleting_other_rows():
    engine = create_engine("sqlite:///:memory:")
    frame = pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "date": "2026-09-01",
                "description": "Updated",
                "amount": -12.5,
                "currency": "USD",
                "category": "Food",
                "account": "Checking",
                "transaction_type": "expense",
                "month": 9,
                "year": 2026,
            }
        ]
    )

    with engine.begin() as connection:
        ensure_transactions_table(connection)
        connection.execute(
            text(
                "INSERT INTO transactions (transaction_id, description) "
                "VALUES (2, 'Keep me')"
            )
        )
        load_transactions(connection, frame)
        load_transactions(connection, frame)
        rows = connection.execute(
            text(
                "SELECT transaction_id, description FROM transactions "
                "ORDER BY transaction_id"
            )
        ).all()

    assert rows == [(1, "Updated"), (2, "Keep me")]
    engine.dispose()


def test_load_transactions_replaces_table_only_when_explicitly_requested():
    engine = create_engine("sqlite:///:memory:")
    frame = pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "date": "2026-09-01",
                "description": "Replacement",
                "amount": 1.0,
                "currency": "USD",
                "category": "Food",
                "account": "Checking",
                "transaction_type": "income",
                "month": 9,
                "year": 2026,
            }
        ]
    )

    with engine.begin() as connection:
        ensure_transactions_table(connection)
        connection.execute(
            text(
                "INSERT INTO transactions (transaction_id, description) "
                "VALUES (2, 'Remove me')"
            )
        )
        load_transactions(connection, frame, replace_all=True)
        rows = connection.execute(
            text("SELECT transaction_id, description FROM transactions")
        ).all()

    assert rows == [(1, "Replacement")]
    engine.dispose()