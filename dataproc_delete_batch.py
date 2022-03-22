
"""Example Airflow DAG that kicks off a batches job which will run a linear regression Spark ML job
This DAG relies on an Airflow variable
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* project_id - Google Cloud Project ID to use for the Cloud Dataproc Template.
* bucket_path - Google Cloud Storage bucket where you've stored the natality_spark_ml file

"""

import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteBatchOperator
from airflow.utils.dates import days_ago

project_id = '{{ var.value.project_id }}'

default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "project_id": project_id,
}

with models.DAG(
    "dataproc_create_batch_operator",  # The id you will see in the DAG airflow page
    default_args=default_args,  # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
) as dag:
    delete_batch = DataprocDeleteBatchOperator(
        task_id="my-batch",
        project_id=project_id,
        region="us-central1",
        batch_id="my-batch",
    )
