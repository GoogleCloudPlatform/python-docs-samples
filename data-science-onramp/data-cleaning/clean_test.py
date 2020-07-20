import os
import re
import uuid

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

# Set global variables
PROJECT = os.environ['GCLOUD_PROJECT']
DATAPROC_CLUSTER = f'clean-test-{uuid.uuid4()}'
BUCKET_NAME = f'clean-test-code-{uuid.uuid4()}'
CLUSTER_REGION = "us-east4"
DESTINATION_BLOB_NAME = "clean.py"
JOB_FILE_NAME = f'gs://{BUCKET_NAME}/clean.py'
JOB_DETAILS = {  # Job configuration
    'placement': {
        'cluster_name': DATAPROC_CLUSTER
    },
    'pyspark_job': {
        'main_python_file_uri': JOB_FILE_NAME,
        'args': [
            PROJECT,
            BUCKET_NAME,
            "--dry-run",
        ],
        "jar_file_uris": [
                "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
        ],
    },
}
CLUSTER_IMAGE = "1.5.4-debian10"
CLUSTER_DATA = {  # Create cluster configuration
    'project_id': PROJECT,
    'cluster_name': DATAPROC_CLUSTER,
    'config': {
        'gce_cluster_config': {
            'zone_uri': '',
            "metadata": {
                "PIP_PACKAGES": "google-cloud-storage"
            },
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
            "image_version": CLUSTER_IMAGE,
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
        'api_endpoint': f'{CLUSTER_REGION}-dataproc.googleapis.com:443'
    })
    operation = cluster_client.create_cluster(PROJECT, CLUSTER_REGION, CLUSTER_DATA)

    # Wait for cluster to provision
    operation.result()

    yield

    # Delete cluster
    operation = cluster_client.delete_cluster(PROJECT, CLUSTER_REGION, DATAPROC_CLUSTER)
    operation.result()


@pytest.fixture(autouse=True)
def setup_and_teardown_bucket():
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    # Upload file
    blob = bucket.blob(DESTINATION_BLOB_NAME)
    blob.upload_from_filename("clean.py")

    yield

    # Delete GCS bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.delete(force=True)


def is_in_table(value, out):
    return re.search(f"\\| *{value} *\\|", out)


def get_blob_from_path(path):
    bucket_name = re.search("dataproc.+?/", path).group(0)[0:-1]
    bucket = storage.Client().get_bucket(bucket_name)
    output_location = re.search("google-cloud-dataproc.+", path).group(0)
    return bucket.blob(output_location)


def test_clean():
    '''Tests clean.py by submitting it to a dataproc cluster'''

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': f'{CLUSTER_REGION}-dataproc.googleapis.com:443'
    })
    response = job_client.submit_job_as_operation(project_id=PROJECT, region=CLUSTER_REGION, job=JOB_DETAILS)

    # Wait for job to complete
    result = response.result()

    # Get job output
    output_location = result.driver_output_resource_uri + ".000000000"
    blob = get_blob_from_path(output_location)
    out = blob.download_as_string().decode("utf-8")

    # tripDuration
    assert not is_in_table("(\\d+(?:\\.\\d+)?) s", out)
    assert not is_in_table("(\\d+(?:\\.\\d+)?) min", out)
    assert not is_in_table("(\\d+(?:\\.\\d+)?) h", out)

    # station latitude & longitude
    assert not is_in_table("[0-9]+" + u"\u00B0" + "[0-9]+\'[0-9]+\"", out)

    assert is_in_table("\\d*.\\d*")

    # gender
    assert not is_in_table("M", out)
    assert not is_in_table("m", out)
    assert not is_in_table("male", out)
    assert not is_in_table("MALE", out)
    assert not is_in_table("F", out)
    assert not is_in_table("f", out)
    assert not is_in_table("female", out)
    assert not is_in_table("FEMALE", out)
    assert not is_in_table("U", out)
    assert not is_in_table("u", out)
    assert not is_in_table("unknown", out)
    assert not is_in_table("UNKNOWN", out)

    assert is_in_table("Male", out)
    assert is_in_table("Female", out)

    # customer_plan
    assert not is_in_table("subscriber", out)
    assert not is_in_table("SUBSCRIBER", out)
    assert not is_in_table("sub", out)
    assert not is_in_table("customer", out)
    assert not is_in_table("CUSTOMER", out)
    assert not is_in_table("cust", out)

    assert is_in_table("Subscriber", out)
    assert is_in_table("Customer", out)
