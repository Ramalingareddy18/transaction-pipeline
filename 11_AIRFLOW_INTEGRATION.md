# ✈️ Apache Airflow Integration Guide

## Workflow Orchestration & Scheduling

**Read Time**: 15 minutes  
**Audience**: DevOps, Data Engineers, Schedulers  
**Tool**: Apache Airflow 2.7+

---

## 📋 What is Airflow?

Apache Airflow is a workflow orchestration platform that lets you schedule, monitor, and manage data pipelines.

### Before Airflow

```bash
# Manual scheduling
0 2 * * * python /app/etl_pipeline.py

# No visibility into failures
# No retry logic
# No dependencies tracking
# Difficult to debug
```

### With Airflow

```
DAG (Directed Acyclic Graph):
    Task 1: Extract
        ↓
    Task 2: Validate
        ↓
    Task 3: Transform
        ↓
    Task 4: Load
        ↓
    Task 5: Notify

✓ Visual monitoring
✓ Automatic retries
✓ Dependency tracking
✓ Easy debugging
```

---

## 🚀 Quick Start

### Step 1: Install Airflow

```bash
# Install Airflow
pip install apache-airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin123 \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

### Step 2: Start Airflow

**Terminal 1: Webserver (UI)**
```bash
airflow webserver --port 8080

# Access at: http://localhost:8080
# Login with: admin / admin123
```

**Terminal 2: Scheduler**
```bash
airflow scheduler

# Starts background scheduler service
```

### Step 3: View UI

Open http://localhost:8080 to see:
- DAG list
- DAG execution history
- Task logs
- Monitoring

---

## 📊 DAG Structure

### Understanding DAGs

**DAG** = Directed Acyclic Graph

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define DAG
dag = DAG(
    'transaction_pipeline',
    default_args={
        'owner': 'data-team',
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Daily transaction processing',
    schedule_interval='0 2 * * *',  # Every day at 2 AM
    start_date=datetime(2026, 1, 1),
    catchup=False
)

# Define tasks
def extract():
    # Extract data
    print("Extracting...")

def validate():
    # Validate data
    print("Validating...")

def load():
    # Load to database
    print("Loading...")

# Create task instances
task_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)

task_validate = PythonOperator(
    task_id='validate',
    python_callable=validate,
    dag=dag
)

task_load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag
)

# Set dependencies
task_extract >> task_validate >> task_load
```

---

## 🔄 Current Implementation

### File Location
`dags/transaction_pipeline_dag.py`

### Current DAG Structure

```
transaction_pipeline DAG
├─ Run ETL Pipeline
│  └─ Load CSV
│  └─ Validate
│  └─ Transform
│  └─ Insert to DB
└─ Notify on completion
```

### View Current DAG

```bash
# List all DAGs
airflow dags list

# List tasks in DAG
airflow tasks list transaction_pipeline

# Show DAG structure
airflow dags show transaction_pipeline
```

---

## 📅 Scheduling

### Schedule Intervals

```python
# Daily at 2 AM
schedule_interval='0 2 * * *'

# Every 6 hours
schedule_interval=timedelta(hours=6)

# Every Monday at 9 AM
schedule_interval='0 9 * * 1'

# Production (every 1 hour)
schedule_interval=timedelta(hours=1)

# No automatic scheduling (manual only)
schedule_interval=None
```

### Cron Expression Format

```
minute hour day month weekday
  0     2    *    *      *
  │     │    │    │      └─ Day of week (0-6, 0=Sunday)
  │     │    │    └────── Month (1-12)
  │     │    └─────────── Day of month (1-31)
  │     └──────────────── Hour (0-23)
  └─────────────────────── Minute (0-59)
```

**Examples**
```
'0 0 * * *'      = Every midnight
'0 */6 * * *'    = Every 6 hours
'0 9 * * 1-5'    = Weekdays at 9 AM
'0 9 1 * *'      = First of month
'*/5 * * * *'    = Every 5 minutes
```

---

## 🔧 Task Operators

### Python Operator

Execute Python functions:

```python
from airflow.operators.python import PythonOperator

def my_task():
    print("Task running")
    return "Success"

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag
)
```

### Bash Operator

Execute shell commands:

```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id='run_script',
    bash_command='python /app/etl_pipeline.py',
    dag=dag
)
```

### Sensor Operator

Wait for conditions:

```python
from airflow.sensors.filesystem import FileSensor

task = FileSensor(
    task_id='wait_for_file',
    filepath='/data/raw/transactions.csv',
    poke_interval=60,  # Check every 60 seconds
    timeout=3600,      # Timeout after 1 hour
    dag=dag
)
```

---

## 🎯 Advanced Features

### Retry Logic

```python
from airflow import DAG
from datetime import timedelta

dag = DAG(
    'transaction_pipeline',
    default_args={
        'retries': 3,                      # Retry 3 times
        'retry_delay': timedelta(minutes=5) # Wait 5 min between retries
    }
)
```

### Timeout

```python
task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    execution_timeout=timedelta(hours=1),  # Kill if > 1 hour
    dag=dag
)
```

### Trigger Rules

