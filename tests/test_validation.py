import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd

from validation import validate_transactions


def test_validate_transactions_accepts_valid_dataset():
    df = pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "date": "2026-08-01",
                "description": "Salary",
                "amount": 3000,
                "currency": "USD",
                "category": "Income",
                "account": "Checking",
            }
        ]
    )

    result = validate_transactions(df)

    assert list(result.columns) == [
        "transaction_id",
        "date",
        "description",
        "amount",
        "currency",
        "category",
        "account",
    ]
    assert len(result) == 1


def test_validate_transactions_rejects_missing_required_columns():
    df = pd.DataFrame({"id": [1], "amount": [10]})

    try:
        validate_transactions(df)
        assert False, "Expected ValueError for missing required columns"
    except ValueError:
        pass
