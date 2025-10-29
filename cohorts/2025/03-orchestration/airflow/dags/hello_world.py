# Generate a simple dag to test the airflow setup, use the PythonOperator
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def print_hello(**kwargs):
    print("Hello World from Airflow!")
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 1),
}

with DAG(
    dag_id='test_hello_world',
    default_args=default_args,
    catchup=False,
) as dag:

    hello_task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    hello_task