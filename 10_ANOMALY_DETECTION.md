# 🚨 Anomaly Detection Guide

## Machine Learning-Based Outlier Detection

**Read Time**: 15 minutes  
**Audience**: Data Scientists, Analysts, DevOps  
**Algorithm**: Isolation Forest

---

## 📊 What is Anomaly Detection?

Anomaly detection identifies unusual transactions that deviate from normal patterns.

### Examples of Anomalies

```
✓ Detected:
  - $25,000 transfer (vs typical $50)
  - Unusual category spending
  - Transactions outside normal times
  - Duplicate transactions

✗ Missed by rule-based detection:
  - Context-dependent anomalies
  - Multiple small suspicious transactions
  - Slow-changing trends
```

---

## 🤖 Isolation Forest Algorithm

### How It Works

```
Normal Transaction:
$50 coffee purchase
↓
Scores high on isolation
(Takes many conditions to isolate)
↓
Anomaly Score: -20
(Low = Normal)

Anomalous Transaction:
$25,000 wire transfer
↓
Scores low on isolation
(Easy to isolate as unusual)
↓
Anomaly Score: -85
(High magnitude = Anomaly)
```

### Why Isolation Forest?

| Characteristic | Benefit |
|---|---|
| **Unsupervised** | No labeled data needed |
| **Fast** | O(n log n) complexity |
| **Scalable** | Works with 1000s of records |
| **Robust** | Not affected by data scale |
| **Interpretable** | Clear anomaly scores |

---

## 🚀 Using Anomaly Detection

### Via API Endpoint

**Endpoint**: `GET /analytics/anomalies`

```bash
# Get all anomalies
curl http://127.0.0.1:8000/analytics/anomalies

# Get high-severity anomalies (score < -80)
curl "http://127.0.0.1:8000/analytics/anomalies?min_score=-80"

# Get specific count
curl "http://127.0.0.1:8000/analytics/anomalies?limit=5"
```

**Response**
```json
{
  "anomalies_detected": 125,
  "total_transactions": 5000,
  "anomaly_percentage": 2.5,
  "data": [
    {
      "transaction_id": 2847,
      "date": "2026-07-15",
      "description": "Large Wire",
      "amount": -25000.00,
      "category": "Transfers",
      "is_anomaly": true,
      "anomaly_score": -87.5,
      "severity": "high"
    }
  ]
}
```

### Via Python Script

**File**: `anomaly_detection.py`

```python
import pandas as pd
from anomaly_detection import detect_anomalies

# Load transaction data
df = pd.read_csv('data/raw/transactions.csv')

# Detect anomalies
result_df = detect_anomalies(df)

# Get high-severity anomalies
high_anomalies = result_df[result_df['is_anomaly'] & (result_df['anomaly_score'] < -70)]

print(f"Found {len(high_anomalies)} high-severity anomalies:")
print(high_anomalies[['description', 'amount', 'anomaly_score']])
```

---

## 📊 Anomaly Severity Levels

### Severity Classification

```
Severity Distribution:
├─ HIGH (< -70)    ════════════ 15%  → Requires immediate review
├─ MEDIUM (-70 to -50) ══════ 35%  → Review recommended
└─ LOW (> -50)     ═════════════ 50%  → Monitor only
```

### Severity Thresholds

| Severity | Score Range | Action | Example |
|----------|---|--|---|
| **HIGH** | < -70 | Investigate immediately | $25,000 transfer, $0 transaction |
| **MEDIUM** | -70 to -50 | Review in next update | $500 unusual category |
| **LOW** | > -50 | Monitor | $3 unusual store |

---

## 🔧 Configuration

### Model Parameters

**File**: `anomaly_detection.py`

```python
from sklearn.ensemble import IsolationForest

# Model configuration
model = IsolationForest(
    contamination=0.10,      # Expect ~10% anomalies
    random_state=42,         # Reproducible results
    n_estimators=100,        # Number of trees
    max_samples='auto'       # Sample size
)
```

**Contamination Rate**
```
0.10 = Expect 10% anomalies
      If 1000 transactions, ~100 are anomalies

Lower (0.05):  Stricter detection, fewer anomalies
Higher (0.20): Relaxed detection, more anomalies
```

### Adjust Contamination Rate

