## Homework

The goal of this homework is to familiarize users with monitoring for ML batch services, using PostgreSQL database to store metrics and Grafana to visualize them.



## Q1. Prepare the dataset

Start with `baseline_model_nyc_taxi_data.ipynb`. Download the March 2024 Green Taxi data. We will use this data to simulate a production usage of a taxi trip duration prediction service.

What is the shape of the downloaded data? How many rows are there?

* 72044
* 78537 
* [x] 57457
* 54396


## Q2. Metric

Let's expand the number of data quality metrics we’d like to monitor! Please add one metric of your choice and a quantile value for the `"fare_amount"` column (`quantile=0.5`).

Hint: explore evidently metric `ColumnQuantileMetric` (from `evidently.metrics import ColumnQuantileMetric`) 

What metric did you choose? **R: MedianValue**

```
    MedianValue(column='fare_amount')
```


## Q3. Monitoring

Let’s start monitoring. Run expanded monitoring for a new batch of data (March 2024). 

What is the maximum value of metric `quantile = 0.5` on the `"fare_amount"` column during March 2024 (calculated daily)?

* 10
* [x] 13.5
* 14.2
* 14.8

```json
{'metrics': [{'id': 'bfc6e8246d39abff41fc2e002575d9a3',
   'metric_name': 'ValueDrift(column=prediction,method=Wasserstein distance (normed),threshold=0.1)',
   'config': {'type': 'evidently:metric_v2:ValueDrift',
    'column': 'prediction',
    'method': 'Wasserstein distance (normed)',
    'threshold': 0.1},
   'value': np.float64(0.010064593780096793)},
  {'id': '15e89f895b482f9b84ba7274ed18a106',
   'metric_name': 'DriftedColumnsCount(drift_share=0.5)',
   'config': {'type': 'evidently:metric_v2:DriftedColumnsCount',
    'drift_share': 0.5},
   'value': {'count': 0.0, 'share': 0.0}},
  {'id': 'd57fce37e7dac2a48797649e0e142902',
   'metric_name': 'MissingValueCount(column=prediction)',
   'config': {'type': 'evidently:metric_v2:MissingValueCount',
    'column': 'prediction'},
   'value': {'count': 0.0, 'share': np.float64(0.0)}},
  {'id': '641f3d487377ef8aeba674733f8705f4',
   'metric_name': 'QuantileValue(column=fare_amount,quantile=0.5)',
   'config': {'type': 'evidently:metric_v2:QuantileValue',
    'column': 'fare_amount',
    'quantile': 0.5},
   'value': np.float64(13.5)},
  {'id': '078b1875ab41e040e9930bde0eb09801',
   'metric_name': 'MedianValue(column=fare_amount)',
   'config': {'type': 'evidently:metric_v2:MedianValue',
    'column': 'fare_amount'},
   'value': np.float64(13.5)}],
 'tests': []}
 ```


## Q4. Dashboard


Finally, let’s add panels with new added metrics to the dashboard. After we customize the  dashboard let's save a dashboard config, so that we can access it later. Hint: click on “Save dashboard” to access JSON configuration of the dashboard. This configuration should be saved locally.

Where to place a dashboard config file?

* `project_folder` (05-monitoring)
* [x] `project_folder/config`  (05-monitoring/config)
* `project_folder/dashboards`  (05-monitoring/dashboards)
* `project_folder/data`  (05-monitoring/data)


## Submit the results

* Submit your answers here: https://courses.datatalks.club/mlops-zoomcamp-2025/homework/hw5
