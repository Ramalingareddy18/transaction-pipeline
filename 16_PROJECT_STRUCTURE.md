# 📁 Project Structure & Organization

## File Organization & Module Reference

**Read Time**: 10 minutes  
**Audience**: Developers, Maintainers  
**Format**: Directory Tree + File Purpose

---

## 🏗️ Complete Project Structure

```
transaction-pipeline/
│
├─ 📂 src/                          # Core ETL pipeline
│  ├─ project_paths.py              # Project root path resolution
│  ├─ database_config.py            # Database configuration
│  ├─ database_connection.py        # SQLAlchemy engine/session
│  ├─ etl_pipeline.py               # Main ETL orchestration
│  ├─ validation.py                 # Data validation logic
│  ├─ transform.py                  # Data transformation logic
│  └─ __init__.py                   # Package initialization
│
├─ 📂 app/                          # FastAPI application
│  ├─ main.py                       # FastAPI app & 8 endpoints
│  ├─ database.py                   # SQLAlchemy ORM models
│  ├─ health_check.py               # Health check functions
│  └─ __init__.py                   # Package initialization
│
├─ 📂 scripts/                      # Automation scripts
│  ├─ create_db.py                  # Database initialization
│  ├─ load_and_insert.py            # Direct data loading
│  ├─ smoke_test_e2e.py             # E2E system tests
│  ├─ validate_project.py           # Pre-flight checks
│  ├─ init-db.sql                   # SQL initialization
│  ├─ deploy.sh                     # Linux/macOS deployment
│  └─ deploy.ps1                    # Windows deployment
│
├─ 📂 dags/                         # Airflow DAGs
│  └─ transaction_pipeline_dag.py   # Airflow DAG definition
│
├─ 📂 models/                       # ML models
│  └─ anomaly_model.pkl             # Trained anomaly model
│
├─ 📂 data/                         # Data directory
│  ├─ raw/
│  │  └─ transactions.csv           # Input CSV
│  └─ processed/                    # Processed data
│
├─ 📂 backup/                       # Database backups
│  └─ backup_*.sql.gz               # Compressed backups
│
├─ 📂 logs/                         # Application logs
│  └─ app.log                       # Main log file
│
├─ 📂 tests/                        # Test suite
│  ├─ test_etl_pipeline.py          # Pipeline tests
│  ├─ test_api.py                   # API tests
│  ├─ test_database.py              # Database tests
│  └─ conftest.py                   # Pytest fixtures
│
├─ 📂 .github/                      # GitHub configuration
│  └─ workflows/
│     └─ ci.yml                     # GitHub Actions CI
│
├─ 📂 .streamlit/                   # Streamlit config
│  └─ config.toml                   # UI configuration
│
├─ 📂 docs/                         # Documentation
│  ├─ DOCS_INDEX.md                 # Documentation hub
│  ├─ 1_QUICKSTART.md               # Quick start guide
│  ├─ 2_INSTALLATION_GUIDE.md       # Installation steps
│  ├─ 3_PROJECT_ARCHITECTURE.md     # System architecture
│  ├─ 4_API_DOCUMENTATION.md        # API reference
│  ├─ 5_DASHBOARD_GUIDE.md          # Dashboard usage
│  ├─ 6_DATABASE_GUIDE.md           # Database setup
│  ├─ 7_DEPLOYMENT_GUIDE.md         # Production deployment
│  ├─ 8_DOCKER_GUIDE.md             # Docker guide
│  ├─ 9_TESTING_GUIDE.md            # Testing strategy
│  ├─ 10_ANOMALY_DETECTION.md       # ML detection
│  ├─ 11_AIRFLOW_INTEGRATION.md     # Airflow setup
│  ├─ 12_MONITORING_HEALTH.md       # Health checks
│  ├─ 13_CONFIGURATION_GUIDE.md     # Configuration
│  ├─ 14_TROUBLESHOOTING_GUIDE.md   # Troubleshooting
│  ├─ 15_EXAMPLES_RECIPES.md        # Code examples
│  └─ 16_PROJECT_STRUCTURE.md       # This file
│
├─ anomaly_detection.py             # ML anomaly detection
├─ dashboard.py                     # Streamlit dashboard
├─ requirements.txt                 # Python dependencies
├─ requirements-dev.txt             # Dev dependencies
├─ Dockerfile                       # Production container
├─ docker-compose.yml               # Dev environment
├─ docker-compose.prod.yml          # Prod environment
├─ .dockerignore                    # Docker ignore rules
├─ .gitignore                       # Git ignore rules
├─ .env.example                     # Config template
├─ README.md                        # Main readme
├─ LICENSE                          # License
└─ pyproject.toml                   # Python project config

```

---

## 📋 File Purposes

