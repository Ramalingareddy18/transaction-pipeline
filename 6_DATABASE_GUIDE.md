# 🗄️ PostgreSQL Database Guide

## Database Setup & Management

**Read Time**: 15 minutes  
**Audience**: DBAs, Developers, Data Engineers

---

## 📋 Quick Overview

**Database**: PostgreSQL 14+  
**Schema Name**: public (default)  
**Main Tables**: transactions, audit_logs  
**Access**: `psql` command-line or GUI tools

---

## 🚀 Initial Setup

### Step 1: Install PostgreSQL

**Windows**
1. Download: https://www.postgresql.org/download/windows/
2. Run installer
3. Choose password for postgres user
4. Note the port (default 5432)

**macOS**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Verify Installation

```bash
# Check version
psql --version

# Should show: psql (PostgreSQL) 14.x or higher
```

### Step 3: Connect to PostgreSQL

```bash
# Connect as default user
psql -U postgres

# Connected! You see:
# postgres=#

# Exit psql
\q
```

---

## 📊 Database Schema

### Transactions Table

**Purpose**: Store all transaction data  
**Records**: Typically 1000s to millions

```sql
CREATE TABLE transactions (
    transaction_id      INTEGER PRIMARY KEY,
    date               DATE NOT NULL,
    description        TEXT,
    amount             NUMERIC(15,2) NOT NULL,
    currency           VARCHAR(3) DEFAULT 'USD',
    category           VARCHAR(100),
    account            VARCHAR(100),
    transaction_type   VARCHAR(10),
    month              INTEGER,
    year               INTEGER,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns Explained**

| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| `transaction_id` | INTEGER | Unique ID | 1, 2, 3 |
| `date` | DATE | Transaction date | 2026-08-01 |
| `description` | TEXT | What purchased | "Coffee Shop" |
| `amount` | NUMERIC | Dollar amount | 3.50, -1000 |
| `currency` | VARCHAR | Currency code | "USD", "EUR" |
| `category` | VARCHAR | Spending category | "Food", "Transport" |
| `account` | VARCHAR | Account name | "Checking", "Credit" |
| `transaction_type` | VARCHAR | Debit/Credit | "Debit", "Credit" |
| `month` | INTEGER | Month (1-12) | 1, 8, 12 |
| `year` | INTEGER | Year | 2026, 2027 |
| `created_at` | TIMESTAMP | Creation time | Auto-set |
| `updated_at` | TIMESTAMP | Last update | Auto-set |

---

### Audit Logs Table

**Purpose**: Track all data changes for compliance  
**Retention**: Typically 1-7 years

```sql
CREATE TABLE audit_logs (
    audit_id       SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(transaction_id),
    action         VARCHAR(50),
    old_values     JSONB,
    new_values     JSONB,
    changed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by     VARCHAR(100) DEFAULT 'system'
);
```

---

## 🔑 Indexes

**Purpose**: Speed up queries  
**Tradeoff**: Faster reads, slower writes

### Current Indexes

```sql
CREATE INDEX idx_transactions_date 
    ON transactions(date);

CREATE INDEX idx_transactions_category 
    ON transactions(category);

CREATE INDEX idx_transactions_amount 
    ON transactions(amount);

CREATE INDEX idx_transactions_account 
    ON transactions(account);
```

### View Existing Indexes

```bash
# Connect to database
psql -U postgres -d transaction_pipeline_db

# List indexes
\d transactions

# Shows table structure and indexes

# Exit
\q
```

---

## 🔐 Database Credentials

### Default Credentials

```bash
# Connection string format
postgresql://username:password@host:port/database

# For local development
postgresql://postgres:Rheb@117@localhost:5432/transaction_pipeline_db
```

### Store Safely in .env

**File**: `.env`

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=postgres
DB_PASSWORD=<your-password>
```

**IMPORTANT**: Never commit `.env` to Git!

### Change Password

```bash
# Connect as postgres user
psql -U postgres

# In psql:
ALTER USER postgres WITH PASSWORD 'new_password';

# Exit
\q
```

