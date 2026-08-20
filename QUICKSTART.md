# Quick Start Guide

Get the Transaction Pipeline running in 5 minutes.

## Windows (PowerShell)

### Local Development

```powershell
# 1. Open PowerShell and navigate to project
cd "C:\Users\linga\OneDrive\Desktop\python projects\transcation.csv"

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
copy .env.example .env
# Edit .env with your database credentials

# 5. Initialize database
python scripts\create_db.py

# 6. Open three terminals and run:

# Terminal 1: API Server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Dashboard
streamlit run dashboard.py

# Terminal 3: Run smoke tests
python scripts\smoke_test_e2e.py
```

**Access:**
- API: http://127.0.0.1:8000
- Dashboard: http://127.0.0.1:8501
- API Docs: http://127.0.0.1:8000/docs

### Docker Deployment

```powershell
# 1. Build and start
docker-compose up --build

# 2. Wait for services to be healthy (30-40 seconds)

# 3. Access the services
# API: http://localhost:8000
# Dashboard: http://localhost:8501
# Database: localhost:5432

# 4. Stop services
docker-compose down
```

## macOS/Linux

### Local Development

```bash
# 1. Navigate to project
cd /path/to/transcation.csv

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with credentials

# 5. Initialize database
python scripts/create_db.py

# 6. Run the application
# Terminal 1:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2:
streamlit run dashboard.py

# Terminal 3:
python scripts/smoke_test_e2e.py
```

### Docker Deployment

```bash
# Using deployment script
bash scripts/deploy.sh development

# Or manually:
docker-compose up --build
```

## Verify Installation

### Quick Health Check

```bash
# API Health
curl http://127.0.0.1:8000/health

# Detailed Health
curl http://127.0.0.1:8000/health/detailed

# Transactions
curl http://127.0.0.1:8000/transactions?limit=5

# Anomalies
curl http://127.0.0.1:8000/analytics/anomalies
```

### Run Tests

```bash
python -m pytest -q
python scripts/smoke_test_e2e.py
```

## Common Issues

### "Port 8000 already in use"

```powershell
# Windows: Kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS:
lsof -i :8000
kill -9 <PID>
```

### "Database connection refused"

```bash
# Check PostgreSQL is running
# Windows: Services > PostgreSQL
# Linux: sudo systemctl status postgresql
# macOS: brew services list

# Or use Docker
docker-compose up postgres -d
```

### "Module not found" errors

```bash
# Ensure virtual environment is activated
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. ✅ Application is running
2. 📊 Open dashboard at http://127.0.0.1:8501
3. 📝 Load transaction data: `python src/etl_pipeline.py`
4. 🔍 Check API docs: http://127.0.0.1:8000/docs
5. 🧪 Run tests: `python -m pytest`
6. 🚀 Deploy to Docker: `docker-compose up --build`

## Support

- **API Documentation**: http://127.0.0.1:8000/docs
- **Main README**: See README.md
- **Database Setup**: See README_DB.md
- **Troubleshooting**: See README.md Troubleshooting section
