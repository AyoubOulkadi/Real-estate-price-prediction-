from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.data_processing.processing_data import run_processing_pipeline
from src.data_ingestion.ingestion import transfer_files_S3

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
    upload_raw_data = PythonOperator(
        task_id='upload_raw_data_to_s3',
        python_callable=transfer_files_S3,
        op_kwargs={
            'bucket_name': 'sarouty-bucket',
            'folder_path': '/opt/airflow/raw_data',
            'target_folder': 'raw_data'
        }
    )

    process_data_task = PythonOperator(
        task_id='process_sarouty_data',
        python_callable=run_processing_pipeline
    )

    upload_processed_data = PythonOperator(
        task_id='upload_processed_data_to_s3',
        python_callable=transfer_files_S3,
        op_kwargs={
            'bucket_name': 'sarouty-bucket',
            'folder_path': '/opt/airflow/processed_data',
            'target_folder': 'processed_data'
        }
    )

    upload_raw_data >> process_data_task >> upload_processed_data
