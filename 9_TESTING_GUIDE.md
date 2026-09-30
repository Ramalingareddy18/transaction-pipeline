# 🧪 Testing & Quality Assurance Guide

## Testing Strategy & Execution

**Read Time**: 15 minutes  
**Audience**: QA Engineers, Developers, DevOps  
**Framework**: pytest, unittest

---

## 📊 Testing Pyramid

```
        ▲
       /|\       E2E Tests (Few, Slow, Comprehensive)
      / | \      
     /  |  \     Integration Tests (Medium, Moderate)
    /   |   \    
   /    |    \   Unit Tests (Many, Fast, Focused)
  /_____|_____\
```

---

## ✅ Unit Tests

### Purpose
Test individual functions/methods in isolation

### Location
- `tests/test_validation.py`
- `tests/test_transform.py`
- `tests/test_database.py`

### Run Unit Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all unit tests
pytest -v

# Run specific test file
pytest tests/test_validation.py -v

# Run specific test
pytest tests/test_validation.py::test_validate_required_columns -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Coverage report: htmlcov/index.html
```

### Example Unit Test

**File**: `tests/test_validation.py`

```python
import pytest
import pandas as pd
from src.validation import validate_transactions

def test_validate_required_columns():
    """Test that missing required columns raises error"""
    # Arrange
    df = pd.DataFrame({
        'date': ['2026-08-01'],
        'amount': [100],
        # Missing 'description'
    })
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate_transactions(df)

def test_validate_valid_data():
    """Test that valid data passes validation"""
    # Arrange
    df = pd.DataFrame({
        'transaction_id': [1],
        'date': ['2026-08-01'],
        'description': ['Coffee'],
        'amount': [3.50],
        'currency': ['USD'],
        'category': ['Food'],
        'account': ['Checking'],
        'transaction_type': ['Debit']
    })
    
    # Act
    result = validate_transactions(df)
    
    # Assert
    assert len(result) == 1
    assert result['amount'].iloc[0] == 3.50
```

---

## 🔗 Integration Tests

### Purpose
Test how multiple components work together

### Location
- `tests/test_etl_integration.py`
- `tests/test_api_integration.py`

### Run Integration Tests

```bash
# Run integration tests only
pytest tests/test_*_integration.py -v

# Run specific integration test
pytest tests/test_etl_integration.py::test_full_pipeline -v
```

### Example Integration Test

```python
import pytest
from src.etl_pipeline import run_pipeline
from src.database_connection import get_session

def test_etl_pipeline_full():
    """Test complete ETL pipeline with database"""
    # Setup
    csv_path = "data/raw/test_transactions.csv"
    
    # Execute
    output_path = run_pipeline(csv_path)
    
    # Verify output file exists
    assert os.path.exists(output_path)
    
    # Verify data in database
    session = get_session()
    count = session.query(Transaction).count()
    assert count > 0
```

---

## 🌐 End-to-End (E2E) Tests

### Purpose
Test entire system from API to database

### Location
`scripts/smoke_test_e2e.py`

### Run E2E Tests

```bash
# Run smoke tests
python scripts/smoke_test_e2e.py

# Expected output:
# TRANSACTION PIPELINE END-TO-END SMOKE TEST
# [1/6] Testing database connectivity... ✓
# [2/6] Running ETL pipeline... ✓
# [3/6] Testing API health endpoint... ✓
# [4/6] Testing /transactions endpoint... ✓
# [5/6] Testing anomaly detection... ✓
# [6/6] Testing full data flow... ✓
# 
# RESULTS: 6/6 tests passed
# ✓ ALL SMOKE TESTS PASSED
```

### E2E Test Stages

**1. Database Connectivity**
```python
def test_database_connectivity():
    """Verify database connection works"""
    session = get_session()
    result = session.execute(text("SELECT 1"))
    assert result is not None
```

**2. ETL Pipeline**
```python
def test_etl_pipeline():
    """Verify ETL loads data"""
    run_pipeline()
    session = get_session()
    count = session.query(Transaction).count()
    assert count > 0
