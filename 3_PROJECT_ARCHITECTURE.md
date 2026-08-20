# 🏗️ Project Architecture & Design

## System Overview

**Read Time**: 15 minutes  
**Audience**: Developers, Architects, DevOps

---

## 📊 High-Level Architecture

### System Flow Diagram

```
┌─────────────────┐
│   CSV Files     │
│ (data/raw/)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   ETL Pipeline          │
│ ┌─────────────────────┐ │
│ │ 1. Validation       │ │  (src/validation.py)
│ │ - Schema check      │ │
│ │ - Data cleaning     │ │
│ └──────────┬──────────┘ │
│            │            │
│ ┌──────────▼──────────┐ │
│ │ 2. Transformation   │ │  (src/transform.py)
│ │ - Column derivation │ │
│ │ - Date parsing      │ │
│ └──────────┬──────────┘ │
│            │            │
│ ┌──────────▼──────────┐ │
│ │ 3. Loading          │ │  (src/etl_pipeline.py)
│ │ - DB insertion      │ │
│ │ - Index creation    │ │
│ └──────────┬──────────┘ │
└─────────────┼────────────┘
              │
              ▼
    ┌─────────────────────┐
    │   PostgreSQL DB     │
    │ ┌─────────────────┐ │
    │ │ transactions    │ │
    │ │ (indexed)       │ │
    │ ├─────────────────┤ │
    │ │ audit_logs      │ │
    │ └─────────────────┘ │
    └────────┬──────────┬─┘
             │          │
      ┌──────▼──┐  ┌───▼──────┐
      │          │  │           │
      ▼          ▼  ▼           ▼
   ┌────────────────┐    ┌──────────────────┐
   │  FastAPI       │    │  Streamlit       │
   │                │    │  Dashboard       │
   │ - Health       │    │                  │
   │ - Transactions │    │ - Charts         │
   │ - Analytics    │    │ - Analysis       │
   │ - Anomalies    │    │ - Exploration    │
   └────────────────┘    └──────────────────┘
        ▲                        ▲
        │                        │
        └────────┬───────────────┘
                 │
          ┌──────▼──────┐
          │   Client    │
          │   Browser   │
          └─────────────┘
```

---

## 🎯 Components Breakdown

### 1. Data Ingestion Layer

**Files**: `src/load_data.py`  
**Technology**: Pandas, SQLAlchemy

```python
# Reads CSV files from disk
# Handles various formats and encodings
# Manages file paths project-root aware

Features:
- Multiple CSV file support
- Flexible column mapping
- Error handling and logging
- Batch insertion optimization
```

### 2. Validation Layer

**Files**: `src/validation.py`  
**Technology**: Pandas

```python
# Ensures data quality
# Validates against schema
# Cleans invalid rows

Features:
- Required column checking
- Data type validation
- Missing value handling
- Error reporting
```

### 3. Transformation Layer

**Files**: `src/transform.py`  
**Technology**: Pandas, Python

```python
# Derives new columns
# Parses dates
# Categorizes transactions
# Calculates metrics

Features:
- Date/time extraction
- Categorical mapping
- Amount normalization
- Month/year calculation
```

### 4. Database Layer

**Files**: `app/database.py`, `src/database_config.py`  
**Technology**: SQLAlchemy, PostgreSQL

```
┌─ Tables ─────────────────┐
│ • transactions           │  Main transaction records
│ • audit_logs            │  Change audit trail
└──────────────────────────┘

┌─ Indexes ────────────────┐
│ • idx_date              │  Date-based queries
│ • idx_category          │  Category filtering
│ • idx_amount            │  Amount range queries
│ • idx_account           │  Account lookup
└──────────────────────────┘
```

### 5. API Layer

**Files**: `app/main.py`, `app/schemas.py`  
**Technology**: FastAPI

```
8 Endpoints:
├── Health Checks (4 endpoints)
│   ├── /health (basic)
│   ├── /health/detailed (comprehensive)
│   ├── /health/database (DB stats)
│   └── /health/data-quality (quality metrics)
│
├── Data Access (3 endpoints)
│   ├── /transactions (list with pagination)
│   ├── /transactions/{id} (single record)
│   └── /analytics/summary (summary stats)
│
└── Analytics (1 endpoint)
    └── /analytics/anomalies (ML detection)
```