**For different datasets:**

```python
# High-fraud environment
contamination = 0.15  # Expect 15% anomalies

# Low-fraud environment
contamination = 0.05  # Expect 5% anomalies

# Typical personal finance
contamination = 0.10  # Expect 10% anomalies (default)
```

---

## 🎯 Features Used

### Current Feature Set

The model considers:
- **Transaction Amount** (primary feature)
- **Transaction Frequency** (secondary)
- **Category** (when available)

### Add More Features

**File**: `anomaly_detection.py`

```python
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Enhanced with more features"""
    
    # Prepare features
    features = df[[
        'amount',
        'month',
        'day_of_week',  # New
        'hour_of_day'   # New
    ]].copy()
    
    # Normalize
    features = (features - features.mean()) / features.std()
    
    # Fit model
    model = IsolationForest(contamination=0.10)
    predictions = model.fit_predict(features)
    
    df['is_anomaly'] = predictions == -1
    df['anomaly_score'] = model.score_samples(features) * 100
    
    return df
```

---

## 📈 Anomaly Analysis

### Find Patterns in Anomalies

```python
import requests

# Get anomalies from API
response = requests.get('http://127.0.0.1:8000/analytics/anomalies')
anomalies = response.json()['data']

# Analyze by category
from collections import Counter
categories = Counter(a['category'] for a in anomalies)
print("Anomalies by category:", categories)

# Analyze by amount
amounts = [abs(a['amount']) for a in anomalies]
print(f"Avg anomaly amount: ${sum(amounts)/len(amounts):.2f}")

# Identify patterns
high_severity = [a for a in anomalies if a['anomaly_score'] < -80]
print(f"High-severity anomalies: {len(high_severity)}")
```

### Temporal Analysis

```python
# Anomalies by month
from datetime import datetime

by_month = {}
for anomaly in anomalies:
    month = anomaly['date'][:7]  # YYYY-MM
    if month not in by_month:
        by_month[month] = 0
    by_month[month] += 1

print("Anomalies by month:")
for month, count in sorted(by_month.items()):
    print(f"  {month}: {count}")
```

---

## ⚠️ False Positives vs False Negatives

### Understanding Trade-offs

```
Higher Sensitivity (Catch more anomalies)
├─ More False Positives (Normal flagged as anomaly)
├─ Fewer False Negatives (Anomalies not missed)
└─ More manual review needed

Lower Sensitivity (Catch fewer anomalies)
├─ Fewer False Positives
├─ More False Negatives (Anomalies missed)
└─ Might miss real issues
```

### Adjust Threshold

```python
# Original threshold
anomalies = df[df['anomaly_score'] < -50]

# Stricter (fewer false positives)
anomalies = df[df['anomaly_score'] < -70]

# Relaxed (fewer false negatives)
anomalies = df[df['anomaly_score'] < -30]
```

---

## 🔄 Real-World Usage Patterns

### Pattern 1: Daily Review

```python
import requests
from datetime import datetime, timedelta

# Get today's anomalies
yesterday = datetime.now() - timedelta(days=1)
response = requests.get('http://127.0.0.1:8000/analytics/anomalies')
anomalies = response.json()['data']

# Filter to yesterday's transactions
recent = [a for a in anomalies if a['date'] >= str(yesterday.date())]

# Alert on high-severity
high = [a for a in recent if a['anomaly_score'] < -80]
if high:
    print(f"⚠️ {len(high)} high-severity anomalies detected!")
    for a in high:
        print(f"  - {a['description']}: ${a['amount']}")
```

### Pattern 2: Category-Specific Monitoring

```python
# Monitor specific category for anomalies
response = requests.get('http://127.0.0.1:8000/analytics/anomalies')
all_anomalies = response.json()['data']

# Filter by category
food_anomalies = [a for a in all_anomalies 
                 if a['category'] == 'Food & Dining']

print(f"Food category anomalies: {len(food_anomalies)}")
```

### Pattern 3: Trend Analysis

```python
# Track anomaly count over time
import requests

daily_anomalies = {}

for day in range(30):
    response = requests.get(
        'http://127.0.0.1:8000/analytics/anomalies'
    )
    count = response.json()['anomalies_detected']
    daily_anomalies[day] = count

# Calculate trend
avg = sum(daily_anomalies.values()) / len(daily_anomalies)
print(f"Average anomalies per day: {avg}")
```