```

**3. API Health**
```python
def test_api_health():
    """Verify API responds"""
    response = requests.get("http://127.0.0.1:8000/health")
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
```

**4. Transactions Endpoint**
```python
def test_transactions_endpoint():
    """Verify /transactions endpoint works"""
    response = requests.get("http://127.0.0.1:8000/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**5. Anomaly Detection**
```python
def test_anomaly_detection():
    """Verify anomaly detection works"""
    response = requests.get("http://127.0.0.1:8000/analytics/anomalies")
    assert response.status_code == 200
    assert 'anomalies' in response.json()
```

**6. Full Data Flow**
```python
def test_full_data_flow():
    """Test complete flow: CSV → DB → API"""
    # Load data
    run_pipeline()
    
    # Query API
    response = requests.get("http://127.0.0.1:8000/transactions?limit=1")
    data = response.json()
    
    # Verify data
    assert len(data) > 0
```

---

## 🚀 Continuous Integration Tests

### GitHub Actions (CI/CD)

**File**: `.github/workflows/ci.yml`

Automatically runs tests on every commit:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest -v --cov
```

---

## 📊 Test Coverage

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=src --cov=app --cov-report=html

# View report
# Open: htmlcov/index.html in browser
```

### Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| **src/** | 90% | 88% |
| **app/** | 85% | 82% |
| **Overall** | 85% | 84% |

---

## 🧪 Testing Best Practices

### 1. Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_validation.py       # Validation tests
├── test_transform.py        # Transformation tests
├── test_database.py         # Database tests
├── test_api_integration.py  # API tests
└── test_pipeline_e2e.py     # End-to-end tests
```

### 2. Use Fixtures

```python
import pytest
import pandas as pd

@pytest.fixture
def sample_transactions():
    """Sample transaction data for testing"""
    return pd.DataFrame({
        'transaction_id': [1, 2, 3],
        'date': ['2026-08-01', '2026-08-02', '2026-08-03'],
        'description': ['Coffee', 'Lunch', 'Dinner'],
        'amount': [3.50, 12.00, 25.00],
        'currency': ['USD', 'USD', 'USD'],
        'category': ['Food', 'Food', 'Food'],
        'account': ['Checking', 'Checking', 'Checking'],
        'transaction_type': ['Debit', 'Debit', 'Debit']
    })

def test_validate_transactions(sample_transactions):
    """Test validation with sample data"""
    result = validate_transactions(sample_transactions)
    assert len(result) == 3
```

### 3. Mock External Dependencies

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_api_with_mock(mock_get):
    """Test API without making real requests"""
    # Setup mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'ok'}
    mock_get.return_value = mock_response
    
    # Test
    response = requests.get('http://localhost:8000/health')
    
    # Assert
    assert response.status_code == 200
```

### 4. Test Edge Cases

```python
def test_empty_dataframe():
    """Test with empty data"""
    df = pd.DataFrame()
    result = validate_transactions(df)
    assert len(result) == 0

def test_negative_amounts():
    """Test with negative amounts"""
    df = pd.DataFrame({
        'amount': [-100, -50, -10]
    })
    # Validation should handle negative amounts

def test_special_characters():
    """Test with special characters in description"""
    df = pd.DataFrame({
        'description': ["It's", "café", "北京"]
    })
    # Should handle without errors
```

---

## 🐛 Debug Mode

### Run Tests with Debugging

```bash
# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Verbose mode
pytest -vv

# Run with debugger
pytest --pdb

# Combine options
pytest -s -x --pdb
```

### Print During Tests

```python
def test_something():
    data = process_data()
    print(f"\nData: {data}")  # Shows with -s flag
    assert len(data) > 0
```

---

## 📈 Performance Testing

### Measure Function Performance

```python
import time

def test_etl_performance():
    """Test ETL completes in reasonable time"""
    start = time.time()
    
    run_pipeline()
    
    duration = time.time() - start
    
    # Should complete in under 30 seconds
    assert duration < 30, f"ETL took {duration}s, expected < 30s"
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
# Run: locust -f locustfile.py

# Test API under load
```

---

## ✅ Pre-Deployment Test Checklist

Before deploying, ensure:

- [ ] All unit tests pass: `pytest`
- [ ] Integration tests pass
- [ ] E2E smoke tests pass: `python scripts/smoke_test_e2e.py`
- [ ] Code coverage > 85%: `pytest --cov`
- [ ] No security warnings: `bandit -r src app`
- [ ] No linting errors: `pylint src app`
- [ ] Database schema verified
- [ ] Configuration correct

---

## 🔄 Continuous Testing

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
# Runs tests before each commit
```

### Docker-based Testing

```bash
# Test in isolated environment
docker-compose -f docker-compose.test.yml up

# Or manually
docker run --rm -v $(pwd):/app python:3.11 pytest /app
```

---

## 📊 Test Metrics

### Track Over Time

```bash
# Generate metrics
pytest --cov=src --cov-report=term-missing

# Record results
echo "Date,Coverage,Tests" >> metrics.csv
echo "$(date),85%,42" >> metrics.csv
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[1_QUICKSTART.md](1_QUICKSTART.md)** — Quick start
- **[14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)** — Troubleshooting

---

**Testing ensures code quality and reliability!** 🧪✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