### 🔧 Core Configuration

| File | Purpose | Key Content |
|------|---------|-------------|
| `src/project_paths.py` | Absolute path resolution | `PROJECT_ROOT`, `resolve_project_path()` |
| `src/database_config.py` | DB configuration | `get_db_settings()`, `build_database_url()` |
| `.env` | Environment variables | `DB_*`, `API_*`, `ENVIRONMENT` |
| `.env.example` | Config template | Example values (no secrets) |
| `pyproject.toml` | Project metadata | Version, name, build config |

---

### 🗄️ Database Layer

| File | Purpose | Key Functions |
|------|---------|---|
| `src/database_connection.py` | SQLAlchemy setup | `create_engine()`, `SessionLocal` factory |
| `scripts/create_db.py` | Database initialization | Creates schema, tables, indexes |
| `scripts/init-db.sql` | SQL setup | Raw SQL for schema creation |
| `app/database.py` | ORM models | `Transaction` model (10 columns) |

---

### 📤 ETL Pipeline

| File | Purpose | Key Functions |
|------|---------|---|
| `src/etl_pipeline.py` | Main ETL orchestration | `run_pipeline()`, workflow logic |
| `src/validation.py` | Data validation | `validate_transactions()` |
| `src/transform.py` | Data transformation | `transform_transactions()` |
| `scripts/load_and_insert.py` | Direct loading | Alternative load method |
| `data/raw/transactions.csv` | Input data | Source CSV file |

---

### 🌐 API Layer

| File | Purpose | Key Endpoints |
|------|---------|---|
| `app/main.py` | FastAPI app | 8 REST endpoints, health checks |
| `app/health_check.py` | Health diagnostics | 4 health check functions |
| `.github/workflows/ci.yml` | CI/CD pipeline | Tests, builds, deploys |

---

### 📊 Analytics & ML

| File | Purpose | Key Functions |
|------|---------|---|
| `anomaly_detection.py` | Anomaly detection | `detect_anomalies()`, ML model |
| `dashboard.py` | Streamlit UI | Charts, metrics, data table |
| `.streamlit/config.toml` | Dashboard config | Theme, server settings |

---

### 🐳 Deployment

| File | Purpose | Key Config |
|------|---------|---|
| `Dockerfile` | Container image | Multi-stage build, health check |
| `docker-compose.yml` | Dev environment | 3 services: postgres, api, dashboard |
| `docker-compose.prod.yml` | Prod environment | Security hardened, Alpine images |
| `scripts/deploy.sh` | Linux deployment | Bash automation |
| `scripts/deploy.ps1` | Windows deployment | PowerShell automation |

---

### 🔍 Testing

| File | Purpose | Key Coverage |
|------|---------|---|
| `tests/test_etl_pipeline.py` | ETL tests | Validation, transformation |
| `tests/test_api.py` | API tests | Endpoints, responses |
| `tests/test_database.py` | Database tests | Connections, queries |
| `tests/conftest.py` | Test fixtures | Mock data, setup/teardown |
| `scripts/smoke_test_e2e.py` | E2E validation | System integration tests |

---

### 📚 Documentation

| File | Read Time | Audience |
|------|-----------|----------|
| `DOCS_INDEX.md` | 5 min | All users |
| `1_QUICKSTART.md` | 5 min | Quick starters |
| `2_INSTALLATION_GUIDE.md` | 20 min | Installers |
| `3_PROJECT_ARCHITECTURE.md` | 15 min | Architects |
| `4_API_DOCUMENTATION.md` | 15 min | API users |
| `5_DASHBOARD_GUIDE.md` | 10 min | Dashboard users |
| `6_DATABASE_GUIDE.md` | 15 min | DBAs |
| `7_DEPLOYMENT_GUIDE.md` | 20 min | DevOps |
| `8_DOCKER_GUIDE.md` | 15 min | Container ops |
| `9_TESTING_GUIDE.md` | 15 min | QA/Devs |
| `10_ANOMALY_DETECTION.md` | 15 min | Data scientists |
| `11_AIRFLOW_INTEGRATION.md` | 15 min | Schedulers |
| `12_MONITORING_HEALTH.md` | 15 min | SREs |
| `13_CONFIGURATION_GUIDE.md` | 15 min | DevOps |
| `14_TROUBLESHOOTING_GUIDE.md` | 20 min | Support |
| `15_EXAMPLES_RECIPES.md` | 20 min | Developers |
| `16_PROJECT_STRUCTURE.md` | 10 min | Architects |

---

## 🔗 Import Patterns

### Importing from src/

```python
# Project paths
from src.project_paths import PROJECT_ROOT, resolve_project_path

# Database
from src.database_config import get_db_settings, build_database_url
from src.database_connection import create_engine, SessionLocal

# ETL
from src.etl_pipeline import run_pipeline
from src.validation import validate_transactions
from src.transform import transform_transactions
```

