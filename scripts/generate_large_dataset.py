#!/usr/bin/env python
"""
High-Performance Large Real-World Transaction Dataset Generator.

Generates 100,000 to 1,000,000+ realistic transaction records with:
- Natural distributions of categories, merchants, and amounts
- Authentic date ranges and temporal patterns
- Inject Machine Learning anomalies (outliers, large wire transfers, zero amounts, suspicious spikes)
- Fast bulk load into PostgreSQL
"""

import argparse
import io
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

if (
    hasattr(sys.stdout, "buffer")
    and sys.stdout.encoding
    and sys.stdout.encoding.lower() != "utf-8"
):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from etl_pipeline import run_pipeline
from project_paths import resolve_project_path


def generate_dataset(num_records=100000):
    print(f"⚡ Generating {num_records:,} real-world transaction records...")
    start_time = time.time()

    np.random.seed(42)

    # Categories and realistic merchants/descriptions
    category_templates = {
        "Income": [
            "Corporate Payroll Deposit",
            "Freelance Project Payment",
            "Vanguard Investment Dividend",
            "Consulting Fee Direct Deposit",
            "Tax Refund",
        ],
        "Food & Dining": [
            "Starbucks Coffee",
            "Chipotle Mexican Grill",
            "Uber Eats",
            "DoorDash Food Delivery",
            "Local Bakery",
            "Panera Bread",
            "Subway Sandwiches",
            "Downtown Bistro",
        ],
        "Groceries": [
            "Whole Foods Market",
            "Trader Joe's",
            "Walmart Supercenter",
            "Kroger Supermarket",
            "Costco Wholesale",
            "Target Superstore",
        ],
        "Utilities": [
            "PG&E Electric Utility",
            "City Water Dept",
            "Comcast Xfinity Internet",
            "AT&T Wireless Bill",
            "Trash & Recycling Service",
        ],
        "Shopping": [
            "Amazon.com Order",
            "Apple Store Online",
            "Best Buy Electronics",
            "Nike Official Store",
            "Nordstrom Department",
            "IKEA Home Furnishings",
        ],
        "Transport": [
            "Uber Ride",
            "Lyft Ride Share",
            "Shell Gas Station",
            "Chevron Fuel",
            "Metropolitan Transit Fare",
            "MTA Subway Pass",
        ],
        "Entertainment": [
            "Netflix Monthly Subscription",
            "Spotify Premium",
            "AMC Movie Theaters",
            "Steam Games Purchase",
            "PlayStation Network",
            "Concert Ticketmaster",
        ],
        "Health & Fitness": [
            "Equinox Gym Membership",
            "CVS Pharmacy",
            "Walgreens Health",
            "Dental Clinic Copay",
            "Quest Diagnostics",
        ],
        "Travel": [
            "Delta Air Lines Ticket",
            "United Airlines Flight",
            "Marriott Hotel Resort",
            "Airbnb Vacation Rental",
            "Hertz Car Rental",
        ],
        "Transfer": [
            "Transfer to High-Yield Savings",
            "Venmo P2P Payment",
            "Zelle Transfer to Friend",
            "Brokerage Transfer",
        ],
    }

    accounts = [
        "Checking Account",
        "Savings Account",
        "Credit Card",
        "Investment Account",
    ]
    # Category probabilities
    categories = list(category_templates.keys())
    cat_weights = [0.05, 0.25, 0.20, 0.08, 0.15, 0.12, 0.06, 0.04, 0.02, 0.03]

    chosen_cats = np.random.choice(categories, size=num_records, p=cat_weights)

    descriptions = []
    amounts = []

    for cat in chosen_cats:
        options = category_templates[cat]
        desc = np.random.choice(options)
        descriptions.append(desc)

        if cat == "Income":
            # Income amounts: positive $1,500 to $8,500
            amt = np.round(np.random.normal(3500, 1200), 2)
            amt = max(200.0, amt)
        elif cat == "Groceries":
            amt = -np.round(np.random.gamma(shape=3, scale=25), 2)
        elif cat == "Food & Dining":
            amt = -np.round(np.random.exponential(scale=22), 2)
        elif cat == "Utilities":
            amt = -np.round(np.random.normal(135, 45), 2)
        elif cat == "Shopping":
            amt = -np.round(np.random.exponential(scale=65), 2)
        elif cat == "Travel":
            amt = -np.round(np.random.normal(350, 150), 2)
        else:
            amt = -np.round(np.random.exponential(scale=35), 2)

        amounts.append(amt)

    # Dates spanning past 2 years up to current date
    start_date = pd.to_datetime("2024-01-01")
    end_date = pd.to_datetime("2026-08-19")
    random_days = np.random.randint(
        0, (end_date - start_date).days + 1, size=num_records
    )
    dates = start_date + pd.to_timedelta(random_days, unit="D")

    chosen_accounts = np.random.choice(
        accounts, size=num_records, p=[0.45, 0.20, 0.30, 0.05]
    )

    df = pd.DataFrame(
        {
            "transaction_id": np.arange(1, num_records + 1),
            "date": dates.strftime("%Y-%m-%d"),
            "description": descriptions,
            "amount": amounts,
            "currency": "USD",
            "category": chosen_cats,
            "account": chosen_accounts,
        }
    )

    # Inject Machine Learning Anomalies (~0.5% explicit extreme outliers)
    num_anomalies = max(10, int(num_records * 0.005))
    anomaly_indices = np.random.choice(num_records, size=num_anomalies, replace=False)

    anomaly_descriptions = [
        "UNAUTHORIZED HIGH-VOLUME WIRE TRANSFER #9948",
        "UNKNOWN OVERSEAS OFFSHORE ACCOUNT DEPOSIT",
        "SUSPICIOUS ATM MULTI-WITHDRAWAL SPIKE",
        "CRITICAL SYSTEM ZERO GLITCH ENTRY",
        "EXORBITANT BULK LUXURY PURCHASE",
        "UNVERIFIED FOREIGN CURRENCY ARBITRAGE",
    ]

    for idx in anomaly_indices:
        df.at[idx, "description"] = np.random.choice(anomaly_descriptions)
        # Inject extreme outlier amounts
        anomaly_type = np.random.choice(["huge_positive", "huge_negative", "zero"])
        if anomaly_type == "huge_positive":
            df.at[idx, "amount"] = float(np.random.randint(45000, 250000))
        elif anomaly_type == "huge_negative":
            df.at[idx, "amount"] = -float(np.random.randint(25000, 150000))
        else:
            df.at[idx, "amount"] = 0.00
        df.at[idx, "category"] = "Anomalous Outlier"

    # Save to CSV files
    raw_dir = resolve_project_path("data", "raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_csv = raw_dir / "transactions.csv"
    data_csv = resolve_project_path("data", "transactions.csv")

    df.to_csv(raw_csv, index=False)
    df.to_csv(data_csv, index=False)

    gen_duration = time.time() - start_time
    print(f"✓ Generated {len(df):,} records in {gen_duration:.2f} seconds.")
    print(f"  Saved to: {raw_csv}")
    print(f"  Sample dataset head:\n{df.head(5)}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate transaction dataset.")
    parser.add_argument(
        "--count",
        type=int,
        default=100000,
        help="Number of records to generate (default: 100,000)",
    )
    args = parser.parse_args()

    df = generate_dataset(num_records=args.count)

    print("\n🚀 Executing ETL pipeline to bulk load dataset into PostgreSQL...")
    run_pipeline(csv_path=str(resolve_project_path("data", "transactions.csv")))
    print(
        "\n🎉 Bulk load complete! Enterprise dataset is live in PostgreSQL and Dashboard!"
    )
