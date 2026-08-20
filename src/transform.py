import pandas as pd


def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    transformed = df.copy()

    transformed["date"] = pd.to_datetime(transformed["date"], errors="coerce")
    transformed["amount"] = pd.to_numeric(transformed["amount"], errors="coerce")

    transformed["transaction_type"] = transformed["amount"].apply(
        lambda value: "income" if value >= 0 else "expense"
    )
    transformed["month"] = transformed["date"].dt.month
    transformed["year"] = transformed["date"].dt.year

    transformed["description"] = transformed["description"].astype(str).str.strip()
    transformed["currency"] = transformed["currency"].astype(str).str.strip().str.upper()
    transformed["category"] = transformed["category"].astype(str).str.strip().str.title()
    transformed["account"] = transformed["account"].astype(str).str.strip().str.title()

    return transformed.reset_index(drop=True)
