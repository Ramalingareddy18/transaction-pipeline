# 🚀 Production Deployment Guide

## Deploy to Production

**Read Time**: 20 minutes  
**Audience**: DevOps, System Administrators, Deployment Engineers  
**Platforms**: Linux, Windows, macOS

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

- [ ] Code is tested locally
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.env` file configured with production values
- [ ] Database backups configured
- [ ] SSL/TLS certificates prepared
- [ ] Firewall rules configured
- [ ] Monitoring and alerting set up
- [ ] Rollback plan documented

---

## 🏗️ Part 1: Choose Deployment Method

### Option A: Docker Compose (Recommended for Most)

**Pros**
- Single command deployment
- All services in containers
- Easy rollback and scaling
- Works on any system with Docker

**Cons**
- Single server limitation
- No auto-scaling
- Manual failover

**Best For**: Small to medium deployments

### Option B: Kubernetes (Enterprise)

**Pros**
- Auto-scaling
- Self-healing
- Multi-server distribution
- Production-grade

**Cons**
- Complexity
- Learning curve
- Requires infrastructure

**Best For**: Large deployments, high availability

### Option C: Cloud Platform

**Options**
- AWS (ECS, Elastic Beanstalk, RDS)
- Google Cloud (Cloud Run, Cloud SQL)
- Azure (Container Instances, Database)
- Heroku (Simple deployment)

---

## 🐳 Part 2: Docker Compose Deployment

### Step 1: Prepare Server

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Prepare Application

```bash
# Clone or copy project to server
cd /opt/transaction-pipeline
git clone https://github.com/yourorg/transaction-pipeline.git .

