# Copyright 2020 Google LLC
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
from google.api_core.exceptions import (AlreadyExists, InternalServerError, InvalidArgument, NotFound,
                                        ServiceUnavailable)
from google.cloud import dataproc_v1 as dataproc
import pytest

import submit_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"


@pytest.fixture(scope='module')
def cluster_client():
    return dataproc.ClusterControllerClient(
        client_options={
            "api_endpoint": f"{REGION}-dataproc.googleapis.com:443"
        }
    )


@backoff.on_exception(backoff.expo, (ServiceUnavailable, InvalidArgument), max_tries=5)
def setup_cluster(cluster_client, curr_cluster_name):

    CLUSTER = {
        "project_id": PROJECT_ID,
        "cluster_name": curr_cluster_name,
        "config": {
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_size_gb": 100}},
            "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_size_gb": 100}},
        },
    }

    # Create the cluster.
    operation = cluster_client.create_cluster(
        request={"project_id": PROJECT_ID, "region": REGION, "cluster": CLUSTER}
    )
    operation.result()


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def teardown_cluster(cluster_client, curr_cluster_name):
    try:
        operation = cluster_client.delete_cluster(
            request={
                "project_id": PROJECT_ID,
                "region": REGION,
                "cluster_name": curr_cluster_name,
            }
        )
        operation.result()

    except NotFound:
        print("Cluster already deleted")


@pytest.fixture(scope='module')
def cluster_name(cluster_client):
    curr_cluster_name = f"py-sj-test-{str(uuid.uuid4())}"

    try:
        setup_cluster(cluster_client, curr_cluster_name)
        yield curr_cluster_name
    except AlreadyExists:  # 409 can happen when we backoff on service errors during submission
        print("Already exists, skipping cluster creation")
        yield curr_cluster_name
    finally:
        teardown_cluster(cluster_client, curr_cluster_name)


# InvalidArgument is thrown when the subnetwork is not ready
@backoff.on_exception(backoff.expo, (InvalidArgument, InternalServerError, ServiceUnavailable), max_tries=5)
def test_submit_job(capsys, cluster_name, cluster_client):
    request = dataproc.GetClusterRequest(project_id=PROJECT_ID, region=REGION, cluster_name=cluster_name)
    response = cluster_client.get_cluster(request=request)
    # verify the cluster is in the RUNNING state before proceeding
    # this prevents a retry on InvalidArgument if the cluster is in an ERROR state
    assert response.status.state == dataproc.ClusterStatus.State.RUNNING
    submit_job.submit_job(PROJECT_ID, REGION, cluster_name)
    out, _ = capsys.readouterr()

    assert "Job finished successfully" in out
