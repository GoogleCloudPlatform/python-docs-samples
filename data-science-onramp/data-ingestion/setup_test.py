"""Test file for the setup job in the Data Science Onramp sample application
Creates a test Dataproc cluster and runs the job with a --test flag.
The job uploads a subset of the data to BigQuery.
Then, data is pulled from BigQuery and checks are made to see if the data is dirty.
"""

import os
import re
import uuid

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

# Set global variables
PROJECT = os.environ['GCLOUD_PROJECT']
REGION = "us-central1"
CLUSTER_NAME = f'setup-test-{uuid.uuid4()}'
BUCKET_NAME = f'setup-test-code-{uuid.uuid4()}'
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


def get_blob_from_path(path):
    bucket_name = re.search("dataproc.+?/", path).group(0)[0:-1]
    bucket = storage.Client().get_bucket(bucket_name)
    output_location = re.search("google-cloud-dataproc.+", path).group(0)
    return bucket.blob(output_location)


def is_in_table(value, out):
    return re.search(f"\\| *{value} *\\|", out)


def table_uploaded(table_name, out):
    return re.search(f"Table {table_name} successfully written to BigQuery", out)


def test_setup():
    '''Tests setup.py by submitting it to a dataproc cluster'''

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': f'{REGION}-dataproc.googleapis.com:443'
    })
    response = job_client.submit_job_as_operation(project_id=PROJECT, region=REGION,
                                                  job=JOB_DETAILS)

    # Wait for job to complete
    result = response.result()

    # Get job output
    output_location = result.driver_output_resource_uri + ".000000000"
    blob = get_blob_from_path(output_location)
    out = blob.download_as_string().decode("utf-8")

    # Check if table upload success message was printed
    for table_name in TABLE_NAMES:
        assert table_uploaded(table_name, out)

    # tripDuration
    assert is_in_table("(\\d+(?:\\.\\d+)?) s", out)
    assert is_in_table("(\\d+(?:\\.\\d+)?) min", out)
    assert is_in_table("(\\d+(?:\\.\\d+)?) h", out)

    # station latitude & longitude
    assert is_in_table("[0-9]+" + u"\u00B0" + "[0-9]+\'[0-9]+\"", out)

    # birth_year
    assert is_in_table("19[0-9][0-9]", out)
    assert is_in_table("20[0-9][0-9]", out)

    # gender
    assert is_in_table("M", out)
    assert is_in_table("m", out)
    assert is_in_table("male", out)
    assert is_in_table("MALE", out)
    assert is_in_table("F", out)
    assert is_in_table("f", out)
    assert is_in_table("female", out)
    assert is_in_table("FEMALE", out)
    assert is_in_table("U", out)
    assert is_in_table("u", out)
    assert is_in_table("unknown", out)
    assert is_in_table("UNKNOWN", out)

    # customer_plan
    assert is_in_table("Subscriber", out)
    assert is_in_table("subscriber", out)
    assert is_in_table("SUBSCRIBER", out)
    assert is_in_table("sub", out)
    assert is_in_table("Customer", out)
    assert is_in_table("customer", out)
    assert is_in_table("CUSTOMER", out)
    assert is_in_table("cust", out)

    # Missing data
    assert is_in_table("null", out)
