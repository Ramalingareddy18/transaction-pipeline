# 🏥 Health Monitoring & Observability

## System Health Checks & Monitoring

**Read Time**: 15 minutes  
**Audience**: DevOps, SREs, System Administrators  
**Tools**: Health Checks, Logs, Metrics

---

## 📊 Health Check Overview

Health checks verify that all system components are functioning correctly.

### 4-Level Health Check Architecture

```
Level 1: Container Health (Docker)
├─ HEALTHCHECK in Dockerfile
└─ Probes container every 30s

Level 2: API Health (FastAPI)
├─ /health - Basic status
├─ /health/detailed - Comprehensive
└─ /health/database - DB specific
└─ /health/data-quality - Data stats

Level 3: Database Health
├─ Connection pool
├─ Query performance
└─ Storage capacity

Level 4: Application Health
├─ Service availability
├─ Error rates
└─ Performance metrics
```

---

## 🚀 Accessing Health Endpoints

### Endpoint 1: Basic Health

**Purpose**: Load balancer compatibility

```bash
curl http://127.0.0.1:8000/health

# Response:
# {"status": "ok"}
```

**Use**: Health checks for reverse proxy, load balancer

---

### Endpoint 2: Detailed Health

**Purpose**: Comprehensive system status

```bash
curl http://127.0.0.1:8000/health/detailed

# Response:
{
  "status": "healthy",
  "checks": {
    "database": "connected",
    "api": "responsive",
    "data_quality": "good"
  },
  "timestamp": "2026-08-01T12:00:00Z",
  "uptime_seconds": 3600,
  "version": "1.0.0"
}
```

**Status Values**: `healthy`, `degraded`, `unhealthy`

---

### Endpoint 3: Database Health

**Purpose**: Database-specific diagnostics

```bash
curl http://127.0.0.1:8000/health/database

# Response:
{
  "status": "connected",
  "database": "transaction_pipeline_db",
  "host": "localhost",
  "port": 5432,
  "transaction_count": 5000,
  "last_transaction_date": "2026-08-01",
  "table_sizes": {
    "transactions": "2.5 MB",
    "audit_logs": "500 KB"
  },
  "indexes": 4,
  "timestamp": "2026-08-01T12:00:00Z"
}
```

**Monitor**:
- `transaction_count`: Increasing?
- `last_transaction_date`: Recent?
- `table_sizes`: Growing too fast?

---

### Endpoint 4: Data Quality

**Purpose**: Validate data integrity

```bash
curl http://127.0.0.1:8000/health/data-quality

# Response:
{
  "status": "good",
  "total_records": 5000,
  "valid_records": 4900,
  "invalid_records": 100,
  "validation_rate": 98.0,
  "anomaly_percentage": 2.5,
  "missing_values": {
    "description": 5,
    "category": 2,
    "amount": 0
  },
  "timestamp": "2026-08-01T12:00:00Z"
}
```

**Thresholds**:
- `validation_rate` > 95% = Good
- `validation_rate` < 80% = Alert

---

## 🔍 Docker Health Checks

### Health Check in Dockerfile

```dockerfile
# Check API every 30 seconds
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Interpretation

```
✓ healthy (green)
  - Health check passed
  - Container is working

⚠ starting (yellow)
  - First 40 seconds
  - Still starting up

✗ unhealthy (red)
  - Health check failed
  - Container may restart
```

### Check Container Health

```bash
# View health status
docker-compose ps

# Example output:
# NAME              STATUS
# transaction-db    Up (healthy)
# transaction-api   Up (unhealthy)  ← Problem!

# View details
docker-compose logs transaction-api
```

---

## 📊 Monitoring Strategies

### Strategy 1: Passive Monitoring

Just check health endpoints:

```bash
#!/bin/bash
# health_check.sh

