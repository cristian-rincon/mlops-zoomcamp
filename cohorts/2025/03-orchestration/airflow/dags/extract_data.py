from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import requests

def download_parquet(taxi_type, year, month, **kwargs):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    local_path = f"/tmp/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    response = requests.get(url)
    # response.raise_for_status()
    with open(local_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} to {local_path}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 1),
}

with DAG(
    dag_id='download_taxi_tripdata',
    default_args=default_args,
    catchup=False,
    params={
        'taxi_type': 'green',
        'year': 2025,
        'month': 1,
    },
) as dag:

    download_task = PythonOperator(
        task_id='download_parquet',
        python_callable=download_parquet,
        op_kwargs={
            'taxi_type': '{{ params.taxi_type }}',
            'year': '{{ params.year }}',
            'month': '{{ params.month }}',
        },
    )

    download_task