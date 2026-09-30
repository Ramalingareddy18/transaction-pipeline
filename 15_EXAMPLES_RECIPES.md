# 📚 Examples & Recipes

## Practical Code Examples & Use Cases

**Read Time**: 20 minutes  
**Audience**: Developers, Data Analysts  
**Format**: Copy & Paste Ready Examples

---

## 🐍 Python Examples

### Example 1: Direct ETL Pipeline Execution

```python
# Load and process data programmatically

from src.etl_pipeline import run_pipeline
from src.database_connection import SessionLocal
from app.database import Transaction

# Run ETL
run_pipeline(csv_path='data/raw/transactions.csv')

# Query results
session = SessionLocal()
transactions = session.query(Transaction).limit(10).all()

for tx in transactions:
    print(f"ID: {tx.transaction_id}, Amount: {tx.amount}")

session.close()
```

---

### Example 2: Anomaly Detection

```python
# Detect anomalies in transactions

import pandas as pd
from anomaly_detection import detect_anomalies
from src.database_connection import SessionLocal
from app.database import Transaction

# Load transactions from database
session = SessionLocal()
transactions = session.query(Transaction).all()
session.close()

# Convert to DataFrame
df = pd.DataFrame([
    {
        'transaction_id': tx.transaction_id,
        'amount': tx.amount,
        'category': tx.category
    }
    for tx in transactions
])

# Detect anomalies
df_with_anomalies = detect_anomalies(df)

# Find anomalous transactions
anomalies = df_with_anomalies[df_with_anomalies['is_anomaly'] == 1]
print(f"Found {len(anomalies)} anomalies:")
print(anomalies[['transaction_id', 'amount', 'anomaly_score']])
```

---

### Example 3: Database Queries

```python
# Complex database queries

from sqlalchemy import func, desc
from src.database_connection import SessionLocal
from app.database import Transaction
from datetime import datetime, timedelta

session = SessionLocal()

# Query 1: Total transactions by category
categories = session.query(
    Transaction.category,
    func.count(Transaction.id).label('count'),
    func.sum(Transaction.amount).label('total')
).group_by(Transaction.category).all()

for cat, count, total in categories:
    print(f"{cat}: {count} transactions, ${total}")

# Query 2: High-value transactions
high_value = session.query(Transaction).filter(
    Transaction.amount > 10000
).order_by(desc(Transaction.amount)).limit(5).all()

for tx in high_value:
    print(f"${tx.amount} - {tx.description}")

# Query 3: Transactions in last 30 days
thirty_days_ago = datetime.now() - timedelta(days=30)
recent = session.query(Transaction).filter(
    Transaction.date >= thirty_days_ago
).count()

print(f"Transactions in last 30 days: {recent}")

session.close()
```

---

### Example 4: Data Export

```python
# Export data to various formats

import pandas as pd
from src.database_connection import SessionLocal
from app.database import Transaction

session = SessionLocal()
transactions = session.query(Transaction).all()
session.close()

# Convert to DataFrame
df = pd.DataFrame([
    {
        'ID': tx.transaction_id,
        'Date': tx.date,
        'Amount': tx.amount,
        'Category': tx.category,
        'Description': tx.description
    }
    for tx in transactions
])

# Export to CSV
df.to_csv('export/transactions.csv', index=False)
print("Exported to CSV")

# Export to Excel
df.to_excel('export/transactions.xlsx', index=False)
print("Exported to Excel")

# Export to JSON
df.to_json('export/transactions.json', orient='records')
print("Exported to JSON")
```

---

## 🌐 API Usage Examples

### JavaScript/Node.js

```javascript
// Fetch transactions from API

const API_URL = 'http://127.0.0.1:8000';

async function getTransactions() {
    const response = await fetch(`${API_URL}/transactions?limit=10`);
    const data = await response.json();
    return data;
}

async function getAnalytics() {
    const response = await fetch(`${API_URL}/analytics/summary`);
    const data = await response.json();
    return data;
}

async function detectAnomalies() {
    const response = await fetch(`${API_URL}/analytics/anomalies`);
    const data = await response.json();
    return data;
}

// Usage
getTransactions().then(data => {
    console.log(`Found ${data.total} transactions`);
    data.items.forEach(tx => {
        console.log(`${tx.date}: $${tx.amount}`);
    });
});
```

---

### Python Requests

```python
# Call API from Python

import requests
import json

API_URL = 'http://127.0.0.1:8000'

# Get transactions
response = requests.get(f'{API_URL}/transactions', params={
    'limit': 10,
    'category': 'food'
})
transactions = response.json()
print(f"Found {len(transactions['items'])} transactions")

# Get analytics
response = requests.get(f'{API_URL}/analytics/summary')
analytics = response.json()
print(f"Total transactions: {analytics['total_transactions']}")
print(f"Total amount: ${analytics['total_amount']:.2f}")

# Get anomalies
response = requests.get(f'{API_URL}/analytics/anomalies')
anomalies = response.json()
print(f"Found {len(anomalies)} anomalies")

# Filter by date
response = requests.get(f'{API_URL}/transactions', params={
    'start_date': '2026-08-01',
    'end_date': '2026-08-31'
})
august_data = response.json()
```

---

### cURL (Command Line)

```bash
# Get health status
curl http://127.0.0.1:8000/health

# Get transactions with pagination
curl "http://127.0.0.1:8000/transactions?limit=5&offset=0"

# Filter by category
curl "http://127.0.0.1:8000/transactions?category=food&limit=10"

# Get specific transaction
curl http://127.0.0.1:8000/transactions/123

# Get analytics
curl http://127.0.0.1:8000/analytics/summary

# Get anomalies
curl http://127.0.0.1:8000/analytics/anomalies

# With headers
curl -H "Content-Type: application/json" \
     http://127.0.0.1:8000/analytics/summary
```

