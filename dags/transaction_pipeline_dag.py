from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.etl_pipeline import run_pipeline

default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="transaction_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["transactions", "etl"],
) as dag:
    ingest_and_process = PythonOperator(
        task_id="run_transaction_etl",
        python_callable=run_pipeline,
    )

    ingest_and_process
