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

import datetime
from airflow.utils.dates import days_ago
from airflow import models
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator

gs = "gs://"
JSONPath = "gs://"+models.Variable.get('bucket_name')+"/jsonSchema.json"
javascriptTextTransformGcsPath ="gs://"+models.Variable.get('bucket_name')+"/inputFile.txt"
inputFilePattern = "gs://"+models.Variable.get('bucket_name')+"/inputFile.txt"
outputTable = models.Variable.get('project_id')+":average_weather.average_weather"
outputDeadletterTable = models.Variable.get('project_id')+":average_weather.average_weather_error_records"
bigQueryLoadingTemporaryDirectory = "gs://"+models.Variable.get('bucket_name')+"/tmp/"

default_args = {
    #Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    'dataflow_default_options': {

        'project': models.Variable.get('project_id'),
        #Set to your region
        'region': models.Variable.get('gce_zone'),
        #Set to your zone
        'zone': models.Variable.get('gce_zone'),
        #This is a subfolder for storing temporary files, like the staged pipeline job.
        'tempLocation': "gs://"+models.Variable.get('bucket_name')+"/tmp/"
        }
    }

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
    #The id you will see in the DAG airflow page
    "composer_dataflow_dag",
    default_args=default_args,

    #The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1)  # Override to match your needs
) as dag:


    start_template_job = DataflowTemplateOperator(
        #The task id of your job
        task_id="composer_dataflow_dag",
        #The name of the template that you're using. Below is a list of all the templates you can use.
        #For versions in non-production environments, use the subfolder 'latest'
        #https://cloud.google.com/dataflow/docs/guides/templates/provided-streaming#cloudpubsubtobigquery
        template='gs://dataflow-templates/latest/Stream_GCS_Text_to_BigQuery',

        #Use the link above to specify the correct parameters for your template.
        parameters={
            #TODO: Replace projectId with your project id.
            #TODO: Replace bucketName with your bucket name.
            'javascriptTextTransformFunctionName': "transformCSVtoJSON",
            'JSONPath': 'JSONPath',
            'javascriptTextTransformGcsPath': javascriptTextTransformGcsPath,
            'inputFilePattern': inputFilePattern,
            'outputTable': outputTable,
            'outputDeadletterTable': outputDeadletterTable,
            'bigQueryLoadingTemporaryDirectory': bigQueryLoadingTemporaryDirectory,
        },
    )