---

## 🔍 Debugging Anomalies

### Why Certain Transactions Flagged?

```python
# Get detailed info about an anomaly
response = requests.get(
    'http://127.0.0.1:8000/transactions/2847'
)
transaction = response.json()

print(f"Amount: ${transaction['amount']}")
print(f"Typical range: $50 - $200")
print(f"Deviation: {transaction['amount'] / 100}x normal")
print(f"Category: {transaction['category']}")
print(f"Score: {anomaly['anomaly_score']}")
```

### Visualize Anomalies

```python
import matplotlib.pyplot as plt
import requests

# Get all transactions
response = requests.get('http://127.0.0.1:8000/transactions?limit=1000')
all_transactions = response.json()['data']

# Get anomalies
response = requests.get('http://127.0.0.1:8000/analytics/anomalies?limit=1000')
anomalies = response.json()['data']

# Create scatter plot
normal_amounts = [t['amount'] for t in all_transactions 
                  if t['transaction_id'] not in [a['transaction_id'] for a in anomalies]]
anomaly_amounts = [a['amount'] for a in anomalies]

plt.figure(figsize=(12, 6))
plt.scatter(range(len(normal_amounts)), normal_amounts, label='Normal', alpha=0.5)
plt.scatter(range(len(anomaly_amounts)), anomaly_amounts, label='Anomaly', color='red')
plt.ylabel('Amount ($)')
plt.legend()
plt.show()
```

---

## 📊 Model Retraining

### When to Retrain

```
Retrain if:
✓ Spending patterns changed significantly
✓ New normal activity level (salary increase)
✓ Business model changed
✓ Seasonal patterns emerging
✓ Model accuracy < 85%
```

### Retrain Script

```python
# File: scripts/retrain_anomaly_model.py

import pickle
import pandas as pd
from sklearn.ensemble import IsolationForest

# Load all transaction data
df = pd.read_csv('data/raw/transactions.csv')

# Prepare features
features = df[['amount']].copy()
features = (features - features.mean()) / features.std()

# Train new model
model = IsolationForest(
    contamination=0.10,
    random_state=42,
    n_estimators=100
)
model.fit(features)

# Save model
with open('models/isolation_forest.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model retrained successfully!")
```

### Schedule Retraining

```bash
# Add to crontab for weekly retraining (Sunday 2 AM)
0 2 * * 0 cd /opt/transaction-pipeline && python scripts/retrain_anomaly_model.py
```

---

## 📚 Advanced Topics

### Ensemble Methods

```python
from sklearn.ensemble import IsolationForest, LocalOutlierFactor

# Use multiple models
if1 = IsolationForest(contamination=0.10)
lof = LocalOutlierFactor(contamination=0.10)

pred1 = if1.fit_predict(features)
pred2 = lof.fit_predict(features)

# Anomaly if both agree
ensemble_pred = (pred1 == -1) & (pred2 == -1)
```

### Time-Series Anomalies

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Detect anomalies in time-series
decomposition = seasonal_decompose(time_series, model='additive')
residuals = decomposition.resid

# Anomalies are large residuals
threshold = residuals.std() * 3
anomalies = abs(residuals) > threshold
```

---

## 🚨 Alerting Setup

### Email Alerts on Anomalies

```python
import requests
import smtplib

def alert_on_anomalies():
    """Send email alert if high-severity anomalies found"""
    
    response = requests.get('http://127.0.0.1:8000/analytics/anomalies')
    anomalies = response.json()['data']
    
    # Filter high-severity
    high = [a for a in anomalies if a['anomaly_score'] < -80]
    
    if high:
        # Send email alert
        # (Implementation depends on email service)
        send_email_alert(f"Found {len(high)} anomalies!")

# Schedule daily
schedule.every().day.at("09:00").do(alert_on_anomalies)
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)** — API endpoints
- **[5_DASHBOARD_GUIDE.md](5_DASHBOARD_GUIDE.md)** — Dashboard
- **[15_EXAMPLES_RECIPES.md](15_EXAMPLES_RECIPES.md)** — Code examples

---

**Anomaly detection protects your data quality!** 🚨✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
