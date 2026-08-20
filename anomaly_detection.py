from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(frame: pd.DataFrame) -> pd.DataFrame:
    """Flag unusually large transactions using an Isolation Forest model."""
    data = frame.copy()
    if data.empty:
        data["is_anomaly"] = pd.Series(dtype=bool)
        return data

    numeric = data[["amount"]].copy()
    numeric["amount"] = pd.to_numeric(numeric["amount"], errors="coerce")
    numeric = numeric.fillna(0.0)

    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(numeric)

    result = data.copy()
    result["is_anomaly"] = predictions == -1
    result["anomaly_score"] = model.score_samples(numeric)
    return result
