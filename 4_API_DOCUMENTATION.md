# 📡 Complete API Documentation

## REST API Reference

**Read Time**: 20 minutes  
**Audience**: Developers, API Users  
**API Base URL**: `http://127.0.0.1:8000`

---

## 🚀 Getting Started with API

### API Documentation UI

```
Interactive Swagger UI: http://127.0.0.1:8000/docs
ReDoc UI:              http://127.0.0.1:8000/redoc
OpenAPI JSON:          http://127.0.0.1:8000/openapi.json
```

### Authentication
Currently uses environment-based configuration. Future versions will support JWT.

### Response Format
All responses are JSON with consistent structure:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "Description",
  "timestamp": "2026-08-01T12:00:00Z"
}
```

---

## 🏥 Health Check Endpoints

### 1. Basic Health Check
**Endpoint**: `GET /health`

**Purpose**: Load balancer health verification

**Request**
```bash
curl http://127.0.0.1:8000/health
```

**Response** (200 OK)
```json
{
  "status": "ok"
}
```

**Use Case**: Health checks for Docker containers, load balancers

---

### 2. Detailed Health Check
**Endpoint**: `GET /health/detailed`

**Purpose**: Comprehensive system status

**Request**
```bash
curl http://127.0.0.1:8000/health/detailed
```

**Response** (200 OK)
```json
{
  "status": "healthy",
  "checks": {
    "database": "connected",
    "api": "responsive",
    "data_quality": "good"
  },
  "timestamp": "2026-08-01T12:00:00Z",
  "uptime_seconds": 3600,
  "version": "1.0.0"
}
```

**Status Values**: `healthy`, `degraded`, `unhealthy`

---

### 3. Database Health Check
**Endpoint**: `GET /health/database`

**Purpose**: Database-specific diagnostics

**Request**
```bash
curl http://127.0.0.1:8000/health/database
```

**Response** (200 OK)
```json
{
  "status": "connected",
  "database": "transaction_pipeline_db",
  "host": "localhost",
  "port": 5432,
  "transaction_count": 5000,
  "last_transaction_date": "2026-08-01",
  "table_sizes": {
    "transactions": "2.5 MB",
    "audit_logs": "500 KB"
  },
  "indexes": 4,
  "timestamp": "2026-08-01T12:00:00Z"
}
```

---

### 4. Data Quality Check
**Endpoint**: `GET /health/data-quality`

**Purpose**: Data validation metrics

**Request**
```bash
curl http://127.0.0.1:8000/health/data-quality
```

**Response** (200 OK)
```json
{
  "status": "good",
  "total_records": 5000,
  "valid_records": 4900,
  "invalid_records": 100,
  "validation_rate": 98.0,
  "anomaly_percentage": 2.5,
  "missing_values": {
    "description": 5,
    "category": 2,
    "amount": 0
  },
  "timestamp": "2026-08-01T12:00:00Z"
}
```

**Status Values**: `good`, `fair`, `poor`

---

## 📊 Transaction Endpoints

### 5. List Transactions
**Endpoint**: `GET /transactions`

**Purpose**: Retrieve paginated transaction list

**Request Parameters**
```bash
curl "http://127.0.0.1:8000/transactions?limit=10&offset=0&category=Food"
```

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `limit` | integer | 100 | No | Records per page (1-10000) |
| `offset` | integer | 0 | No | Pagination offset |
| `category` | string | None | No | Filter by category |

**Response** (200 OK)
```json
[
  {
    "transaction_id": 1,
    "date": "2026-08-01",
    "description": "Coffee Shop",
    "amount": -3.5,
    "currency": "USD",
    "category": "Food & Dining",
    "account": "Personal Checking",
    "transaction_type": "expense",
    "month": 8,
    "year": 2026
  }
]
```

**Example Requests**
```bash
# Get first 20 transactions
curl "http://127.0.0.1:8000/transactions?limit=20"

# Get food category transactions
curl "http://127.0.0.1:8000/transactions?category=Food"

