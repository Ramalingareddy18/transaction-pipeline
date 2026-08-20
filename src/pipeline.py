import pandas as pd
from project_paths import find_csv_file, resolve_project_path

RAW_FILE = str(find_csv_file())

# EXTRACT
df = pd.read_csv(RAW_FILE)

print("Data loaded successfully!")
print("File used:", RAW_FILE)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nColumns:")
print(df.columns.tolist())

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

for column, formatter in [
    ("payment method", lambda s: s.astype(str).str.strip().str.upper()),
    ("location", lambda s: s.astype(str).str.strip().str.title()),
    ("status", lambda s: s.astype(str).str.strip().str.title()),
]:
    if column in df.columns:
        df[column] = formatter(df[column])
    else:
        print(f"Column '{column}' not found in dataset; skipped.")

print("\nUpdated columns:")
print(df.columns.tolist())

OUTPUT_DIR = resolve_project_path("data", "processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "cleaned_transactions.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCleaned data saved successfully!")
print("Output file:", OUTPUT_FILE)

