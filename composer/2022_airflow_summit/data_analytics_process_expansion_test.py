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

from google.api_core.exceptions import Aborted, NotFound
from google.cloud import bigquery
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest


# GCP Project
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_ID = uuid.uuid4()
DATAPROC_REGION = "northamerica-northeast1"


# Google Cloud Storage constants
# filenames include dataproc_expansion path for nox to run properly
BUCKET_NAME = f"data-analytics-expansion-{TEST_ID}"
BUCKET_BLOB = "data_analytics_process_expansion.py"
TEST_CSV_FILE = "test_data_expansion.csv"

BQ_CLIENT = bigquery.Client(project=PROJECT_ID)

# BigQuery configs
BQ_DESTINATION_DATASET_NAME = f"expansion_project_test_{TEST_ID}".replace("-", "_")
BQ_DESTINATION_TABLE_NAME = "ghcnd_stations_joined"
BQ_DESTINATION_TABLE_ID = (
    f"{PROJECT_ID}.{BQ_DESTINATION_DATASET_NAME}.{BQ_DESTINATION_TABLE_NAME}"
)
BQ_NORMALIZED_TABLE_NAME = "ghcnd_stations_normalized"
BQ_PRCP_MEAN_TABLE_NAME = "ghcnd_stations_prcp_mean"
BQ_SNOW_MEAN_TABLE_NAME = "ghcnd_stations_prcp_mean"
BQ_PHX_PRCP_TABLE_NAME = "phx_annual_prcp"
BQ_PHX_SNOW_TABLE_NAME = "phx_annual_snow"

PROCESSING_PYTHON_FILE = f"gs://{BUCKET_NAME}/{BUCKET_BLOB}"


@pytest.fixture(scope="function")
def test_dataproc_batch(test_bucket, bq_dataset):
    # check that the results tables aren't there
    # considered using pytest parametrize, but did not want rest of test
    # to run 5 times - only this part
    output_tables = [
        BQ_NORMALIZED_TABLE_NAME,
        BQ_PRCP_MEAN_TABLE_NAME,
        BQ_SNOW_MEAN_TABLE_NAME,
        BQ_PHX_PRCP_TABLE_NAME,
        BQ_PHX_SNOW_TABLE_NAME,
    ]
    for output_table in output_tables:
        with pytest.raises(NotFound):
            BQ_CLIENT.get_table(f"{BQ_DESTINATION_DATASET_NAME}.{output_table}")

    BATCH_ID = f"summit-dag-expansion-test-{TEST_ID}"  # Dataproc serverless only allows lowercase characters
    BATCH_CONFIG = {
        "pyspark_batch": {
            "runtime_config": {
                "version": "1.1"
            },
            "main_python_file_uri": PROCESSING_PYTHON_FILE,
            "args": [
                BUCKET_NAME,
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_DESTINATION_TABLE_NAME}",
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_NORMALIZED_TABLE_NAME}",
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PRCP_MEAN_TABLE_NAME}",
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_SNOW_MEAN_TABLE_NAME}",
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_PRCP_TABLE_NAME}",
                f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_SNOW_TABLE_NAME}",
            ],
        }
    }

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
    try:
        # Make the request
        operation = dataproc_client.create_batch(request=request)

        print("Waiting for operation to complete...")

        response = operation.result()
    except Aborted as e:
        # retry once if we see a flaky 409 "subnet not ready error"
        if "/subnetworks/default" in str(e):
            # delete the errored out batch so we don't see an "AlreadyExists"
            delete_request = dataproc.DeleteBatchRequest(
                name=f"projects/{PROJECT_ID}/locations/{DATAPROC_REGION}/batches/{BATCH_ID}"
            )
            dataproc_client.delete_batch(request=delete_request)
            # retry the creation operation once
            create_request = dataproc.CreateBatchRequest(
                parent=f"projects/{PROJECT_ID}/regions/{DATAPROC_REGION}",
                batch=BATCH_CONFIG,
                batch_id=BATCH_ID,
            )
            operation = dataproc_client.create_batch(request=create_request)

            print("Waiting for operation to complete...")

            response = operation.result()
        else:
            raise (e)

    yield response
    dataproc_client = dataproc.BatchControllerClient(
        client_options={
            "api_endpoint": f"{DATAPROC_REGION}-dataproc.googleapis.com:443"
        }
    )
    request = dataproc.DeleteBatchRequest(
        name=f"projects/{PROJECT_ID}/locations/{DATAPROC_REGION}/batches/{BATCH_ID}"
    )

    # Declare variable outside of try/except so it can be printed in the exception
    response = None
    try:
        # Make the request
        response = dataproc_client.delete_batch(request=request)
    except NotFound:
        # There will only be a response if the deletion fails
        # otherwise response will be None
        print(response)


@pytest.fixture(scope="module")
def test_bucket():
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)
    print(os.listdir())

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


@pytest.fixture(autouse=True)
def bq_dataset(test_bucket):
    # Create dataset and table for test CSV
    BQ_CLIENT.create_dataset(BQ_DESTINATION_DATASET_NAME)

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("ID", "STRING"),
            bigquery.SchemaField("LATITUDE", "FLOAT"),
            bigquery.SchemaField("LONGITUDE", "FLOAT"),
            bigquery.SchemaField("STATE", "STRING"),
            bigquery.SchemaField("DATE", "STRING"),
            bigquery.SchemaField("ELEMENT", "STRING"),
            bigquery.SchemaField("VALUE", "FLOAT"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://{BUCKET_NAME}/{TEST_CSV_FILE}"

    load_job = BQ_CLIENT.load_table_from_uri(
        uri, BQ_DESTINATION_TABLE_ID, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = BQ_CLIENT.get_table(
        BQ_DESTINATION_TABLE_ID
    )  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

    yield

    # Delete Dataset
    try:
        BQ_CLIENT.delete_dataset(BQ_DESTINATION_DATASET_NAME, delete_contents=True)
    except NotFound as e:
        print(f"Ignoring NotFound on cleanup, details: {e}")


def test_process(test_dataproc_batch):
    print(test_dataproc_batch)

    # check that the results table is there now
    assert (
        BQ_CLIENT.get_table(
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_NORMALIZED_TABLE_NAME}"
        ).num_rows
        > 0
    )
    assert (
        BQ_CLIENT.get_table(
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PRCP_MEAN_TABLE_NAME}"
        ).num_rows
        > 0
    )
    assert (
        BQ_CLIENT.get_table(
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_SNOW_MEAN_TABLE_NAME}"
        ).num_rows
        > 0
    )
    assert (
        BQ_CLIENT.get_table(
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_PRCP_TABLE_NAME}"
        ).num_rows
        > 0
    )
    assert (
        BQ_CLIENT.get_table(
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_SNOW_TABLE_NAME}"
        ).num_rows
        > 0
    )
