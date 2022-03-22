
"""Example Airflow DAG that kicks off a batches job which will run a linear regression Spark ML job
This DAG relies on an Airflow variable
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* project_id - Google Cloud Project ID to use for the Cloud Dataproc Template.
* bucket_path - Google Cloud Storage bucket where you've stored the natality_spark_ml file

"""

import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.utils.dates import days_ago

project_id = '{{ var.value.project_id }}'
bucket_name = models.Variable.get("bucket_path")
sparkml_file_location = bucket_name+"natality_sparkml.py"  # the location where the Spark ML python file is stored.
# Start a single node Dataproc Cluster for viewing Persistent History of Spark jobs
phs_cluster = "projects/project-ID/regions/region-name/clusters/cluster-name"
# for e.g. projects/my-project/regions/my-region/clusters/my-cluster"
spark_bigquery_jar_file = "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"

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

    create_batch = DataprocCreateBatchOperator(
        task_id="batch-via-dag",
        project_id=project_id,
        region="us-central1",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": sparkml_file_location,
                "jar_file_uris": [spark_bigquery_jar_file],
            },
            "environment_config":{
                "peripherals_config":{
                     "spark_history_server_config":{
                        "dataproc_cluster": phs_cluster,
                     },
                 },
            },
        },
        batch_id="batch-via-dag",
)
