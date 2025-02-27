from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from src.data_collection.scraping_data import scraper
from preprocessing_data import preprocessing 

# initializing the default arguments
default_args = {
    'owner': 'Ayoub_oulkadi',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 8),
    'email': ['ayouboulkadi5@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Instantiate a DAG object
real_estate_dag = DAG('real_estate_dag',
		default_args=default_args,
		description='real_estate',
		schedule_interval='@daily',
		catchup=False,
		tags=['example, helloworld']
)
# Creating first task
start_task = DummyOperator(task_id='start_task', dag=real_estate_dag)

# Creating second task
hello_world_task = PythonOperator(task_id='hello_world_task', python_callable=scraper, dag=real_estate_dag)

# Creating third task
end_task = PythonOperator(task_id='end_task',python_callable=preprocessing, dag=real_estate_dag)


# Set the order of execution of tasks.
start_task >> hello_world_task >> end_task