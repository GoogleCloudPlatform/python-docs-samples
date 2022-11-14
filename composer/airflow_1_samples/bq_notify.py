# Copyright 2018 Google LLC
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

"""Example Airflow DAG that creates a BigQuery dataset, populates the dataset
by performing a queries for recent popular StackOverflow questions against the
public dataset `bigquery-public-data.stackoverflow.posts_questions`. The DAG
exports the results of the query as a CSV to Cloud Storage, and sends an email
with path to the CSV file and the title and view count of the most popular
question. Lastly, the DAG cleans up the BigQuery dataset.

This DAG relies on three Airflow variables
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* gcp_project - Google Cloud Project to use for BigQuery.
* gcs_bucket - Google Cloud Storage bucket to use for result CSV file.
  See https://cloud.google.com/storage/docs/creating-buckets for creating a
  bucket.
* email - The email used to receive DAG updates.
"""

import datetime

# [START composer_notify_failure_airflow_1]
from airflow import models

# [END composer_notify_failure_airflow_1]
from airflow.contrib.operators import bigquery_get_data

# [START composer_bigquery_airflow_1]
from airflow.contrib.operators import bigquery_operator

# [END composer_bigquery_airflow_1]
from airflow.contrib.operators import bigquery_to_gcs

# [START composer_bash_bq_airflow_1]
from airflow.operators import bash_operator

# [END composer_bash_bq_airflow_1]
# [START composer_email_airflow_1]
from airflow.operators import email_operator

# [END composer_email_airflow_1]
from airflow.utils import trigger_rule


bq_dataset_name = "airflow_bq_notify_dataset_{{ ds_nodash }}"
bq_recent_questions_table_id = bq_dataset_name + ".recent_questions"
BQ_MOST_POPULAR_TABLE_NAME = "most_popular"
bq_most_popular_table_id = bq_dataset_name + "." + BQ_MOST_POPULAR_TABLE_NAME
output_file = "gs://{gcs_bucket}/recent_questionsS.csv".format(
    gcs_bucket="{{var.value.gcs_bucket}}"
)

# Data from the month of January 2018
# You may change the query dates to get data from a different time range. You
# may also dynamically pick a date range based on DAG schedule date. Airflow
# macros can be useful for this. For example, {{ macros.ds_add(ds, -7) }}
# corresponds to a date one week (7 days) before the DAG was run.
# https://airflow.apache.org/code.html?highlight=execution_date#airflow.macros.ds_add
max_query_date = "2018-02-01"
min_query_date = "2018-01-01"

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1), datetime.datetime.min.time()
)

# [START composer_notify_failure_airflow_1]
default_dag_args = {
    "start_date": yesterday,
    # Email whenever an Operator in the DAG fails.
    "email": "{{var.value.email}}",
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "project_id": "{{var.value.gcp_project}}",
}

with models.DAG(
    "composer_sample_bq_notify",
    schedule_interval=datetime.timedelta(weeks=4),
    default_args=default_dag_args,
) as dag:
    # [END composer_notify_failure_airflow_1]

    # [START composer_bash_bq_airflow_1]
    # Create BigQuery output dataset.
    make_bq_dataset = bash_operator.BashOperator(
        task_id="make_bq_dataset",
        # Executing 'bq' command requires Google Cloud SDK which comes
        # preinstalled in Cloud Composer.
        bash_command="bq ls {} || bq mk {}".format(bq_dataset_name, bq_dataset_name),
    )
    # [END composer_bash_bq_airflow_1]

    # [START composer_bigquery_airflow_1]
    # Query recent StackOverflow questions.
    bq_recent_questions_query = bigquery_operator.BigQueryOperator(
        task_id="bq_recent_questions_query",
        sql="""
        SELECT owner_display_name, title, view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE creation_date < CAST('{max_date}' AS TIMESTAMP)
            AND creation_date >= CAST('{min_date}' AS TIMESTAMP)
        ORDER BY view_count DESC
        LIMIT 100
        """.format(
            max_date=max_query_date, min_date=min_query_date
        ),
        use_legacy_sql=False,
        destination_dataset_table=bq_recent_questions_table_id,
    )
    # [END composer_bigquery_airflow_1]

    # Export query result to Cloud Storage.
    export_questions_to_gcs = bigquery_to_gcs.BigQueryToCloudStorageOperator(
        task_id="export_recent_questions_to_gcs",
        source_project_dataset_table=bq_recent_questions_table_id,
        destination_cloud_storage_uris=[output_file],
        export_format="CSV",
    )

    # Perform most popular question query.
    bq_most_popular_query = bigquery_operator.BigQueryOperator(
        task_id="bq_most_popular_question_query",
        sql="""
        SELECT title, view_count
        FROM `{table}`
        ORDER BY view_count DESC
        LIMIT 1
        """.format(
            table=bq_recent_questions_table_id
        ),
        use_legacy_sql=False,
        destination_dataset_table=bq_most_popular_table_id,
    )

    # Read most popular question from BigQuery to XCom output.
    # XCom is the best way to communicate between operators, but can only
    # transfer small amounts of data. For passing large amounts of data, store
    # the data in Cloud Storage and pass the path to the data if necessary.
    # https://airflow.apache.org/concepts.html#xcoms
    bq_read_most_popular = bigquery_get_data.BigQueryGetDataOperator(
        task_id="bq_read_most_popular",
        dataset_id=bq_dataset_name,
        table_id=BQ_MOST_POPULAR_TABLE_NAME,
    )

    # [START composer_email_airflow_1]
    # Send email confirmation
    email_summary = email_operator.EmailOperator(
        task_id="email_summary",
        to="{{var.value.email}}",
        subject="Sample BigQuery notify data ready",
        html_content="""
        Analyzed Stack Overflow posts data from {min_date} 12AM to {max_date}
        12AM. The most popular question was '{question_title}' with
        {view_count} views. Top 100 questions asked are now available at:
        {export_location}.
        """.format(
            min_date=min_query_date,
            max_date=max_query_date,
            question_title=(
                "{{ ti.xcom_pull(task_ids='bq_read_most_popular', "
                "key='return_value')[0][0] }}"
            ),
            view_count=(
                "{{ ti.xcom_pull(task_ids='bq_read_most_popular', "
                "key='return_value')[0][1] }}"
            ),
            export_location=output_file,
        ),
    )
    # [END composer_email_airflow_1]

    # Delete BigQuery dataset
    # Delete the bq table
    delete_bq_dataset = bash_operator.BashOperator(
        task_id="delete_bq_dataset",
        bash_command="bq rm -r -f %s" % bq_dataset_name,
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE,
    )

    # Define DAG dependencies.
    (
        make_bq_dataset
        >> bq_recent_questions_query
        >> export_questions_to_gcs
        >> delete_bq_dataset
    )
    (
        bq_recent_questions_query
        >> bq_most_popular_query
        >> bq_read_most_popular
        >> delete_bq_dataset
    )
    export_questions_to_gcs >> email_summary
    bq_read_most_popular >> email_summary
