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
from google.api_core.exceptions import (InternalServerError, NotFound,
                                        ServiceUnavailable)
from google.cloud.dataproc_v1.services.cluster_controller.client import \
    ClusterControllerClient
import pytest

import update_cluster

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = f"py-cc-test-{str(uuid.uuid4())}"
NEW_NUM_INSTANCES = 5
CLUSTER = {
    "project_id": PROJECT_ID,
    "cluster_name": CLUSTER_NAME,
    "config": {
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
    },
}


@pytest.fixture
def cluster_client():
    cluster_client = ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION)}
    )
    return cluster_client


@pytest.fixture(autouse=True)
def setup_teardown(cluster_client):
    try:
        # Create the cluster.
        operation = cluster_client.create_cluster(
            request={"project_id": PROJECT_ID, "region": REGION, "cluster": CLUSTER}
        )
        operation.result()

        yield
    finally:
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


@backoff.on_exception(backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5)
def test_update_cluster(capsys, cluster_client: ClusterControllerClient):
    # Wrapper function for client library function
    update_cluster.update_cluster(PROJECT_ID, REGION, CLUSTER_NAME, NEW_NUM_INSTANCES)
    new_num_cluster = cluster_client.get_cluster(
        project_id=PROJECT_ID, region=REGION, cluster_name=CLUSTER_NAME
    )

    out, _ = capsys.readouterr()
    assert CLUSTER_NAME in out
    assert new_num_cluster.config.worker_config.num_instances == NEW_NUM_INSTANCES
