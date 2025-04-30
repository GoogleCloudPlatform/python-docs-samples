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
import backoff
import uuid
from google.cloud import container_v1 as gke
import get_namespace
import pytest

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
SERVICE_ACCOUNT_KEY = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
ZONE = "us-central1-a"
REGION = "us-central1"
CLUSTER_NAME = f"cluster-{uuid.uuid4().hex[:10]}"

@pytest.fixture(autouse=True)
def setup_and_tear_down() -> None:
    # nohing to setup here

    # run the tests here
    yield

    try:
        # delete the cluster
        client = gke.ClusterManagerClient()
        cluster_location = client.common_location_path(PROJECT_ID, ZONE)
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

def on_success(details: dict[str, str]) -> None:
    """
    A handler function to pass into the retry backoff algorithm as the function
    to be executed upon a successful attempt.

    Read the `Event handlers` section of the backoff python module at:
    https://pypi.org/project/backoff/
    """
    print("Successfully created cluster after {elapsed:0.1f} seconds".format(**details))


def on_failure(details: dict[str, str]) -> None:
    """
    A handler function to pass into the retry backoff algorithm as the function
    to be executed upon a failed attempt.

    Read the `Event handlers` section of the backoff python module at:
    https://pypi.org/project/backoff/
    """
    print("Backing off {wait:0.1f} seconds after {tries} tries".format(**details))


@backoff.on_predicate(
    # the backoff algorithm to use. we use exponential backoff here
    backoff.expo,
    # the test function on the return value to determine if a retry is necessary
    lambda x: x != gke.Operation.Status.DONE,
    # maximum number of times to retry before giving up
    max_tries=20,
    # function to execute upon a failure and when a retry a scheduled
    on_backoff=on_failure,
    # function to execute upon a successful attempt and no more retries needed
    on_success=on_success,
)
def poll_for_op_status(
    client: gke.ClusterManagerClient, op_id: str
) -> gke.Operation.Status:
    """
    This function calls the Operation API in GCP with the given operation id. It
    serves as a simple retry function that fetches the operation and returns
    it's status.

    We use the 'backoff' python module to provide us the implementation of the
    backoff & retry strategy. The function is annotated with the `backoff`
    python module to schedule this function based on a reasonable backoff
    algorithm.
    """

    op = client.get_operation({"name": op_id})
    return op.status


def create_cluster(project_id: str, location: str, cluster_name: str):
    """Create a new GKE cluster in the given GCP Project and Zone/Region."""
    # Initialize the Cluster management client.
    client = gke.ClusterManagerClient()
    cluster_location = client.common_location_path(project_id, location)
    print({cluster_location})
    cluster_def = {
        "name": str(cluster_name),
        "initial_node_count": 1,
        "node_config": {"machine_type": "e2-standard-2"},
        "fleet": {"project": str(project_id)},
    }
    
    # Create the request object with the location identifier.
    request = {"parent": cluster_location, "cluster": cluster_def}
    create_response = client.create_cluster(request)
    op_identifier = f"{cluster_location}/operations/{create_response.name}"
    # poll for the operation status and schedule a retry until the cluster is created
    poll_for_op_status(client, op_identifier)

def test_get_namespace() -> None:
    create_cluster(PROJECT_ID, ZONE, CLUSTER_NAME)
    membership_name = f"projects/{PROJECT_ID}/locations/{REGION}/memberships/{CLUSTER_NAME}"
    results = get_namespace.get_namespace(membership_name, REGION, SERVICE_ACCOUNT_KEY)
    assert results is not None
    assert results.Metadata.Name == "Default"