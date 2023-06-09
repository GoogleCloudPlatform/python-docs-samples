# Copyright 2021 Google LLC
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

# This sample walks a user through updating the number of clusters using the Dataproc
# client library.

import os
import uuid

import backoff
from google.api_core.exceptions import (
    AlreadyExists,
    Cancelled,
    InternalServerError,
    InvalidArgument,
    NotFound,
    ServiceUnavailable,
)
from google.cloud.dataproc_v1 import ClusterStatus, GetClusterRequest
from google.cloud.dataproc_v1.services.cluster_controller.client import (
    ClusterControllerClient,
)
import pytest

import update_cluster

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = f"py-cc-test-{str(uuid.uuid4())}"
NEW_NUM_INSTANCES = 3
CLUSTER = {
    "project_id": PROJECT_ID,
    "cluster_name": CLUSTER_NAME,
    "config": {
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_size_gb": 100}},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_size_gb": 100}},
    },
}


@pytest.fixture(scope='module')
def cluster_client():
    cluster_client = ClusterControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )
    return cluster_client


@backoff.on_exception(backoff.expo, (ServiceUnavailable, InvalidArgument), max_tries=5)
def setup_cluster(cluster_client):
    try:
        # Create the cluster.
        operation = cluster_client.create_cluster(
            request={"project_id": PROJECT_ID, "region": REGION, "cluster": CLUSTER}
        )
        operation.result()
    except AlreadyExists:
        print("Cluster already exists, utilize existing cluster")


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def teardown_cluster(cluster_client):
    try:
        operation = cluster_client.delete_cluster(
            request={
                "project_id": PROJECT_ID,
                "region": REGION,
                "cluster_name": CLUSTER_NAME,
            }
        )
        operation.result()
    except NotFound:
        print("Cluster already deleted")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, Cancelled), max_tries=5
)
def test_update_cluster(capsys, cluster_client: ClusterControllerClient):

    try:
        setup_cluster(cluster_client)
        request = GetClusterRequest(project_id=PROJECT_ID, region=REGION, cluster_name=CLUSTER_NAME)
        response = cluster_client.get_cluster(request=request)
        # verify the cluster is in the RUNNING state before proceeding
    # this prevents a retry on InvalidArgument if the cluster is in an ERROR state
        assert response.status.state == ClusterStatus.State.RUNNING

        # Wrapper function for client library function
        update_cluster.update_cluster(PROJECT_ID, REGION, CLUSTER_NAME, NEW_NUM_INSTANCES)
        new_num_cluster = cluster_client.get_cluster(
            project_id=PROJECT_ID, region=REGION, cluster_name=CLUSTER_NAME
        )
        out, _ = capsys.readouterr()
        assert CLUSTER_NAME in out
        assert new_num_cluster.config.worker_config.num_instances == NEW_NUM_INSTANCES

    finally:
        teardown_cluster(cluster_client)
