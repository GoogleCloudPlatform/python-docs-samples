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
from google.api_core.exceptions import (InternalServerError, InvalidArgument, NotFound,
                                        ServiceUnavailable)
from google.cloud import dataproc_v1 as dataproc
import pytest

import create_cluster

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "northamerica-northeast1"
CLUSTER_NAME = "py-cc-test-{}".format(str(uuid.uuid4()))


@pytest.fixture(autouse=True)
def teardown():
    yield

    cluster_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )
    # Client library function
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


# InvalidArgument is thrown when the subnetwork is not ready
@backoff.on_exception(backoff.expo, (InternalServerError, ServiceUnavailable, InvalidArgument), max_tries=5)
def test_cluster_create(capsys):
    # Wrapper function for client library function
    create_cluster.create_cluster(PROJECT_ID, REGION, CLUSTER_NAME)

    out, _ = capsys.readouterr()
    assert CLUSTER_NAME in out
