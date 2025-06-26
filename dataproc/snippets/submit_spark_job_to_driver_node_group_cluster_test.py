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
from google.api_core.exceptions import (
    Aborted,
    InternalServerError,
    ServiceUnavailable,
    NotFound,
)

from google.cloud import dataproc_v1 as dataproc
import submit_spark_job_to_driver_node_group_cluster

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = f"py-ss-test-{str(uuid.uuid4())}"

cluster_client = dataproc.ClusterControllerClient(
    client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
)


@backoff.on_exception(backoff.expo, (Exception), max_tries=5)
def teardown():
    try:
        operation = cluster_client.delete_cluster(
            request={
                "project_id": PROJECT_ID,
                "region": REGION,
                "cluster_name": CLUSTER_NAME,
            }
        )
        # Wait for cluster to delete
        operation.result()
    except NotFound:
        print("Cluster already deleted")


@backoff.on_exception(
    backoff.expo,
    (
        InternalServerError,
        ServiceUnavailable,
        Aborted,
    ),
    max_tries=5,
)
def test_workflows(capsys):

    # create temporary cluster for test
    request = dataproc.GetClusterRequest(
        project_id=PROJECT_ID, region=REGION, cluster_name=CLUSTER_NAME
    )
    response = cluster_client.get_cluster(request=request)

    # Wrapper function for client library function
    submit_spark_job_to_driver_node_group_cluster.submit_job(PROJECT_ID, REGION, CLUSTER_NAME)

    out, _ = capsys.readouterr()
    assert "successfully" in out

    # cluster deleted in teardown()
