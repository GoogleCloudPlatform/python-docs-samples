# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

import backoff
from google.cloud import container_v1 as gke
import pytest

import create_cluster as gke_create

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
CLUSTER_NAME = f"py-container-repo-test-{uuid.uuid4().hex[:10]}"


@pytest.fixture(autouse=True)
def setup_and_tear_down() -> None:
    # nohing to setup here

    # run the tests here
    yield

    try:
        # delete the cluster
        client = gke.ClusterManagerClient()
        cluster_location = client.common_location_path(PROJECT_ID, REGION)
        cluster_name = f"{cluster_location}/clusters/{CLUSTER_NAME}"
        op = client.delete_cluster({"name": cluster_name})
        op_id = f"{cluster_location}/operations/{op.name}"

    finally:
        # schedule a retry to ensure the cluster is deleted
        @backoff.on_predicate(
            backoff.expo, lambda x: x != gke.Operation.Status.DONE, max_tries=20
        )
        def wait_for_delete() -> gke.Operation.Status:
            return client.get_operation({"name": op_id}).status

        wait_for_delete()


def test_create_clusters(capsys: object) -> None:
    gke_create.create_cluster(PROJECT_ID, REGION, CLUSTER_NAME)
    out, _ = capsys.readouterr()

    assert "Backing off " in out
    assert "Successfully created cluster after" in out

    client = gke.ClusterManagerClient()
    cluster_location = client.common_location_path(PROJECT_ID, REGION)
    list_response = client.list_clusters({"parent": cluster_location})

    list_of_clusters = []
    for cluster in list_response.clusters:
        list_of_clusters.append(cluster.name)

    assert CLUSTER_NAME in list_of_clusters