### 6. Anomaly Detection Layer

**Files**: `anomaly_detection.py`  
**Technology**: scikit-learn, Isolation Forest

```python
# Detects unusual transactions
# Uses statistical ML model
# Returns anomaly scores

Model: Isolation Forest
- Contamination: 10% (expected anomaly rate)
- Random State: 42 (reproducible)
- Features: Transaction amount

Output:
- is_anomaly: boolean flag
- anomaly_score: float (-100 to 0)
```

### 7. Dashboard Layer

**Files**: `dashboard.py`  
**Technology**: Streamlit, Plotly

```
Dashboard Components:
├── Summary Section
│   ├── Total transactions
│   ├── Net amount
│   └── Average amount
│
├── Visualization Section
│   ├── Category spending (bar chart)
│   ├── Daily totals (line chart)
│   └── Time series analysis
│
└── Data Explorer
    └── Full transaction table
```

### 8. Orchestration Layer

**Files**: `dags/transaction_pipeline_dag.py`  
**Technology**: Apache Airflow

```
Daily DAG:
Start → ETL Pipeline → Success
        │
        └─→ Error Handling → Notification
```

---

## 📊 Data Flow Diagram

```
1. CSV Input
   │
   ├─→ [Validation] ─→ ✓ Valid / ✗ Invalid (logged)
   │
   ├─→ [Transform] ─→ Derived columns, parsed dates
   │
   ├─→ [Clean] ─→ Remove duplicates, null handling
   │
   ├─→ [Load] ─→ PostgreSQL
   │     │
   │     └─→ Create indexes, audit trail
   │
   ├─→ [API Access] ─→ Endpoints serve data
   │
   ├─→ [Anomaly Detection] ─→ ML model flags outliers
   │
   └─→ [Dashboard] ─→ Visual analytics
```

---

## 🗄️ Database Schema

### Transactions Table

```sql
CREATE TABLE transactions (
    transaction_id  INTEGER PRIMARY KEY,
    date           DATE,
    description    TEXT,
    amount         NUMERIC,
    currency       TEXT,
    category       TEXT,
    account        TEXT,
    transaction_type TEXT,
    month          INTEGER,
    year           INTEGER,
    created_at     TIMESTAMP DEFAULT NOW(),
    updated_at     TIMESTAMP DEFAULT NOW()
);
```

### Audit Logs Table

```sql
CREATE TABLE audit_logs (
    audit_id       SERIAL PRIMARY KEY,
    transaction_id INTEGER,
    action         TEXT,
    old_values     JSONB,
    new_values     JSONB,
    changed_at     TIMESTAMP DEFAULT NOW(),
    changed_by     TEXT DEFAULT 'system'
);
```

### Indexes

```sql
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_category ON transactions(category);
CREATE INDEX idx_transactions_amount ON transactions(amount);
CREATE INDEX idx_transactions_account ON transactions(account);
```

---

## 🔄 Request/Response Flow

### Example: Getting Transactions

```
1. CLIENT REQUEST
   GET http://127.0.0.1:8000/transactions?limit=10&category=Food
   
2. API RECEIVES
   FastAPI route handler processes request
   
3. VALIDATION
   Validate parameters (limit, offset, category)
   
4. DATABASE QUERY
   SELECT * FROM transactions 
   WHERE category = 'Food' 
   LIMIT 10
   
5. RESPONSE ASSEMBLY
   Pydantic schemas format response
   
6. CLIENT RECEIVES
   JSON Array:
   [
     {
       "transaction_id": 1,
       "date": "2026-08-01",
       "description": "Coffee",
       "amount": -3.50,
       "currency": "USD",
       "category": "Food",
       ...
     },
     ...
   ]
```

---

## 🐳 Deployment Architecture

### Local Development
```
Your Computer
├── Python Virtual Environment
├── PostgreSQL (local or Docker)
├── Uvicorn (API)
├── Streamlit (Dashboard)
└── Browser (Client)
```

### Docker Development
```
Docker Host
├── Container 1: PostgreSQL
├── Container 2: FastAPI (Uvicorn)
├── Container 3: Streamlit (Dashboard)
└── Bridge Network: Internal communication
```

