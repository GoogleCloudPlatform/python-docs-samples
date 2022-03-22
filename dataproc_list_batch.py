
import datetime

from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocListBatchesOperator
from airflow.utils.dates import days_ago

project_id = models.Variable.get("project_id")
default_args = {
    "start_date": days_ago(1),
    "project_id": project_id,
}

with models.DAG(
    "dataproc_list_batch_operator",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1),
) as dag:
    list_batches = DataprocListBatchesOperator(
        task_id="my-batch",
        project_id=project_id,
        region="us-central1",
    )