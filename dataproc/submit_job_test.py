# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid
import pytest

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage

import submit_job


PROJECT_ID = os.environ['GCLOUD_PROJECT']
REGION = 'us-central1'
CLUSTER_NAME = 'test-cluster-{}'.format(str(uuid.uuid4()))
STAGING_BUCKET = 'test-bucket-{}'.format(str(uuid.uuid4()))
JOB_FILE_NAME = 'sum.py'


@pytest.fixture(autouse=True)
def setup_teardown():
    sort_file = """
    import pyspark
    sc = pyspark.SparkContext()
    rdd = sc.parallelize((1,2,3,4,5)
    sum = rdd.reduce(lambda x, y: x + y)
    """

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(STAGING_BUCKET)
    blob = bucket.blob(JOB_FILE_NAME)
    blob.upload_from_string(sort_file)

    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format(REGION)
    })

    cluster = {
        'project_id': PROJECT_ID,
        'cluster_name': CLUSTER_NAME,
        'config': {}
    }

    # Create the cluster
    operation = cluster_client.create_cluster(PROJECT_ID, REGION, cluster)
    operation.result()

    yield

    cluster_client.delete_cluster(PROJECT_ID, REGION, CLUSTER_NAME)

    blob.delete()


def test_submit_job(capsys):
    # Wrapper function for client library function
    job_file_path = 'gs://{}/{}'.format(STAGING_BUCKET, JOB_FILE_NAME)
    submit_job.submit_job(PROJECT_ID, REGION, CLUSTER_NAME, job_file_path)

    out, _ = capsys.readouterr()
    assert 'finished' in out
