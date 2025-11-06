import os
import pickle
from datetime import datetime

import pandas as pd
import requests
from airflow.providers.standard.operators.python import PythonOperator
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import mlflow
from airflow import DAG


def extract_data(taxi_type, year, month, **kwargs):
    parsed_month = month.zfill(2)
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{parsed_month}.parquet"
    data_path = f"/tmp/{taxi_type}_tripdata_{year}-{parsed_month}.parquet"
    if os.path.exists(data_path):
        print(f"File {data_path} already exists. Skipping download.")
        return data_path
    response = requests.get(url)
    response.raise_for_status()
    with open(data_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} to {data_path}")
    return data_path


def count_rows(data_path, **kwargs):
    df = pd.read_parquet(data_path)
    row_count = len(df)
    print("Question 3: Let's read the March 2023 Yellow taxi trips data.")
    print("How many rows are there in the dataset?")
    print(f"The file {data_path} has {row_count} rows.")


def transform_and_load_data(filename, **kwargs):
    df = pd.read_parquet(filename)

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    print("Question 4: Let's apply to the data we loaded in question 3.")
    print("What's the size of the result? ")
    print(f"Filtered data has {len(df)} rows after removing outliers.")
    filtered_path = filename.replace(".parquet", "_filtered.parquet")
    df.to_parquet(filtered_path, index=False)
    print(f"Filtered data saved to {filtered_path}")

    return filtered_path


def train_and_load_model(data_path, **kwargs):
    df = pd.read_parquet(data_path)

    # [START] One-hot encoding
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    train_dicts = df[categorical].to_dict(orient="records")
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    y_train = df.duration.values
    # [END] One-hot encoding

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    print("Intercept:", lr.intercept_)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred)
    print(f"Training completed. MSE: {mse}")

    experiment_name = "nyc-taxi-duration-prediction-v1"

    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    print("MLflow Tracking URI:", mlflow.get_tracking_uri())
    mlflow.set_experiment(experiment_name)
    mlflow.sklearn.autolog()

    with open("/tmp/lin_reg.bin", "wb") as f_out:
        pickle.dump((dv, lr), f_out)

    with mlflow.start_run():
        mlflow.set_tag("developer", "crincon")
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(lr, name="model_linear_regression")
        mlflow.sklearn.log_model(dv, name="dict_vectorizer")
        mlflow.log_artifact("/tmp/lin_reg.bin")


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 3, 1),
}

with DAG(
    dag_id="mlops_pipeline_v1",
    default_args=default_args,
    catchup=False,
    params={
        "taxi_type": "yellow",
        "year": 2023,
        "month": 3,
    },
) as dag:
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
        op_kwargs={
            "taxi_type": "{{ params.taxi_type }}",
            "year": "{{ params.year }}",
            "month": "{{ params.month }}",
        },
    )

    count_task = PythonOperator(
        task_id="count_rows",
        python_callable=count_rows,
        op_kwargs={
            "data_path": '{{ ti.xcom_pull(task_ids="extract_data") }}',
        },
    )

    transform_and_load_data_task = PythonOperator(
        task_id="transform_and_load_data",
        python_callable=transform_and_load_data,
        op_kwargs={
            "filename": '{{ ti.xcom_pull(task_ids="extract_data") }}',
        },
    )

    train_and_load_model_task = PythonOperator(
        task_id="train_and_load_model",
        python_callable=train_and_load_model,
        op_kwargs={
            "data_path": '{{ ti.xcom_pull(task_ids="transform_and_load_data") }}',
        },
    )

    extract_task >> [count_task, transform_and_load_data_task]
    transform_and_load_data_task >> train_and_load_model_task
