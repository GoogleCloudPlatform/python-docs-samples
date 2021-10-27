# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from airflow import DAG
from airflow import models
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago

##Project Variables

PROJECT = 'your_project_id'
DATASETID = 'rp_demo_cmek'

##Example args for the Dag to execute weekly 

with models.DAG(
    "rp_bqml_xgboost_fraud_dag",
    schedule_interval='@weekly',
    start_date=days_ago(1)
) as dag:

    ##Task 1 - will create a test sample data set from the ulb fraud dataset using the FARM FINGER print method

    t1 = BigQueryInsertJobOperator(
        task_id='create_test_sample_table',
        configuration={
            'query':{
                "query":"{% include '/include/ulb_fraud_20_pcnt_sample.sql' %}",
                'destinationTable': {
                    'projectId': PROJECT,
                    'datasetId': DATASETID,
                    'tableId': 'ulb_fraud_test_sample_table'
                },
                'useLegacySql': False,
                'allowLargeResults': True,
                'writeDisposition':'WRITE_TRUNCATE',
            }
        }
    )

    ##Task 2 - will create a training sample data set by getting the remainder of rows from the ulb fraud data set

    t2 = BigQueryInsertJobOperator(
        task_id='create_training_sample_table',
        configuration={
            'query':{
                "query":"{% include '/include/ulb_fraud_80_pcnt_sample_training.sql' %}",
                'destinationTable': {
                    'projectId': PROJECT,
                    'datasetId': DATASETID,
                    'tableId': 'ulb_fraud_training_sample_table'
                },
                'useLegacySql': False,
                'allowLargeResults': True,
                'writeDisposition':'WRITE_TRUNCATE',
            }
        }
    )

    ##Task 3 - will create the XGBoost Boosted Tree Classifier BQML model 

    t3 = BigQueryInsertJobOperator(
        task_id='create_xgboost_fraud_classifier_model',
        configuration={
            "query": {
                "query": "{% include '/include/create_xgboost_fraud_model.sql' %}",
                "useLegacySql": False,
            }
        },
        location='US',
    )

    ##Task 4 - will run the XGBoost Boosted Tree Classifier BQML model and output the results to a table    

    t4 = BigQueryInsertJobOperator(
        task_id='run_xgboost_fraud_classifier_model',
        configuration={
            'query':{
                "query":"{% include '/include/run_xgboost_fraud_model.sql' %}",
                'destinationTable': {
                    'projectId': PROJECT,
                    'datasetId': DATASETID,
                    'tableId': 'ulb_fraud_classifications_table'
                },
                'useLegacySql': False,
                'allowLargeResults': True,
                'writeDisposition':'WRITE_TRUNCATE',
            }
        }
    )
    
    t1 >> t2 >> t3 >> t4
