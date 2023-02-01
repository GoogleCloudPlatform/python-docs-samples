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

import backoff
from google.api_core.exceptions import ServiceUnavailable
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

import quickstart


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = "py-qs-test-{}".format(str(uuid.uuid4()))
STAGING_BUCKET = "py-dataproc-qs-bucket-{}".format(str(uuid.uuid4()))
JOB_FILE_NAME = "sum.py"
JOB_FILE_PATH = "gs://{}/{}".format(STAGING_BUCKET, JOB_FILE_NAME)
SORT_CODE = (
    "import pyspark\n"
    "sc = pyspark.SparkContext()\n"
    "rdd = sc.parallelize((1,2,3,4,5))\n"
    "sum = rdd.reduce(lambda x, y: x + y)\n"
)


@pytest.fixture(autouse=True)
def blob():
    storage_client = storage.Client()

    @backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
    def create_bucket():
        return storage_client.create_bucket(STAGING_BUCKET)

    bucket = create_bucket()
    blob = bucket.blob(JOB_FILE_NAME)
    blob.upload_from_string(SORT_CODE)

    yield

    blob.delete()
    bucket.delete()


@pytest.fixture(autouse=True)
def cluster():
    yield

    # The quickstart sample deletes the cluster, but if the test fails
    # before cluster deletion occurs, it can be manually deleted here.
    cluster_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION)}
    )

    clusters = cluster_client.list_clusters(
        request={"project_id": PROJECT_ID, "region": REGION}
    )

    for cluster in clusters:
        if cluster.cluster_name == CLUSTER_NAME:
            cluster_client.delete_cluster(
                request={
                    "project_id": PROJECT_ID,
                    "region": REGION,
                    "cluster_name": CLUSTER_NAME,
                }
            )


def test_quickstart(capsys):
    quickstart.quickstart(PROJECT_ID, REGION, CLUSTER_NAME, JOB_FILE_PATH)
    out, _ = capsys.readouterr()

    assert "Cluster created successfully" in out
    assert "Job finished successfully" in out
    assert "successfully deleted" in out
