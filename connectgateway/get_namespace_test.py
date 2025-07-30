# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from time import sleep
import uuid


from google.cloud import container_v1 as gke

import pytest

import get_namespace

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ZONE = "us-central1-a"
REGION = "us-central1"
CLUSTER_NAME = f"cluster-{uuid.uuid4().hex[:10]}"


@pytest.fixture(autouse=True)
def setup_and_tear_down() -> None:
    create_cluster(PROJECT_ID, ZONE, CLUSTER_NAME)

    yield

    delete_cluster(PROJECT_ID, ZONE, CLUSTER_NAME)


def poll_operation(client: gke.ClusterManagerClient, op_id: str) -> None:

    while True:
        # Make GetOperation request
        operation = client.get_operation({"name": op_id})
        # Print the Operation Information
        print(operation)

        # Stop polling when Operation is done.
        if operation.status == gke.Operation.Status.DONE:
            break

        # Wait 30 seconds before polling again
        sleep(30)


def create_cluster(project_id: str, location: str, cluster_name: str) -> None:
    """Create a new GKE cluster in the given GCP Project and Zone/Region."""
    # Initialize the Cluster management client.
    client = gke.ClusterManagerClient()
    cluster_location = client.common_location_path(project_id, location)
    cluster_def = {
        "name": str(cluster_name),
        "initial_node_count": 1,
        "fleet": {"project": str(project_id)},
    }

    # Create the request object with the location identifier.
    request = {"parent": cluster_location, "cluster": cluster_def}
    create_response = client.create_cluster(request)
    op_identifier = f"{cluster_location}/operations/{create_response.name}"
    # poll for the operation status and schedule a retry until the cluster is created
    poll_operation(client, op_identifier)


def delete_cluster(project_id: str, location: str, cluster_name: str) -> None:
    """Delete the created GKE cluster."""
    client = gke.ClusterManagerClient()
    cluster_location = client.common_location_path(project_id, location)
    cluster_name = f"{cluster_location}/clusters/{cluster_name}"
    client.delete_cluster({"name": cluster_name})


def test_get_namespace() -> None:
    membership_name = f"projects/{PROJECT_ID}/locations/{REGION}/memberships/{CLUSTER_NAME}"
    results = get_namespace.get_namespace(membership_name, REGION)

    assert results is not None
    assert results.metadata.name == "default"