---

## 🔄 Data Operations

### Import CSV Data

**Method 1: Using Python ETL**
```bash
python src/etl_pipeline.py

# Reads from data/raw/transactions.csv
# Validates and transforms
# Loads into PostgreSQL
```

**Method 2: Using psql COPY

```bash
# Connect to database
psql -U postgres -d transaction_pipeline_db

# Copy data from CSV
COPY transactions(transaction_id, date, description, amount, currency, category, account, transaction_type)
FROM '/path/to/transactions.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

# Exit
\q
```

### Export Data

**Export to CSV**
```bash
# Connect to database
psql -U postgres -d transaction_pipeline_db

# Export all transactions
\COPY (SELECT * FROM transactions) TO 'output.csv' WITH CSV HEADER;

# Exit
\q
```

**Export to JSON**
```bash
psql -U postgres -d transaction_pipeline_db -c \
  "SELECT json_agg(t) FROM transactions t" > output.json
```

---

## 🔍 Database Queries

### View All Transactions

```sql
SELECT * FROM transactions LIMIT 10;
```

### Transactions by Category

```sql
SELECT category, COUNT(*), SUM(amount)
FROM transactions
GROUP BY category
ORDER BY SUM(amount) DESC;
```

### Transactions in Date Range

```sql
SELECT * FROM transactions
WHERE date BETWEEN '2026-08-01' AND '2026-08-31'
ORDER BY date;
```

### Find Largest Transactions

```sql
SELECT * FROM transactions
ORDER BY ABS(amount) DESC
LIMIT 10;
```

### Count by Month

```sql
SELECT year, month, COUNT(*) as count
FROM transactions
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

### Audit Trail for Transaction

```sql
SELECT * FROM audit_logs
WHERE transaction_id = 1
ORDER BY changed_at DESC;
```

---

## 🛠️ Database Maintenance

### Backup Database

**Automated Backup Script**
```bash
#!/bin/bash
# File: backup_db.sh

BACKUP_DIR="/backup/transaction-pipeline"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create backup
pg_dump -U postgres transaction_pipeline_db > \
  $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

echo "Backup created: $BACKUP_DIR/db_$DATE.sql.gz"

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

**Manual Backup**
```bash
pg_dump -U postgres transaction_pipeline_db > backup.sql
```

### Restore Database

```bash
# Create new empty database
createdb -U postgres transaction_pipeline_db_restored

# Restore from backup
psql -U postgres transaction_pipeline_db_restored < backup.sql
```

### Vacuum (Cleanup)

Removes dead tuples and optimizes storage:

```bash
# Connect to database
psql -U postgres -d transaction_pipeline_db

# Full vacuum (locks table)
VACUUM FULL;

# Regular vacuum (no lock)
VACUUM;

# Exit
\q
```

### Analyze (Statistics)

Updates query planner statistics:

```bash
psql -U postgres -d transaction_pipeline_db -c "ANALYZE;"
```

### Reindex (Optimize Indexes)

```bash
psql -U postgres -d transaction_pipeline_db -c "REINDEX DATABASE transaction_pipeline_db;"
```

---

## 📊 Database Statistics

### View Table Size

```bash
psql -U postgres -d transaction_pipeline_db

# In psql:
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname='public';

# Exit
\q
```

### View Database Size

```bash
psql -U postgres -d transaction_pipeline_db -c \
  "SELECT pg_size_pretty(pg_database_size('transaction_pipeline_db'));"
```

### Query Performance

```bash
# Enable timing
psql -U postgres -d transaction_pipeline_db

# In psql, enable timing:
\timing on

# Run query (shows execution time)
SELECT COUNT(*) FROM transactions;

# Exit
\q
```

---

## 🔐 User Management

### Create New User

```bash
psql -U postgres

# In psql:
CREATE USER data_analyst WITH PASSWORD 'secure_password';

# Grant permissions
GRANT SELECT ON transactions TO data_analyst;
GRANT SELECT ON audit_logs TO data_analyst;

# Exit
\q
```