```python
from airflow.utils.trigger_rule import TriggerRule

# Run only if previous task succeeded
trigger_rule=TriggerRule.ALL_SUCCESS

# Run if any previous task failed
trigger_rule=TriggerRule.ONE_FAILED

# Run regardless of upstream status
trigger_rule=TriggerRule.NONE_FAILED

# Run only if all upstream failed
trigger_rule=TriggerRule.ALL_FAILED
```

### Branching

```python
from airflow.operators.python import BranchPythonOperator

def decide_path(**context):
    if condition:
        return 'task_a'
    else:
        return 'task_b'

branch_task = BranchPythonOperator(
    task_id='branch',
    python_callable=decide_path,
    dag=dag
)
```

---

## 📊 Monitoring

### Web UI Monitoring

Access http://localhost:8080

**Features**
```
- DAG list
- Execution history
- Task status
- Task logs
- Execution times
- Alerts
```

### Command Line Monitoring

```bash
# List recent runs
airflow dags list-runs -d transaction_pipeline

# Show run details
airflow dags list-runs -d transaction_pipeline --limit 5

# Show task details
airflow tasks list-runs -d transaction_pipeline -t run_etl

# Show task logs
airflow tasks logs transaction_pipeline run_etl 2026-08-01
```

### Manual Trigger

```bash
# Trigger DAG manually
airflow dags trigger transaction_pipeline

# Trigger with specific date
airflow dags trigger transaction_pipeline \
  --exec-date 2026-08-01T00:00:00
```

---

## 🔒 Security

### Connection Management

```bash
# Set database connection
airflow connections add 'postgres_default' \
  --conn-type 'postgres' \
  --conn-host 'localhost' \
  --conn-port '5432' \
  --conn-login 'postgres' \
  --conn-password 'password' \
  --conn-schema 'transaction_pipeline_db'

# Use in DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

task = PostgresOperator(
    task_id='run_query',
    sql='SELECT COUNT(*) FROM transactions;',
    postgres_conn_id='postgres_default',
    dag=dag
)
```

### Variables

Store configuration securely:

```bash
# Set variable
airflow variables set environment production

# Use in DAG
from airflow.models import Variable

env = Variable.get('environment')
print(f"Running in {env}")
```

---

## 📈 Scale Airflow

### Multi-node Setup

```
Scheduler Node
├─ Manages DAG parsing
├─ Triggers tasks
└─ Monitors execution

Worker Nodes (Multiple)
├─ Execute tasks
├─ Report status
└─ Handle failures

Database (Shared)
├─ Stores DAG definitions
├─ Tracks executions
└─ Manages state
```

### Kubernetes Integration

```python
from airflow.providers.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

task = KubernetesPodOperator(
    task_id='process_data',
    image='transaction-pipeline:latest',
    namespace='default',
    dag=dag
)
```

---

## 🐛 Troubleshooting

### DAG Not Showing Up

```bash
# DAGs folder must exist
ls $AIRFLOW_HOME/dags/

# DAG file must have 'dag' object
grep "dag = DAG" dags/transaction_pipeline_dag.py

# Refresh UI
# Admin → Clear cache
```

### Task Failed

```bash
# View logs
airflow tasks logs transaction_pipeline run_etl 2026-08-01

# View detailed error
airflow tasks test transaction_pipeline run_etl 2026-08-01

# Reset task state
airflow tasks clear transaction_pipeline -t run_etl
```

### Scheduler Not Running

```bash
# Check scheduler status
ps aux | grep airflow

# Start scheduler
airflow scheduler

# Check logs
tail -f $AIRFLOW_HOME/logs/scheduler/latest/
```

---

## 📝 Best Practices

### 1. Idempotent Tasks

```python
# Good: Idempotent (safe to run multiple times)
def load_data():
    # Delete existing data
    db.delete_where(...)
    # Insert fresh data
    db.insert(...)

# Bad: Not idempotent
def load_data():
    # Append data (runs twice = duplicate data)
    db.insert(...)
```

### 2. Task Dependencies

```python
# Explicit dependencies
task_a >> task_b >> task_c

# Clear if/else dependencies
if condition:
    task_a >> task_b
else:
    task_a >> task_c
```

### 3. Logging

```python
import logging

logger = logging.getLogger(__name__)

def my_task():
    logger.info("Starting task")
    logger.warning("Warning message")
    logger.error("Error message")
```

### 4. Error Handling

```python
def my_task():
    try:
        # Do something
        result = process_data()
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise  # Re-raise to trigger retry
```

---

## 🚀 Production Checklist

- [ ] DAG runs successfully manually
- [ ] Scheduled interval is correct
- [ ] Retry logic configured
- [ ] Error notifications set up
- [ ] Logs are clear
- [ ] Database connections secure
- [ ] Monitoring enabled
- [ ] Backup/recovery plan

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[3_PROJECT_ARCHITECTURE.md](3_PROJECT_ARCHITECTURE.md)** — Architecture
- **[12_MONITORING_HEALTH.md](12_MONITORING_HEALTH.md)** — Monitoring
- **[14_TROUBLESHOOTING_GUIDE.md](14_TROUBLESHOOTING_GUIDE.md)** — Troubleshooting

---

**Airflow orchestrates your workflows reliably!** ✈️✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
