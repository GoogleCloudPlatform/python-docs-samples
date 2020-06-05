import os
import re

import uuid

from google.api_core.exceptions import GoogleAPICallError

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
from google.cloud.exceptions import NotFound

import pytest

waiting_cluster_callback = False

# Set global variables
project = os.environ['GCLOUD_PROJECT']
region = "us-central1"
zone = "us-central1-a"
cluster_name = 'setup-test-{}'.format(str(uuid.uuid4()))
bucket_name = 'setup-test-code-{}'.format(str(uuid.uuid4()))


@pytest.fixture(autouse=True)
def teardown():
    yield

    # Delete cluster
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': f'{region}-dataproc.googleapis.com:443'
    })

    try:
        operation = cluster_client.delete_cluster(project, region,
                                                  cluster_name)
        operation.result()
    except GoogleAPICallError:
        pass

    # Delete GCS bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete(force=True)
    except NotFound:
        pass


def test_setup(capsys):
    '''Tests setup.py by submitting it to a dataproc cluster'''

    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    # Upload file
    destination_blob_name = "setup.py"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename("setup.py")

    job_file_name = "gs://" + bucket_name + "/setup.py"

    # Create cluster configuration
    zone_uri = \
        'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(
            project, zone)
    cluster_data = {
        'project_id': project,
        'cluster_name': cluster_name,
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
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    cluster = cluster_client.create_cluster(project, region, cluster_data)
    cluster.add_done_callback(callback)

    # Wait for cluster to provision
    global waiting_cluster_callback
    waiting_cluster_callback = True

    wait_for_cluster_creation()

    # Create job configuration
    job_details = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': job_file_name,
            'args': [
                bucket_name,
                "--test",
            ],
            "jar_file_uris": [
                "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
            ],
        },
    }

    # Submit job to dataproc cluster
    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    result = job_client.submit_job(project_id=project, region=region,
                                   job=job_details)

    job_id = result.reference.job_id
    print('Submitted job \"{}\".'.format(job_id))

    # Wait for job to complete
    wait_for_job(job_client, job_id)

    # Get job output
    cluster_info = cluster_client.get_cluster(project, region, cluster_name)
    bucket = storage_client.get_bucket(cluster_info.config.config_bucket)
    output_blob = (
        'google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'
        .format(cluster_info.cluster_uuid, job_id))
    out = bucket.blob(output_blob).download_as_string().decode("utf-8")

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


def callback(operation_future):
    '''Sets a flag to stop waiting'''
    global waiting_cluster_callback
    waiting_cluster_callback = False


def wait_for_cluster_creation():
    '''Waits for cluster to create'''
    while True:
        if not waiting_cluster_callback:
            break


def wait_for_job(job_client, job_id):
    '''Waits for job to finish'''
    while True:
        job = job_client.get_job(project, region, job_id)
        assert job.status.State.Name(job.status.state) != "ERROR"

        if job.status.State.Name(job.status.state) == "DONE":
            return
