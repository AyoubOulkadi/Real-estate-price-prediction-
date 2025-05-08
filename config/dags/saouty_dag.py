from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.data_processing.processing_data import run_processing_pipeline
from src.data_ingestion.ingestion import create_databases, ingest_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 3),
    'retries': 1,
    'email': 'ayouboulkadi5@gmail.com'

}

with DAG(
        dag_id='sarouty_data_pipeline',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False,
        description='Process Sarouty data and upload to S3',
) as dag:
    process_data_task = PythonOperator(
        task_id='process_sarouty_data',
        python_callable=run_processing_pipeline
    )

    create_dbs = PythonOperator(
        task_id='create_databases',
        python_callable=create_databases
    )

    ingest_data = PythonOperator(
        task_id='ingest_data_to_mysql',
        python_callable=ingest_data
    )

    process_data_task >> create_dbs >> ingest_data
