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
import subprocess
import uuid

import backoff
from google.api_core.exceptions import (
    Aborted,
    InternalServerError,
    NotFound,
    ServiceUnavailable,
)
from google.cloud import dataproc_v1 as dataproc

import submit_pyspark_job_to_driver_node_group_cluster

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
    # Setup driver node group cluster. TODO: cleanup b/424371877
    command = f"""gcloud dataproc clusters create {CLUSTER_NAME} \
            --region {REGION} \
            --project {PROJECT_ID} \
            --driver-pool-size=1 \
            --driver-pool-id=pytest"""

    output = subprocess.run(
        command,
        capture_output=True,
        shell=True,
        check=True,
    )
    print(output)

    # Wrapper function for client library function
    submit_pyspark_job_to_driver_node_group_cluster.submit_job(
        PROJECT_ID, REGION, CLUSTER_NAME
    )

    out, _ = capsys.readouterr()
    assert "Job finished successfully" in out

    # cluster deleted in teardown()
