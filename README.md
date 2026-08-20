# Transaction Pipeline

A production-grade transaction processing and analytics platform built with Python, FastAPI, PostgreSQL, and Streamlit.

## Features

- **Data Processing**: CSV ingestion, validation, transformation, and persistence
- **ETL Pipeline**: Scheduled data processing with Apache Airflow
- **Analytics API**: RESTful API with health checks, filtering, and anomaly detection
- **Dashboard**: Interactive Streamlit dashboard for visualization
- **Anomaly Detection**: ML-based detection using Isolation Forest
- **Docker Deployment**: Complete containerized stack with health checks
- **Production Ready**: Comprehensive logging, monitoring, and error handling

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Data Sources (CSV)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          ETL Pipeline (Python + Pandas)                 │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ Validation   │ Transform    │ Load to DB   │         │
│  └──────────────┴──────────────┴──────────────┘         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
│  ┌─────────────┬──────────────┬─────────────┐           │
│  │Transactions │Audit Logs    │Indexes      │           │
│  └─────────────┴──────────────┴─────────────┘           │
└────────┬──────────────────────────────────┬──────────────┘
         │                                  │
         ▼                                  ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│   FastAPI Service       │    │  Streamlit Dashboard    │
│  ┌───────────────────┐  │    │  ┌───────────────────┐  │
│  │ Health Checks     │  │    │  │ Analytics Charts  │  │
│  │ Transaction API   │  │    │  │ Category Summary  │  │
│  │ Anomaly Detection │  │    │  │ Time Series       │  │
│  │ Summary Analytics │  │    │  │ Data Exploration  │  │
│  └───────────────────┘  │    │  └───────────────────┘  │
└─────────────────────────┘    └─────────────────────────┘
```

## Project Structure

```
.
├── app/                          # FastAPI application
│   ├── main.py                   # API endpoints and routes
│   ├── database.py               # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic response schemas
│   └── health_check.py           # Health monitoring
├── src/                          # Data processing modules
│   ├── etl_pipeline.py           # Main ETL orchestration
│   ├── validation.py             # Data validation logic
│   ├── transform.py              # Data transformation
│   ├── load_data.py              # Database loading
│   ├── pipeline.py               # CSV preview pipeline
│   ├── database_config.py        # DB configuration
│   ├── database_connection.py    # Connection testing
│   └── project_paths.py          # Path resolution
├── dags/                         # Airflow DAGs
│   └── transaction_pipeline_dag.py
├── dashboard.py                  # Streamlit dashboard
├── anomaly_detection.py          # ML anomaly detection
├── tests/                        # Test suite
│   ├── test_api_smoke.py         # API smoke tests
│   ├── test_anomaly_detection.py # ML model tests
│   └── test_validation.py        # Data validation tests
├── scripts/                      # Utility and deployment scripts
│   ├── deploy.sh                 # Linux/macOS deployment
│   ├── deploy.ps1                # Windows PowerShell deployment
│   ├── smoke_test_e2e.py         # End-to-end validation
│   ├── check_api.py              # API health check
│   ├── create_db.py              # Database initialization
│   ├── load_and_insert.py        # Bulk data loading
│   └── init-db.sql               # SQL schema initialization
├── data/                         # Data directories
│   ├── raw/                      # Raw CSV input
│   └── processed/                # Processed output
├── docker-compose.yml            # Development composition
├── docker-compose.prod.yml       # Production composition
├── Dockerfile                    # Container image definition
├── .dockerignore                 # Docker build exclusions
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (for containerized deployment)
- pip package manager

## Local Development Setup

### 1. Clone and Setup

```bash
cd c:\Users\linga\OneDrive\Desktop\python projects\transcation.csv

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your PostgreSQL credentials
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=transaction_pipeline_db
# DB_USER=postgres
# DB_PASSWORD=your_password
```

### 4. Initialize Database

```bash
# Create the database
python scripts\create_db.py

# Test connection
python src\database_connection.py
```

## Running the Application

### Run ETL Pipeline

```bash
python src\etl_pipeline.py
```

Processes CSV files from `data/raw/` and loads into PostgreSQL. Output is saved to `data/processed/`.

### Start API Server

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

API available at: **http://127.0.0.1:8000**

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/detailed` | Comprehensive health status |
| GET | `/health/database` | Database health and stats |
| GET | `/health/data-quality` | Data quality metrics |
| GET | `/transactions` | List transactions (paginated) |
| GET | `/transactions/{id}` | Get single transaction |
| GET | `/analytics/anomalies` | Detect transaction anomalies |
| GET | `/analytics/summary` | Summary statistics |
| GET | `/docs` | Interactive API documentation |

### Start Dashboard

```bash
streamlit run dashboard.py --server.address 127.0.0.1 --server.port 8501
```

Dashboard available at: **http://127.0.0.1:8501**

## Testing

### Run All Tests

```bash
python -m pytest -q
```

### Run Specific Tests

```bash
# API smoke tests
python -m pytest tests/test_api_smoke.py -v

# Anomaly detection tests
python -m pytest tests/test_anomaly_detection.py -v

