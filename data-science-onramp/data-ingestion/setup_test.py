import os
import re

import uuid

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage

import pytest


# Set global variables
PROJECT = os.environ['GCLOUD_PROJECT']
REGION = "us-central1"
ZONE = "us-central1-a"
CLUSTER_NAME = f'setup-test-{uuid.uuid4()}'
BUCKET_NAME = f'setup-test-code-{uuid.uuid4()}'

BUCKET = None


@pytest.fixture(autouse=True)
def setup_and_teardown_cluster():
    # Create cluster configuration
    zone_uri = \
        f'https://www.googleapis.com/compute/v1/projects/{PROJECT}/zones/{ZONE}'
    cluster_data = {
        'project_id': PROJECT,
        'cluster_name': CLUSTER_NAME,
        'config': {
            'gce_cluster_config': {
                'zone_uri': zone_uri,
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
            "initialization_actions": [
                {
                    "executable_file": ("gs://dataproc-initialization-actions/"
                                        "python/pip-install.sh"),
                }
            ],
            "software_config": {
                "image_version": "1.5.4-debian10",
                "optional_components": [
                    "ANACONDA"
                ],
            }
        }
    }

    # Create cluster using cluster client
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(REGION)
    })

    operation = cluster_client.create_cluster(PROJECT, REGION, cluster_data)

    # Wait for cluster to provision
    operation.result()

    yield

    # Delete cluster
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': f'{REGION}-dataproc.googleapis.com:443'
    })

    operation = cluster_client.delete_cluster(PROJECT, REGION,
                                              CLUSTER_NAME)
    operation.result()


@pytest.fixture(autouse=True)
def setup_and_teardown_bucket():
    global BUCKET
    # Create GCS Bucket
    storage_client = storage.Client()
    BUCKET = storage_client.create_bucket(BUCKET_NAME)

    yield

    # Delete GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.delete(force=True)


def test_setup(capsys):
    '''Tests setup.py by submitting it to a dataproc cluster'''

    # Upload file
    destination_blob_name = "setup.py"
    blob = BUCKET.blob(destination_blob_name)
    blob.upload_from_filename("setup.py")

    job_file_name = "gs://" + BUCKET_NAME + "/setup.py"

    # Create job configuration
    job_details = {
        'placement': {
            'cluster_name': CLUSTER_NAME
        },
        'pyspark_job': {
            'main_python_file_uri': job_file_name,
            'args': [
                BUCKET_NAME,
                "--test",
            ],
            "jar_file_uris": [
                "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
            ],
        },
    }

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(REGION)
    })

    response = job_client.submit_job_as_operation(project_id=PROJECT, region=REGION,
                                                  job=job_details)

    # Wait for job to complete
    result = response.result()

    # Get job output
    output_location = result.driver_output_resource_uri + ".000000000"
    blob = get_blob_from_path(output_location)
    out = blob.download_as_string().decode("utf-8")

    # tripDuration
    assert re.search("[0-9] s", out)
    assert re.search("[0-9] m", out)
    assert re.search("[0-9] h", out)

    # station latitude & longitude
    assert re.search(u"\u00B0" + "[0-9]+\'[0-9]+\"", out)

    # birth_year
    assert re.search("19[0-9][0-9]\\|", out)
    assert re.search("20[0-9][0-9]\\|", out)

    # gender
    assert "M" in out
    assert "male" in out
    assert "MALE" in out
    assert "F" in out
    assert "female" in out
    assert "FEMALE" in out
    assert "u" in out
    assert "unknown" in out
    assert "UNKNOWN" in out

    # customer_plan
    assert "Subscriber" in out
    assert "subscriber" in out
    assert "SUBSCRIBER" in out
    assert "sub" in out
    assert "Customer" in out
    assert "customer" in out
    assert "CUSTOMER" in out
    assert "cust" in out

    # Missing data
    assert "null" in out


def get_blob_from_path(path):
    bucket_name = re.search("dataproc.+?/", path).group(0)[0:-1]
    bucket = storage.Client().get_bucket(bucket_name)
    output_location = re.search("google-cloud-dataproc.+", path).group(0)
    return bucket.blob(output_location)