# Get page 2 with 50 per page
curl "http://127.0.0.1:8000/transactions?limit=50&offset=50"
```

---

### 6. Get Single Transaction
**Endpoint**: `GET /transactions/{transaction_id}`

**Purpose**: Retrieve specific transaction details

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `transaction_id` | integer | Yes | Transaction ID |

**Request**
```bash
curl http://127.0.0.1:8000/transactions/1
```

**Response** (200 OK)
```json
{
  "transaction_id": 1,
  "date": "2026-08-01",
  "description": "Coffee Shop",
  "amount": -3.50,
  "currency": "USD",
  "category": "Food & Dining",
  "account": "Personal Checking",
  "transaction_type": "expense",
  "month": 8,
  "year": 2026
}
```

**Error Response** (404 Not Found)
```json
{
  "detail": "Transaction not found"
}
```

---

## 📈 Analytics Endpoints

### 7. Summary Statistics
**Endpoint**: `GET /analytics/summary`

**Purpose**: Get aggregate transaction statistics

**Request**
```bash
curl "http://127.0.0.1:8000/analytics/summary"
```

**Response** (200 OK)
```json
{
  "total_amount": 125000.5,
  "average_amount": 25.0,
  "max_amount": 10000.0,
  "min_amount": -5000.0,
  "transaction_count": 5000,
  "categories": 8,
  "status": "ok"
}
```

---

### 8. Anomaly Detection
**Endpoint**: `GET /analytics/anomalies`

**Purpose**: Detect unusual transactions using ML

**Request**
```bash
curl "http://127.0.0.1:8000/analytics/anomalies"
```

**Response** (200 OK)
```json
{
  "count": 1,
  "model": "IsolationForest",
  "anomalies": [
    {
      "transaction_id": 2847,
      "date": "2026-07-15",
      "description": "Large Wire Transfer",
      "amount": -25000.00,
      "category": "Transfers",
      "is_anomaly": true,
      "anomaly_score": -0.72
    }
  ]
}
```

The response includes the model's raw Isolation Forest `score_samples` value. The API does not currently assign severity levels.

---

## 🔗 Common Use Cases

### Use Case 1: Monitor System Health

**Script**
```bash
#!/bin/bash

# Check basic health
curl http://127.0.0.1:8000/health

# Get detailed status
curl http://127.0.0.1:8000/health/detailed

# Check database
curl http://127.0.0.1:8000/health/database
```

### Use Case 2: Paginate Through All Transactions

**Python Example**
```python
import requests

BASE_URL = "http://127.0.0.1:8000"
all_transactions = []
limit = 100
offset = 0

while True:
    response = requests.get(
        f"{BASE_URL}/transactions",
        params={"limit": limit, "offset": offset}
    )
    
    data = response.json()
    all_transactions.extend(data)
    
    # Check if more records
    if len(data) < limit:
        break
    
    offset += limit

print(f"Total transactions: {len(all_transactions)}")
```

### Use Case 3: Find Anomalies and Alert

**Python Example**
```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Get anomalies
response = requests.get(f"{BASE_URL}/analytics/anomalies")

anomalies = response.json()['anomalies']

# Alert on each anomaly
for anomaly in anomalies:
    print(f"⚠️ ALERT: {anomaly['description']}")
    print(f"   Amount: {anomaly['amount']}")
    print(f"   Score: {anomaly['anomaly_score']}")
```

### Use Case 4: Category Analysis

**Python Example**
```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Get food transactions
response = requests.get(
    f"{BASE_URL}/transactions",
    params={"category": "Food & Dining"}
)

transactions = response.json()

# Calculate totals
total_spent = sum(t['amount'] for t in transactions)
avg_spent = total_spent / len(transactions)

