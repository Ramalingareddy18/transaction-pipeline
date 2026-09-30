# ⚡ Quick Start Guide - 5 Minutes

## Get the Transaction Pipeline Running Right Now

**Estimated Time**: 5 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Python 3.11+, pip

---

## 🎯 Choose Your Setup Method

### Option A: Local Development (Recommended for Beginners)

#### Windows PowerShell

```powershell
# Step 1: Open PowerShell and navigate to project
cd "C:\Users\linga\OneDrive\Desktop\python projects\transcation.csv"

# Step 2: Create virtual environment
python -m venv .venv

# Step 3: Activate virtual environment
.venv\Scripts\Activate.ps1

# Step 4: Upgrade pip
python -m pip install --upgrade pip

# Step 5: Install dependencies
pip install -r requirements.txt

# Step 6: Copy environment file
copy .env.example .env

# Step 7: Create database
python scripts\create_db.py

# Step 8: Open three separate PowerShell windows and run:

# Window 1: Start API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Window 2: Start Dashboard
streamlit run dashboard.py

# Window 3: Test the system
python scripts\smoke_test_e2e.py
```

#### macOS/Linux

```bash
# Navigate to project
cd /path/to/transcation.csv

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Create database
python scripts/create_db.py

# In three separate terminal windows:

# Terminal 1: Start API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Dashboard
streamlit run dashboard.py

# Terminal 3: Test the system
python scripts/smoke_test_e2e.py
```

---

### Option B: Docker (Recommended for Production)

#### Windows

```powershell
# Navigate to project
cd "C:\Users\linga\OneDrive\Desktop\python projects\transcation.csv"

# Start all services
docker-compose up --build

# Wait for services to start (30-40 seconds)
# You'll see "Application startup complete" when ready
```

#### macOS/Linux

```bash
# Navigate to project
cd /path/to/transcation.csv

# Start all services
docker-compose up --build

# Wait for services to start
```

---

## ✅ Verify Everything Works

### Check the API

```bash
# Test health endpoint
curl http://127.0.0.1:8000/health

# You should see:
# {"status": "ok"}
```

### Check the Dashboard

Open your browser:
```
http://127.0.0.1:8501
```

### Check Detailed Health

```bash
curl http://127.0.0.1:8000/health/detailed

# Response includes database status and transaction count
```

---

## 🎮 Access Points

After setup, you can access:

| Service | URL | Purpose |
|---------|-----|---------|
| **API** | http://127.0.0.1:8000 | Transaction endpoints |
| **API Documentation** | http://127.0.0.1:8000/docs | Interactive Swagger UI |
| **Dashboard** | http://127.0.0.1:8501 | Analytics & charts |
| **Health Check** | http://127.0.0.1:8000/health | System status |

---

## 🧪 Run Your First Test

```bash
# Run comprehensive smoke test
python scripts\smoke_test_e2e.py

# Expected output:
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

---

## 📊 Load Sample Data

```bash
# Run the ETL pipeline
python src\etl_pipeline.py

# This will:
# 1. Read transactions.csv from data/raw/
# 2. Validate the data
# 3. Transform columns
# 4. Load into PostgreSQL
```

---

## 🆘 Something Didn't Work?

### Issue: "Module not found" error

**Solution**: Make sure virtual environment is activated
```powershell
# Windows - run this in PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### Issue: "Port 8000 already in use"

**Solution**: Stop the API or use a different port
```bash
# Check what's using port 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Kill the process or change port
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### Issue: "Database connection refused"

**Solution**: Check if PostgreSQL is running
```bash
# Windows - check PostgreSQL service
# Go to Services > PostgreSQL and start it

# Or use Docker PostgreSQL
docker run -d \
  -e POSTGRES_DB=transaction_pipeline_db \
  -e POSTGRES_USER=postgres \
   -e POSTGRES_PASSWORD=replace-with-a-unique-local-password \
  -p 5432:5432 \
  postgres:16
```

### Issue: Dashboard shows "Unable to reach the API"

**Solution**: Make sure API is running first
```powershell
# Start API first
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Then start dashboard (in another window)
streamlit run dashboard.py
```

---

## 📚 Next Steps

### I got it running, now what?

1. **Explore the Dashboard**
   - Open http://127.0.0.1:8501
   - See transaction charts and analytics
   - Click on expandable sections

2. **Try the API**
   - Open http://127.0.0.1:8000/docs
   - Try out the endpoints
   - See the responses

3. **Load Your Own Data**
   - Place CSV in `data/raw/`
   - Column names must match schema
   - Run `python src/etl_pipeline.py`

4. **Read More Documentation**
   - [INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md) — Detailed setup
   - [API_DOCUMENTATION.md](4_API_DOCUMENTATION.md) — All endpoints
   - [DASHBOARD_GUIDE.md](5_DASHBOARD_GUIDE.md) — Dashboard features

---

## 🚀 Production Deployment

When you're ready for production:

```bash
# Using Docker (recommended)
docker-compose -f docker-compose.prod.yml up -d

# Or follow: [DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)
```

---

## 📞 Need More Help?

- **Detailed Setup**: [2_INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md)
- **Understanding the Project**: [3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)
- **API Reference**: [4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)
- **Troubleshooting**: [14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)
- **All Documentation**: [DOCS_INDEX.md](DOCS_INDEX.md)

---

## ✨ You're All Set!

Your Transaction Pipeline is now running. Explore the dashboard, try the API, and check out the other documentation to learn more.

**Happy coding!** 🎉

---

**Quick Reference**
- Start API: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Start Dashboard: `streamlit run dashboard.py`
- Run Tests: `python scripts\smoke_test_e2e.py`
- Load Data: `python src\etl_pipeline.py`

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
