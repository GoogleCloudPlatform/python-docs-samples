# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START composer_dataflow_dag]

from airflow import models
from airflow.utils.dates import days_ago
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
import datetime

# [END composer_dataflow_dag]

bucket_path = "gs://" + models.Variable.get("bucket_name")
project_id = models.Variable.get("project_id")
gce_zone = models.Variable.get("gce-zone")

# [START composer_dataflow_dag]


# TODO: Replace all instances of project_id with your project id.
# TODO: Replace bucket_name with your bucket name.

default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "dataflow_default_options": {
        "project": project_id,
        # Set to your region
        "region": gce_zone,
        # Set to your zone
        "zone": gce_zone,
        # This is a subfolder for storing temporary files, like the staged pipeline job.
        "temp_location": bucket_path + "/tmp/",
    },
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
    # The id you will see in the DAG airflow page
    "composer_dataflow_dag",
    default_args=default_args,
    # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
) as dag:

    start_template_job = DataflowTemplateOperator(
        # The task id of your job
        task_id="dataflow_operator_transform_CSV_to_BQ",
        # The name of the template that you're using.
        # Below is a list of all the templates you can use.
        # For versions in non-production environments, use the subfolder 'latest'
        # https://cloud.google.com/dataflow/docs/guides/templates/provided-streaming#gcstexttobigquerystream
        template="gs://dataflow-templates/latest/Stream_GCS_Text_to_BigQuery",
        # Use the link above to specify the correct parameters for your template.
        parameters={
            "javascriptTextTransformFunctionName": "transformCSVtoJSON",
            "JSONPath": bucket_path + "/jsonSchema.json",
            "javascriptTextTransformGcsPath": bucket_path + "/inputFile.txt",
            "inputFilePattern": bucket_path + "/inputFile.txt",
            "outputTable": project_id + ":average_weather.average_weather",
            "outputDeadletterTable": project_id + ":average_weather.average_weather",
            "bigQueryLoadingTemporaryDirectory": bucket_path + "/tmp/",
        },
    )

# [END composer_dataflow_dag]
