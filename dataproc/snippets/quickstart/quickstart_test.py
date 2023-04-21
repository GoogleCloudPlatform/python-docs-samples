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
import time

import backoff
from google.api_core.exceptions import InvalidArgument, ServiceUnavailable, Conflict
from google.cloud import compute_v1
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import pytest

import quickstart


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
SUBNET = "quickstart-test-subnet"

JOB_FILE_NAME = "sum.py"
SORT_CODE = (
    "import pyspark\n"
    "sc = pyspark.SparkContext()\n"
    "rdd = sc.parallelize((1,2,3,4,5))\n"
    "sum = rdd.reduce(lambda x, y: x + y)\n"
)


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def delete_bucket(bucket):
    bucket.delete()


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def delete_blob(blob):
    blob.delete()


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def upload_blob(bucket, contents):
    blob = bucket.blob(JOB_FILE_NAME)
    blob.upload_from_string(contents)
    return blob


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def create_bucket(bucket_name):
    storage_client = storage.Client()
    return storage_client.create_bucket(bucket_name)


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def create_subnet():
    instance_client = compute_v1.SubnetworksClient()
    try:
        instance_client.insert(
            project=PROJECT_ID,
            region=REGION,
            subnetwork_resource=compute_v1.Subnetwork(
                name=SUBNET,
                network="global/networks/default",
                ip_cidr_range="172.16.0.0/12",
            )
        )
        time.sleep(10)
    except Conflict:
        pass


@pytest.fixture(scope="module")
def staging_bucket_name():
    bucket_name = "py-dataproc-qs-bucket-{}".format(str(uuid.uuid4()))
    bucket = create_bucket(bucket_name)
    blob = upload_blob(bucket, SORT_CODE)
    try:
        yield bucket_name
    finally:
        delete_blob(blob)
        delete_bucket(bucket)



@pytest.fixture(scope="module")
def subnetwork_uri():
    create_subnet()
    return f"projects/{PROJECT_ID}/regions/{REGION}/subnetworks/{SUBNET}"


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def verify_cluster_teardown(cluster_name):
    # The quickstart sample deletes the cluster, but if the test fails
    # before cluster deletion occurs, it can be manually deleted here.
    cluster_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION)}
    )

    clusters = cluster_client.list_clusters(
        request={"project_id": PROJECT_ID, "region": REGION}
    )
    for cluster in clusters:
        if cluster.cluster_name == cluster_name:
            cluster_client.delete_cluster(
                request={
                    "project_id": PROJECT_ID,
                    "region": REGION,
                    "cluster_name": cluster_name,
                }
            )


@backoff.on_exception(backoff.expo, InvalidArgument, max_tries=3)
def test_quickstart(capsys, staging_bucket_name, subnetwork_uri):
    cluster_name = "py-qs-test-{}".format(str(uuid.uuid4()))
    try:
        quickstart.quickstart(
            PROJECT_ID,
            REGION,
            cluster_name,
            "gs://{}/{}".format(staging_bucket_name, JOB_FILE_NAME),
            subnetwork_uri,
        )
        out, _ = capsys.readouterr()

        assert "Cluster created successfully" in out
        assert "Job finished successfully" in out
        assert "successfully deleted" in out
    finally:
        verify_cluster_teardown(cluster_name)