# Or copy directly
scp -r ./* user@server:/opt/transaction-pipeline/
```

### Step 3: Configure Environment

```bash
# Navigate to project
cd /opt/transaction-pipeline

# Copy and edit .env
cp .env.example .env
nano .env

# Update these values for PRODUCTION:
DB_HOST=postgres-db          # Use service name in Docker
DB_PORT=5432
DB_NAME=transaction_pipeline_db
DB_USER=postgres
DB_PASSWORD=<strong-password>  # USE STRONG PASSWORD!
ENVIRONMENT=production
DEBUG=false
```

**Security: Strong Password**
```bash
# Generate strong password
openssl rand -base64 32

# Copy output to DB_PASSWORD in .env
```

### Step 4: Use Production Compose File

```bash
# Production deployment uses special compose file
docker-compose -f docker-compose.prod.yml config

# Check for errors (should output full config without errors)
```

### Step 5: Start Services

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# Wait 30-60 seconds for startup

# Check status
docker-compose -f docker-compose.prod.yml ps

# Expected output:
# NAME                STATUS
# transaction-db      Up (healthy)
# transaction-api     Up (healthy)
# transaction-dash    Up (healthy)
```

### Step 6: Verify Deployment

```bash
# Check API health
curl http://localhost:8000/health

# Expected: {"status": "ok"}

# Check detailed health
curl http://localhost:8000/health/detailed

# Expected: Detailed status object

# Check database
curl http://localhost:8000/health/database

# Expected: Database connection details
```

### Step 7: Access Services

```
API:       http://your-server-ip:8000
Swagger:   http://your-server-ip:8000/docs
Dashboard: http://your-server-ip:8501
```

---

## 🔒 Part 3: Security Configuration

### Enable HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificate saved to:
# /etc/letsencrypt/live/your-domain.com/
```

### Configure Reverse Proxy (Nginx)

**File**: `/etc/nginx/sites-available/transaction-pipeline`

```nginx
upstream api {
    server 127.0.0.1:8000;
}

upstream dashboard {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # API endpoint
    location /api/ {
        proxy_pass http://api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Dashboard
    location / {
        proxy_pass http://dashboard/;
        proxy_set_header Host $host;
    }
}
```

**Enable Nginx**
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/transaction-pipeline \
          /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 📊 Part 4: Database Configuration

### Database Backup Strategy

```bash
# Create backup directory
mkdir -p /backup/transaction-pipeline

# Automated daily backup
# File: /usr/local/bin/backup-db.sh
#!/bin/bash
BACKUP_DIR="/backup/transaction-pipeline"
DATE=$(date +%Y%m%d_%H%M%S)

docker-compose -f /opt/transaction-pipeline/docker-compose.prod.yml exec \
  -T postgres pg_dump -U postgres transaction_pipeline_db \
  > $BACKUP_DIR/db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/db_$DATE.sql

# Keep last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Add to cron
sudo crontab -e
# Add line: 0 2 * * * /usr/local/bin/backup-db.sh
```

### Database Monitoring

```bash
# Check database health
curl http://localhost:8000/health/database

# Connect to database
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U postgres -d transaction_pipeline_db

# Check table sizes
\dt+

# Exit
\q
```

---

## 🔍 Part 5: Monitoring & Logging

### View Logs

```bash
# API logs
docker-compose -f docker-compose.prod.yml logs -f transaction-api

# Database logs
docker-compose -f docker-compose.prod.yml logs -f postgres

# Dashboard logs
docker-compose -f docker-compose.prod.yml logs -f transaction-dash

# All logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Set Up Monitoring

**Option 1: Health Check Polling**
```bash
#!/bin/bash
# File: /usr/local/bin/check-health.sh

while true; do
    STATUS=$(curl -s http://localhost:8000/health | grep -c "ok")
    if [ $STATUS -eq 0 ]; then
        # Send alert (email, Slack, PagerDuty, etc.)
        echo "Alert: API is down" | mail -s "Alert" admin@example.com
    fi
    sleep 60
done
```

**Option 2: Prometheus + Grafana**
```bash
# Install Prometheus
docker run -d --name prometheus \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Install Grafana
docker run -d --name grafana \
  -p 3000:3000 \
  grafana/grafana
```

---

## 🚨 Part 6: Alerting Setup

### Email Alerts

```bash
# Install mail utility
sudo apt-get install mailutils

# Test email
echo "Test alert" | mail -s "Alert Test" admin@example.com
```

### Slack Notifications

```python
# File: alerts.py
import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    payload = {
        "text": message,
        "channel": "#alerts",
        "username": "Transaction Pipeline"
    }
    requests.post(webhook_url, json=payload)

# Usage
send_slack_alert("⚠️ Alert: API health check failed")
```

---

## 📈 Part 7: Scaling & Performance

### Horizontal Scaling (Multiple Servers)

```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┼────┐
    │    │    │
   API1 API2 API3  (Multiple API instances)
    │    │    │
    └────┼────┘
         │
    ┌────▼────┐
    │ Database │  (Shared database)
    └──────────┘
```

### Database Connection Pooling

```python
# File: src/database_config.py (updated)

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Connection pooling
engine = create_engine(
    db_url,
    poolclass=QueuePool,
    pool_size=20,           # Connections per instance
    max_overflow=40,        # Additional connections
    pool_recycle=3600,      # Recycle connections hourly
    pool_pre_ping=True      # Verify connection before using
)
```

---

## 🔄 Part 8: Update & Rollback

### Update Application

```bash
# 1. Pull latest code
cd /opt/transaction-pipeline
git pull origin main

# 2. Update dependencies
pip install -r requirements.txt

# 3. Rebuild containers
docker-compose -f docker-compose.prod.yml build

# 4. Stop old services
docker-compose -f docker-compose.prod.yml down

# 5. Start new services
docker-compose -f docker-compose.prod.yml up -d

# 6. Verify
curl http://localhost:8000/health
```

### Rollback to Previous Version

```bash
# 1. Keep backup of previous version
cp -r /opt/transaction-pipeline /opt/transaction-pipeline.backup

# 2. If something goes wrong, restore
rm -rf /opt/transaction-pipeline
mv /opt/transaction-pipeline.backup /opt/transaction-pipeline

# 3. Restart with old version
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## ✅ Post-Deployment Checklist

After deployment:

- [ ] All services started successfully
- [ ] API responding to requests
- [ ] Dashboard accessible
- [ ] Database contains data
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] SSL certificate installed
- [ ] Firewall rules applied
- [ ] Load testing completed

---

## 📊 Performance Targets

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| API Response | <200ms | Scale API instances |
| Database Query | <100ms | Add indexes |
| Dashboard Load | <2s | Cache dashboard |
| Error Rate | <0.1% | Review logs |
| CPU Usage | <70% | Scale services |
| Memory Usage | <80% | Increase resources |

---

## 🆘 Troubleshooting Deployment

### Issue: Services won't start

**Diagnosis**
```bash
docker-compose -f docker-compose.prod.yml logs

# Look for error messages
```

**Solution**
```bash
# 1. Check .env file
cat .env | grep DB_

# 2. Check database password
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres

# 3. Check port availability
netstat -tlnp | grep 5432
netstat -tlnp | grep 8000
```

### Issue: API can't connect to database

**Solution**
```bash
# 1. Verify database is running
docker-compose -f docker-compose.prod.yml ps

# 2. Check network connectivity
docker-compose -f docker-compose.prod.yml exec transaction-api \
  ping postgres

# 3. Check database credentials
curl http://localhost:8000/health/database
```

### Issue: Dashboard shows "Unable to reach API"

**Solution**
```bash
# 1. Check API is running
curl http://localhost:8000/health

# 2. Check dashboard can reach API
docker-compose -f docker-compose.prod.yml logs transaction-dash

# 3. Verify network connectivity
docker-compose -f docker-compose.prod.yml exec transaction-dash \
  curl http://transaction-api:8000/health
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[8_DOCKER_GUIDE.md](8_DOCKER_GUIDE.md)** — Docker details
- **[12_MONITORING_HEALTH.md](12_MONITORING_HEALTH.md)** — Monitoring setup
- **[14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)** — Common issues

---

**Deployment is production-ready and well-documented!** 🚀

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
