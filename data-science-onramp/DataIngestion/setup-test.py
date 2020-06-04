import os

from time import sleep
import uuid

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage

waiting_cluster_callback = False

# Set variables
project = os.environ['GCLOUD_PROJECT']
region = "us-central1"
zone = "us-central1-a"
cluster_name = 'setup-test-{}'.format(str(uuid.uuid4()))


def test_setup(capsys):
    '''Create GCS Bucket'''
    storage_client = storage.Client()
    bucket_name = 'setup-test-code-{}'.format(str(uuid.uuid4()))
    bucket = storage_client.create_bucket(bucket_name)

    '''Upload file'''
    destination_blob_name = "setup.py"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename("setup.py")

    job_file_name = "gs://" + bucket_name + "/setup.py"

    '''Create Cluster'''
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
                'num_instances': 8,
                'machine_type_uri': 'n1-standard-8'
            },
            "initialization_actions": [
                {
                    "executable_file": "gs://dataproc-initialization-actions/python/pip-install.sh",
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

    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })
    cluster = cluster_client.create_cluster(project, region, cluster_data)
    cluster.add_done_callback(callback)

    global waiting_cluster_callback
    waiting_cluster_callback = True

    wait_for_cluster_creation()

    '''Submit job'''
    job_details = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': job_file_name,
            'args': [
                bucket_name,
                "0.01",
            ],
            "jar_file_uris": [
                "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
            ],
        },
    }

    job_client = dataproc.JobControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    sleep(120)  # Wait for job to complete

    result = job_client.submit_job(project_id=project, region=region,
                                   job=job_details)

    job_id = result.reference.job_id
    print('Submitted job \"{}\".'.format(job_id))

    # Get job output
    cluster_info = cluster_client.get_cluster(project, region, cluster_name)
    bucket = storage_client.get_bucket(cluster_info.config.config_bucket)
    output_blob = (
        'google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'
        .format(cluster_info.cluster_uuid, job_id))
    out = bucket.blob(output_blob)

    assert type(out) == str
    assert len(out) > 0

    # tripDuration

    # starttime

    # stoptime

    # start_station_id

    # start_station_latitude

    # start_station_longitude

    # end_station_id

    # end_station_name

    # end_station_latitude

    # end_station_longitude

    # bikeid

    # birth_year

    # gender
    assert "M" in out
    assert "male" in out
    assert "MALE" in out
    assert "F" in out
    assert "female" in out
    assert "FEMALE" in out

    # customer_plan
    assert "Subscriber" in out
    assert "subscriber" in out
    assert "SUBSCRIBER" in out
    assert "sub" in out
    assert "Customer" in out
    assert "customer" in out
    assert "CUSTOMER" in out
    assert "cust" in out


def callback(operation_future):
    global waiting_cluster_callback
    waiting_cluster_callback = False


def wait_for_cluster_creation():
    while True:
        if not waiting_cluster_callback:
            break