---

### Importing from app/

```python
# FastAPI app
from app.main import app

# Models
from app.database import Transaction

# Health checks
from app.health_check import check_database_health
```

---

### Importing Analytics

```python
# Anomaly detection
from anomaly_detection import detect_anomalies

# Dashboard (run separately)
# streamlit run dashboard.py
```

---

## 📦 Dependencies by Layer

### Core (Always needed)
```
python>=3.11
pandas>=2.0
sqlalchemy>=2.0
psycopg2-binary>=2.9
python-dotenv>=0.19
pathlib
```

### API (For REST endpoints)
```
fastapi>=0.100
uvicorn>=0.23
pydantic>=2.0
```

### Analytics (For dashboard)
```
streamlit>=1.28
plotly>=5.17
requests>=2.31
```

### ML (For anomaly detection)
```
scikit-learn>=1.3
numpy>=1.24
```

### Deployment (For containerization)
```
docker>=20.10
docker-compose>=2.0
```

### Testing (For tests)
```
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.21
```

### Orchestration (For Airflow)
```
apache-airflow>=2.7
```

---

## 🔄 Module Dependencies

```
app/
├─ database.py
│  └─ src/database_connection.py
│     └─ src/database_config.py
│        └─ .env (via python-dotenv)
│
├─ health_check.py
│  └─ src/database_connection.py
│
└─ main.py
   ├─ app/health_check.py
   ├─ anomaly_detection.py
   └─ fastapi, uvicorn

src/
├─ etl_pipeline.py
│  ├─ src/validation.py
│  ├─ src/transform.py
│  └─ src/database_connection.py
│
├─ validation.py
│  └─ pandas
│
├─ transform.py
│  └─ pandas
│
└─ database_connection.py
   └─ src/database_config.py
```

---

## 🎯 How to Add New Features

### Adding a New API Endpoint

```
1. Define route in app/main.py
2. Add logic in app/database.py if needed
3. Add tests in tests/test_api.py
4. Update 4_API_DOCUMENTATION.md
5. Run: docker-compose restart api
```

---

### Adding a New ETL Step

```
1. Add function in src/transform.py
2. Call it in src/etl_pipeline.py
3. Add validation in src/validation.py
4. Add tests in tests/test_etl_pipeline.py
5. Update 3_PROJECT_ARCHITECTURE.md
```

---

### Adding a Dashboard Widget

```
1. Add code to dashboard.py
2. Fetch data from API (app/main.py)
3. Display with streamlit
4. Update 5_DASHBOARD_GUIDE.md
5. Test: streamlit run dashboard.py
```

---

### Adding a New Database Table

```
1. Define model in app/database.py
2. Create migration if needed
3. Update scripts/init-db.sql
4. Update 6_DATABASE_GUIDE.md
5. Run: python scripts/create_db.py
```

---

## 📊 Code Coverage

```
src/              90%+ coverage
app/              85%+ coverage
anomaly_detection 80%+ coverage
dashboard         75%+ coverage (UI heavy)
```

**Run coverage report**
```bash
pytest --cov=src --cov=app --cov-report=html
# View: htmlcov/index.html
```

---

## 🔍 Finding What You Need

### I need to...

**Add an API endpoint**
→ Edit: `app/main.py`
→ Read: `4_API_DOCUMENTATION.md`

**Fix database issue**
→ Edit: `src/database_config.py` or `app/database.py`
→ Read: `6_DATABASE_GUIDE.md`

**Change validation logic**
→ Edit: `src/validation.py`
→ Test: `tests/test_etl_pipeline.py`

**Deploy to production**
→ Run: `scripts/deploy.sh` or `.ps1`
→ Read: `7_DEPLOYMENT_GUIDE.md`

**Fix anomaly detection**
→ Edit: `anomaly_detection.py`
→ Read: `10_ANOMALY_DETECTION.md`

**Improve dashboard**
→ Edit: `dashboard.py`
→ Read: `5_DASHBOARD_GUIDE.md`

**Set up monitoring**
→ Read: `12_MONITORING_HEALTH.md`
→ Use: API endpoints `/health/*`

**Configure environment**
→ Edit: `.env`
→ Read: `13_CONFIGURATION_GUIDE.md`

**Debug issues**
→ Read: `14_TROUBLESHOOTING_GUIDE.md`
→ Run: `scripts/validate_project.py`

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)** — System architecture
- **[9_TESTING_GUIDE.md](9_TESTING_GUIDE.md)** — Test organization
- **[README.md](README.md)** — Main overview

---

**Understanding structure accelerates development!** 📁✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
