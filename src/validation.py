import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "date",
    "description",
    "amount",
    "currency",
    "category",
    "account",
]


def validate_transactions(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset=["transaction_id"], keep="last")
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned = cleaned.dropna(
        subset=[
            "transaction_id",
            "date",
            "description",
            "amount",
            "currency",
            "category",
            "account",
        ]
    )

    cleaned["currency"] = cleaned["currency"].astype(str).str.strip().str.upper()
    cleaned["category"] = cleaned["category"].astype(str).str.strip().str.title()
    cleaned["account"] = cleaned["account"].astype(str).str.strip().str.title()
    cleaned["description"] = cleaned["description"].astype(str).str.strip()

    return cleaned.reset_index(drop=True)
