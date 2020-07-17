"""Test file for the setup job in the Data Science Onramp sample application
Creates a test Dataproc cluster and runs the job with a --test flag.
The job uploads a subset of the data to BigQuery.
Then, data is pulled from BigQuery and checks are made to see if the data is dirty.
"""

import os
import re
import uuid

from google.cloud import bigquery
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

# Set global variables
ID = uuid.uuid4()

PROJECT = os.environ['GCLOUD_PROJECT']
REGION = "us-central1"
CLUSTER_NAME = f'setup-test-{ID}'
BUCKET_NAME = f'setup-test-{ID}'
DATASET_NAME = f'setup-test-{ID}'.replace("-", "_")
CITIBIKE_TABLE = "new_york_citibike_trips"
DESTINATION_BLOB_NAME = "setup.py"
JOB_FILE_NAME = f'gs://{BUCKET_NAME}/setup.py'
TABLE_NAMES = [
    "new_york_citibike_trips",
    "gas_prices",
]
JOB_DETAILS = {  # Job configuration
    'placement': {
        'cluster_name': CLUSTER_NAME
    },
    'pyspark_job': {
        'main_python_file_uri': JOB_FILE_NAME,
        'args': [
            BUCKET_NAME,
            DATASET_NAME,
            "--test",
        ],
        "jar_file_uris": [
                "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
        ],
    },
}
CLUSTER_DATA = {  # Create cluster configuration
    'project_id': PROJECT,
    'cluster_name': CLUSTER_NAME,
    'config': {
        'gce_cluster_config': {
            'zone_uri': '',
        },
        'master_config': {
            'num_instances': 1,
            'machine_type_uri': 'n1-standard-8'
        },
        'worker_config': {
            'num_instances': 6,
            'machine_type_uri': 'n1-standard-8'
        },
        "software_config": {
            "image_version": "1.5.4-debian10",
            "optional_components": [
                "ANACONDA"
            ],
        }
    }
}


@pytest.fixture(autouse=True)
def setup_and_teardown_cluster():
    # Create cluster using cluster client
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': f'{REGION}-dataproc.googleapis.com:443'
    })
    operation = cluster_client.create_cluster(PROJECT, REGION, CLUSTER_DATA)

    # Wait for cluster to provision
    operation.result()

    yield

    # Delete cluster
    operation = cluster_client.delete_cluster(PROJECT, REGION,
                                              CLUSTER_NAME)
    operation.result()


@pytest.fixture(autouse=True)
def setup_and_teardown_bucket():
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    # Upload file
    blob = bucket.blob(DESTINATION_BLOB_NAME)
    blob.upload_from_filename("setup.py")

    yield

    # Delete GCS bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.delete(force=True)


@pytest.fixture(autouse=True)
def setup_and_teardown_bq_dataset():
    # Dataset is created by the client
    bq_client = bigquery.Client(project=PROJECT)

    yield

    # Delete Dataset
    bq_client.delete_dataset(DATASET_NAME, delete_contents=True)


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
    assert re.search(f"Table {table_name} successfully written to BigQuery", out), \
        f"Table {table_name} sucess message not printed in job logs"


def test_setup():
    """Test setup.py by submitting it to a dataproc cluster
    Check table upload success message as well as data in the table itself"""

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': f'{REGION}-dataproc.googleapis.com:443'
    })
    response = job_client.submit_job_as_operation(project_id=PROJECT, region=REGION,
                                                  job=JOB_DETAILS)

    # Wait for job to complete
    result = response.result()

    # Get job output
    out = get_dataproc_job_output(result)

    # Check logs to see if tables were uploaded
    for table_name in TABLE_NAMES:
        assert_table_success_message(table_name, out)

    # Query BigQuery Table
    client = bigquery.Client()

    regex_dict = {
        "tripduration": ["(\\d+(?:\\.\\d+)?) s", "(\\d+(?:\\.\\d+)?) min", "(\\d+(?:\\.\\d+)?) h"],
        "gender": ['f', 'F', 'm', 'M', 'u', 'U', 'male', 'MALE', 'female', 'FEMALE', 'unknown', 'UNKNOWN'],
        "start_station_latitude": ["[0-9]+" + u"\u00B0" + "[0-9]+\'[0-9]+\""],
        "start_station_longitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "end_station_latitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "end_station_longitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "usertype": ["Subscriber", "subscriber", "SUBSCRIBER", "sub", "Customer", "customer", "CUSTOMER", "cust"],
    }

    for column_name, regexes in regex_dict.items():
        query = f"SELECT {column_name} FROM `{PROJECT}.{DATASET_NAME}.{CITIBIKE_TABLE}`"
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
            assert found, \
                f"No matches to regular expression \"{regex}\" found in column {column_name}"