### Production
```
Load Balancer
    ↓
API Cluster
├── API Pod 1
├── API Pod 2
└── API Pod N
    ↓
PostgreSQL Cluster (Replicated)
    ↓
Cache Layer (Redis)
    ↓
Dashboard (Separate Deployment)
```

---

## 🔒 Security Architecture

### Authentication
- Environment-based secrets (.env)
- Connection pooling with auth
- No credentials in code

### Authorization
- Future: JWT tokens
- Role-based access control (RBAC)
- API key management

### Data Protection
- SQL injection prevention (parameterized queries)
- Input validation on all endpoints
- HTTPS ready (deploy with TLS)

### Monitoring
- Health check endpoints
- Audit logging
- Error logging
- Performance metrics

---

## ⚙️ Technology Stack

### Backend
| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python | 3.11+ |
| **API** | FastAPI | 0.100+ |
| **Server** | Uvicorn | 0.23+ |
| **Database** | PostgreSQL | 14+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Driver** | psycopg2 | 2.9+ |

### Data Processing
| Layer | Technology | Version |
|-------|-----------|---------|
| **Transformation** | Pandas | 2.0+ |
| **ML** | scikit-learn | 1.3+ |
| **Processing** | NumPy | 1.24+ |

### Frontend & Visualization
| Layer | Technology | Version |
|-------|-----------|---------|
| **Dashboard** | Streamlit | 1.28+ |
| **Charts** | Plotly | 5.17+ |
| **HTTP** | requests | 2.31+ |

### Deployment & Orchestration
| Layer | Technology | Version |
|-------|-----------|---------|
| **Containerization** | Docker | 20.10+ |
| **Composition** | Docker Compose | 2.0+ |
| **Scheduling** | Apache Airflow | 2.7+ |

---

## 📈 Scalability Considerations

### Horizontal Scaling
```
Multiple API Instances
    ↓
Connection Pooling (pgBouncer)
    ↓
PostgreSQL Primary/Replica
    ↓
Read Replicas for Dashboard
```

### Vertical Scaling
- Increase container resources
- Larger database instances
- Caching layer (Redis)

### Performance
- Query optimization
- Index tuning
- Connection pooling
- Result caching

---

## 🚀 Deployment Options

### Option 1: Local Development
- Single machine
- Direct Python execution
- Local PostgreSQL

### Option 2: Docker Compose
- All services in containers
- Single host
- Development & testing

### Option 3: Kubernetes
- Distributed deployment
- Auto-scaling
- High availability
- Production-grade

### Option 4: Cloud Platforms
- AWS (ECS, RDS)
- Google Cloud (Cloud Run, Cloud SQL)
- Azure (Container Instances, Database)

---

## 🔗 Integration Points

### External Systems
- **CSV Files**: Input data source
- **Email**: Future notifications
- **Webhooks**: Future event triggers
- **Analytics Platforms**: Future data export

### APIs
- **Airflow**: Pipeline orchestration
- **PostgreSQL**: Data persistence
- **FastAPI**: REST interface
- **Streamlit**: Web dashboard

---

## 📊 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **API Response Time** | <100ms | Per endpoint |
| **Database Query** | <50ms | Average |
| **ETL Processing** | ~1-5 sec | Per 1000 rows |
| **Memory Usage** | ~500MB | Typical |
| **Disk Usage** | ~1GB | With data |
| **Max Concurrent Users** | 100+ | With scaling |

---

## 🎯 Design Principles

1. **Separation of Concerns**
   - ETL separate from API
   - API separate from Dashboard
   - Database independent

2. **Scalability**
   - Stateless services
   - Horizontal scaling ready
   - Connection pooling

3. **Reliability**
   - Error handling
   - Validation
   - Health checks
   - Audit logging

4. **Maintainability**
   - Clear code structure
   - Comprehensive documentation
   - Configuration externalized
   - Logging throughout

5. **Security**
   - Environment-based secrets
   - Input validation
   - SQL injection prevention
   - Audit trails

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[2_INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md)** — Setup instructions
- **[4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)** — API endpoints
- **[7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)** — Production deployment
- **[8_DOCKER_GUIDE.md](8_DOCKER_GUIDE.md)** — Docker setup

---

**Architecture is modular, scalable, and production-ready.** ✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
