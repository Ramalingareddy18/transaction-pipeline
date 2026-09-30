# 🔧 Complete Installation Guide

## Step-by-Step Local Setup

**Estimated Time**: 20-30 minutes  
**Difficulty**: Beginner  
**Platforms**: Windows, macOS, Linux

---

## 📋 Pre-Installation Checklist

Before you start, verify you have:

- [ ] Python 3.11 or higher installed
- [ ] pip package manager
- [ ] PostgreSQL 14+ (local or Docker)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] ~2 GB free disk space
- [ ] Internet connection

### Check Your System

```bash
# Check Python version
python --version

# Should show: Python 3.11.x or higher

# Check pip
pip --version

# Should show: pip 23.x or higher
```

---

## 🔧 Part 1: Environment Setup

### Step 1.1: Navigate to Project

**Windows PowerShell**
```powershell
cd "C:\Users\linga\OneDrive\Desktop\python projects\transcation.csv"
```

**macOS/Linux Terminal**
```bash
cd /path/to/transcation.csv
```

### Step 1.2: Create Virtual Environment

Virtual environment isolates project dependencies.

**Windows PowerShell**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# You should see (.venv) prefix in terminal
```

**macOS/Linux**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# You should see (.venv) prefix in terminal
```

### Step 1.3: Upgrade pip

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Verify
pip --version
```

---

## 📦 Part 2: Install Dependencies

### Step 2.1: Review Dependencies

Open `requirements.txt` to see all dependencies:

```
pandas                 # Data processing
sqlalchemy            # Database ORM
psycopg2-binary       # PostgreSQL driver
python-dotenv         # Environment variables
fastapi               # API framework
uvicorn               # ASGI server
apache-airflow        # Workflow scheduling
streamlit             # Dashboard framework
plotly                # Charting library
scikit-learn          # ML library
requests              # HTTP client
```

### Step 2.2: Install All Dependencies

```bash
# Install all at once
pip install -r requirements.txt

# This will take 2-3 minutes
```

### Step 2.3: Verify Installation

```bash
# Check installed packages
pip list

# Should show all packages from requirements.txt
```

---

## 🗄️ Part 3: Database Configuration

### Step 3.1: Configure Environment File

```bash
# Copy the example environment file
# Windows:
copy .env.example .env

# macOS/Linux:
cp .env.example .env
```

### Step 3.2: Edit .env File

Open `.env` in your text editor and verify/update:

```bash
# Database Configuration
DB_HOST=localhost          # Usually localhost for local dev
DB_PORT=5432              # Default PostgreSQL port
DB_NAME=transaction_pipeline_db   # Database name
DB_USER=postgres          # PostgreSQL username
DB_PASSWORD=replace-with-a-unique-local-password  # Set your local PostgreSQL password
```

**Important**: Never commit `.env` to version control!

### Step 3.3: Verify .env File

```bash
# Windows
type .env

# macOS/Linux
cat .env

# Should show all database variables
```

---

## 🐘 Part 4: PostgreSQL Setup

### Option A: Local PostgreSQL (Windows)

1. Download from: https://www.postgresql.org/download/windows/
2. Run installer
3. Set password for `postgres` user
4. Remember the password
5. Verify installation:
   ```bash
   psql --version
   ```

### Option B: Local PostgreSQL (macOS)

```bash
# Using Homebrew
brew install postgresql@16
brew services start postgresql@16

# Verify
psql --version
```

### Option C: Local PostgreSQL (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Verify
psql --version
```

### Option D: PostgreSQL via Docker (All Platforms)

```bash
# Start PostgreSQL in Docker
docker run -d \
  --name transaction_db \
  -e POSTGRES_DB=transaction_pipeline_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=replace-with-a-unique-local-password \
  -p 5432:5432 \
  postgres:16

# Verify (should show container running)
docker ps | grep transaction_db
```

### Step 4.2: Test PostgreSQL Connection

```bash
# Test connection using psql
psql -h localhost -U postgres -d transaction_pipeline_db -c "SELECT VERSION();"

# Should return PostgreSQL version

# Or run the test script
python src\database_connection.py

# Should print: "PostgreSQL version: X.X"
```

---

## 🗃️ Part 5: Create Database & Schema

### Step 5.1: Run Database Creation Script

```bash
# Create the database
python scripts\create_db.py

# Expected output:
# Database created successfully!
# or
# Database already exists
```

### Step 5.2: Verify Database Exists

```bash
# List all databases
psql -h localhost -U postgres -l | grep transaction

# Should show: transaction_pipeline_db
```

### Step 5.3: Check Database Schema

```bash
# Connect to database
psql -h localhost -U postgres -d transaction_pipeline_db

# List tables
\dt

# Should be empty initially (tables created by ETL)

# Exit psql
\q
```

---

## 🏃 Part 6: Run the Application

### Step 6.1: Validate Project

