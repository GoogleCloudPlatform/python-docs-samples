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
from google.cloud import bigquery
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


# def is_in_table(value, out):
#     return re.search(f"\\| *{value} *\\|", out)


def assert_table_success_message(table_name, out):
    """Check table upload success message was printed in job logs."""
    assert re.search(f"Table {table_name} successfully written to BigQuery", out), \
        f"Table {table_name} sucess message not printed in job logs"



def assert_regexes_in_table(regex_dict, query_result):
    """Assert that at least one row satisfies each regex.
    The arguments are
    - regex_dict: a dictionary where the keys are column
                    names and values are lists of regexes;
    - query_result: the bigquery query result of the whole table.
    """

    # Create dictionary with keys column names and values dictionaries
    # The dictionaries stored have keys regexes and values booleans
    # `regex_found_dict[column][regex]` hold the truth value of
    # whether the there is at least one row of column with name `column`
    # which satisfies the regular expression `regex`.
    regex_found_dict = {}
    for column, regexes in regex_dict.items():
        regex_found_dict[column] = {}
        for regex in regexes:
            regex_found_dict[column][regex] = False

    # Outer loop is over `query_result` since this is
    # an iterator which can only iterate once
    for row in query_result:
        for column_name, regexes in regex_dict.items():
            for regex in regexes:
                if row[column_name] and re.match(f"\\A{regex}\\Z", row[column_name]):
                    regex_found_dict[column_name][regex] = True

    # Assert that all entries in regex_found_dict are true
    for column_name in regex_found_dict:
        for regex, found in regex_found_dict[column_name].items():
            assert found, \
                    f"No matches to regular expression \"{regex}\" found in column {column_name}"


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
    query = f"SELECT * FROM `{PROJECT}.{DATASET_NAME}.{CITIBIKE_TABLE}`"
    query_job = client.query(query)

    result = query_job.result()

    regex_dict = {
        "tripduration": ["(\\d+(?:\\.\\d+)?) s", "(\\d+(?:\\.\\d+)?) min", "(\\d+(?:\\.\\d+)?) h"],
        "gender": ['f', 'F', 'm', 'M', 'u', 'U', 'male', 'MALE', 'female', 'FEMALE', 'unknown', 'UNKNOWN'],
        "start_station_latitude": ["[0-9]+" + u"\u00B0" + "[0-9]+\'[0-9]+\""],
        "start_station_longitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "end_station_latitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "end_station_longitude": ["-?[0-9]+" + u"\u00B0" + "-?[0-9]+\'-?[0-9]+\""],
        "usertype": ["Subscriber", "subscriber", "SUBSCRIBER", "sub", "Customer", "customer", "CUSTOMER", "cust"],
    }

    assert_regexes_in_table(regex_dict, result)

