import pandas as pd

from anomaly_detection import detect_anomalies


def test_detect_anomalies_flags_large_spike_and_unusual_amount():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3, 4, 5],
            "amount": [10.0, 12.0, 11.0, 900.0, 13.0],
            "category": ["Food", "Food", "Food", "Food", "Food"],
            "description": ["a", "b", "c", "d", "e"],
        }
    )

    flagged = detect_anomalies(df)

    assert "is_anomaly" in flagged.columns
    assert flagged["is_anomaly"].sum() >= 1
    assert flagged.loc[flagged["transaction_id"] == 4, "is_anomaly"].item() is True
