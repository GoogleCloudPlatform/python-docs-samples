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
from google.api_core.exceptions import (InternalServerError, InvalidArgument, NotFound,
                                        ServiceUnavailable)
from google.cloud import dataproc_v1 as dataproc
import pytest

import submit_job

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = "py-sj-test-{}".format(str(uuid.uuid4()))
CLUSTER = {
    "project_id": PROJECT_ID,
    "cluster_name": CLUSTER_NAME,
    "config": {
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
    },
}


@pytest.fixture(autouse=True)
def setup_teardown():
    # Retry on InvalidArgument subnetwork not ready error
    @backoff.on_exception(backoff.expo, (InvalidArgument), max_tries=3)
    def eventually_consistent_operation():
        try:
            cluster_client = dataproc.ClusterControllerClient(
                client_options={
                    "api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION)
                }
            )

            # Create the cluster.
            operation = cluster_client.create_cluster(
                request={"project_id": PROJECT_ID, "region": REGION, "cluster": CLUSTER}
            )
            print("hi")
            operation.result()
            print("yes")
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
    eventually_consistent_operation()


@backoff.on_exception(backoff.expo, (InternalServerError, ServiceUnavailable), max_tries=5)
def test_submit_job(capsys):
    submit_job.submit_job(PROJECT_ID, REGION, CLUSTER_NAME)
    out, _ = capsys.readouterr()

    assert "Job finished successfully" in out