print(f"Food spending: {total_spent:.2f}")
print(f"Average per transaction: {avg_spent:.2f}")
```

---

## 🔧 Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Transaction retrieved successfully |
| 400 | Bad Request | Invalid parameter value |
| 404 | Not Found | Transaction ID doesn't exist |
| 422 | Validation Error | Invalid data format |
| 500 | Server Error | Internal server error |

### Error Response Format

```json
{
  "detail": "Transaction not found"
}
```

### Error Examples

**Invalid Transaction ID**
```bash
curl http://127.0.0.1:8000/transactions/99999
```
Response:
```json
{
  "detail": "Transaction not found"
}
```

**Invalid Parameter**
```bash
curl "http://127.0.0.1:8000/transactions?limit=10001"
```
Response:
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["query", "limit"],
      "msg": "Input should be less than or equal to 10000"
    }
  ]
}
```

---

## 📝 Request Examples by Language

### Python (requests library)

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# 1. Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Get transactions
response = requests.get(
    f"{BASE_URL}/transactions",
    params={
        "limit": 10,
        "category": "Food"
    }
)
print(response.json())

# 3. Get specific transaction
response = requests.get(f"{BASE_URL}/transactions/1")
print(response.json())

# 4. Get summary
response = requests.get(f"{BASE_URL}/analytics/summary")
print(response.json())

# 5. Get anomalies
response = requests.get(f"{BASE_URL}/analytics/anomalies")
print(response.json())
```

### JavaScript (fetch)

```javascript
const BASE_URL = 'http://127.0.0.1:8000';

// 1. Health check
fetch(`${BASE_URL}/health`)
  .then(r => r.json())
  .then(data => console.log(data));

// 2. Get transactions
fetch(`${BASE_URL}/transactions?limit=10&category=Food`)
  .then(r => r.json())
  .then(data => console.log(data));

// 3. Get anomalies
fetch(`${BASE_URL}/analytics/anomalies`)
  .then(r => r.json())
  .then(data => console.log(data));
```

### cURL (shell)

```bash
BASE_URL="http://127.0.0.1:8000"

# 1. Health check
curl $BASE_URL/health

# 2. Get transactions with category filter
curl "$BASE_URL/transactions?category=Food"

# 3. Get anomalies
curl "$BASE_URL/analytics/anomalies"

# 4. Get with custom headers
curl -H "Content-Type: application/json" \
     "$BASE_URL/transactions"
```

### PowerShell

```powershell
$BaseURL = "http://127.0.0.1:8000"

# 1. Health check
$response = Invoke-WebRequest "$BaseURL/health"
$response.Content | ConvertFrom-Json

# 2. Get transactions
$response = Invoke-WebRequest "$BaseURL/transactions?limit=10"
$response.Content | ConvertFrom-Json

# 3. Get anomalies
$response = Invoke-WebRequest "$BaseURL/analytics/anomalies"
$response.Content | ConvertFrom-Json
```

---

## 🚦 Rate Limiting & Performance

### Current Limits
- **Requests per second**: Unlimited (configure in production)
- **Batch size limit**: 100 records per request
- **Timeout**: 30 seconds per request

### Performance Tips
1. Use pagination with `limit` and `offset`
2. Filter by `category` when possible
3. Use date range filters to reduce results
4. Cache API responses when appropriate

---

## 📚 API Versioning

### Current Version
```
Version: 1.0.0
Release Date: 2026-08-01
Status: Stable
```

### API Version Header
```
GET /transactions
X-API-Version: 1.0.0
```

---

## 🔐 Security Notes

### Data Protection
- Parameterized queries prevent SQL injection
- Input validation on all parameters
- Environment-based credentials

### HTTPS
In production, always use HTTPS:
```
https://api.yourdomain.com/transactions
```

### API Keys (Future)
```
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://127.0.0.1:8000/transactions
```

---

## 📞 API Support

- **Interactive Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **GitHub Issues**: [Project repo]
- **Email**: support@example.com

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)** — System design
- **[5_DASHBOARD_GUIDE.md](5_DASHBOARD_GUIDE.md)** — Dashboard interface
- **[10_ANOMALY_DETECTION.md](10_ANOMALY_DETECTION.md)** — Anomaly details

---

**API is fully documented and production-ready.** ✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