---

### Postman Collection

```json
{
  "info": {
    "name": "Transaction Pipeline API",
    "version": "1.0"
  },
  "item": [
    {
      "name": "Get Transactions",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/transactions?limit=10"
      }
    },
    {
      "name": "Get Analytics",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/analytics/summary"
      }
    },
    {
      "name": "Get Anomalies",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/analytics/anomalies"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    }
  ]
}
```

---

## 📊 Dashboard Customization

### Custom Chart Addition

```python
# Add new chart to dashboard.py

import streamlit as st
import plotly.graph_objects as go
import requests

API_URL = 'http://127.0.0.1:8000'

# Fetch analytics
response = requests.get(f'{API_URL}/analytics/summary')
analytics = response.json()

# Create custom chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=['Food', 'Transport', 'Entertainment'],
    y=[analytics['total_by_category'].get('Food', 0),
       analytics['total_by_category'].get('Transport', 0),
       analytics['total_by_category'].get('Entertainment', 0)],
    name='Amount Spent'
))

fig.update_layout(
    title='Spending by Category',
    xaxis_title='Category',
    yaxis_title='Amount ($)',
    height=500
)

st.plotly_chart(fig, use_container_width=True)
```

---

## 🔄 Database Operations

### Backup Database

```bash
# Linux/macOS
pg_dump -h localhost -U postgres transaction_pipeline_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Windows (PowerShell)
$filename = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql.gz"
pg_dump -h localhost -U postgres transaction_pipeline_db | gzip > $filename
```

### Restore Database

```bash
# Linux/macOS
gunzip < backup_20260801_120000.sql.gz | psql -h localhost -U postgres transaction_pipeline_db

# Windows (PowerShell)
Get-Content backup_20260801_120000.sql.gz | 
    C:\Program Files\PostgreSQL\14\bin\psql.exe -h localhost -U postgres -d transaction_pipeline_db
```

### Bulk Insert from CSV

```python
# Import CSV directly using PostgreSQL COPY

from src.database_connection import get_engine

engine = get_engine()
with engine.connect() as conn:
    # Clear existing data
    conn.execute("DELETE FROM transactions")
    
    # Copy from CSV
    conn.execute("""
        COPY transactions (
            transaction_id, date, description, amount, 
            currency, category, account, transaction_type
        ) FROM '/path/to/data.csv' 
        WITH (FORMAT csv, HEADER true)
    """)
    
    conn.commit()
```

---

## 🚀 Deployment Examples

### Docker Development Environment

```bash
# Quick start development
docker-compose up -d

# Check all services
docker-compose ps

# View logs
docker-compose logs -f

# Run shell in container
docker-compose exec api bash

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
```

---

### Production Deployment (AWS)

```bash
# Build image
docker build -t transaction-pipeline:1.0 .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login \
  --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag transaction-pipeline:1.0 \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/transaction-pipeline:1.0

docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/transaction-pipeline:1.0
```

---

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transaction-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: transaction-api
  template:
    metadata:
      labels:
        app: transaction-api
    spec:
      containers:
      - name: api
        image: transaction-pipeline:1.0
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: postgres.default.svc.cluster.local
        - name: DB_NAME
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: db-name
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## 🔐 Security Examples

### Secure Configuration

```python
# Use environment variables, not hardcoded secrets

import os
from dotenv import load_dotenv

load_dotenv()

# ✅ CORRECT
DB_PASSWORD = os.getenv('DB_PASSWORD')

# ❌ WRONG
DB_PASSWORD = "never-hardcode-a-real-secret"
```

---

### SQL Injection Prevention

```python
# Use parameterized queries

from src.database_connection import SessionLocal
from app.database import Transaction
from sqlalchemy import text

session = SessionLocal()

# ❌ VULNERABLE to SQL injection
# user_input = "'; DROP TABLE transactions; --"
# query = f"SELECT * FROM transactions WHERE category = '{user_input}'"

# ✅ SAFE - Use parameterized queries
query = session.query(Transaction).filter(
    Transaction.category == user_input  # Parameter binding
)

results = query.all()
session.close()
```

---

## 📈 Monitoring Examples

### Health Check Script

```python
# Monitor system health continuously

#!/usr/bin/env python3

import requests
import time
import json
from datetime import datetime

def monitor_health(interval=60):
    """Monitor system health"""
    
    API_URL = 'http://127.0.0.1:8000'
    
    while True:
        try:
            # Check health
            response = requests.get(f'{API_URL}/health/detailed')
            
            if response.status_code == 200:
                data = response.json()
                print(f"[{datetime.now()}] Status: {data['status']}")
                
                # Save to log
                with open('health.log', 'a') as f:
                    f.write(json.dumps(data) + '\n')
            else:
                print(f"[{datetime.now()}] Error: {response.status_code}")
                
        except Exception as e:
            print(f"[{datetime.now()}] Connection failed: {e}")
        
        time.sleep(interval)

if __name__ == '__main__':
    monitor_health()
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)** — API endpoints
- **[5_DASHBOARD_GUIDE.md](5_DASHBOARD_GUIDE.md)** — Dashboard usage
- **[6_DATABASE_GUIDE.md](6_DATABASE_GUIDE.md)** — Database operations

---

**These examples accelerate development!** 📚✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
