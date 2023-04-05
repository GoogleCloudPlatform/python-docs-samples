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
"""Test file for the setup job in the Data Science Onramp sample application Creates a test Dataproc cluster and runs the job with a --test flag.
The job uploads a subset of the data to BigQuery.
Then, data is pulled from BigQuery and checks are made to see if the data is dirty.
"""

import os
import re
import uuid

from google.api_core import retry
from google.api_core.exceptions import InvalidArgument, NotFound
from google.cloud import bigquery
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

# GCP Project
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_ID = uuid.uuid4()

# Google Cloud Storage constants
BUCKET_NAME = f"ingestion-test-{TEST_ID}"
BUCKET_BLOB = "ingestion.py"

BQ_DATASET = f"setup-test-{TEST_ID}".replace("-", "_")
BQ_CITIBIKE_TABLE = "RAW_DATA"
BQ_TABLES = [
    BQ_CITIBIKE_TABLE,
    "gas_prices",
]

# Dataproc constants
DATAPROC_CLUSTER = f"ingestion-test-{TEST_ID}"
CLUSTER_REGION = "us-central1"
CLUSTER_IMAGE = "2.0-debian10"
CLUSTER_CONFIG = {  # Dataproc cluster configuration
    "project_id": PROJECT_ID,
    "cluster_name": DATAPROC_CLUSTER,
    "config": {
        "gce_cluster_config": {"zone_uri": ""},
        # We recommend these configs when running the full code
        # We use a less robust machine type for the tests
        # "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-8"},
        # "worker_config": {"num_instances": 6, "machine_type_uri": "n1-standard-8"},
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-4"},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-4"},
        "software_config": {
            "image_version": CLUSTER_IMAGE,
        },
    },
}
DATAPROC_JOB = {  # Dataproc job configuration
    "placement": {"cluster_name": DATAPROC_CLUSTER},
    "pyspark_job": {
        "main_python_file_uri": f"gs://{BUCKET_NAME}/{BUCKET_BLOB}",
        "args": [BUCKET_NAME, BQ_DATASET, "--test"],
        "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
    },
}


@pytest.fixture(autouse=True)
def setup_and_teardown_cluster():
    try:
        # Create cluster using cluster client
        cluster_client = dataproc.ClusterControllerClient(
            client_options={
                "api_endpoint": f"{CLUSTER_REGION}-dataproc.googleapis.com:443"
            }
        )

        operation = cluster_client.create_cluster(
            project_id=PROJECT_ID, region=CLUSTER_REGION, cluster=CLUSTER_CONFIG
        )

        # Wait for cluster to provision
        operation.result()

        yield
    finally:
        try:
            # Delete cluster
            operation = cluster_client.delete_cluster(
                project_id=PROJECT_ID,
                region=CLUSTER_REGION,
                cluster_name=DATAPROC_CLUSTER,
            )
            operation.result()
        except NotFound:
            print("Cluster already deleted")


@pytest.fixture(autouse=True)
def setup_and_teardown_bucket():
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    # Upload file
    blob = bucket.blob(BUCKET_BLOB)
    blob.upload_from_filename("ingestion.py")

    yield

    # Delete GCS bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.delete(force=True)


@pytest.fixture(autouse=True)
def setup_and_teardown_bq_dataset():
    # Dataset is created by the client
    bq_client = bigquery.Client(project=PROJECT_ID)

    yield

    # Delete Dataset
    try:
        bq_client.delete_dataset(BQ_DATASET, delete_contents=True)
    except NotFound as e:
        print(f"Ignoring NotFound on cleanup, details: {e}")


def get_blob_from_path(path):
    bucket_name = re.search("dataproc.+?/", path).group(0)[0:-1]
    bucket = storage.Client().get_bucket(bucket_name)
    output_location = re.search("google-cloud-dataproc.+", path).group(0)
    return bucket.blob(output_location)


def get_dataproc_job_output(result):
    """Get the dataproc job logs in plain text"""
    output_location = result.driver_output_resource_uri + ".000000000"
    blob = get_blob_from_path(output_location)
    return blob.download_as_string().decode("utf-8")


def assert_table_success_message(table_name, out):
    """Check table upload success message was printed in job logs."""
    assert re.search(
        f"Table {table_name} successfully written to BigQuery", out
    ), f"Table {table_name} sucess message not printed in job logs"


@retry.Retry(predicate=retry.if_exception_type(InvalidArgument))
def test_setup():
    """Test setup.py by submitting it to a dataproc cluster
    Check table upload success message as well as data in the table itself"""

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(
        client_options={"api_endpoint": f"{CLUSTER_REGION}-dataproc.googleapis.com:443"}
    )
    response = job_client.submit_job_as_operation(
        project_id=PROJECT_ID, region=CLUSTER_REGION, job=DATAPROC_JOB
    )

    # Wait for job to complete
    result = response.result()

    # Get job output
    out = get_dataproc_job_output(result)

    # Check logs to see if tables were uploaded
    for table_name in BQ_TABLES:
        assert_table_success_message(table_name, out)

    # Query BigQuery Table
    client = bigquery.Client()

    dms_regex = "-?[0-9]+\u00B0-?[0-9]+'-?[0-9]+\""

    regex_dict = {
        "tripduration": [
            "(\\d+(?:\\.\\d+)?) s",
            "(\\d+(?:\\.\\d+)?) min",
            "(\\d+(?:\\.\\d+)?) h",
        ],
        "gender": [
            "f",
            "F",
            "m",
            "M",
            "u",
            "U",
            "male",
            "MALE",
            "female",
            "FEMALE",
            "unknown",
            "UNKNOWN",
        ],
        "start_station_latitude": [dms_regex],
        "start_station_longitude": [dms_regex],
        "end_station_latitude": [dms_regex],
        "end_station_longitude": [dms_regex],
        "usertype": [
            "Subscriber",
            "subscriber",
            "SUBSCRIBER",
            "sub",
            "Customer",
            "customer",
            "CUSTOMER",
            "cust",
        ],
    }

    for column_name, regexes in regex_dict.items():
        query = (
            f"SELECT {column_name} FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_CITIBIKE_TABLE}`"
        )
        query_job = client.query(query)

        result = query_job.result()

        rows = []
        for row in result:
            rows.append(row[column_name])

        for regex in regexes:
            found = False
            for row in rows:
                if row and re.match(f"\\A{regex}\\Z", row):
                    found = True
                    break
            assert (
                found
            ), f'No matches to regular expression "{regex}" found in column {column_name}'