while true; do
    STATUS=$(curl -s http://127.0.0.1:8000/health)
    if [[ $STATUS == *"ok"* ]]; then
        echo "✓ API is healthy"
    else
        echo "✗ API is down"
        # Send alert
    fi
    sleep 60
done
```

### Strategy 2: Active Monitoring

```python
import requests
import smtplib
from datetime import datetime

def check_system_health():
    """Comprehensive health check"""
    
    checks = {
        'api': check_api_health(),
        'database': check_database_health(),
        'data': check_data_quality(),
        'disk': check_disk_space()
    }
    
    # Report
    report = f"""
    System Health Report - {datetime.now()}
    
    API:       {checks['api']['status']}
    Database:  {checks['database']['status']}
    Data:      {checks['data']['status']}
    Disk:      {checks['disk']['status']}
    """
    
    if any(v['status'] != 'ok' for v in checks.values()):
        send_alert_email(report)
    
    return checks

def check_api_health():
    try:
        response = requests.get('http://127.0.0.1:8000/health')
        return {'status': 'ok'} if response.status_code == 200 else {'status': 'error'}
    except:
        return {'status': 'unreachable'}

def check_database_health():
    try:
        response = requests.get('http://127.0.0.1:8000/health/database')
        return {'status': 'ok'} if response.status_code == 200 else {'status': 'error'}
    except:
        return {'status': 'unreachable'}
```

### Strategy 3: Prometheus + Grafana

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

## 📈 Metrics to Monitor

### Key Performance Indicators (KPIs)

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Response Time** | <100ms | 100-500ms | >500ms |
| **Error Rate** | <0.1% | 0.1-1% | >1% |
| **CPU Usage** | <50% | 50-70% | >70% |
| **Memory Usage** | <60% | 60-80% | >80% |
| **Disk Usage** | <70% | 70-85% | >85% |
| **DB Connections** | <5 | 5-10 | >10 |
| **Transactions/sec** | Steady | ±10% | ±20% |
| **Anomaly Rate** | <3% | 3-5% | >5% |

---

## 🔔 Alerting

### Alert Conditions

```python
# Example: Alert if API response time > 500ms

def check_api_performance():
    start = time.time()
    response = requests.get('http://127.0.0.1:8000/health')
    duration = (time.time() - start) * 1000  # ms
    
    if duration > 500:
        send_alert(f"API response time: {duration}ms")
    
    return duration

# Alert if error rate > 1%

def check_error_rate():
    response = requests.get('http://127.0.0.1:8000/health/detailed')
    data = response.json()
    
    total = data['checks']['total_requests']
    errors = data['checks']['failed_requests']
    rate = (errors / total) * 100 if total > 0 else 0
    
    if rate > 1:
        send_alert(f"Error rate: {rate}%")
```

### Alert Methods

**Email Alerts**
```python
import smtplib

def send_email_alert(message):
    # Configure SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.login('your-email@gmail.com', 'password')
    server.send_message(
        subject='Alert',
        message=message,
        from_addr='your-email@gmail.com',
        to_addrs=['admin@example.com']
    )
    server.quit()
```

**Slack Alerts**
```python
import requests

def send_slack_alert(message):
    webhook = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    payload = {
        'text': f':warning: Alert: {message}',
        'channel': '#alerts'
    }
    requests.post(webhook, json=payload)
```

**PagerDuty**
```python
import requests

def send_pagerduty_alert(message):
    url = "https://events.pagerduty.com/v2/enqueue"
    payload = {
        'routing_key': 'YOUR_ROUTING_KEY',
        'event_action': 'trigger',
        'payload': {
            'summary': message,
            'severity': 'error',
            'source': 'transaction-pipeline'
        }
    }
    requests.post(url, json=payload)
```

---

## 📋 Health Check Runbook

When something goes wrong:

### API Not Responding

```bash
# 1. Check API status
curl http://127.0.0.1:8000/health

# 2. Check logs
docker-compose logs transaction-api

# 3. Check if process is running
ps aux | grep uvicorn

# 4. Restart if needed
docker-compose restart transaction-api

# 5. Verify
curl http://127.0.0.1:8000/health
```

### Database Connection Failed

```bash
# 1. Check database health
curl http://127.0.0.1:8000/health/database

# 2. Check database running
docker-compose ps postgres

# 3. Test direct connection
psql -h localhost -U postgres -d transaction_pipeline_db

# 4. Check credentials
grep DB_ .env

# 5. Restart if needed
docker-compose restart postgres

# 6. Verify
curl http://127.0.0.1:8000/health/database
```

### High Memory Usage

```bash
# 1. Check usage
docker stats

# 2. View logs for memory leaks
docker-compose logs --tail 100

# 3. Restart service
docker-compose restart transaction-api

# 4. Check if memory decreases
docker stats

# 5. If problem persists, investigate code
```

### High Error Rate

```bash
# 1. Check error logs
curl http://127.0.0.1:8000/health/detailed

# 2. View detailed logs
docker-compose logs transaction-api | tail -50

# 3. Check data quality
curl http://127.0.0.1:8000/health/data-quality

# 4. Check recent changes
git log --oneline -10

# 5. Review error patterns
# Look for common errors
```

---

## 📊 Logging

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail 100

# Service-specific
docker-compose logs transaction-api

# With timestamps
docker-compose logs --timestamps
```

### Log Levels

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug info")           # Development
logger.info("Info message")          # General info
logger.warning("Warning message")    # Potential issue
logger.error("Error message")        # Error occurred
logger.critical("Critical error")    # System critical
```

### Log Aggregation

```bash
# Send to Elasticsearch
docker run -d --name elasticsearch \
  -p 9200:9200 \
  docker.elastic.co/elasticsearch/elasticsearch:8.0.0

# Visualize with Kibana
docker run -d --name kibana \
  -p 5601:5601 \
  docker.elastic.co/kibana/kibana:8.0.0
```

---

## 🔄 Continuous Monitoring Schedule

### Daily Checks (8 AM)
- [ ] Review overnight logs
- [ ] Check error rates
- [ ] Verify data quality

### Weekly Checks (Monday 9 AM)
- [ ] Capacity planning
- [ ] Review trends
- [ ] Update dashboards

### Monthly Checks (1st of month)
- [ ] Performance analysis
- [ ] Archival old logs
- [ ] Update alerts

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[4_API_DOCUMENTATION.md](4_API_DOCUMENTATION.md)** — API endpoints
- **[7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)** — Deployment
- **[14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)** — Troubleshooting

---

**Health monitoring ensures your system runs reliably!** 🏥✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