# Data validation tests
python -m pytest tests/test_validation.py -v
```

### End-to-End Validation

```bash
# Start API first (in another terminal)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Run comprehensive smoke tests
python scripts\smoke_test_e2e.py
```

## Docker Deployment

### Development Deployment

```bash
# Build and start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

```bash
# Linux/macOS:
bash scripts/deploy.sh production

# Windows PowerShell:
.\scripts\deploy.ps1 -Environment production
```

#### Using Docker Compose (Production)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Health Checks

The application includes comprehensive health checks at multiple levels:

### Container Health

Each container has a built-in health check:

```bash
# Check container health
docker-compose ps

# View health details
docker ps --format "{{.Names}}\t{{.Status}}"
```

### API Health Endpoints

```bash
# Basic health check
curl http://127.0.0.1:8000/health

# Detailed health
curl http://127.0.0.1:8000/health/detailed

# Database health
curl http://127.0.0.1:8000/health/database

# Data quality
curl http://127.0.0.1:8000/health/data-quality
```

### Automated Smoke Testing

```bash
python scripts\smoke_test_e2e.py
```

This validates:
- Database connectivity
- ETL pipeline
- API endpoints
- Anomaly detection
- Full data flow

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=postgres
DB_PASSWORD=your_secure_password

# API Configuration (for dashboard)
API_BASE_URL=http://127.0.0.1:8000
```

### Database Configuration

Edit `src/database_config.py` to customize:
- Database connection pooling
- URL building
- Admin connection settings

### Logging

Logs are written to:
- Docker containers: `docker-compose logs`
- Local files: Create `logs/` directory (auto-created)

## Airflow Integration

### Setup Airflow

```bash
# Initialize Airflow home
set AIRFLOW_HOME=%CD%\airflow
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

### Start Airflow Scheduler

```bash
airflow scheduler
```

### Start Airflow Webserver

```bash
airflow webserver --port 8080
```

Access Airflow UI at **http://localhost:8080**

## Anomaly Detection

The system uses Isolation Forest to detect unusual transactions:

```python
from anomaly_detection import detect_anomalies
import pandas as pd

df = pd.read_csv("transactions.csv")
flagged = detect_anomalies(df)

# flagged dataframe includes:
# - is_anomaly (boolean)
# - anomaly_score (float: lower = more anomalous)
```

API endpoint: `GET /analytics/anomalies`

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
python src\database_connection.py

# Check PostgreSQL service status (Windows)
net start postgresql-x64-14

# Check PostgreSQL status (Linux)
sudo systemctl status postgresql
```

### API Not Responding

```bash
# Check if port 8000 is in use
netstat -an | find ":8000"

# Kill process using port 8000
taskkill /F /PID <PID>
```

### Dashboard Connection Issues

```bash
# Verify API is running
curl http://127.0.0.1:8000/health

# Check Streamlit logs
streamlit run dashboard.py --logger.level=debug
```

### Docker Issues

```bash
# Clean up Docker resources
docker-compose down -v
docker system prune -a

# Rebuild images
docker-compose build --no-cache

# Check container logs
docker logs transaction_api
docker logs transaction_db
docker logs transaction_dashboard
```

## Performance Optimization

### Database Optimization

```sql
-- Add indexes (performed automatically)
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_category ON transactions(category);

-- Check query performance
EXPLAIN ANALYZE SELECT * FROM transactions WHERE category = 'Food';
```

### API Performance

- Connection pooling enabled
- Pagination implemented (limit/offset)
- Optional query parameter filtering

### Data Processing

- Pandas vectorized operations
- Batch database inserts
- Optional parallel processing

## Security Considerations

- **Secrets**: Store `DB_PASSWORD` in `.env` (not in version control)
- **API**: Add authentication layer for production
- **Database**: Use strong passwords, restrict network access
- **Docker**: Run containers with minimal privileges
- **Validation**: All input is validated before processing

## Production Checklist

- [ ] Environment variables set securely
- [ ] Database backups configured
- [ ] API authentication enabled
- [ ] HTTPS/TLS configured
- [ ] Health checks passing
- [ ] Smoke tests passing
- [ ] Logging and monitoring active
- [ ] Database indexes created
- [ ] Data retention policies set
- [ ] Disaster recovery plan in place

## Deployment Strategies

### Blue-Green Deployment

```bash
# Spin up new version
docker-compose -f docker-compose.new.yml up -d

# Test new version
python scripts/smoke_test_e2e.py

# Switch traffic
# Then tear down old
docker-compose down
```

### Rolling Updates

Update services one at a time while maintaining availability.

## Monitoring & Observability

### Logs

```bash
# View API logs
docker logs -f transaction_api

# View database logs
docker logs -f transaction_db

# View dashboard logs
docker logs -f transaction_dashboard
```

### Metrics

Available via health check endpoints:

```bash
curl http://127.0.0.1:8000/health/detailed
```

Returns:
- Database connection status
- Transaction count
- Data quality score
- System timestamps

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request
6. Ensure all tests pass
7. Update documentation

## License

Proprietary - All rights reserved

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review application logs
3. Run end-to-end smoke tests
4. Consult deployment documentation

---

**Last Updated**: 2026-08-13
**Version**: 1.0.0
**Status**: Production Ready
