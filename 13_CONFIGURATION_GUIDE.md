# ⚙️ Configuration Guide

## Environment & Application Configuration

**Read Time**: 15 minutes  
**Audience**: DevOps, Developers, Sysadmins

---

## 📋 Configuration Overview

Configuration is managed through:
1. `.env` file (environment variables)
2. Python configuration files
3. YAML/JSON config files
4. Docker environment

---

## 🔧 Environment Variables (.env)

### File Location

```
project-root/
└── .env          ← Configuration file (DO NOT commit to Git)
```

### Default .env.example

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=postgres
DB_PASSWORD=Rheb@117

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=false
API_WORKERS=4

# Dashboard Configuration
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8501

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Setup .env

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env  # Linux/macOS
# or
notepad .env  # Windows
```

---

## 🔐 Security: Passwords & Secrets

### Store Sensitive Data in .env

**NEVER HARDCODE SECRETS IN CODE!**

```python
# ❌ BAD - Never do this
DB_PASSWORD = "Rheb@117"

# ✅ GOOD - Use environment variables
from dotenv import load_dotenv
import os

load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

### .env Should Never Be Committed

**File**: `.gitignore`

```
.env                    # Environment file with secrets
.env.local             # Local overrides
.env.production        # Production secrets
*.key                  # Private keys
*.pem                  # Certificates
secrets/               # Secrets directory
```

### Strong Passwords

```bash
# Generate strong password
openssl rand -base64 32

# Copy to .env
DB_PASSWORD=<generated-password>
```

---

## 📝 Database Configuration

### PostgreSQL Connection

**File**: `src/database_config.py`

```python
import os
from sqlalchemy import create_engine

# Load environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'transaction_pipeline_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Check required password
if not DB_PASSWORD:
    raise RuntimeError('DB_PASSWORD environment variable not set')

# Build connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Connection pool size
    max_overflow=10,       # Additional connections
    pool_recycle=3600      # Recycle hourly
)
```

### Local Development

```bash
# .env for local development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=postgres
DB_PASSWORD=your-local-password
```

### Production

```bash
# .env for production
DB_HOST=prod-db.example.com
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=prod_user
DB_PASSWORD=strong-generated-password
```

---

## 🚀 API Configuration

### FastAPI Settings

**File**: `app/main.py`

```python
from fastapi import FastAPI
import os

app = FastAPI(
    title="Transaction Pipeline API",
    version="1.0.0",
    description="Transaction processing and analytics",
    debug=os.getenv('API_DEBUG', 'false').lower() == 'true'
)

# CORS configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Change in production
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

### Uvicorn Server

```bash
# Basic
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# With workers
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With reload (development)
python -m uvicorn app.main:app --reload

# With logging
python -m uvicorn app.main:app --log-level info
```

**Docker Configuration**

```yaml
services:
  api:
    environment:
      API_HOST: 0.0.0.0
      API_PORT: 8000
      API_DEBUG: "false"
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 Dashboard Configuration

### Streamlit Settings

**File**: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#F8F9FA"
secondaryBackgroundColor = "#E8EAED"
textColor = "#262730"

[client]
showErrorDetails = false

[server]
port = 8501
headless = true
maxUploadSize = 200
```

### Environment-Based Config

```python
# File: dashboard.py

import os
import streamlit as st

# Configuration based on environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000')

if ENVIRONMENT == 'production':
    st.set_page_config(page_title="Dashboard", layout="wide")
    cache_ttl = 300  # 5 minutes
else:
    cache_ttl = 60   # 1 minute (for development)
```

---

## 🐳 Docker Configuration

### Docker Environment

**File**: `docker-compose.yml`

```yaml
services:
  postgres:
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  api:
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      API_DEBUG: "false"
```

### Build Configuration

```dockerfile
# Dockerfile

# Build-time variables
ARG PYTHON_VERSION=3.11
ARG BASE_IMAGE=python:${PYTHON_VERSION}-slim

FROM ${BASE_IMAGE}

# Build arguments passed to container
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL version=${VERSION}
LABEL date=${BUILD_DATE}
```

---

## 🔐 Logging Configuration

### Python Logging

**File**: `src/logging_config.py`

```python
import logging
import os

# Get log level from environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### .env Logging Settings

```bash
# .env
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=app.log
LOG_FORMAT=json             # json or text
```

---

## 📈 Anomaly Detection Configuration

### Model Configuration