### Grant Permissions

```bash
psql -U postgres -d transaction_pipeline_db

# In psql:
# Give all permissions to user
GRANT ALL PRIVILEGES ON transactions TO username;

# Exit
\q
```

### Create Read-Only User

```bash
psql -U postgres

# In psql:
CREATE USER data_reader WITH PASSWORD 'read_only_password';
GRANT CONNECT ON DATABASE transaction_pipeline_db TO data_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_reader;

# Exit
\q
```

---

## 🐛 Database Troubleshooting

### Issue: "Cannot connect to database"

**Diagnosis**
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# If not running:
# Windows: Start PostgreSQL service in Services
# macOS: brew services start postgresql@16
# Linux: sudo systemctl start postgresql
```

### Issue: "Role does not exist"

**Solution**
```bash
psql -U postgres

# In psql:
CREATE ROLE postgres WITH LOGIN;

# Exit
\q
```

### Issue: "Database does not exist"

**Solution**
```bash
createdb -U postgres transaction_pipeline_db
```

### Issue: "Disk space full"

**Solution**
```bash
# Check disk usage
df -h

# Clean old backups
rm /backup/transaction-pipeline/*.sql.gz

# Vacuum database
psql -U postgres -d transaction_pipeline_db -c "VACUUM FULL;"
```

---

## 🔧 Performance Tuning

### Connection Pool Size

**Edit**: `src/database_config.py`

```python
# For typical use
pool_size=5
max_overflow=10

# For heavy load
pool_size=20
max_overflow=40
```

### Query Optimization

**Use EXPLAIN to analyze queries**
```bash
psql -U postgres -d transaction_pipeline_db

# In psql:
EXPLAIN SELECT * FROM transactions WHERE category = 'Food';

# Shows query plan without executing

# Exit
\q
```

### Add Composite Indexes

```bash
psql -U postgres -d transaction_pipeline_db

# In psql:
CREATE INDEX idx_category_date ON transactions(category, date);
CREATE INDEX idx_date_amount ON transactions(date, amount);

# Exit
\q
```

---

## 📚 GUI Tools

### pgAdmin (Web-based)

```bash
# Install pgAdmin
docker run -p 5050:80 dpage/pgadmin4

# Access at: http://localhost:5050
# Login with default email/password
```

### DBeaver (Desktop)

```bash
# Download: https://dbeaver.io/download/
# Install and run
# File → New Database Connection
# Choose PostgreSQL
# Enter connection details
```

### DataGrip (IDE)

```
JetBrains IDE for databases
Download: https://www.jetbrains.com/datagrip/
```

---

## 📖 Common SQL Queries

### Dashboard Data

```sql
-- Total transactions by category
SELECT category, COUNT(*) as count, SUM(amount) as total
FROM transactions
GROUP BY category;

-- Monthly summary
SELECT year, month, SUM(amount) as total, COUNT(*) as count
FROM transactions
GROUP BY year, month
ORDER BY year DESC, month DESC;

-- Top 10 transactions
SELECT * FROM transactions
ORDER BY ABS(amount) DESC
LIMIT 10;

-- Recent transactions
SELECT * FROM transactions
ORDER BY date DESC
LIMIT 20;
```

---

## 🔄 Continuous Monitoring

### Health Check Query

```bash
psql -U postgres -d transaction_pipeline_db -c \
  "SELECT 
    (SELECT COUNT(*) FROM transactions) as transaction_count,
    (SELECT COUNT(*) FROM audit_logs) as audit_count,
    MAX(date) as latest_date
   FROM transactions;"
```

### Scheduled Maintenance

```bash
# Add to crontab for daily maintenance at 2 AM
0 2 * * * psql -U postgres -d transaction_pipeline_db -c "VACUUM ANALYZE;"
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[2_INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md)** — Installation
- **[3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)** — Architecture
- **[13_CONFIGURATION_GUIDE.md](13_CONFIGURATION_GUIDE.md)** — Configuration

---

**Database is production-ready and fully documented!** 🗄️✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
