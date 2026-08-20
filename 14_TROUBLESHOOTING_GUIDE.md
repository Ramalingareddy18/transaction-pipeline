# 🔧 Troubleshooting Guide

## Common Issues & Solutions

**Read Time**: 20 minutes  
**Audience**: All Users  
**Format**: Problem → Symptoms → Solution

---

## 🆘 Quick Issue Finder

**Can't start the application?**
→ [Installation Issues](#-installation-issues)

**API or Dashboard not working?**
→ [Runtime Issues](#-runtime-issues)

**Database connection problems?**
→ [Database Issues](#-database-issues)

**Got an error message?**
→ [Error Messages](#-common-error-messages)

---

## 📋 Installation Issues

### Issue: "ModuleNotFoundError" after pip install

**Symptoms**
```
ModuleNotFoundError: No module named 'pandas'
```

**Causes**
- Virtual environment not activated
- Dependencies not installed
- Wrong Python version

**Solution**
```bash
# 1. Verify Python version
python --version
# Should be 3.11+

# 2. Activate virtual environment
# Windows:
.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# 3. Verify venv is active (should see (.venv) prefix)

# 4. Reinstall dependencies
pip install -r requirements.txt

# 5. Verify installation
python -c "import pandas; print(pandas.__version__)"
```

---

### Issue: "Permission denied" on Unix systems

**Symptoms**
```
bash: activate: Permission denied
```

**Solution**
```bash
# Make script executable
chmod +x .venv/bin/activate

# Then activate
source .venv/bin/activate
```

---

### Issue: Virtual environment won't activate (Windows)

**Symptoms**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution**
```powershell
# Run PowerShell as Administrator

# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Now activate
.venv\Scripts\Activate.ps1

# Verify (should see (.venv) prefix)
```

---

### Issue: "pip install" fails with SSL error

**Symptoms**
```
ERROR: Could not install packages due to an EnvironmentError: 
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution**
```bash
# Update certificates
pip install --upgrade certifi

# Try install again
pip install -r requirements.txt

# Or temporarily bypass (not recommended for production)
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

## 🗄️ Database Issues

### Issue: "Cannot connect to database"

**Symptoms**
```
ERROR: could not connect to server: Connection refused
Is the server running on host "localhost" (127.0.0.1) and accepting
TCP/IP connections on port 5432?
```

**Diagnosis**
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Expected output:
# localhost:5432 - accepting connections
```

**Solution**

Windows:
```
1. Open Services (services.msc)
2. Find "PostgreSQL"
3. Right-click → Start
4. Try connecting again
```

macOS:
```bash
brew services start postgresql@16
```

Linux:
```bash
sudo systemctl start postgresql
```

Docker:
```bash
docker-compose up -d postgres
```

---

### Issue: "FATAL: password authentication failed"

**Symptoms**
```
FATAL: password authentication failed for user "postgres"
```

**Causes**
- Wrong password in .env
- PostgreSQL password changed
- Wrong username

**Solution**
```bash
# 1. Verify .env has correct password
cat .env | grep DB_PASSWORD

# 2. Reset PostgreSQL password
# Windows: Use pgAdmin
# macOS/Linux:
sudo -u postgres psql

# In psql:
ALTER USER postgres WITH PASSWORD 'new_password';
\q

# 3. Update .env
DB_PASSWORD=new_password

# 4. Test connection
psql -h localhost -U postgres -d transaction_pipeline_db
```

---

### Issue: "Database does not exist"

**Symptoms**
```
FATAL: database "transaction_pipeline_db" does not exist
```

**Solution**
```bash
# 1. Create database
createdb -U postgres transaction_pipeline_db

# Or with Python:
python scripts/create_db.py

# 2. Verify it exists
psql -l | grep transaction

# 3. Try connecting
psql -h localhost -U postgres -d transaction_pipeline_db
```

---

### Issue: "Disk space full" in database

**Symptoms**
```
ERROR: could not write to file "base/...": No space left on device
```

**Solution**
```bash
# 1. Check disk space
df -h

# 2. Find large files
du -sh * | sort -h

# 3. Remove old backups
rm -f /backup/*.sql.gz

# 4. Vacuum database
psql -U postgres -d transaction_pipeline_db -c "VACUUM FULL;"

# 5. If still full, add more disk space
```

---

## 🚀 Runtime Issues

### Issue: "API won't start"

**Symptoms**
```
Uvicorn running on http://127.0.0.1:8000
<hangs and doesn't continue>
```

**Diagnosis**
```bash
# Check what's happening
# Look for errors in the output
# Press Ctrl+C and try with more verbose output
python -m uvicorn app.main:app --log-level debug
```

**Solution**

If stuck at startup:
```bash
# 1. Check for import errors
python -c "from app import main"

# 2. Check database connection
python src/database_connection.py

# 3. Verify configuration
cat .env

# 4. Try with simpler config
# Disable optional features if needed

# 5. Restart
Ctrl+C
python -m uvicorn app.main:app
```

---

### Issue: "Port already in use"

**Symptoms**
```
OSError: [Errno 48] Address already in use
```

**Solution**

Windows (PowerShell):
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --port 8001
```

macOS/Linux:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

---

### Issue: "API responds slowly"

**Symptoms**
```
curl http://127.0.0.1:8000/transactions takes > 5 seconds
```

**Causes**
- Large dataset
- Database overloaded
- Network issue
- API code inefficient

**Solution**

```bash
# 1. Check server resources
docker stats

# 2. Check API logs
docker-compose logs transaction-api | tail -20

# 3. Limit query size
curl "http://127.0.0.1:8000/transactions?limit=10"

# 4. Check database
curl http://127.0.0.1:8000/health/database

# 5. Restart services
docker-compose restart

# 6. Check if data is corrupt
python scripts/validate_project.py
```

---

### Issue: "Dashboard says 'Unable to reach the API'"

**Symptoms**
```
In dashboard web interface:
"Unable to reach the API at http://127.0.0.1:8000"
```

**Causes**
- API not running
- Wrong API URL configured
- Network issue

**Solution**
```bash
# 1. Check if API is running
curl http://127.0.0.1:8000/health

# If fails, API is not running:
# Terminal 1:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# 2. Check dashboard configuration
# In dashboard.py, verify API_URL:
grep "API_URL" dashboard.py

# Should be: http://127.0.0.1:8000

# 3. Restart dashboard
# Ctrl+C in dashboard terminal
streamlit run dashboard.py
```

---

### Issue: "Docker container keeps restarting"

**Symptoms**
```
docker-compose ps shows:
transaction-api    Up (starting for 3 seconds)
```

**Solution**
```bash
# 1. Check logs
docker-compose logs transaction-api

# 2. Look for specific error (usually at end)

# 3. Common causes:
# - Port already in use
# - Database not ready
# - Configuration missing

# 4. Restart services in order
docker-compose down
docker-compose up -d postgres
sleep 10
docker-compose up -d api
docker-compose up -d dashboard

# 5. Verify health
docker-compose ps
```

---

## 📊 Data Issues

### Issue: "No data in dashboard"

**Symptoms**
```
Dashboard shows 0 transactions
API returns empty list
```

**Causes**
- ETL hasn't run
- Data not loaded
- Database empty

**Solution**
```bash
# 1. Load sample data
python src/etl_pipeline.py

# 2. Verify data loaded
curl http://127.0.0.1:8000/analytics/summary

# 3. Check database directly
psql -h localhost -U postgres -d transaction_pipeline_db
# In psql:
SELECT COUNT(*) FROM transactions;
\q

# 4. Check file exists
ls -la data/raw/transactions.csv

# 5. Check file format
head -3 data/raw/transactions.csv
```

---

### Issue: "Invalid CSV file"

**Symptoms**
```
KeyError: 'transaction_id'
ValueError: cannot parse...
```

**Solution**
```bash
# 1. Verify CSV has required columns
head -1 data/raw/transactions.csv

# Required columns:
# transaction_id, date, description, amount, currency, 
# category, account, transaction_type

# 2. Check file encoding
file data/raw/transactions.csv

# 3. Validate data
python -c "
import pandas as pd
df = pd.read_csv('data/raw/transactions.csv')
print(f'Columns: {df.columns.tolist()}')
print(f'Rows: {len(df)}')
print(df.head())
"

# 4. If missing columns, update CSV or skip validation
```

---

### Issue: "High anomaly rate (>10%)"

**Symptoms**
```
/analytics/anomalies returns many anomalies
```

**Causes**
- Contamination rate too high
- Data changed significantly
- Model needs retraining

**Solution**
```bash
# 1. Check current anomaly rate
curl http://127.0.0.1:8000/health/data-quality

# 2. Review anomalies
curl "http://127.0.0.1:8000/analytics/anomalies?limit=10"

# 3. Are they legitimate anomalies?
# If yes, normal behavior

# 4. If too many false positives, retrain model
python scripts/retrain_anomaly_model.py

# 5. Adjust contamination rate in anomaly_detection.py
# contamination=0.05  # If too strict
# contamination=0.15  # If too relaxed
```

---

## 🔐 Security Issues

### Issue: ".env file leaked to GitHub"

**Symptoms**
```
Found .env in git history
```

**Solution (IMMEDIATE)**
```bash
# 1. Revoke all secrets
# Password, API keys, etc.

# 2. Remove from git history
git filter-branch --tree-filter 'rm -f .env' HEAD

# 3. Force push (carefully!)
git push origin --force-with-lease

# 4. Add to .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
git push
```

---

### Issue: "Access denied" to database

**Symptoms**
```
psql: error: could not translate host name "postgres" to address
```

**Causes**
- Wrong hostname
- Network issue
- Container not running

**Solution**
```bash
# 1. Check container is running
docker-compose ps

# 2. Test container communication
docker-compose exec api ping postgres

# 3. Check network
docker network ls

# 4. Verify connection string in .env
# For Docker: DB_HOST=postgres (service name)
# For local: DB_HOST=localhost

# 5. Restart containers
docker-compose down
docker-compose up -d
```

---

## 🎯 Performance Issues

### Issue: "Memory usage growing"

**Symptoms**
```
Memory increases over time
Eventually API crashes
```

**Solution**
```bash
# 1. Check memory usage
docker stats

# 2. View logs for errors
docker-compose logs -f transaction-api

# 3. Restart service
docker-compose restart transaction-api

# 4. Monitor recovery
docker stats

# 5. If problem persists:
# - Check for memory leaks in code
# - Increase container memory limits
# - Enable memory profiling
```

---

### Issue: "CPU usage spike"

**Symptoms**
```
CPU usage suddenly jumps to 100%
```

**Solution**
```bash
# 1. Check processes
ps aux | grep python

# 2. Check logs
docker-compose logs --tail 50

# 3. Identify bottleneck
# - Large database query
# - Inefficient algorithm
# - Infinite loop

# 4. Restart and monitor
docker-compose restart

# 5. Check resource limits
# Increase if needed in docker-compose.yml
```

---

## 📞 Getting Help

### When stuck, try:

1. **Search logs**
   ```bash
   docker-compose logs | grep -i error
   ```

2. **Run validation**
   ```bash
   python scripts/validate_project.py
   ```

3. **Check health**
   ```bash
   curl http://127.0.0.1:8000/health/detailed
   ```

4. **Restart services**
   ```bash
   docker-compose restart
   ```

5. **Review documentation**
   - [DOCS_INDEX.md](DOCS_INDEX.md)
   - [14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[2_INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md)** — Installation steps
- **[12_MONITORING_HEALTH.md](12_MONITORING_HEALTH.md)** — Health monitoring
- **[7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)** — Production deployment

---

**Troubleshooting resolves issues quickly!** 🔧✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