**File**: `anomaly_detection.py`

```python
import os

# Get contamination rate from environment
CONTAMINATION_RATE = float(os.getenv('ANOMALY_CONTAMINATION', '0.10'))

# Train model
model = IsolationForest(
    contamination=CONTAMINATION_RATE,
    random_state=42,
    n_estimators=100
)
```

### .env Configuration

```bash
# .env
ANOMALY_CONTAMINATION=0.10     # 10% anomaly rate
ANOMALY_SCORE_THRESHOLD=-70    # Score threshold for alerts
ANOMALY_MODEL_PATH=models/     # Where to save models
```

---

## 🔄 Environment-Specific Configurations

### Development

```bash
# .env.development
ENVIRONMENT=development
DB_HOST=localhost
DB_PORT=5432
API_DEBUG=true
LOG_LEVEL=DEBUG
ANOMALY_CONTAMINATION=0.15
```

### Testing

```bash
# .env.testing
ENVIRONMENT=testing
DB_HOST=postgres-test
DB_NAME=transaction_pipeline_test
API_DEBUG=false
LOG_LEVEL=WARNING
```

### Production

```bash
# .env.production (keep secure!)
ENVIRONMENT=production
DB_HOST=prod-db.example.com
API_DEBUG=false
LOG_LEVEL=WARNING
API_WORKERS=8
```

---

## 🛠️ Runtime Configuration

### Via Python

```python
# Override at runtime
import os

os.environ['DB_HOST'] = 'new-host'
os.environ['API_DEBUG'] = 'true'
```

### Via Command Line

```bash
# Set variables before running
export DB_HOST=my-database
python -m uvicorn app.main:app

# Or inline
DB_HOST=my-database python -m uvicorn app.main:app
```

### Via Docker

```bash
# Override in docker-compose
docker-compose -e DB_PASSWORD=newsecret up

# Or in .env.production
docker-compose --env-file .env.production up
```

---

## 🔄 Configuration Validation

### Startup Validation

```python
# src/config.py

import os
from pathlib import Path

def validate_configuration():
    """Validate all required configuration on startup"""
    
    required = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing = []
    
    for var in required:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        raise RuntimeError(f"Missing configuration: {', '.join(missing)}")
    
    # Also validate values
    db_port = int(os.getenv('DB_PORT', '5432'))
    if db_port < 1 or db_port > 65535:
        raise ValueError("Invalid DB_PORT")
    
    return True

# Call on startup
if __name__ == '__main__':
    validate_configuration()
    run_app()
```

### Pre-deployment Check

```bash
# scripts/validate_config.py

#!/usr/bin/env python3

import os
import sys

def check_config():
    checks = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PASSWORD': bool(os.getenv('DB_PASSWORD')),
        'API_PORT': int(os.getenv('API_PORT', '8000')),
    }
    
    for key, value in checks.items():
        if not value:
            print(f"❌ {key} not configured")
            return False
        print(f"✓ {key} configured")
    
    return True

if __name__ == '__main__':
    if not check_config():
        sys.exit(1)
    print("✓ All configuration validated")
```

---

## 📚 Configuration Management Tools

### Option 1: direnv

```bash
# Install
brew install direnv

# Create .envrc
echo "export $(cat .env | xargs)" > .envrc

# Allow
direnv allow

# Auto-loaded when entering directory
```

### Option 2: python-dotenv

```python
from dotenv import load_dotenv, find_dotenv
import os

# Find and load .env
load_dotenv(find_dotenv())

# Access
db_password = os.getenv('DB_PASSWORD')
```

### Option 3: pydantic

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_password: str
    api_port: int = 8000
    
    class Config:
        env_file = '.env'

settings = Settings()
```

---

## 🚀 Configuration for Scaling

### Multi-instance Configuration

```bash
# .env for load-balanced setup
DB_HOST=db-cluster.internal        # Shared database
DB_POOL_SIZE=10                    # Per-instance pool
REDIS_URL=redis://cache.internal   # Shared cache
```

### Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DB_HOST: "postgres.default.svc.cluster.local"
  LOG_LEVEL: "INFO"
  API_WORKERS: "4"
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[2_INSTALLATION_GUIDE.md](2_INSTALLATION_GUIDE.md)** — Installation
- **[7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)** — Deployment
- **[14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)** — Troubleshooting

---

**Proper configuration makes systems flexible and secure!** ⚙️✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