```bash
# Run validation script
python scripts\validate_project.py

# Should show:
# [1/8] Checking project structure... ✓
# [2/8] Checking Python environment... ✓
# [3/8] Checking database connectivity... ✓
# [4/8] Checking environment configuration... ✓
# [5/8] Checking data files... ✓
# [6/8] Checking database schema... ✓
# [7/8] Checking API imports... ✓
# [8/8] Checking pipeline modules... ✓
# 
# RESULTS: 8/8 checks passed
# ✓ PROJECT IS READY FOR DEPLOYMENT
```

### Step 6.2: Run ETL Pipeline (Optional)

```bash
# Load sample data into database
python src\etl_pipeline.py

# Expected output:
# Pipeline completed successfully. Output: data/processed/cleaned_transactions.csv
```

### Step 6.3: Start API Server

**Open Terminal 1** (keep running)

```bash
# Start the API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Expected output:
# Uvicorn running on http://127.0.0.1:8000
# Application startup complete
```

### Step 6.4: Start Dashboard

**Open Terminal 2** (keep running)

```bash
# Start the dashboard
streamlit run dashboard.py

# Expected output:
# You can now view your Streamlit app in your browser.
# URL: http://127.0.0.1:8501
```

### Step 6.5: Run Smoke Tests

**Open Terminal 3**

```bash
# Run end-to-end smoke tests
python scripts\smoke_test_e2e.py

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
# ✓ ALL SMOKE TESTS PASSED - Project is production-ready
```

---

## ✅ Verify Everything Works

### Check API Health

```bash
# In Terminal 3 or new terminal
curl http://127.0.0.1:8000/health

# Response: {"status": "ok"}
```

### Open Dashboard

Open your browser:
```
http://127.0.0.1:8501
```

You should see:
- Transaction summary statistics
- Category spending charts
- Time-series graphs

### Open API Documentation

Open your browser:
```
http://127.0.0.1:8000/docs
```

You should see interactive Swagger documentation for all endpoints.

### Run Unit Tests

```bash
# Run all unit tests
python -m pytest -q

# Expected output: Test results showing passed/failed
```

---

## 🚀 You're Installed!

Congratulations! Your Transaction Pipeline is now installed and running.

### What's Running

| Service | URL | Command | Status |
|---------|-----|---------|--------|
| **API** | http://127.0.0.1:8000 | Terminal 1 | ✓ Running |
| **Dashboard** | http://127.0.0.1:8501 | Terminal 2 | ✓ Running |
| **Database** | localhost:5432 | PostgreSQL | ✓ Running |

---

## 🧹 Common Tasks After Installation

### Load Your Own CSV Data

```bash
# Place your CSV in: data/raw/transactions.csv
# Ensure column names match the schema

# Then run:
python src\etl_pipeline.py
```

### Stop All Services

```bash
# Press Ctrl+C in each terminal window
# Or close the terminal windows
```

### Clean Up Virtual Environment

```bash
# Deactivate environment
deactivate

# Delete it
# Windows: rmdir /s .venv
# macOS/Linux: rm -rf .venv
```

### Update Dependencies

```bash
# With virtual environment activated
pip install --upgrade -r requirements.txt
```

---

## 🆘 Troubleshooting Installation

### Issue: "python: command not found"

**Solution**: Python not installed or not in PATH
- Download from https://www.python.org
- During install, CHECK "Add Python to PATH"

### Issue: "Permission denied" on activate script

**Solution**: Windows security issue
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "pip install" fails with SSL error

**Solution**: Update certificates
```bash
pip install --upgrade certifi
pip install --upgrade -r requirements.txt
```

### Issue: "ModuleNotFoundError" when running scripts

**Solution**: Virtual environment not activated
```bash
# Windows:
.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate
```

### Issue: "FATAL: password authentication failed"

**Solution**: Wrong PostgreSQL password in .env
- Check your .env file
- Verify PostgreSQL password is correct
- Update if needed
- Run again

### Issue: "Port 5432 already in use"

**Solution**: PostgreSQL already running or port in use
```bash
# Windows - find process
netstat -ano | findstr :5432

# macOS/Linux - find process
lsof -i :5432

# Kill the process or use different port in .env
```

---

## 📚 Next Steps

### Learn the System

1. **Read Architecture**: [3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)
2. **Explore API**: [4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)
3. **Use Dashboard**: [5_DASHBOARD_GUIDE.md](5_DASHBOARD_GUIDE.md)

### Deploy to Production

1. **Follow**: [7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)
2. **Or use Docker**: [8_DOCKER_GUIDE.md](8_DOCKER_GUIDE.md)

### Load Data

1. **Prepare CSV**: Matching schema in requirements
2. **Run**: `python src\etl_pipeline.py`
3. **View**: Dashboard at http://127.0.0.1:8501

---

## 📞 Getting Help

- **Quick Start**: [1_QUICKSTART.md](1_QUICKSTART.md)
- **Architecture**: [3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)
- **Troubleshooting**: [14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)
- **All Docs**: [DOCS_INDEX.md](DOCS_INDEX.md)

---

**Installation complete! Start exploring!** 🎉

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
