## Google Cloud Platform Python Samples - Apache Airflow Third party libraries

This folder holds modified third party modules from [Apache Airflow]
(https://airflow.apache.org/), including operators and hooks to be deployed as 
plugins.

## Instructions

1. Copy the required operator or hook module inside 
`plugins/$defined_plugin/operators` or `plugins/$defined_plugin/hooks` 
respectively within your Airflow/Composer environment

2. If requires another module as dependency, download it from the Airflow 
Github repository, e.g., GCS hook:
    ```
    cd plugins/gcs_plugin/hooks
    wget https://raw.githubusercontent.com/apache/incubator-airflow/v1-10-stable/airflow/contrib/hooks/gcs_hook.py
    ```

## Licensing

* See [LICENSE](LICENSE)
