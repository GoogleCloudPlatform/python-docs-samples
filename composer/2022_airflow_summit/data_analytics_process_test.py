# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test file for the data processing job in data analytics sample DAG.
Creates a test dataset and table from csv data, runs a serverless dataproc job on it,
and checks the existence of a new output table in that dataset.
"""

import os
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest


# GCP Project
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_ID = uuid.uuid4()

# Google Cloud Storage constants
BUCKET_NAME = f"data-analytics-dag-process-test-{TEST_ID}"
BUCKET_BLOB = "data_analytics_dag_process.py"
TEST_CSV_FILE = "test_data.csv"

BQ_CLIENT = bigquery.Client(project=PROJECT_ID)

BQ_DATASET = f"data-analytics-process-test-{TEST_ID}".replace("-", "_")
BQ_READ_TABLE = f"data-analyticsprocess-test-joined-{TEST_ID}".replace("-", "_")
BQ_WRITE_TABLE = f"data-analytics-process-test-normalized-{TEST_ID}".replace("-", "_")
TABLE_ID = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_READ_TABLE}"

DATAPROC_REGION = "us-central1"
PYSPARK_JAR = "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
PROCESSING_PYTHON_FILE = f"gs://{BUCKET_NAME}/{BUCKET_BLOB}"

BATCH_ID = (
    f"summit-dag-test-{TEST_ID}"  # Dataproc serverless only allows lowercase characters
)
BATCH_CONFIG = {
    "pyspark_batch": {
        "jar_file_uris": [PYSPARK_JAR],
        "main_python_file_uri": PROCESSING_PYTHON_FILE,
        "args": [
            PROJECT_ID,
            f"{BQ_DATASET}.{BQ_READ_TABLE}",
            f"{BQ_DATASET}.{BQ_WRITE_TABLE}",
        ],
    },
}


@pytest.fixture(scope="module")
def test_bucket():
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    # Upload dag processing file
    blob = bucket.blob(BUCKET_BLOB)
    blob.upload_from_filename(BUCKET_BLOB)

    # Upload test csv file
    blob2 = bucket.blob(TEST_CSV_FILE)
    blob2.upload_from_filename(TEST_CSV_FILE)

    yield

    # Delete GCS bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.delete(force=True)


# TODO(coleleah): teardown any previous resources
@pytest.fixture(autouse=True)
def bq_dataset(test_bucket):
    # Create dataset and table tfor test CSV
    BQ_CLIENT.create_dataset(BQ_DATASET)

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Date", "Date"),
            bigquery.SchemaField("Holiday", "STRING"),
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("element", "STRING"),
            bigquery.SchemaField("value", "FLOAT"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://{BUCKET_NAME}/{TEST_CSV_FILE}"

    load_job = BQ_CLIENT.load_table_from_uri(
        uri, TABLE_ID, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = BQ_CLIENT.get_table(TABLE_ID)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

    yield

    # Delete Dataset
    try:
        BQ_CLIENT.delete_dataset(BQ_DATASET, delete_contents=True)
    except NotFound as e:
        print(f"Ignoring NotFound on cleanup, details: {e}")


def test_process(test_bucket):
    # check that the results table isnt there
    with pytest.raises(NotFound):
        BQ_CLIENT.get_table(f"{BQ_DATASET}.{BQ_WRITE_TABLE}")

    # do the process
    # assert the column is there
    # create a batch
    dataproc_client = dataproc.BatchControllerClient(
        client_options={
            "api_endpoint": f"{DATAPROC_REGION}-dataproc.googleapis.com:443"
        }
    )
    request = dataproc.CreateBatchRequest(
        parent=f"projects/{PROJECT_ID}/regions/{DATAPROC_REGION}",
        batch=BATCH_CONFIG,
        batch_id=BATCH_ID,
    )
    # Make the request
    operation = dataproc_client.create_batch(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

    # check that the results table is there now
    assert BQ_CLIENT.get_table(f"{BQ_DATASET}.{BQ_WRITE_TABLE}").num_rows > 0
